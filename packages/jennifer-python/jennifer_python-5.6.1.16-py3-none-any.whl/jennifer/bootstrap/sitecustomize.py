import os
import sys
import traceback
from os import path

_debug_mode = os.getenv('JENNIFER_PY_DBG')


def _debug_log(text):
    if _debug_mode:
        log_socket = __import__('jennifer').get_log_socket()
        if log_socket is not None:
            log_socket.log(text)


if _debug_mode:
    try:
        if _debug_mode != "1":
            import pydevd
            pydevd.settrace(_debug_mode, port=15555, stdoutToServer=True, stderrToServer=True, suspend=False)
    except ImportError:
        pass

try:
    jennifer = __import__('jennifer')
except ImportError as e:
    jennifer_path = path.abspath(path.join(path.dirname(__file__), '..', '..'))
    sys.path.append(jennifer_path)
    jennifer = __import__('jennifer')

if os.environ.get('JENNIFER_MASTER_ADDRESS') is not None:
    try:
        jennifer.startup.init()
    except Exception as e:
        print(os.getpid(), 'jennifer.exception', 'site_customize', e)
        if _debug_mode:
            traceback.print_exc()


