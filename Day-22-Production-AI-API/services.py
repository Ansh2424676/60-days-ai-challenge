import asyncio
import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from openai import AsyncOpenAI, RateLimitError

load_dotenv()


OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.6-luna"
)

MAX_RETRIES = int(
    os.getenv("MAX_RETRIES", "3")
)

INITIAL_BACKOFF = float(
    os.getenv("INITIAL_BACKOFF", "1.0")
)

TEST_MODE = (
    os.getenv("TEST_MODE", "true").lower() == "true"
)


client = None

if os.getenv("OPENAI_API_KEY"):
    client = AsyncOpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )


# ==================================================
# RETRIEVAL
# ==================================================

async def retrieve_documents(query: str):
    """
    Retrieval layer.

    Day 20 ke actual RAG retrieval ko baad mein
    isi function ke andar connect kar sakte hain.
    """

    # Deliberate failure trigger
    if query.lower().startswith(
        "trigger retrieval failure"
    ):
        raise RuntimeError(
            "Knowledge base retrieval failed."
        )

    await asyncio.sleep(0.05)

    return [
        {
            "id": "doc-001",
            "content": (
                "Retrieval Augmented Generation (RAG) "
                "combines information retrieval with "
                "large language model generation."
            )
        },
        {
            "id": "doc-002",
            "content": (
                "FastAPI is a Python framework for "
                "building high-performance APIs."
            )
        }
    ]


# ==================================================
# LLM GENERATION + RETRY
# ==================================================

async def generate_answer(
    query: str,
    context: str
) -> str:

    # Local testing mode
    if TEST_MODE:
        await asyncio.sleep(0.2)

        return (
            f"Test response for: {query}\n\n"
            f"Retrieved context:\n{context}"
        )

    if client is None:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured."
        )

    prompt = f"""
You are a grounded AI assistant.

Answer the user's question using only the
provided context.

Context:
{context}

Question:
{query}
"""

    # Exponential backoff
    for attempt in range(MAX_RETRIES + 1):

        try:
            response = await client.responses.create(
                model=OPENAI_MODEL,
                input=prompt
            )

            return response.output_text

        except RateLimitError:

            if attempt >= MAX_RETRIES:
                raise

            delay = INITIAL_BACKOFF * (
                2 ** attempt
            )

            print(
                f"Rate limit detected. "
                f"Retry {attempt + 1}/{MAX_RETRIES} "
                f"after {delay}s"
            )

            await asyncio.sleep(delay)

    raise RuntimeError(
        "LLM generation failed after retries."
    )


# ==================================================
# STREAMING
# ==================================================

async def stream_answer(
    query: str,
    context: str
) -> AsyncGenerator[str, None]:

    # Local testing mode
    if TEST_MODE:

        text = (
            f"Streaming response for {query}. "
            "This response is delivered incrementally "
            "using FastAPI StreamingResponse."
        )

        for word in text.split():

            await asyncio.sleep(0.08)

            yield word + " "

        return

    if client is None:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured."
        )

    prompt = f"""
Answer the question using only this context.

Context:
{context}

Question:
{query}
"""

    for attempt in range(MAX_RETRIES + 1):

        try:

            stream = await client.responses.create(
                model=OPENAI_MODEL,
                input=prompt,
                stream=True
            )

            async for event in stream:

                if event.type == (
                    "response.output_text.delta"
                ):
                    yield event.delta

            return

        except RateLimitError:

            if attempt >= MAX_RETRIES:
                raise

            delay = INITIAL_BACKOFF * (
                2 ** attempt
            )

            print(
                f"Streaming rate limit. "
                f"Retrying after {delay}s"
            )

            await asyncio.sleep(delay)


# ==================================================
# TIMEOUT TEST
# ==================================================

async def simulate_slow_pipeline():

    # Deliberately longer than 15 seconds
    await asyncio.sleep(20)