import json
from pathlib import Path


DIMENSIONS = [
    "groundedness",
    "correctness",
    "completeness",
]

DEFAULT_THRESHOLD = 0.5


def aggregate_scores(results: list[dict]) -> dict:
    """
    Calculate average score for each evaluation dimension.
    """

    if not results:
        raise ValueError("No evaluation results provided.")

    totals = {
        dimension: 0
        for dimension in DIMENSIONS
    }

    counts = {
        dimension: 0
        for dimension in DIMENSIONS
    }

    for result in results:

        evaluation = result.get("evaluation")

        if not evaluation:
            continue

        for dimension in DIMENSIONS:

            score = evaluation[dimension]["score"]

            totals[dimension] += score
            counts[dimension] += 1

    averages = {}

    for dimension in DIMENSIONS:

        if counts[dimension] == 0:
            raise ValueError(
                f"No scores found for {dimension}."
            )

        averages[dimension] = round(
            totals[dimension] / counts[dimension],
            2,
        )

    return averages


def identify_lowest_dimension(
    aggregate_scores: dict,
) -> tuple[str, float]:
    """
    Identify the dimension with the lowest average score.
    """

    lowest_dimension = min(
        aggregate_scores,
        key=aggregate_scores.get,
    )

    lowest_score = aggregate_scores[
        lowest_dimension
    ]

    return lowest_dimension, lowest_score


def compare_with_baseline(
    current_scores: dict,
    baseline_scores: dict,
    threshold: float = DEFAULT_THRESHOLD,
) -> dict:
    """
    Compare current evaluation scores with stored baseline.

    FAIL occurs when the score drops more than the threshold.
    """

    comparison = {}

    for dimension in DIMENSIONS:

        baseline = baseline_scores[dimension]
        current = current_scores[dimension]

        drop = round(
            baseline - current,
            2,
        )

        passed = drop <= threshold

        comparison[dimension] = {
            "baseline": baseline,
            "current": current,
            "drop": drop,
            "threshold": threshold,
            "status": "PASS" if passed else "FAIL",
        }

    return comparison


def regression_test_runner(
    current_scores: dict,
    baseline_path: str = "baselines/baseline.json",
) -> dict:
    """
    Run regression tests against a stored baseline.
    """

    path = Path(baseline_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Baseline file not found: {baseline_path}"
        )

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:
        baseline_data = json.load(file)

    baseline_scores = {
        dimension: baseline_data[dimension]
        for dimension in DIMENSIONS
    }

    threshold = baseline_data.get(
        "threshold",
        DEFAULT_THRESHOLD,
    )

    comparison = compare_with_baseline(
        current_scores=current_scores,
        baseline_scores=baseline_scores,
        threshold=threshold,
    )

    overall_pass = all(
        item["status"] == "PASS"
        for item in comparison.values()
    )

    print("\n" + "=" * 60)
    print("REGRESSION TEST RESULTS")
    print("=" * 60)

    for dimension, result in comparison.items():

        print(
            f"{dimension.capitalize():15} "
            f"Baseline: {result['baseline']:.2f} | "
            f"Current: {result['current']:.2f} | "
            f"Drop: {result['drop']:.2f} | "
            f"{result['status']}"
        )

    print("-" * 60)

    print(
        "Overall Status:",
        "PASS" if overall_pass else "FAIL",
    )

    print("=" * 60)

    return {
        "overall_status": (
            "PASS"
            if overall_pass
            else "FAIL"
        ),
        "dimensions": comparison,
    }


def save_baseline(
    aggregate_scores: dict,
    baseline_path: str = "baselines/baseline.json",
    threshold: float = DEFAULT_THRESHOLD,
):
    """
    Save aggregate evaluation scores as the regression baseline.
    """

    path = Path(baseline_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    baseline_data = {
        "groundedness": aggregate_scores["groundedness"],
        "correctness": aggregate_scores["correctness"],
        "completeness": aggregate_scores["completeness"],
        "threshold": threshold,
    }

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            baseline_data,
            file,
            indent=4,
        )

    print(
        f"Baseline saved to: {baseline_path}"
    )


if __name__ == "__main__":

    example_scores = {
        "groundedness": 4.7,
        "correctness": 4.8,
        "completeness": 4.5,
    }

    lowest_dimension, lowest_score = (
        identify_lowest_dimension(
            example_scores
        )
    )

    print(
        f"Lowest dimension: "
        f"{lowest_dimension}"
    )

    print(
        f"Lowest score: "
        f"{lowest_score}"
    )