# -*- coding: utf-8 -*-
"""Wsgi Agent for Jennifer APM
"""
import os
import sys
import base64
import struct
import traceback

from jennifer.agent import jennifer_agent
from email.utils import formatdate
import time

try:
    import Cookie as cookies
except ImportError:
    from http import cookies

wmonid_pack = struct.Struct('>Q')


def _wrap_wsgi_start_response(origin, set_wmonid, wmonid_cookie_postfix, total_seconds_per_year, new_wmonid=None):
    def handler(*args, **kwargs):
        if set_wmonid:
            if len(args) == 2:
                expire = formatdate(
                    timeval=time.time() + total_seconds_per_year,
                    localtime=False,
                    usegmt=True
                )
                set_cookie = 'WMONID=%s; expires=%s; Max-Age=%s; path=/ %s' % (
                    base64.b64encode(new_wmonid).decode('ascii'), expire, total_seconds_per_year, wmonid_cookie_postfix)
                args[1].append(('Set-Cookie', str(set_cookie)))
        else:
            if total_seconds_per_year < 0 and len(args) == 2:
                set_cookie = 'WMONID=deleted; expires=Thu, 01, Jan 1970 00:00:00 GMT; path=/; Max-Age=-1'
                args[1].append(('Set-Cookie', str(set_cookie)))
        return origin(*args, **kwargs)
    return handler


def _wrap_wsgi_handler(original_app_func):
    def handler(*args, **kwargs):
        environ = {}
        modargs = []
        wmonid = None
        start_response = None
        active_object = None
        ret = None

        try:
            agent = jennifer_agent()

            new_wmonid_val = (os.getpid() << 32) + int(time.time())
            new_wmonid = wmonid_pack.pack(new_wmonid_val)

            if len(args) == 3:
                environ = args[1]  # self, environ, start_response
                modargs = [args[0], args[1], ]
                start_response = args[2]
            elif len(args) == 2:
                environ = args[0]  # environ, start_response
                modargs = [args[0], ]
                start_response = args[1]

            url_scheme = environ.get('wsgi.url_scheme')
            http_method = environ.get('REQUEST_METHOD')
            host_host = environ.get('HTTP_HOST')
            req_uri = environ.get('REQUEST_URI') or environ.get('RAW_URI')
            ignore_req = is_ignore_urls(agent, req_uri)

            cookie = cookies.SimpleCookie()
            cookie.load(environ.get('HTTP_COOKIE', ''))
            cookie_wmonid = cookie.get('WMONID')
            if cookie_wmonid is None:
                wmonid = new_wmonid_val
            else:
                try:
                    wmonid, = wmonid_pack.unpack(base64.b64decode(cookie_wmonid.value))
                except:  # incorrect wmonid
                    cookie_wmonid = None
                    wmonid = new_wmonid_val

            wmonid_http_only = ''
            wmonid_http_secure = ''

            wmonid_cookie_expire_sec = 31536000
            if agent is not None:
                if agent.app_config.enable_http_only_for_wmonid_cookie:
                    wmonid_http_only = '; HttpOnly'
                if agent.app_config.enable_secure_for_wmonid_cookie:
                    wmonid_http_secure = '; Secure'
                wmonid_cookie_expire_sec = agent.app_config.expire_date_for_wmonid_cookie * 24 * 60 * 60

            wmonid_cookie_append = wmonid_http_only + wmonid_http_secure
            modargs.append(
                _wrap_wsgi_start_response(start_response,
                                          set_wmonid=(cookie_wmonid is None),
                                          wmonid_cookie_postfix=wmonid_cookie_append,
                                          total_seconds_per_year=wmonid_cookie_expire_sec,
                                          new_wmonid=new_wmonid)
            )

            if not ignore_req and agent is not None:
                active_object = agent.start_trace(environ, wmonid, req_uri)
                if active_object is not None:
                    active_object.initialize("wsgi_handler")
                    if agent.app_config.dump_http_query:
                        req_uri_msg = '[%s] %s://%s%s' % (http_method, url_scheme, host_host, req_uri)
                        active_object.profiler.add_message(req_uri_msg)

        except Exception as e:
            print(os.getpid(), '[jennifer]', 'exception', 'wsgi_handler', e)

        err = None
        try:
            ret = original_app_func(*modargs, **kwargs)
        except Exception as e:
            err = e  # wsgi 내부에서는 원래 예외가 발생하지 않음!

        if active_object is not None and hasattr(ret, 'status_code'):
            active_object.http_status_code = ret.status_code

            if ret.status_code == 404:
                active_object.profiler.add_service_error_profile(None)
            elif ret.status_code >= 400:
                ex_result = ''
                if hasattr(ret, 'current_exception_info'):
                    cei = ret.current_exception_info
                    if hasattr(cei, '__traceback__'):
                        ex_result = traceback.format_exception(type(cei), cei, cei.__traceback__)
                        ex_result = ''.join(ex_result)
                    else:
                        ex_result = str(cei)
                active_object.profiler.add_service_error_profile("Service Error: " + ret.reason_phrase + " " + ex_result)

        try:
            if active_object is not None:
                agent.end_trace(active_object)
        except Exception as e:
            print(os.getpid(), '[jennifer]', 'exception', e)

        if err is not None:
            raise err

        return ret
    return handler


def is_ignore_urls(agent, req_uri):
    if agent.app_config.ignore_url_postfix is None:
        return False

    for ext in agent.app_config.ignore_url_postfix:
        if req_uri.endswith(ext):
            return True

    return False


def wrap_wsgi_app(original_app_func):
    return _wrap_wsgi_handler(original_app_func)


def _debug_log(text):
    if os.getenv('JENNIFER_PY_DBG'):
        try:
            log_socket = __import__('jennifer').get_log_socket()
            if log_socket is not None:
                log_socket.log(text)
        except ImportError as e:
            print(e)
