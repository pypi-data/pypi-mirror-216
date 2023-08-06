import sys
from jennifer.agent import jennifer_agent
from distutils.version import LooseVersion

__hooking_module__ = 'requests'
__minimum_python_version__ = LooseVersion("2.7")
_original_requests_send = None
__target_version = None


global parse_url_func


def get_target_version():
    global __target_version
    return str(__target_version)


def parse_url2(url):
    from urlparse import urlparse
    return urlparse(url)


def parse_url3(url):
    from urllib import parse
    return parse.urlparse(url)


def wrap_send(origin):
    global parse_url_func

    if sys.version_info.major == 3:
        parse_url_func = parse_url3
    else:
        parse_url_func = parse_url2

    def handler(self, request, **kwargs):
        o = None
        pi = None
        ret = None

        try:
            agent = jennifer_agent()
            if agent is not None:
                o = agent.current_active_object()
                url = request.url

                if o is not None:
                    url_info = parse_url_func(url)
                    pi = o.profiler.start_external_call(
                        protocol=url_info.scheme,
                        host=url_info.hostname,
                        port=url_info.port or 80,
                        url=url,
                        caller='requests.Session.send')
        except:
            pass

        err = None
        try:
            ret = origin(self, request, **kwargs)
        except Exception as e:
            err = e

        try:
            if pi is not None:
                o.profiler.end_external_call(pi, err)
        except:
            pass

        return ret

    return handler


def unhook(requests_module):
    global _original_requests_send
    if _original_requests_send is not None:
        requests_module.Session.send = _original_requests_send


def hook(requests_module):
    global _original_requests_send

    global __target_version
    if str(requests_module.Session.send).startswith('jennifer.hooks') is True:
        return False

    __target_version = requests_module.__version__

    _original_requests_send = requests_module.Session.send
    requests_module.Session.send = wrap_send(requests_module.Session.send)
    return True
