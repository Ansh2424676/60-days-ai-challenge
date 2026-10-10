
"""Day 46: Advanced retrieval evaluation scaffold."""

import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
RESULTS_FILE = RESULTS_DIR / "advanced_retrieval_results.csv"

FIELDNAMES = [
    "query",
    "technique",
    "answer",
    "quality_score",
    "latency_seconds",
    "notes",
]


def save_results(rows):
    """Save measured evaluation results to CSV."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    with RESULTS_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Results saved to: {RESULTS_FILE}")


if __name__ == "__main__":
    print("Day 46 evaluation scaffold is ready.")
    print("Next: connect the retriever and Day 29 LLM judge.")

def summarize_results(rows):
    """Summarize measured quality and latency by technique."""
    from collections import defaultdict
    from statistics import mean

    grouped = defaultdict(list)

    for row in rows:
        grouped[row["technique"]].append(row)

    summary = {}

    for technique, items in grouped.items():
        quality_scores = [
            float(item["quality_score"])
            for item in items
            if item.get("quality_score") not in ("", None)
        ]
        latencies = [
            float(item["latency_seconds"])
            for item in items
            if item.get("latency_seconds") not in ("", None)
        ]

        summary[technique] = {
            "evaluated_queries": len(items),
            "mean_quality": (
                round(mean(quality_scores), 3)
                if quality_scores else None
            ),
            "mean_latency_seconds": (
                round(mean(latencies), 3)
                if latencies else None
            ),
        }

    return summary
