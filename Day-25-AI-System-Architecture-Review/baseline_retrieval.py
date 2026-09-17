import json
from pathlib import Path

from rag_pipeline import retrieve
from evaluate import TESTS


BASE_DIR = Path(__file__).resolve().parent


def main() -> None:
    """Run the 15-query retrieval evaluation and save baseline results."""
    results = []

    for test in TESTS:
        retrieved = retrieve(test["query"], k=3)

        row = {
            "id": test["id"],
            "query": test["query"],
            "expected_ids": test["expected_ids"],
            "retrieved_ids": [item["id"] for item in retrieved],
            "retrieval_scores": [
                round(item["score"], 4)
                for item in retrieved
            ],
        }

        results.append(row)

        print(
            f"{test['id']}: "
            f"Expected={test['expected_ids']} "
            f"Retrieved={row['retrieved_ids']}"
        )

    output_path = BASE_DIR / "results" / "baseline_before.json"

    output_path.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8",
    )

    print("\nRetrieval baseline saved:")
    print(output_path)


if __name__ == "__main__":
    main()