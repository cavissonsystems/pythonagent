
"""Probing the MySQLdb package.

"""

from __future__ import unicode_literals
import weakref

from .dbapi import DbAPIConnectionProbe, DbAPICursorProbe


class MySQLdbConnectionProbe(DbAPIConnectionProbe):
    def get_backend_properties(self, conn, *args, **kwargs):
        host = kwargs.get('host', 'localhost')
        port = kwargs.get('port', '3306')
        db = kwargs.get('database', kwargs.get('db', ''))
        return host, port, db, 'MYSQL'


class MySQLdbCursorProbe(DbAPICursorProbe):
    def get_connection(self, cursor):
        conn = cursor.connection
        if isinstance(conn, weakref.ReferenceType):
            conn = conn()
        return conn


def probe_MySQLdb_connection(agent, mod):
    MySQLdbConnectionProbe(agent, mod.Connection, MySQLdbCursorProbe).attach('__init__')
