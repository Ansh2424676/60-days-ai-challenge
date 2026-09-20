import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4o-mini"
)


def run_assistant(
    question: str,
    context: str,
) -> str:
    """
    Run the knowledge assistant using the supplied context.

    The context represents the information retrieved
    for the evaluation question.
    """

    prompt = f"""
You are a knowledge assistant.

Answer the user's question using ONLY the provided
retrieved context.

Do not invent facts.

If the context does not contain enough information,
say that the available context is insufficient.

RETRIEVED CONTEXT:
{context}

USER QUESTION:
{question}

Provide a concise and factual answer.
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a grounded knowledge assistant."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    answer = response.choices[0].message.content

    if not answer:
        raise ValueError(
            "Assistant returned an empty response."
        )

    return answer.strip()


def run_evaluation_question(item: dict) -> dict:
    """
    Run one labelled evaluation question.
    """

    answer = run_assistant(
        question=item["question"],
        context=item["context"],
    )

    return {
        "id": item["id"],
        "question": item["question"],
        "context": item["context"],
        "answer": answer,
        "ground_truth": item["ground_truth"],
    }


if __name__ == "__main__":

    test_question = {
        "id": 1,
        "question": "What is artificial intelligence?",
        "context": (
            "Artificial intelligence enables computer systems "
            "to perform tasks that normally require human "
            "intelligence, including reasoning, learning, "
            "and pattern recognition."
        ),
        "ground_truth": (
            "Artificial intelligence enables computer systems "
            "to perform tasks that normally require human "
            "intelligence, such as reasoning, learning, and "
            "pattern recognition."
        ),
    }

    result = run_evaluation_question(
        test_question
    )

    print("\nQuestion:")
    print(result["question"])

    print("\nAssistant Answer:")
    print(result["answer"])