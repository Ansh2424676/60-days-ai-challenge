
import csv
import os
from pathlib import Path

from openai import OpenAI
from prompts import PROMPT_V1, PROMPT_V2
from prompt_reliability import validate_response_format

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

TEST_CASES = [
    {
        "id": "Q1",
        "context": "Python is a high-level programming language.",
        "question": "What is Python?",
    },
    {
        "id": "Q2",
        "context": "Python supports lists, tuples, and dictionaries.",
        "question": "Name three data structures in the context.",
    },
    {
        "id": "Q3",
        "context": "",
        "question": "What does the context say about Python?",
    },
    {
        "id": "Q4",
        "context": "Python was created by Guido van Rossum.",
        "question": "Who created Python?",
    },
    {
        "id": "Q5",
        "context": "Python is used for automation and data analysis.",
        "question": "What uses of Python are mentioned?",
    },
]


def run_evaluation(client, prompt, version):
    results = []

    for case in TEST_CASES:
        try:
            result = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": prompt},
                    {
                        "role": "user",
                        "content": (
                            f"Context:\n{case['context']}\n\n"
                            f"Question:\n{case['question']}"
                        ),
                    },
                ],
                temperature=0,
            )

            response = result.choices[0].message.content or ""
            valid, message = validate_response_format(response)

            results.append({
                "version": version,
                "case_id": case["id"],
                "format_valid": int(valid),
                "validation_message": message,
                "response": response,
                "error": "",
            })

        except Exception as exc:
            results.append({
                "version": version,
                "case_id": case["id"],
                "format_valid": 0,
                "validation_message": "",
                "response": "",
                "error": str(exc),
            })

    return results


def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY before running.")

    client = OpenAI()
    results = (
        run_evaluation(client, PROMPT_V1, "v1")
        + run_evaluation(client, PROMPT_V2, "v2")
    )

    output = Path("prompt_evaluation_results.csv")

    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    for version in ("v1", "v2"):
        subset = [r for r in results if r["version"] == version]
        valid = sum(r["format_valid"] for r in subset)
        total = len(subset)
        errors = sum(bool(r["error"]) for r in subset)

        print(
            f"{version}: {valid}/{total} format-valid; "
            f"{errors} API errors"
        )

    print(f"Results saved to: {output.resolve()}")


if __name__ == "__main__":
    main()
