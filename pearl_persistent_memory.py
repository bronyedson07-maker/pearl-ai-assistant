import sqlite3
import os

class PearlPersistentMemory:
    """
    Manages long-term persistent facts, preferences, and project notes
    using a local SQLite database.
    """
    def __init__(self, db_name="pearl_memory.db"):
        self.db_path = os.path.join(os.path.expanduser("~"), db_name)
        self.init_db()

    def init_db(self):
        """Initializes the database schema if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    key_info TEXT UNIQUE NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def remember(self, key_info, category="preference"):
        """Saves or updates a fact into persistent memory."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO memories (category, key_info) VALUES (?, ?)",
                    (category, key_info)
                )
                conn.commit()
                return f"I've remembered that: '{key_info}'"
            except sqlite3.IntegrityError:
                return f"I already have that stored in memory."

    def recall_all(self):
        """Retrieves all stored long-term memories."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, category, key_info FROM memories")
            rows = cursor.fetchall()
            return rows

    def forget(self, memory_id):
        """Deletes a specific memory entry by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            conn.commit()
            return f"Memory ID {memory_id} has been removed."

    def clear_all_memories(self):
        """Clears all long-term persistent memories."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memories")
            conn.commit()
            return "All persistent memories have been cleared."