import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

BASELINE_FILE = (
    BASE_DIR / "results" / "baseline_results.json"
)

AFTER_FILE = (
    BASE_DIR / "results" / "after_defence_results.json"
)


def load_results(path: Path) -> list[dict]:
    """Load attack results from JSON."""

    if not path.exists():
        return []

    return json.loads(
        path.read_text(encoding="utf-8")
    )


def count_classifications(
    results: list[dict],
) -> dict[str, int]:
    """Count attack classifications."""

    counts = {
        "successful_injection": 0,
        "partial_compliance": 0,
        "successfully_blocked": 0,
        "error": 0,
    }

    for result in results:
        classification = result.get(
            "classification",
            "error",
        )

        if classification not in counts:
            counts["error"] += 1
        else:
            counts[classification] += 1

    return counts


def create_comparison(
    baseline: list[dict],
    after: list[dict],
) -> list[dict]:
    """Compare baseline and defended results."""

    after_by_id = {
        result["id"]: result
        for result in after
    }

    comparison = []

    for before_result in baseline:
        attack_id = before_result["id"]

        after_result = after_by_id.get(
            attack_id,
            {},
        )

        comparison.append(
            {
                "id": attack_id,
                "category": before_result.get(
                    "category"
                ),
                "before": before_result.get(
                    "classification"
                ),
                "after": after_result.get(
                    "classification",
                    "not_run",
                ),
            }
        )

    return comparison


def main() -> None:
    baseline = load_results(
        BASELINE_FILE
    )

    after = load_results(
        AFTER_FILE
    )

    if not baseline:
        print(
            "Baseline results not found."
        )
        return

    if not after:
        print(
            "After-defence results not found."
        )
        return

    before_counts = count_classifications(
        baseline
    )

    after_counts = count_classifications(
        after
    )

    comparison = create_comparison(
        baseline,
        after,
    )

    output = {
        "total_attacks": len(baseline),
        "before": before_counts,
        "after": after_counts,
        "comparison": comparison,
    }

    output_file = (
        BASE_DIR
        / "results"
        / "attack_comparison.json"
    )

    output_file.write_text(
        json.dumps(
            output,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"Total attacks: {len(baseline)}"
    )

    print("\nBefore defence:")
    print(
        json.dumps(
            before_counts,
            indent=2,
        )
    )

    print("\nAfter defence:")
    print(
        json.dumps(
            after_counts,
            indent=2,
        )
    )

    print(
        f"\nComparison saved to: {output_file}"
    )


if __name__ == "__main__":
    main()