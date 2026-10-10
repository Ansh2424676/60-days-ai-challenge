
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).with_name("user_memory.db")


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS UserProfile (
                user_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                preferred_response_style TEXT DEFAULT '',
                research_interests TEXT DEFAULT '[]',
                current_goals TEXT DEFAULT '[]',
                knowledge_level TEXT DEFAULT 'intermediate',
                user_summary TEXT DEFAULT '',
                interaction_count INTEGER DEFAULT 0,
                updated_at TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS InteractionHistory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                question TEXT NOT NULL,
                response TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id)
                    REFERENCES UserProfile(user_id)
                    ON DELETE CASCADE
            )
        """)


def create_user(user_id):
    now = datetime.now(timezone.utc).isoformat()

    with get_connection() as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("""
            INSERT OR IGNORE INTO UserProfile
            (user_id, created_at, updated_at)
            VALUES (?, ?, ?)
        """, (user_id, now, now))

    return get_user(user_id)


def get_user(user_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM UserProfile WHERE user_id = ?",
            (user_id,)
        ).fetchone()

    return dict(row) if row else None


def update_user(user_id, **fields):
    allowed_fields = {
        "preferred_response_style",
        "research_interests",
        "current_goals",
        "knowledge_level",
        "user_summary",
        "interaction_count",
    }

    updates = {
        key: value for key, value in fields.items()
        if key in allowed_fields
    }

    if not updates:
        return get_user(user_id)

    for key in ("research_interests", "current_goals"):
        if key in updates and not isinstance(updates[key], str):
            updates[key] = json.dumps(updates[key])

    updates["updated_at"] = datetime.now(timezone.utc).isoformat()

    assignments = ", ".join(f"{key} = ?" for key in updates)
    values = list(updates.values()) + [user_id]

    with get_connection() as conn:
        conn.execute(
            f"UPDATE UserProfile SET {assignments} WHERE user_id = ?",
            values
        )

    return get_user(user_id)


def record_interaction(user_id, question, response):
    now = datetime.now(timezone.utc).isoformat()

    with get_connection() as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("""
            INSERT INTO InteractionHistory
            (user_id, question, response, created_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, question, response, now))

        conn.execute("""
            UPDATE UserProfile
            SET interaction_count = interaction_count + 1,
                updated_at = ?
            WHERE user_id = ?
        """, (now, user_id))


if __name__ == "__main__":
    initialize_database()

    profile = create_user("demo-user")
    update_user(
        "demo-user",
        preferred_response_style="Step-by-step explanations",
        research_interests=["RAG", "AI engineering"],
        current_goals=["Build a research assistant"],
        knowledge_level="intermediate",
    )

    print("Database initialized successfully.")
    print(json.dumps(get_user("demo-user"), indent=2))
