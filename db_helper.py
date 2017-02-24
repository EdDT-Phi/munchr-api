import os
from urllib.parse import urlparse
import psycopg2

from psycopg2.pool import ThreadedConnectionPool


class MySimpleConnectionPool(ThreadedConnectionPool):
    def _connect(self, key=None):
        """Create a new connection and assign it to 'key' if not None."""
        conn = psycopg2.connect(*self._args, **self._kwargs)
        conn.set_session(readonly=True, autocommit=False)
        if key is not None:
            self._used[key] = conn
            self._rused[id(conn)] = key
        else:
            self._pool.append(conn)
        return conn

postgresUri = os.getenv('DATABASE_URL', 'postgresql://localhost/datamart')
_db = None


def get_connection_pool(uri):
    connect_parts = urlparse(uri)
    port = connect_parts.port if connect_parts.port else 5432
    pool = MySimpleConnectionPool(
        1, 5,
        host=connect_parts.hostname,
        database=connect_parts.path[1:],
        user=connect_parts.username,
        password=connect_parts.password,
        port=port)

    return pool


def get_db():
    global _db
    if _db is None:
        print("Connection pool not found, connecting.")
        print("Postgres: %s" % postgresUri)
        _db = get_connection_pool(postgresUri)
    return _db
