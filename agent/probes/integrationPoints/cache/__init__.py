
"""Base probes for distributed caches (typically, key-value stores).

"""

from __future__ import unicode_literals

# from appdynamics.agent.models.exitcalls import EXIT_CACHE, EXIT_SUBTYPE_CACHE
from agent.probes.instrumentation import ExitCallProbe


class CacheProbe(ExitCallProbe):
    """Base class for cache probes.

    Extra Parameters
    -----------------
    vendor : string
        The vendor name of this cache backend e.g. MEMCACHED.

    """

    backend_name_format_string = '{SERVER POOL} - {VENDOR}'

    def __init__(self, agent, cls, vendor):
        self.vendor = vendor
        super(CacheProbe, self).__init__(agent, cls)

    def get_backend(self, server_pool):
        """

        Parameters
        ----------
        server_pool : list of str

        """

        backend_properties = {
            'VENDOR': self.vendor,
            'SERVER POOL': '\n'.join(server_pool),
        }
        return self.agent.backend_registry.get_backend(EXIT_CACHE, EXIT_SUBTYPE_CACHE, backend_properties,
                                                       self.backend_name_format_string)


# from .redis import probe_redis
# from .memcache import probe_memcache

# __all__ = ['probe_redis', 'probe_memcache']
