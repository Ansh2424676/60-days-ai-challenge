import sqlite3
from pathlib import Path

Path("Day-54-User-Feedback").mkdir(exist_ok=True)

db_path = "Day-54-User-Feedback/feedback.db"

with sqlite3.connect(db_path) as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            rating INTEGER CHECK (rating BETWEEN 1 AND 5),
            comment TEXT,
            topic TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

print(f"Feedback database ready: {db_path}")
