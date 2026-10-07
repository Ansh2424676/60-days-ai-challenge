import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional


# Database location
BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE_PATH = BASE_DIR / "app.db"


def get_connection():
    """
    Create and return a SQLite database connection.
    """
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """
    Create required database tables if they do not already exist.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # Request / response logs
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS request_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            query TEXT NOT NULL,
            response_excerpt TEXT,
            latency_ms REAL,
            retrieval_score REAL,
            timestamp TEXT NOT NULL
        )
        """
    )

    # Product feedback
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            query TEXT NOT NULL,
            rating TEXT NOT NULL,
            correct INTEGER NOT NULL,
            grounded INTEGER NOT NULL,
            source_quality INTEGER NOT NULL,
            comment TEXT,
            timestamp TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def log_request(
    session_id: str,
    query: str,
    response_excerpt: str,
    latency_ms: float,
    retrieval_score: Optional[float]
):
    """
    Store one API request/response record.
    """

    connection = get_connection()
    cursor = connection.cursor()

    timestamp = datetime.now(timezone.utc).isoformat()

    cursor.execute(
        """
        INSERT INTO request_logs (
            session_id,
            query,
            response_excerpt,
            latency_ms,
            retrieval_score,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,
            query,
            response_excerpt,
            latency_ms,
            retrieval_score,
            timestamp
        )
    )

    connection.commit()
    connection.close()


def save_feedback(
    session_id: str,
    query: str,
    rating: str,
    correct: bool,
    grounded: bool,
    source_quality: int,
    comment: Optional[str]
):
    """
    Store product-specific user feedback.
    """

    connection = get_connection()
    cursor = connection.cursor()

    timestamp = datetime.now(timezone.utc).isoformat()

    cursor.execute(
        """
        INSERT INTO feedback (
            session_id,
            query,
            rating,
            correct,
            grounded,
            source_quality,
            comment,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,
            query,
            rating,
            int(correct),
            int(grounded),
            source_quality,
            comment,
            timestamp
        )
    )

    feedback_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return feedback_id