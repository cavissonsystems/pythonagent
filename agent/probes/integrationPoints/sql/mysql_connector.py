
"""Probing the mysql-connector-python package.

"""

from __future__ import unicode_literals

from .dbapi import DbAPIConnectionProbe, DbAPICursorProbe


class MySQLConnectionProbe(DbAPIConnectionProbe):
    def get_backend_properties(self, conn, *args, **kwargs):
        return conn._host, conn._port, conn._database, 'MYSQL'


class MySQLCursorProbe(DbAPICursorProbe):
    def get_connection(self, cursor):
        return cursor._connection


def probe_mysql_connector_connection(agent, mod):
    MySQLConnectionProbe(agent, mod.MySQLConnection, MySQLCursorProbe).attach('_open_connection')
