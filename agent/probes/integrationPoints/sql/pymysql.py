

"""Probing the pymysql package.

"""

from __future__ import unicode_literals

from .dbapi import DbAPIConnectionProbe, DbAPICursorProbe


class PymysqlConnectionProbe(DbAPIConnectionProbe):
    def get_backend_properties(self, conn, *args, **kwargs):
        return conn.host, conn.port, conn.db, 'MYSQL'


class PymysqlCursorProbe(DbAPICursorProbe):
    def get_connection(self, cursor):
        return cursor.connection


def intercept_pymysql_connections(agent, mod):
    PymysqlConnectionProbe(agent, mod.Connection, PymysqlCursorProbe).attach('connect')
