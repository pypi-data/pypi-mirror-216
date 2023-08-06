import sys
from jennifer.agent import jennifer_agent
from distutils.version import LooseVersion

__hooking_module__ = 'urllib.request'
__minimum_python_version__ = LooseVersion("2.7")
_original_urllib_request_urlopen = None
__target_version = None


def get_target_version():
    global __target_version
    return str(__target_version)


def wrap_urlopen(urlopen):

    def handler(*args, **kwargs):
        HTTPResponse = None
        o = None
        pi = None
        ret = None

        try:
            from urllib import parse
            from urllib.request import Request
            from http.client import HTTPResponse

            agent = jennifer_agent()

            if agent is not None:
                o = agent.current_active_object()
                url = kwargs.get('url') or args[0]
                if isinstance(url, Request):
                    url = url.full_url

                if o is not None:
                    url_info = parse.urlparse(url)
                    pi = o.profiler.start_external_call(
                        protocol=url_info.scheme,
                        url=url,
                        host=url_info.hostname,
                        port=url_info.port or 80,
                        caller='urllib.request.urlopen')
        except Exception as e:
            pass

        err = None

        try:
            ret = urlopen(*args, **kwargs)
        except Exception as e:
            err = e

        try:
            if pi is not None:
                o.profiler.end_external_call(pi, err)
        except:
            pass

        return ret
    return handler


def unhook(urllib_module):
    if _original_urllib_request_urlopen is not None:
        urllib_module.request.urlopen = _original_urllib_request_urlopen


def hook(urllib_module):

    global __target_version
    __target_version = urllib_module.request.__version__

    if not sys.version_info.major == 3:
        return False

    global _original_urllib_request_urlopen
    if str(urllib_module.request.urlopen).startswith('jennifer.hooks') is True:
        return False

    _original_urllib_request_urlopen = urllib_module.request.urlopen
    urllib_module.request.urlopen = wrap_urlopen(urllib_module.request.urlopen)
    return True
