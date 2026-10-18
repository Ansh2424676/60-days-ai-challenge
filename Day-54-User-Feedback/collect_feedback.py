import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "feedback.db"


def collect_feedback():
    print("\n=== Day 54: User Feedback ===")

    query = input("User query: ").strip()
    if not query:
        print("Query cannot be empty.")
        return

    while True:
        try:
            rating = int(input("Rating (1-5): "))
            if 1 <= rating <= 5:
                break
            print("Enter a rating between 1 and 5.")
        except ValueError:
            print("Enter a valid number.")

    comment = input("Comment (optional): ").strip()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                rating INTEGER CHECK(rating BETWEEN 1 AND 5),
                comment TEXT,
                topic TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            INSERT INTO feedback (query, rating, comment)
            VALUES (?, ?, ?)
        """, (query, rating, comment))

    print("Feedback saved successfully!")


if __name__ == "__main__":
    collect_feedback()