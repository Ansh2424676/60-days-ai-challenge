
import csv
from pathlib import Path

CSV_FILE = Path("prompt_evaluation_results.csv")
REPORT_FILE = Path("DAY47_PROMPT_RELIABILITY_REPORT.md")


def main():
    if not CSV_FILE.exists():
        raise FileNotFoundError(
            "Run evaluate_prompts.py first to create the results CSV."
        )

    with CSV_FILE.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise ValueError("Evaluation CSV has no results.")

    lines = [
        "# Day 47 — Prompt Engineering for Production Reliability",
        "",
        "## Evaluation Results",
        "",
        "| Version | Valid responses | Total | Format compliance | API errors |",
        "|---|---:|---:|---:|---:|",
    ]

    for version in ("v1", "v2"):
        subset = [r for r in rows if r["version"] == version]
        total = len(subset)
        valid = sum(int(r["format_valid"]) for r in subset)
        errors = sum(bool(r.get("error", "").strip()) for r in subset)
        rate = valid / total * 100 if total else 0

        lines.append(
            f"| {version.upper()} | {valid} | {total} | "
            f"{rate:.1f}% | {errors} |"
        )

    lines.extend([
        "",
        "## Per-Question Results",
        "",
        "| Version | Case | Format valid | Error |",
        "|---|---|---:|---|",
    ])

    for row in rows:
        lines.append(
            f"| {row['version']} | {row['case_id']} | "
            f"{row['format_valid']} | "
            f"{'Yes' if row.get('error', '').strip() else 'No'} |"
        )

    lines.extend([
        "",
        "## Scope and Limitations",
        "",
        "- Format compliance checks required sections and allowed status values.",
        "- This metric does not independently verify factual correctness.",
        "- The test set contains only five illustrative questions per prompt.",
        "- API errors are reported separately and should not be counted as successful responses.",
        "",
        "## Conclusion",
        "",
        "Compare V1 and V2 using the measured results above. "
        "Do not claim an improvement unless the results support it.",
        "",
    ])

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report generated: {REPORT_FILE.resolve()}")


if __name__ == "__main__":
    main()
