import json


def classify_response(response, ground_truth):
    print("\n" + "=" * 60)
    print("MODEL RESPONSE")
    print("=" * 60)
    print(response)

    print("\nGROUND TRUTH:")
    print(ground_truth)

    print("\nClassification:")
    print("1 = correct")
    print("2 = partially_correct")
    print("3 = hallucinated")

    choice = input("Enter choice (1/2/3): ").strip()

    classification_map = {
        "1": "correct",
        "2": "partially_correct",
        "3": "hallucinated"
    }

    classification = classification_map.get(choice)

    while classification is None:
        choice = input("Invalid choice. Enter 1, 2 or 3: ").strip()
        classification = classification_map.get(choice)

    hallucination_type = None

    if classification == "hallucinated":
        print("\nHallucination Type:")
        print("1 = fabricated_specific_fact")
        print("2 = outdated_information")
        print("3 = confident_wrong_answer")
        print("4 = plausible_unverifiable_claim")

        type_map = {
            "1": "fabricated_specific_fact",
            "2": "outdated_information",
            "3": "confident_wrong_answer",
            "4": "plausible_unverifiable_claim"
        }

        type_choice = input("Enter choice (1/2/3/4): ").strip()

        hallucination_type = type_map.get(type_choice)

        while hallucination_type is None:
            type_choice = input(
                "Invalid choice. Enter 1, 2, 3 or 4: "
            ).strip()
            hallucination_type = type_map.get(type_choice)

    reason = input("Reason for classification: ").strip()

    return {
        "classification": classification,
        "hallucination_type": hallucination_type,
        "reason": reason
    }


def main():
    with open("results.json", "r", encoding="utf-8") as f:
        results = json.load(f)

    evaluations = []

    print("=" * 60)
    print("DAY 18 - MANUAL HALLUCINATION EVALUATION")
    print("=" * 60)
    print(f"Total responses: {len(results)}")

    for item in results:
        response = item["no_context"].get("response")

        if not response:
            print(
                f"\nQ{item['id']} has no valid response. "
                "Skipping."
            )
            continue

        print("\n" + "#" * 60)
        print(f"QUESTION {item['id']}/20")
        print("#" * 60)
        print(item["question"])

        evaluation = classify_response(
            response,
            item["ground_truth"]
        )

        evaluations.append({
            "id": item["id"],
            "domain": item["domain"],
            "question": item["question"],
            "ground_truth": item["ground_truth"],
            "response": response,
            **evaluation
        })

    with open("evaluation.json", "w", encoding="utf-8") as f:
        json.dump(
            evaluations,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("\n" + "=" * 60)
    print("EVALUATION COMPLETED")
    print("=" * 60)
    print(f"Evaluated responses: {len(evaluations)}")
    print("Saved to: evaluation.json")


if __name__ == "__main__":
    main()