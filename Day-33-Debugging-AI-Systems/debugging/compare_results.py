from typing import Any


def compare_results(
    expected: dict[str, Any],
    actual: dict[str, Any],
) -> dict[str, Any]:
    """Compare expected and actual results."""

    differences: dict[str, dict[str, Any]] = {}

    keys = set(expected) | set(actual)

    for key in sorted(keys):
        expected_value = expected.get(key)
        actual_value = actual.get(key)

        if expected_value != actual_value:
            differences[key] = {
                "expected": expected_value,
                "actual": actual_value,
            }

    return {
        "match": not differences,
        "differences": differences,
    }


def compare_answers(
    expected: str,
    actual: str,
) -> dict[str, Any]:
    """Compare two generated answers."""

    return {
        "match": expected.strip() == actual.strip(),
        "expected": expected,
        "actual": actual,
    }