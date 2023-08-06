# -*- coding: utf8 -*-
import gc
import resource
from datetime import datetime
import threading
import logging
import json
import os
import platform
import sys
import zlib
import traceback
from jennifer.recorder import Recorder
from jennifer.api import task
import socket
import struct
import time
from random import random
from .active_object import ActiveObject
import subprocess
import ctypes
from jennifer.agent.int_bound_set import IntBoundSet
from jennifer.agent.python_def_visitor import PythonDefVisitor

_debug_mode = os.getenv('JENNIFER_PY_DBG')

record_types = {
    'method': 1,
    'sql': 2,
    'event_detail_msg': 3,  # errors
    'service': 4,  # app
    'txcall': 5,
    'browser_info': 6,
    'thread_stack': 8,
    'user_id': 9,
    'dbc': 10,
    'stack_trace': 11,
}


class Agent(object):
    def __init__(self, get_ctx_id_func, is_async):
        self.active_object_meter = {}
        self.active_object_meter_lock = threading.Lock()
        self.inst_id = -1
        self.recorder = None
        self.master_lock = threading.Lock()
        self.logger = logging.getLogger('jennifer')
        self.config_pid = 0
        self.address = ''
        self.masterConnection = None
        self.get_ctx_id_func = get_ctx_id_func
        self.app_config = None
        self.is_async = is_async
        self.python_visitor = PythonDefVisitor()

        # uwsgi 호스팅인 경우 --enable-threads 옵션이 지정되지 않은 상황이라면,
        # run_timer 등의 스레드 관련 기능이 동작하지 않으므로 사후 처리를 해야 함. (TODO: 아직 미구현)
        self.thread_enabled = False
        self.text_cache_record_types = None

    def _get_max_text_length(self, text_kind):
        if self.app_config is None:
            return 0

        return self.app_config.get_attr_by_name(text_kind)

    def _init_text_cache(self):
        self.text_cache_record_types = {
            'method': IntBoundSet(length=self._get_max_text_length('max_number_of_method')),
            'sql': IntBoundSet(length=self._get_max_text_length('max_number_of_sql')),
            'event_detail_msg': IntBoundSet(length=self._get_max_text_length('max_number_of_text')),
            'service': IntBoundSet(length=self._get_max_text_length('max_number_of_text')),
            'txcall': IntBoundSet(length=self._get_max_text_length('max_number_of_text')),
            'browser_info': IntBoundSet(length=self._get_max_text_length('max_number_of_text')),
            'thread_stack': IntBoundSet(length=self._get_max_text_length('max_number_of_stack')),
            'user_id': IntBoundSet(length=self._get_max_text_length('max_number_of_stack')),
            'dbc': IntBoundSet(length=self._get_max_text_length('max_number_of_stack')),
            'stack_trace': IntBoundSet(length=self._get_max_text_length('max_number_of_stack')),
        }

    def set_context_id_func(self, func):
        self.get_ctx_id_func = func

    @staticmethod
    def gen_new_txid():
        return int(str(int(random() * 100)) + str(Agent.current_time()))

    @staticmethod
    def log_ex(text):
        import jennifer
        jennifer.agent.log_ex(text)

    def current_active_object(self, ctx_id=None):
        if ctx_id is None:
            ctx_id = self.get_ctx_id_func()

        with self.active_object_meter_lock:
            return self.active_object_meter.get(ctx_id)

    # config.address == /tmp/jennifer-...sock
    # config.log_dir == /tmp
    def initialize_agent(self):
        config = {
            'address': os.environ['JENNIFER_MASTER_ADDRESS'],
            'log_dir': os.environ['JENNIFER_LOG_DIR'],
            'config_path': os.environ['JENNIFER_CONFIG_FILE'],
        }
        # config.address == /tmp/jennifer-...sock
        # config.log_dir == /tmp

        from .app_config import AppConfig
        self.address = config['address']
        self.recorder = Recorder()
        self.config_pid = os.getpid()
        self.app_config = AppConfig(config['config_path'])
        self._init_text_cache()

        ret = None
        with self.master_lock:
            ret = self.connect_master()

        if ret:
            task.run_timer(self.process_agent_metric, 'jennifer-handler-thread')

    @staticmethod
    def _debug_log(text):
        if os.getenv('JENNIFER_PY_DBG'):
            try:
                log_socket = __import__('jennifer').get_log_socket()
                if log_socket is not None:
                    log_socket.log(text)
            except ImportError as e:
                print(os.getpid(), 'jennifer.diagnostics', e)

    def connect_master(self):
        self.masterConnection = None

        if not os.path.exists(self.address):
            return False

        try:
            self.masterConnection = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.masterConnection.connect(self.address)

            self.handshake_to_master()
            task.run_task(self.master_loop, 'jennifer-master-thread')
            return True
        except Exception as e:
            self.masterConnection = None
            return False

    def handshake_to_master(self):
        try:
            import jennifer
            agent_version = jennifer.__version__
            data = '{"app_dir": "' + os.getcwd() + '", "protocol_version":2,"agent_version":"' + agent_version \
                   + '","pid":' + str(os.getpid()) + '}'

            version = data.encode('utf-8')
            self.masterConnection.send(b'\x08jennifer' + struct.pack('>L', len(version)) + version)
        except:
            jennifer.agent.log_ex('handshake')

    def master_loop(self):
        param = None

        startup_info = {'python_bin_path': os.environ['JENNIFER_PYTHON_PATH']}
        self.send_to_master('startup_info', startup_info)

        while True:
            if self.masterConnection is None:
                break

            try:
                byte_cmd_len = self.masterConnection.recv(1)

                if len(byte_cmd_len) < 1:
                    break  # failed to connect master

                cmd_len = ord(byte_cmd_len)
                cmd = self.masterConnection.recv(cmd_len)
                cmd_text = cmd.decode('utf-8')
                debug_log = self.app_config.cmd_debug == cmd_text
                param_len, = struct.unpack('>L', self.masterConnection.recv(4))

                try:
                    if param_len != 0:
                        param = json.loads(self.masterConnection.recv(param_len))
                except:
                    continue

                if cmd == b'connected':
                    try:
                        import jennifer

                        print('---------------- [App Initialized] ----------------------')
                        print('MachineName = ', socket.gethostname())
                        print('Is64BitProcess = ', platform.architecture())
                        print('Python Version = ', platform.python_version(), platform.python_implementation())
                        print('Current Path = ', os.curdir)
                        print('Jennifer Python Agent Install Path = ', os.path.dirname(os.path.dirname(__file__)))
                        print('Jennifer Server Address = ', param.get('server_address'))
                        print('Jennifer Python Agent Domain ID = ', param.get('domain_id'))
                        print('Jennifer Python Agent Inst ID = ', param.get('inst_id'), ', Version =', jennifer.__version__)
                        print('Jennifer Python Agent Pid = ', os.getpid(), ', tid', threading.get_native_id(),
                              ', thread_ident', self.get_ctx_id_func())
                        print('---------------------------------------------------------')
                    except:
                        pass
                    continue

                if cmd == b'active_detail':
                    txid = param.get('txid')
                    request_id = param.get('request_id')
                    prevent_callstack = param.get('prevent_call_stack')
                    if txid is not None and request_id is not None:
                        data = self.get_active_service_detail(txid, prevent_callstack)
                        if data is not None:
                            data['request_id'] = request_id
                            self.send_to_master('active_detail', data)
                    continue

                if cmd == b'agent_control_gc':
                    gc.collect()
                    continue

                if cmd == b'agent_control_service_dump':
                    request_id = param.get('request_id')
                    dump_file_path = param.get('dump_file_path')
                    prevent_callstack = param.get('prevent_call_stack')
                    data = {'request_id': request_id,
                            'dump_file_path': dump_file_path,
                            'process_info': self.get_process_info(),
                            'service_list': self.get_active_object_list(prevent_callstack)}
                    self.send_to_master('agent_control_service_dump', data)
                    continue

                if cmd == b'agentcheck_env':
                    if debug_log:
                        Agent.log(cmd_text)

                    request_id = param.get('request_id')
                    if request_id is None:
                        continue

                    gc_threshold = [0, 0, 0]
                    gc_count = [0, 0, 0]
                    gc_stats = None
                    gc_enabled = True
                    gc_debug_flags = None

                    try:
                        gc_threshold = gc.get_threshold()
                        gc_count = gc.get_count()
                        gc_enabled = gc.isenabled()
                        gc_debug_flags = gc.get_debug()
                        gc_stats = gc.get_stats()  # Python 3.4
                    except Exception as e:
                        if debug_log:
                            Agent.log('agentcheck_env', 'gc', traceback.format_exc())

                    data = Agent.get_environment_variables()
                    if data is not None:
                        if debug_log:
                            Agent.log('agentcheck_env', 'get_environment_variables')

                        import jennifer.hooks
                        data['jennifer.request_id'] = str(request_id)
                        data['jennifer.hooked'] = Agent.module_list_to_str(jennifer.hooks.__hooked_module__)
                        data['jennifer.gc_threshold'] = str(gc_threshold)
                        data['jennifer.gc_count'] = str(gc_count)
                        data['jennifer.gc_stats'] = str(gc_stats)
                        data['jennifer.gc_enabled'] = str(gc_enabled)
                        data['jennifer.gc_debug'] = str(gc_debug_flags)
                        data['jennifer.python_version'] = platform.python_version()
                        self.send_to_master('agentcheck_env', data)

                    if debug_log:
                        Agent.log('send_to_master')
                    continue

                if cmd == b'agentcheck_jar':  # "분석" / "클래스 파일 위치 검색"
                    request_id = param.get('request_id')
                    class_name = param.get('class_name')
                    if request_id is None:
                        continue

                    self.python_visitor.list_defs(os.getenv('PWD'))
                    data = {'module': self.python_visitor.find_def(class_name), 'jennifer.request_id': str(request_id)}
                    self.send_to_master('agentcheck_jar', data)
                    continue

                if cmd == b'reset_text':
                    self._init_text_cache()
                    continue

                if cmd == b'reload_config':
                    self.app_config.reload()
                    continue

                if cmd == b'gc_collect':
                    gc.collect()
                    continue

                if cmd == b'upgrade_agent':
                    agent_file_path = param.get('agent_file_path')
                    python_bin_path = os.environ['JENNIFER_PYTHON_PATH']
                    print(os.getpid(), cmd, python_bin_path, '-m', 'pip', 'install', agent_file_path)
                    subprocess.check_output([python_bin_path, '-m', 'pip', 'install', agent_file_path])
                    continue

            except (BrokenPipeError, OSError):
                break
            except Exception as e:
                print(os.getpid(), 'jennifer.exception', 'agent-loop', e)
                if _debug_mode:
                    traceback.print_exc()
                continue

    @staticmethod
    def module_list_to_str(module_list):
        ret = []
        for mod_name in module_list.keys():
            ret.append(mod_name)
            ret.append('[')
            version = module_list[mod_name]['version']
            ret.append(version)
            ret.append('],')

        return ''.join(ret)

    def _get_text_cache_size(self):
        size = 0
        for k, v in self.text_cache_record_types.items():
            size = size + len(v)

        return size

    @staticmethod
    def get_environment_variables():
        ret = {}
        for name, value in os.environ.items():
            ret[name] = value

        ret['jennifer.cmd'] = sys.executable
        ret['jennifer.cmd_line'] = str(sys.argv)
        return ret

    def get_process_info(self):
        ret = {'pid': os.getpid(), 'ppid': os.getppid(), 'cpu_user': self.current_cpu_time(),
               'cpu_system': self.current_cpu_time(), 'cpu_idle': self.current_cpu_time(),
               'memory_native': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               'memory_heap': 0}
        return ret

    def get_active_object_list(self, prevent_callstack):
        ret = []
        cpu_time = self.current_cpu_time()
        current_time = self.current_time()

        with self.active_object_meter_lock:
            for t in self.active_object_meter.values():
                stack = 'Failed to get a callstack'
                frame = None
                if self.is_async is True:
                    stack = 'Transaction in async mode'
                elif prevent_callstack:
                    stack = "The operation of obtaining a stack trace is not allowed"
                else:
                    ctx_id = t.get_ctx_id()
                    frame = sys._current_frames().get(ctx_id)

                if frame is not None:
                    thread_ident = t.get_ctx_id()
                    stack = ''.join(traceback.format_stack(frame))

                service_tx = {
                        'txid': t.txid,
                        'thread_id': t.vthread_id,
                        'service_name': t.path_info,
                        'elapsed': current_time - t.start_time,
                        'http_query': t.query_string,
                        'sql_count': t.sql_count,
                        'sql_time': t.sql_time,
                        'tx_time': t.external_call_time,
                        'tx_count': t.external_call_count,
                        'fetch_count': t.fetch_count,
                        'elapsed_cpu': cpu_time - t.start_cpu_time,
                        'start_time': t.start_time,
                        'stack': stack,
                        'client_address': t.client_address,
                        'status': t.status
                }

            ret.append(service_tx)

        return ret

    def get_active_service_detail(self, txid, prevent_callstack):
        ret = None
        cpu_time = self.current_cpu_time()
        current_time = self.current_time()

        with self.active_object_meter_lock:
            for t in self.active_object_meter.values():
                if t.txid == txid:
                    stack = 'Failed to get a callstack'
                    frame = None
                    if self.is_async is True:
                        stack = 'Transaction in async mode'
                    elif prevent_callstack:
                        stack = "The operation of obtaining a stack trace is not allowed"
                    else:
                        ctx_id = t.get_ctx_id()
                        frame = sys._current_frames().get(ctx_id)

                    if frame is not None:
                        stack = "PID: " + str(os.getpid())
                        if t.rthread_id != 0:
                            stack += ", Thread: " + str(t.rthread_id)

                        thread_ident = t.get_ctx_id()
                        vthread_ident = thread_ident & 0xFFFFFFFF
                        stack += ", ident: " + str(thread_ident) + " (" + str(vthread_ident) + ")"
                        stack += os.linesep + ''.join(traceback.format_stack(frame))

                    ret = {
                        'txid': t.txid,
                        'thread_id': t.vthread_id,
                        'service_name': t.path_info,
                        'elapsed': current_time - t.start_time,
                        'method': t.request_method,
                        'http_query': t.query_string,
                        'sql_count': t.sql_count,
                        'sql_time': t.sql_time,
                        'tx_time': t.external_call_time,
                        'tx_count': t.external_call_count,
                        'fetch_count': t.fetch_count,
                        'cpu_time': cpu_time - t.start_cpu_time,
                        'start_time': t.start_time,
                        'stack': stack,
                    }
                    break

        if ret is None:
            ret = {
                'txid': 0,
            }

        return ret

    def process_agent_metric(self):
        try:
            metrics = self.recorder.record_self()
            self.send_to_master('record_metric', metrics)

            current_cpu = Agent.current_cpu_time()
            current = Agent.current_time()

            with self.active_object_meter_lock:
                ax_list = [t.to_active_service_dict(current, current_cpu) for t in
                           self.active_object_meter.values()]

            self.send_to_master('active_service_list', {
                'active_services': ax_list,
            })
        except Exception as e:
            print('process_agent_metric', e)

    def send_to_master(self, cmd, params):
        try:
            p = json.dumps(params, default=str).encode('utf-8')

            pack = struct.pack('>B', len(cmd)) + cmd.encode('utf-8') + struct.pack('>L', len(p)) + p
            with self.master_lock:
                if self.masterConnection is None:
                    if not self.connect_master():
                        return
                self.masterConnection.send(pack)
                return True

        except socket.error as e:  # except (BrokenPipeError, OSError):  # 3.x only

            import errno
            if e.errno != errno.EPIPE:  # 2.7 backward compatibility
                print(os.getpid(), 'jennifer.exception', 'send_to_master', e)
            self.masterConnection = None

        return False

    @staticmethod
    def current_time():
        """
        current time as milli-seconds (int)
        """
        return int(time.time() * 1000)

    @staticmethod
    def current_cpu_time():
        """
        process time as milli-seconds (int)
        python [~3.3): time.clock
        python [3.3 ~]: time.process_time
        """
        if hasattr(time, 'process_time'):
            return int(time.process_time() * 1000)
        return int(time.clock() * 1000)

    def start_trace(self, environ, wmonid, path_info):
        txid = Agent.gen_new_txid()
        ctx_id = self.get_ctx_id_func()
        active_object = ActiveObject(
            agent=self,
            txid=txid,
            environ=environ,
            wmonid=wmonid,
            ctx_id=ctx_id,
            path_info=path_info,
        )

        with self.active_object_meter_lock:
            self.active_object_meter[ctx_id] = active_object

        self.send_to_master('start_service', {})
        return active_object

    def send_profile(self, profiler, profile_data):
        json_data = profiler.to_json_packet(profile_data)
        self.send_to_master('mid_profile', {
            'profile_data': json_data,
        })

    def end_trace(self, o):
        try:
            with self.active_object_meter_lock:
                self.active_object_meter.pop(o.ctx_id, None)

            pi_method = o.profiler.pop_thread_profile()

            # o.profiler.print_profile()
            self.send_to_master('end_service', {
                'xview_data': o.to_xview_data(pi_method),
                'profile_data': o.profiler.to_json_packet(),
            })

            # uwsgi 환경의 --enable-threads 옵션이,
            #  없는 경우를 위한 처리 추가
            #  있는 경우 어차피 run_timer 내에서 처리
            if len(self.active_object_meter) == 0:
                self.process_agent_metric()

        except Exception as e:
            print(os.getpid(), '[jennifer]', 'exception', 'etx', e)

    @staticmethod
    def _hash_text(text):
        hash_value = zlib.crc32(text.encode('utf-8'))
        hash_value = hash_value & 0xFFFFFFFF
        hash_value = ctypes.c_int32(hash_value).value
        return hash_value

    def _text_cache_add(self, text_kind, text_hash_code):
        text_cache = self.text_cache_record_types.get(text_kind, None)
        if text_cache is None:
            return

        text_cache.append(text_hash_code)

    def _text_cache_contains(self, text_kind, text_hash_code):
        text_cache = self.text_cache_record_types.get(text_kind, None)
        if text_cache is None:
            return False

        return text_cache.contains(text_hash_code)

    def hash_text(self, text, text_kind='service'):
        if text is None or len(text) == 0:
            return 0

        text_hash_code = self._hash_text(text)
        if self._text_cache_contains(text_kind, text_hash_code) is True:
            return text_hash_code

        sent = self.send_to_master('record_text', {
            'type': record_types.get(text_kind, 0),
            'text': text,
            'text_hash': text_hash_code,
        })

        if sent is True:
            self._text_cache_add(text_kind, text_hash_code)

        return text_hash_code

    @staticmethod
    def log(*args):
        current_time = time.localtime(time.time())
        time_prefix = time.strftime("%Y%m%d-%H%M%S", current_time)
        print(os.getpid(), '[jennifer]', time_prefix, args)
