
import psycopg2
from contextlib import contextmanager

class DatabaseConnection:
    def __init__(self, config):
        self.config = config

    @contextmanager
    def get_connection(self):
        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            yield conn
        finally:
            if conn:
                conn.close()
