import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

JUDGE_MODEL = "gpt-4o-mini"


JUDGE_PROMPT = """
You are an expert evaluator for an AI knowledge assistant.

Evaluate the assistant's answer using ONLY the information provided
in the question, retrieved context, answer, and ground truth.

Score each dimension from 1 to 5.

SCORING RUBRIC

1. GROUNDEDNESS
Measures whether the answer is supported by the retrieved context.

5 = Every meaningful claim is supported by the context.
4 = Almost completely supported, with only a very minor unsupported detail.
3 = Some claims are supported but there are noticeable unsupported details.
2 = Several important claims are unsupported.
1 = The answer is largely fabricated or unrelated to the context.

2. CORRECTNESS
Measures whether the answer matches the known ground truth.

5 = Fully correct and consistent with the ground truth.
4 = Mostly correct with a minor issue.
3 = Partially correct but contains a meaningful omission or error.
2 = Mostly incorrect.
1 = Completely incorrect.

3. COMPLETENESS
Measures whether the answer fully addresses the question.

5 = All important parts of the question are answered.
4 = Almost complete with a minor omission.
3 = Partially complete with some important information missing.
2 = Major parts of the question are missing.
1 = The question is essentially unanswered.

IMPORTANT RULES

- Do not reward fluent writing by itself.
- Do not assume facts that are not provided.
- Do not use outside knowledge.
- Judge the answer against the supplied context and ground truth.
- Return ONLY valid JSON.
- Scores must be integers from 1 to 5.

Return exactly this structure:

{
    "groundedness": {
        "score": 1,
        "reason": "brief explanation"
    },
    "correctness": {
        "score": 1,
        "reason": "brief explanation"
    },
    "completeness": {
        "score": 1,
        "reason": "brief explanation"
    }
}
"""


def llm_judge(
    question: str,
    context: str,
    answer: str,
    ground_truth: str,
) -> dict:
    """
    Evaluate an AI assistant answer using an LLM judge.

    Returns scores for:
    - groundedness
    - correctness
    - completeness
    """

    user_prompt = f"""
QUESTION:
{question}

RETRIEVED CONTEXT:
{context}

ASSISTANT ANSWER:
{answer}

GROUND TRUTH:
{ground_truth}
"""

    response = client.chat.completions.create(
        model=JUDGE_MODEL,
        temperature=0,
        response_format={
            "type": "json_object"
        },
        messages=[
            {
                "role": "system",
                "content": JUDGE_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    raw_content = response.choices[0].message.content

    if not raw_content:
        raise ValueError(
            "Judge returned an empty response."
        )

    result = json.loads(raw_content)

    validate_judge_result(result)

    return result


def validate_judge_result(result: dict):
    """
    Validate the structure and score range returned by the judge.
    """

    required_dimensions = [
        "groundedness",
        "correctness",
        "completeness",
    ]

    for dimension in required_dimensions:

        if dimension not in result:
            raise ValueError(
                f"Missing dimension: {dimension}"
            )

        if "score" not in result[dimension]:
            raise ValueError(
                f"Missing score for: {dimension}"
            )

        score = result[dimension]["score"]

        if not isinstance(score, int):
            raise ValueError(
                f"Score for {dimension} must be an integer."
            )

        if score < 1 or score > 5:
            raise ValueError(
                f"Score for {dimension} must be between 1 and 5."
            )


if __name__ == "__main__":

    test_result = llm_judge(
        question="What is machine learning?",
        context=(
            "Machine learning is a subset of AI where systems "
            "learn patterns from data and use those patterns "
            "to make predictions or decisions."
        ),
        answer=(
            "Machine learning is a subset of AI that learns "
            "patterns from data to make predictions or decisions."
        ),
        ground_truth=(
            "Machine learning is a subset of artificial intelligence "
            "where systems learn patterns from data and use them "
            "to make predictions or decisions."
        ),
    )

    print(
        json.dumps(
            test_result,
            indent=2,
            ensure_ascii=False,
        )
    )