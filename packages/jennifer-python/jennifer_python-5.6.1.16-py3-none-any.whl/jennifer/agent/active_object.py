# -*- coding: utf8 -*-
from random import random
from jennifer.agent import jennifer_agent
from .profiler import PiProfiler
from jennifer.pconstants import *
from distutils.version import LooseVersion
import platform
import threading


class ActiveObject:
    current_python_ver = LooseVersion(platform.python_version())
    python38_version = LooseVersion("3.8")
    _is_38_or_later = python38_version <= current_python_ver

    def __init__(self, agent, environ, wmonid, txid, ctx_id, path_info):

        self.elapsed = 0
        self.elapsed_cpu = 0

        self.sql_hash = 0
        self.sql_count = 0
        self.sql_call = None
        self.sql_start_time = 0
        self.sql_time = 0
        self.fetch_count = 0
        self.fetch_time = 0
        self.running_profile_number_or_n1 = -1

        self.external_call = None
        self.external_call_count = 0
        self.external_call_time = 0
        self.external_call_name = None
        self.external_call_started = False
        self.external_call_type = REMOTE_CALL_TYPE_NONE

        self.txid = txid
        self.client_address = None
        self.wmonid = wmonid
        self.user_hash = 0
        self.guid = None
        self.browser_info_hash = 0
        self.error_code = 0
        self.http_status_code = 0
        self.service_hash = 0
        self.incoming_remote_call = None
        self.running_data_source_name = None

        if ActiveObject._is_38_or_later:
            self.rthread_id = threading.get_native_id()
        else:
            self.rthread_id = 0

        self.agent = agent
        self.end_system_time = 0
        self.wmonid = wmonid

        # 비동기(async): thread_id (4바이트) == ctx_id (ContextVars에 의해 설정한 4바이트)
        # 동기(sync): thread_id (4바이트) != thread id (최소 6바이트)
        self.ctx_id = ctx_id

        # 단순히 제니퍼 서버와 통신을 위한 thread id
        self.vthread_id = ctx_id & 0xFFFFFFFF

        if environ.get('HTTP_X_FORWARDED_FOR') is not None:
            self.client_address = environ.get('HTTP_X_FORWARDED_FOR')
        elif environ.get('HTTP_CLIENT_IP') is not None:
            self.client_address = environ.get('HTTP_CLIENT_IP')
        else:
            self.client_address = environ.get('REMOTE_ADDR', '')

        self.browser_info_hash = self.agent.hash_text(environ.get('HTTP_USER_AGENT', ''), 'browser_info')

        if path_info is None:
            path_info = environ.get('PATH_INFO', '').encode('iso-8859-1').decode('utf-8')

        self.request_method = environ.get('REQUEST_METHOD', '')
        self.query_string = environ.get('QUERY_STRING', '')

        self.start_time = agent.current_time()
        self.start_cpu_time = agent.current_cpu_time()

        self.path_info = path_info
        self.service_hash = self.agent.hash_text(path_info)

        self.status = ACTIVE_SERVICE_STATUS_CODE_INITIALIZING
        self.profiler = PiProfiler(self, self.service_hash)

    def initialize(self, root_method_name):
        method_hash = self.agent.hash_text(root_method_name, 'method')
        if method_hash != 0:
            self.profiler.push_thread_profile(method_hash)

    def get_method_thread_cpu_time(self, start_cpu, pi_start_cpu=0):
        result = 0
        if start_cpu != 0:  # profile_method_cpu
            result = self.agent.current_cpu_time() - start_cpu - pi_start_cpu
            if result < 0:
                result = 0

        return result

    def get_current_point_time(self):
        result = self.agent.current_time() - self.start_time
        if result < 0:
            result = 0
        return result

    def get_end_of_cpu_time(self):
        result = self.agent.current_cpu_time() - self.start_cpu_time
        if result < 0:
            result = 0
        return result

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def get_ctx_id(self):
        return self.ctx_id

    def to_active_service_dict(self, current_time, current_cpu_time):
        self.elapsed_cpu = current_cpu_time - self.start_cpu_time
        self.elapsed = current_time - self.start_time

        running_mode = ACTIVE_SERVICE_RUNNING_MODE_NONE
        running_hash = 0
        running_time = 0
        if self.sql_hash != 0:
            running_mode = ACTIVE_SERVICE_RUNNING_MODE_SQL
            running_hash = self.sql_hash
            running_time = current_time - self.start_time - self.sql_start_time
        elif self.external_call is not None:
            running_mode = ACTIVE_SERVICE_RUNNING_MODE_EXTERNALCALL
            running_hash = self.external_call.desc_hash
            running_time = current_time - self.start_time - self.external_call.start_time

        data = {'service_hash': self.service_hash, 'elapsed': self.elapsed, 'txid': self.txid, 'wmonid': self.wmonid,
                'thread_id': self.vthread_id, 'client_address': self.client_address, 'elapsed_cpu': self.elapsed_cpu,
                'sql_count': self.sql_count, 'fetch_count': self.fetch_count, 'start_time': self.start_time,
                'running_mode': running_mode, 'running_hash': running_hash,
                'running_time': running_time, 'status_code': self.status}

        return data

    def to_xview_data(self, service_method):
        self.elapsed_cpu = service_method.end_cpu
        self.elapsed = service_method.elapsed_time
        end_time = service_method.end_time

        data = {'txid': self.txid, 'elapsed': self.elapsed, 'elapsed_cpu': self.elapsed_cpu, 'end_time': end_time,
                'sql_count': self.sql_count, 'sql_time': self.sql_time, 'fetch_count': self.fetch_count,
                'fetch_time': self.fetch_time, 'external_call_count': self.external_call_count,
                'external_call_time': self.external_call_time, 'client_address': self.client_address,
                'wmonid': self.wmonid, 'user_hash': self.user_hash, 'service_hash': self.service_hash,
                'guid': self.guid,
                'browser_info_hash': self.browser_info_hash, 'error_code': self.error_code}

        return data
