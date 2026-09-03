import sqlite3
from datetime import datetime

class MemoryDatabase:
    def __init__(self, db_path="pearl_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Initialize database tables for chat history and key-value memory."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Table to store long-term chat history
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Table to store user preferences/memory (e.g., name, favorite topics)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_memory (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_message(self, role: str, content: str):
        """Save a user or assistant message to database."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO chat_history (role, content) VALUES (?, ?)",
                (role, content)
            )
            conn.commit()

    def get_recent_history(self, limit=10):
        """Retrieve recent conversation history."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT role, content FROM chat_history ORDER BY id DESC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            # Reverse to maintain chronological order
            return [{"role": r[0], "content": r[1]} for r in reversed(rows)]

    def set_memory(self, key: str, value: str):
        """Store a preference or key fact about the user."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_memory (key, value, updated_at) 
                VALUES (?, ?, ?) 
                ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at
            """, (key, value, datetime.now()))
            conn.commit()

    def get_memory(self, key: str) -> str:
        """Fetch stored memory value."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM user_memory WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else None