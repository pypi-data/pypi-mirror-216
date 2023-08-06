import sys
from distutils.version import LooseVersion
from jennifer.agent import jennifer_agent

__hooking_module__ = 'urllib3'
__minimum_python_version__ = LooseVersion("2.7")
_original_urllib3_poolmanager_request = None
_original_urllib3_poolmanager_urlopen = None
__target_version = None

global parse_url_func3


def get_target_version():
    global __target_version
    return str(__target_version)


def parse_url2(url):
    from urlparse import urlparse
    return urlparse(url)


def parse_url3(url):
    from urllib import parse
    return parse.urlparse(url)


def wrap_request(urlrequest):
    global parse_url_func3

    if sys.version_info.major == 3:
        parse_url_func3 = parse_url3
    else:
        parse_url_func3 = parse_url2

    def handler(*args, **kwargs):
        o = None
        ret = None
        pi = None

        try:
            from urllib3 import response

            agent = jennifer_agent()
            if agent is not None:
                o = agent.current_active_object()
                url = kwargs.get('url') or args[2]

                if o is not None:
                    url_info = parse_url_func3(url)
                    pi = o.profiler.start_external_call(
                        protocol=url_info.scheme,
                        url=url,
                        host=url_info.hostname,
                        port=url_info.port or 80,
                        caller='urllib3.PoolManager')
        except Exception as e:
            pass

        err = None
        try:
            ret = urlrequest(*args, **kwargs)
        except Exception as e:
            err = e

        try:
            if pi is not None:
                o.profiler.end_external_call(pi, err)
        except:
            pass

        return ret
    return handler


def unhook(urllib3_module):
    global _original_urllib3_poolmanager_request
    global _original_urllib3_poolmanager_urlopen

    if _original_urllib3_poolmanager_request is not None:
        urllib3_module.poolmanager.PoolManager.request = _original_urllib3_poolmanager_request

    if _original_urllib3_poolmanager_urlopen is not None:
        urllib3_module.poolmanager.PoolManager.urlopen = _original_urllib3_poolmanager_urlopen


def hook(urllib3_module):
    global __target_version
    __target_version = urllib3_module.__version__

    if not sys.version_info.major == 3:
        return False

    global _original_urllib3_poolmanager_request
    global _original_urllib3_poolmanager_urlopen

    if str(urllib3_module.poolmanager.PoolManager.request).startswith('jennifer.hooks') is True:
        return False

    _original_urllib3_poolmanager_request = urllib3_module.poolmanager.PoolManager.request
    _original_urllib3_poolmanager_urlopen = urllib3_module.poolmanager.PoolManager.urlopen

    urllib3_module.poolmanager.PoolManager.request = wrap_request(urllib3_module.poolmanager.PoolManager.request)
    urllib3_module.poolmanager.PoolManager.urlopen = wrap_request(urllib3_module.poolmanager.PoolManager.urlopen)
    return True
