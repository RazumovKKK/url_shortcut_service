import sqlite3

from threading import local
from DB.models import URLModel

thread_local = local()

class Database:
    def __init__(self, db_path: str = "urls.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        url_model = URLModel(conn)
        conn.close()
    
    def get_connection(self):
        if not hasattr(thread_local, 'connection'):
            thread_local.connection = sqlite3.connect(
                self.db_path, 
                check_same_thread=False
            )
        return thread_local.connection
    
    def close_connection(self):
        if hasattr(thread_local, 'connection'):
            thread_local.connection.close()
            delattr(thread_local, 'connection')
    
    def get_url_model(self):
        conn = self.get_connection()
        return URLModel(conn)