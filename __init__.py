from .HTTPTestKeywords import HTTPTestKeywords
from .version import VERSION

_version_ = VERSION


class HTTPTestLibrary(HTTPTestKeywords):
    """ HTTPTestLibrary is a HTTP test keyword library that uses
    the requests module from Kenneth Reitz
    https://github.com/kennethreitz/requests


        Examples:
        | ${test_url} | http://172.16.118.28:8090/lokiRest/lokiRest/zdr/commonchoose/count |
        | ${method}  | POST |
        | ${params} | {"authcode":"","entityids":["11120"],"filters":[{"item":"level","value":["402003"]},],"items":["level"],ifcontains":"0"} |
        | ${headers} | {'Content-type': 'application/json'} |
        | Do Test | ${method} | ${test_url} | ${params} | ${headers} |

    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
