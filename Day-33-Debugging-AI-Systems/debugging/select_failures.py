from typing import Any


def select_failures(
    results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Select failed evaluation results."""

    failures = []

    for result in results:
        if not result.get("passed", False):
            failures.append(result)

    return failures


def summarize_failures(
    failures: list[dict[str, Any]],
) -> dict[str, int]:
    """Return a simple failure summary."""

    summary: dict[str, int] = {}

    for failure in failures:
        category = failure.get(
            "category",
            "unknown",
        )

        summary[category] = (
            summary.get(category, 0) + 1
        )

    return summary