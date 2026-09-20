from pathlib import Path

from workflow import run_workflow


TOPICS = [
    "AI Agents",
    "Retrieval Augmented Generation",
    "FastAPI",
]


def main():
    reports = {}

    print("=" * 60)
    print("DAY 28 — THREE TOPIC WORKFLOW")
    print("=" * 60)

    for topic in TOPICS:

        print("\n" + "-" * 60)
        print(f"Running workflow for: {topic}")
        print("-" * 60)

        # Start fresh for each topic
        state = run_workflow(
            topic,
            resume=False,
        )

        if state.error:
            print(
                f"Workflow failed for {topic}: "
                f"{state.error}"
            )
            continue

        reports[topic] = state.final_report

        print(
            f"Completed: {state.completed_steps}"
        )

    # ========================================================
    # COMPARISON
    # ========================================================

    comparison_path = Path(
        "reports/three_report_comparison.md"
    )

    comparison_path.parent.mkdir(
        exist_ok=True
    )

    with open(
        comparison_path,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "# Three Research Reports Comparison\n\n"
        )

        for topic, report in reports.items():

            file.write(
                f"## {topic}\n\n"
            )

            file.write(
                report
            )

            file.write(
                "\n\n---\n\n"
            )

    print("\n" + "=" * 60)
    print("THREE TOPIC COMPARISON COMPLETE")
    print("=" * 60)

    print(
        f"Comparison saved to: {comparison_path}"
    )


if __name__ == "__main__":
    main()