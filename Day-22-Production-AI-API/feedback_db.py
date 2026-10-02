import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).resolve().parent / "feedback.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_feedback_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            query TEXT NOT NULL,
            response_excerpt TEXT NOT NULL,
            rating INTEGER NOT NULL CHECK (rating IN (1, -1)),
            timestamp TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_feedback(
    session_id: str,
    query: str,
    response_excerpt: str,
    rating: int
):
    if rating not in (1, -1):
        raise ValueError("Rating must be 1 or -1")

    response_excerpt = response_excerpt[:100]

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO feedback
        (session_id, query, response_excerpt, rating, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            session_id,
            query,
            response_excerpt,
            rating,
            datetime.now(timezone.utc).isoformat()
        )
    )

    connection.commit()
    connection.close()