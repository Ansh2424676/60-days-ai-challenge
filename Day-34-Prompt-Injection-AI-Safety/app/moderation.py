import os

from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


MODERATION_MODEL = "omni-moderation-latest"


BLOCK_CATEGORIES = {
    "harassment",
    "harassment/threatening",
    "hate",
    "hate/threatening",
    "self-harm",
    "self-harm/intent",
    "self-harm/instructions",
}


def check_moderation(text: str) -> dict:
    """Run OpenAI moderation before sending input to the LLM."""

    response = client.moderations.create(
        model=MODERATION_MODEL,
        input=text,
    )

    result = response.results[0]

    categories = result.categories.model_dump()

    flagged_categories = [
        category
        for category, flagged in categories.items()
        if flagged and category in BLOCK_CATEGORIES
    ]

    return {
        "allowed": not flagged_categories,
        "flagged": bool(flagged_categories),
        "flagged_categories": flagged_categories,
    }