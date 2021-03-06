
"""Base class for HTTP connection probes.

"""

from __future__ import unicode_literals

from agent.probes.instrumentation import ExitCallProbe
# from appdynamics.lang import str, urlparse
# from appdynamics.agent.models.exitcalls import EXIT_HTTP, EXIT_SUBTYPE_HTTP


class HTTPConnectionProbe(ExitCallProbe):
    # If the library you are probing has an HTTPSConnection class which
    # does not subclass httplib.HTTPSConnection, add it to this set.
    https_connection_classes = set()
    backend_name_format_string = '%s://{HOST}:{PORT}{URL}?{QUERY STRING}'

    @classmethod
    def _request_is_https(cls, connection):
        if connection.port == 443:
            return True
        return isinstance(connection, tuple(cls.https_connection_classes))

    def get_backend(self, host, port, scheme, url):
        parsed_url = urlparse(url)
        backend_properties = {
            'HOST': host,
            'PORT': str(port),
            'URL': parsed_url.path,
            'QUERY STRING': parsed_url.query,
        }
        return self.agent.backend_registry.get_backend(EXIT_HTTP, EXIT_SUBTYPE_HTTP, backend_properties,
                                                       self.backend_name_format_string % scheme)


from .httplib import probe_httplib
from .urllib3 import probe_urllib3
from .requests import probe_requests
from .boto import probe_boto
from .tornado_httpclient import probe_tornado_httpclient

__all__ = ['probe_httplib', 'probe_urllib3', 'probe_requests', 'probe_boto',
           'probe_tornado_httpclient']
