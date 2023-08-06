import os
import sys

import jennifer.network_logger
from jennifer.agent import jennifer_agent


# Not used
# def setup_log(config):
#     logger = logging.getLogger('jennifer')
#     logger.setLevel(logging.INFO)
#     logger.propagate = False
#     handler = logging.FileHandler(config['log_dir'])
#     formatter = logging.Formatter('%(asctime)s [JENNIFER Python] %(levelname)s %(message)s')
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)
#     print('setup_log')

# config.address == /tmp/jennifer-...sock
# config.log_dir == /tmp


def _hook_uncaught_exception(exc_type, value, exc_tb):
    import traceback
    print(os.getpid(), 'jennifer.exception', 'uncaught', exc_type, value, exc_tb)
    traceback.print_tb(exc_tb)


try:
    if os.getenv('JENNIFER_PY_DBG'):
        sys.excepthook = _hook_uncaught_exception
except:
    pass


def init():
    jennifer_agent()


def _debug_log(text):
    if os.getenv('JENNIFER_PY_DBG'):
        log_socket = __import__('jennifer').get_log_socket()
        if log_socket is not None:
            log_socket.log(text)
