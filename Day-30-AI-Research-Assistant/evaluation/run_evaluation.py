import json
from pathlib import Path

from dataset import get_evaluation_dataset
from assistant_runner import run_evaluation_question
from evaluator import llm_judge
from regression import (
    aggregate_scores,
    identify_lowest_dimension,
    regression_test_runner,
    save_baseline,
)


RESULTS_PATH = "results/evaluation_results.json"
REPORT_PATH = "results/evaluation_report.md"
BASELINE_PATH = "baselines/baseline.json"


def run_full_evaluation():
    """
    Run the complete 20-question evaluation suite.
    """

    dataset = get_evaluation_dataset()

    results = []

    print("\n" + "=" * 60)
    print("DAY 29 - AI EVALUATION SYSTEM")
    print("=" * 60)

    print(
        f"Total evaluation questions: {len(dataset)}"
    )

    for index, item in enumerate(dataset, start=1):

        print(
            f"\n[{index}/{len(dataset)}] "
            f"{item['question']}"
        )

        try:

            assistant_result = (
                run_evaluation_question(item)
            )

            answer = assistant_result["answer"]

            print(
                f"Assistant answer: {answer}"
            )

            evaluation = llm_judge(
                question=item["question"],
                context=item["context"],
                answer=answer,
                ground_truth=item["ground_truth"],
            )

            print(
                "Scores:",
                f"Groundedness={evaluation['groundedness']['score']}",
                f"Correctness={evaluation['correctness']['score']}",
                f"Completeness={evaluation['completeness']['score']}",
            )

            result = {
                **assistant_result,
                "evaluation": evaluation,
            }

            results.append(result)

        except Exception as error:

            print(
                f"ERROR on question {item['id']}: "
                f"{error}"
            )

    if not results:
        raise RuntimeError(
            "No evaluation results were generated."
        )

    return results


def save_results(results):
    """
    Save detailed evaluation results as JSON.
    """

    path = Path(RESULTS_PATH)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print(
        f"\nDetailed results saved to: "
        f"{RESULTS_PATH}"
    )


def create_report(
    results,
    aggregate_scores,
    lowest_dimension,
    lowest_score,
):
    """
    Create a human-readable evaluation report.
    """

    report_lines = []

    report_lines.append(
        "# Day 29 AI Evaluation Report"
    )

    report_lines.append("")

    report_lines.append(
        "## Evaluation Summary"
    )

    report_lines.append("")

    report_lines.append(
        f"- Questions evaluated: {len(results)}"
    )

    report_lines.append(
        f"- Groundedness: "
        f"{aggregate_scores['groundedness']:.2f}/5"
    )

    report_lines.append(
        f"- Correctness: "
        f"{aggregate_scores['correctness']:.2f}/5"
    )

    report_lines.append(
        f"- Completeness: "
        f"{aggregate_scores['completeness']:.2f}/5"
    )

    report_lines.append("")

    report_lines.append(
        "## Lowest Dimension"
    )

    report_lines.append("")

    report_lines.append(
        f"- Dimension: **{lowest_dimension}**"
    )

    report_lines.append(
        f"- Average score: **{lowest_score:.2f}/5**"
    )

    report_lines.append("")

    report_lines.append(
        "## Per-Question Results"
    )

    report_lines.append("")

    report_lines.append(
        "| ID | Question | Groundedness | "
        "Correctness | Completeness |"
    )

    report_lines.append(
        "|---:|---|---:|---:|---:|"
    )

    for result in results:

        evaluation = result["evaluation"]

        groundedness = evaluation[
            "groundedness"
        ]["score"]

        correctness = evaluation[
            "correctness"
        ]["score"]

        completeness = evaluation[
            "completeness"
        ]["score"]

        question = (
            result["question"]
            .replace("|", "\\|")
        )

        report_lines.append(
            f"| {result['id']} | "
            f"{question} | "
            f"{groundedness} | "
            f"{correctness} | "
            f"{completeness} |"
        )

    report_lines.append("")

    report_lines.append(
        "## Evaluation Method"
    )

    report_lines.append("")

    report_lines.append(
        "Each assistant answer was evaluated by "
        "an LLM judge using three dimensions: "
        "groundedness, correctness, and completeness."
    )

    path = Path(REPORT_PATH)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )

    print(
        f"Evaluation report saved to: "
        f"{REPORT_PATH}"
    )


def main():

    results = run_full_evaluation()

    save_results(results)

    averages = aggregate_scores(
        results
    )

    (
        lowest_dimension,
        lowest_score,
    ) = identify_lowest_dimension(
        averages
    )

    print("\n" + "=" * 60)
    print("AGGREGATE RESULTS")
    print("=" * 60)

    for dimension, score in averages.items():

        print(
            f"{dimension.capitalize():15}: "
            f"{score:.2f}/5"
        )

    print("-" * 60)

    print(
        f"Lowest dimension: "
        f"{lowest_dimension}"
    )

    print(
        f"Lowest score: "
        f"{lowest_score:.2f}/5"
    )

    print("=" * 60)

    create_report(
        results=results,
        aggregate_scores=averages,
        lowest_dimension=lowest_dimension,
        lowest_score=lowest_score,
    )

    baseline_path = Path(
        BASELINE_PATH
    )

    if not baseline_path.exists():

        print(
            "\nNo baseline found."
        )

        print(
            "Creating baseline from "
            "the current evaluation..."
        )

        save_baseline(
            aggregate_scores=averages,
            baseline_path=BASELINE_PATH,
        )

    else:

        print(
            "\nExisting baseline found."
        )

        regression_test_runner(
            current_scores=averages,
            baseline_path=BASELINE_PATH,
        )


if __name__ == "__main__":
    main()