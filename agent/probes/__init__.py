
"""Probes hook into imports to modify third-party module behavior.

"""

from __future__ import unicode_literals
import sys
sys.path.append('')

from .integrationPoints import cache, http, logging, nosql, sql
from .frameworks import django, wsgi


try:
    from importlib.machinery import ModuleSpec
except ImportError:
    pass

# These definitions must come before the subsequent imports to avoid a circular reference.
URL_PROPERTY_MAX_LEN = 100
HOST_PROPERTY_MAX_LEN = 50
DB_NAME_PROPERTY_MAX_LEN = 50
VENDOR_PROPERTY_MAX_LEN = 50

# from . import cache, frameworks, http, logging, mongodb, sql


BT_PROBES = (
    # Entry points
    # ('bottle', frameworks.intercept_bottle),
    # ('flask', frameworks.intercept_flask),
    ('django.core.handlers.wsgi', django.probe_django_wsgi_handler),
    ('django.core.handlers.base', django.probe_django_base_handler),
    # ('cherrypy', frameworks.intercept_cherrypy),
    # ('pyramid.router', frameworks.intercept_pyramid),
    # ('tornado.web', frameworks.intercept_tornado_web),

    # HTTP exit calls
    ('httplib', http.probe_httplib),
    ('http.client', http.probe_httplib),
    ('urllib3', http.probe_urllib3),
    ('requests', http.probe_requests),
    ('boto.https_connection', http.probe_boto),
    ('tornado.httpclient', http.probe_tornado_httpclient),

    # SQL exit calls
    # ('cx_Oracle', sql.cx_oracle.intercept_cx_oracle_connection),
    # ('psycopg2', sql.psycopg2.intercept_psycopg2_connection),
    # ('pymysql.connections', sql.pymysql.intercept_pymysql_connections),
    # ('mysql.connector.connection', sql.mysql_connector.intercept_mysql_connector_connection),
    # ('MySQLdb.connections', sql.mysqldb.intercept_MySQLdb_connection),
    # ('tormysql.client', sql.tormysql.intercept_tormysql_client),

    # Caches
    # ('redis.connection', cache.intercept_redis),
    # ('memcache', cache.intercept_memcache),

    # Logging
    ('logging', logging.probe_logging),

    # MongoDB
    # ('pymongo', mongodb.intercept_pymongo),
)


def add_hook(agent):
    """Add the module probe hook for AppDynamics, if it's not already registered.

    """

    probe = ModuleProbe(agent)
    sys.meta_path.insert(0, probe)
    return probe


class ModuleProbe(object):
    """Intercepts finding and loading modules in order to monkey patch them on load.

    """

    def __init__(self, agent):
        super(ModuleProbe, self).__init__()
        self.agent = agent
        self.module_hooks = {}
        self.probe_modules = set()

    def find_spec(self, full_name, path, target=None):
        if full_name in self.module_hooks:
            return ModuleSpec(full_name, self)
        return None

    def find_module(self, full_name, path=None):
        if full_name in self.module_hooks:
            return self
        return None

    def load_module(self, name):
        # Remove the module from the list of hooks so that we never see it again.
        hooks = self.module_hooks.pop(name, [])

        if name in sys.modules:
            # Already been loaded. Return it as is.
            return sys.modules[name]

        self.agent.logger.debug('Intercepting import %s', name)

        __import__(name)  # __import__('a.b.c') returns <module a>, not <module a.b.c>
        module = sys.modules[name]  # ...so get <module a.b.c> from sys.modules

        self._probe_module(module, hooks)
        return module

    def call_on_import(self, module_name, cb):
        if module_name in sys.modules:
            self._probe_module(sys.modules[module_name], [cb])
        else:
            self.module_hooks.setdefault(module_name, [])
            self.module_hooks[module_name].append(cb)

    def _probe_module(self, module, hooks):
        try:
            for hook in hooks:
                self.agent.logger.debug('Running %s hook %r', module.__name__, hook)
                hook(self.agent, module)
            self.probe_modules.add(module)
        except:
            self.agent.logger.exception('Exception in %s hook.', module.__name__)

            # Re-import to ensure the module hasn't been partially patched.
            self.agent.logger.debug('Re-importing %s after error in module hook', module.__name__)
            reload(module)
