import sqlite3
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
from pathlib import Path

from config import config


class DatabaseManager:
    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or config.database_path
        self._ensure_database()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        finally:
            conn.close()

    def _ensure_database(self):
        """Create database tables if they don't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dates (
                    id INTEGER PRIMARY KEY,
                    date TEXT UNIQUE NOT NULL,
                    year INTEGER,
                    month INTEGER,
                    day INTEGER
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS currencies (
                    id INTEGER PRIMARY KEY,
                    code TEXT UNIQUE NOT NULL,
                    name TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sources (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rates (
                    id INTEGER PRIMARY KEY,
                    datetime_id INTEGER,
                    currency_id INTEGER,
                    source_id INTEGER,
                    rate_value REAL NOT NULL,
                    rate_type TEXT CHECK(rate_type IN ('buy', 'sell')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (datetime_id) REFERENCES dates (id),
                    FOREIGN KEY (currency_id) REFERENCES currencies (id),
                    FOREIGN KEY (source_id) REFERENCES sources (id)
                )
            ''')

            conn.commit()

    def insert_date(self, date_str: str) -> int:
        """Insert or get date ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO dates (date, year, month, day)
                VALUES (?, strftime('%Y', ?), strftime('%m', ?), strftime('%d', ?))
            ''', (date_str, date_str, date_str, date_str))
            conn.commit()

            cursor.execute('SELECT id FROM dates WHERE date = ?', (date_str,))
            return cursor.fetchone()[0]

    def insert_currency(self, code: str, name: str | None = None) -> int:
        """Insert or get currency ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO currencies (code, name)
                VALUES (?, ?)
            ''', (code, name))
            conn.commit()

            cursor.execute('SELECT id FROM currencies WHERE code = ?', (code,))
            return cursor.fetchone()[0]

    def insert_source(self, name: str, description: str | None = None) -> int:
        """Insert or get source ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO sources (name, description)
                VALUES (?, ?)
            ''', (name, description))
            conn.commit()

            cursor.execute('SELECT id FROM sources WHERE name = ?', (name,))
            return cursor.fetchone()[0]

    def insert_rates(self, rates_data: List[Dict[str, Any]]):
        """Insert multiple rate records"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany('''
                INSERT INTO rates (datetime_id, currency_id, source_id, rate_value, rate_type)
                VALUES (?, ?, ?, ?, ?)
            ''', rates_data)
            conn.commit()

    def get_rates_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Query rates within date range"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT r.rate_value, r.rate_type, d.date, c.code, s.name as source
                FROM rates r
                JOIN dates d ON r.datetime_id = d.id
                JOIN currencies c ON r.currency_id = c.id
                JOIN sources s ON r.source_id = s.id
                WHERE d.date BETWEEN ? AND ?
                ORDER BY d.date, c.code
            ''', (start_date, end_date))

            return [dict(row) for row in cursor.fetchall()]


# Global database manager instance
db_manager = DatabaseManager()