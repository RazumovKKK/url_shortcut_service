import sqlite3
from typing import Optional


class URL:
    def __init__(self, id: int, url_shortcut: str, url: str):
        self.id = id
        self.url_shortcut = url_shortcut
        self.url = url

class URLModel:
    def __init__(self, db_path: str = "urls.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()
    
    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()
    
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url_shortcut TEXT NOT NULL UNIQUE,
                url TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_url 
            ON urls(url)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_url_shortcut 
            ON urls(url_shortcut)
        ''')
        self.conn.commit()
    
    def create(self, url_shortcut: str, url: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO urls (url_shortcut, url) VALUES (?, ?)',
            (url_shortcut, url)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    
    def get_by_shortcut(self, url_shortcut: str) -> Optional[URL]:
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT id, url_shortcut, url FROM urls WHERE url_shortcut = ?',
            (url_shortcut,)
        )
        row = cursor.fetchone()
        if row:
            return URL(id=row[0], url_shortcut=row[1], url=row[2])
        return None
    
    def search_by_url(self, url: str) -> list[URL]:
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT id, url_shortcut, url FROM urls WHERE url LIKE ?',
            (f'%{url}%',)
        )
        rows = cursor.fetchall()
        return [
            URL(id=row[0], url_shortcut=row[1], url=row[2])
            for row in rows
        ]
    