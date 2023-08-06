import sys

from jennifer.agent import jennifer_agent
from distutils.version import LooseVersion

__hooking_module__ = 'urllib2'
__minimum_python_version__ = LooseVersion("2.7")
_original_urllib2_urlopen = None
__target_version = None

global parse_url_func2


def get_target_version():
    global __target_version
    return str(__target_version)


def parse_url2(url):
    from urlparse import urlparse
    return urlparse(url)


def parse_url3(url):
    from urllib import parse
    return parse.urlparse(url)


def wrap_urlopen(urlopen):
    global parse_url_func2

    if sys.version_info.major == 3:
        parse_url_func2 = parse_url3
    else:
        parse_url_func2 = parse_url2

    def handler(*args, **kwargs):
        o = None
        pi = None
        ret = None

        try:
            from urllib2 import Request

            agent = jennifer_agent()
            if agent is not None:
                o = agent.current_active_object()
                url = kwargs.get('url') or args[0]
                if isinstance(url, Request):
                    url = url.get_full_url()

                if o is not None:
                    url_info = parse_url_func2(url)
                    pi = o.profiler.start_external_call(
                        protocol=url_info.scheme,
                        host=url_info.hostname,
                        port=url_info.port or 80,
                        url=url,
                        caller='urllib2.urlopen')
        except:
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


def unhook(urllib2_module):
    global _original_urllib2_urlopen
    if _original_urllib2_urlopen is not None:
        urllib2_module.urlopen = _original_urllib2_urlopen


def hook(urllib2_module):
    global __target_version
    __target_version = urllib2_module.__version__

    if not sys.version_info.major == 2:
        return False

    global _original_urllib2_urlopen
    if str(urllib2_module.urlopen).startswith('jennifer.hooks') is True:
        return False

    urllib2_module.urlopen = wrap_urlopen(urllib2_module.urlopen)
    return True
