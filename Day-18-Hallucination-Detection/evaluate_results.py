import json


def main():

    # Load raw experiment results
    with open("results.json", "r", encoding="utf-8") as f:
        results = json.load(f)

    evaluations = []

    print("=" * 70)
    print("DAY 18 - MANUAL EVALUATION")
    print("=" * 70)

    for item in results:

        response = item["no_context"].get("response")

        print("\n" + "-" * 70)
        print(f"Question ID: {item['id']}")
        print(f"Domain: {item['domain']}")
        print(f"Question: {item['question']}")
        print(f"Ground Truth: {item['ground_truth']}")
        print(f"Model Response: {response}")
        print("-" * 70)

        # Manual input
        while True:
            classification = input(
                "Classification "
                "(correct / partially_correct / hallucinated): "
            ).strip().lower()

            if classification in [
                "correct",
                "partially_correct",
                "hallucinated"
            ]:
                break

            print("Invalid classification. Please try again.")

        hallucination_type = None

        if classification == "hallucinated":

            while True:
                hallucination_type = input(
                    "Hallucination type "
                    "(fabricated_specific_fact / outdated_information / "
                    "confident_wrong_answer / plausible_unverifiable_claim): "
                ).strip().lower()

                valid_types = [
                    "fabricated_specific_fact",
                    "outdated_information",
                    "confident_wrong_answer",
                    "plausible_unverifiable_claim"
                ]

                if hallucination_type in valid_types:
                    break

                print("Invalid hallucination type. Please try again.")

        reason = input(
            "Reason for classification: "
        ).strip()

        evaluation = {
            "id": item["id"],
            "condition": "no_context",
            "classification": classification,
            "hallucination_type": hallucination_type,
            "reason": reason
        }

        evaluations.append(evaluation)

    # Save evaluations
    with open("evaluation.json", "w", encoding="utf-8") as f:
        json.dump(
            evaluations,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("\n" + "=" * 70)
    print("EVALUATION COMPLETED")
    print("=" * 70)
    print(f"Evaluated responses: {len(evaluations)}")
    print("Saved to: evaluation.json")


if __name__ == "__main__":
    main()