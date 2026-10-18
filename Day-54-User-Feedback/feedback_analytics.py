import sqlite3
import re
from collections import Counter, defaultdict
from pathlib import Path

DB = Path(__file__).parent / "feedback.db"

TOPICS = {
    "Accuracy": ["wrong", "incorrect", "inaccurate", "hallucination", "fact"],
    "Clarity": ["unclear", "confusing", "clear", "explain", "understand"],
    "Speed": ["slow", "latency", "wait", "timeout", "fast"],
    "Retrieval": ["search", "document", "source", "retrieval", "missing"],
    "Technical": ["error", "bug", "failed", "exception", "crash"],
}

def detect_topic(text):
    text = (text or "").lower()
    counts = {
        topic: sum(1 for word in keywords if word in text)
        for topic, keywords in TOPICS.items()
    }
    best = max(counts, key=counts.get)
    return best if counts[best] else "Other"

def main():
    if not DB.exists():
        print("Database not found:", DB)
        return

    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT query, rating, comment, created_at FROM feedback"
        ).fetchall()

    total = len(rows)
    print("\n=== DAY 54 FEEDBACK REPORT ===")
    print("Total feedback records:", total)

    if not total:
        print("No feedback yet. Collect genuine user responses first.")
        return

    positive = sum(1 for r in rows if r["rating"] and r["rating"] >= 4)
    rated = sum(1 for r in rows if r["rating"] is not None)
    print("Rated responses:", rated)
    print("Positive ratings (4-5):",
          f"{positive / rated * 100:.1f}%" if rated else "N/A")

    groups = defaultdict(list)
    keywords = Counter()

    for r in rows:
        text = f'{r["query"] or ""} {r["comment"] or ""}'
        topic = detect_topic(text)
        failed = r["rating"] is not None and r["rating"] <= 2
        groups[topic].append((failed, text))
        keywords.update(
            w for w in re.findall(r"\b[a-z]{4,}\b", text.lower())
            if w not in {"that", "this", "with", "from", "have", "could"}
        )

    print("\nTopic clusters (highest failure rate first):")
    report = []
    for topic, items in groups.items():
        failures = sum(f for f, _ in items)
        rate = failures / len(items) * 100
        report.append((topic, len(items), failures, rate))

    for topic, count, failures, rate in sorted(
        report, key=lambda x: x[3], reverse=True
    )[:3]:
        print(f"{topic}: {failures}/{count} low ratings ({rate:.1f}% failure proxy)")

    print("\nTop keywords:", keywords.most_common(10))

    print("\n=== PRIORITISED IMPROVEMENTS ===")
    print("1. Fix the topic with the highest low-rating rate; validate with more real queries.")
    print("2. Improve unclear or inaccurate responses; review actual negative comments.")
    print("3. Add monitoring for response quality and latency; compare before/after results.")

    print("\nNote: Low ratings (1-2) are used as a failure proxy, not a verified technical failure.")
    print("This report covers recorded entries only, not necessarily a full 24-hour period.")

if __name__ == "__main__":
    main()