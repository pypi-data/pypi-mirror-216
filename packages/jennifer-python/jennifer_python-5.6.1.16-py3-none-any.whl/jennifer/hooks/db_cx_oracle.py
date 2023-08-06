from distutils.version import LooseVersion
from jennifer.pconstants import *

__hooking_module__ = 'cx_Oracle'
__minimum_python_version__ = LooseVersion("2.7")
_original_db_connect = None
__target_version = None


def get_target_version():
    global __target_version
    return str(__target_version)


def safe_get(properties, idx, default=None):
    try:
        return properties[idx]
    except IndexError:
        return default


def connection_info(*args, **kwargs):
    try:
        dsn = safe_get(args, 2) or kwargs.get('dsn')

        host, port, service_name = get_host_and_service_name(dsn)
        return host, port, service_name
    except:
        return '(None)', 1521, '(None)'


def get_host_and_service_name(dsn_text):
    found = dsn_text.find('/')
    if found == -1:
        host, port = get_host_and_port(dsn_text)
        return host, port, ''

    host, port = get_host_and_port(dsn_text[:found])
    return host, port, dsn_text[found + 1:]


def get_host_and_port(text):
    found = text.find(':')
    if found == -1:
        return text, 1521

    return text[:found], int(text[found + 1:])


def unhook(cx_oracle_module):
    global _original_db_connect
    if _original_db_connect is not None:
        cx_oracle_module.connect = _original_db_connect


def hook(cx_oracle_module):
    from jennifer.wrap import db_api

    global __target_version
    __target_version = cx_oracle_module.__version__

    global _original_db_connect
    if str(cx_oracle_module.connect).startswith('jennifer.hooks') is True:
        return False

    _original_db_connect = db_api.register_database(cx_oracle_module, REMOTE_CALL_TYPE_ORACLE, connection_info)
    return True
