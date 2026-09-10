import json
from collections import Counter


def main():
    with open("evaluation.json", "r", encoding="utf-8") as f:
        evaluations = json.load(f)

    total = len(evaluations)

    classifications = Counter(
        item["classification"]
        for item in evaluations
    )

    hallucinated = classifications.get("hallucinated", 0)
    correct = classifications.get("correct", 0)
    partially_correct = classifications.get(
        "partially_correct", 0
    )

    hallucination_rate = (
        hallucinated / total * 100
        if total > 0
        else 0
    )

    hallucination_types = Counter(
        item["hallucination_type"]
        for item in evaluations
        if item["classification"] == "hallucinated"
    )

    print("=" * 60)
    print("DAY 18 - HALLUCINATION METRICS")
    print("=" * 60)

    print(f"Total responses:       {total}")
    print(f"Correct:               {correct}")
    print(f"Partially correct:     {partially_correct}")
    print(f"Hallucinated:          {hallucinated}")
    print(f"Hallucination rate:    {hallucination_rate:.2f}%")

    print("\nHallucination Categories")
    print("-" * 60)

    categories = [
        "fabricated_specific_fact",
        "outdated_information",
        "confident_wrong_answer",
        "plausible_unverifiable_claim"
    ]

    for category in categories:
        print(
            f"{category}: "
            f"{hallucination_types.get(category, 0)}"
        )


if __name__ == "__main__":
    main()