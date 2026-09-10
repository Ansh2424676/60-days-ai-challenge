import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = "gpt-4o-mini"


def ask_without_context(question):
    """
    Ask GPT-4o-mini a factual question without
    providing any external context or retrieval.
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


def main():

    # Load the 20-question dataset
    with open("questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    results = []

    print("=" * 60)
    print("DAY 18 - NO CONTEXT HALLUCINATION EXPERIMENT")
    print("=" * 60)

    for item in questions:

        print(f"\nProcessing Q{item['id']}/20")
        print(f"Question: {item['question']}")

        try:
            answer = ask_without_context(item["question"])

            result = {
                "id": item["id"],
                "domain": item["domain"],
                "question": item["question"],
                "ground_truth": item["ground_truth"],
                "no_context": {
                    "model": MODEL,
                    "response": answer
                }
            }

            results.append(result)

            print(f"Response: {answer}")

        except Exception as e:

            print(f"ERROR: {e}")

            result = {
                "id": item["id"],
                "domain": item["domain"],
                "question": item["question"],
                "ground_truth": item["ground_truth"],
                "no_context": {
                    "model": MODEL,
                    "response": None,
                    "error": str(e)
                }
            }

            results.append(result)

    # Save results
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(
            results,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("\n" + "=" * 60)
    print("EXPERIMENT COMPLETED")
    print("=" * 60)
    print(f"Total questions: {len(results)}")
    print("Results saved to: results.json")


if __name__ == "__main__":
    main()