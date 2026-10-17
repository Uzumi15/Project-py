import sqlite3
from pathlib import Path


class Database:
    """Небольшой слой доступа к базе SQLite."""

    def __init__(self, db_path=None):
        project_root = Path(__file__).resolve().parent.parent
        self.db_path = Path(db_path) if db_path else project_root / "users.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")

    def initialize(self):
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'user'
                        CHECK (role IN ('user', 'admin')),
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def fetchone(self, query, parameters=()):
        return self.connection.execute(query, parameters).fetchone()

    def fetchall(self, query, parameters=()):
        return self.connection.execute(query, parameters).fetchall()

    def execute(self, query, parameters=()):
        with self.connection:
            cursor = self.connection.execute(query, parameters)
            return cursor.lastrowid

    def close(self):
        self.connection.close()
