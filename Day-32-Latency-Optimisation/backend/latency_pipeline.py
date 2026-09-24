import asyncio
import os
import time

import faiss
import numpy as np
from openai import AsyncOpenAI

from backend.profiler import PipelineProfiler

EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o"

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DOCUMENTS = [
    "Artificial intelligence is used in healthcare for diagnosis and medical research.",
    "Machine learning systems learn patterns from data to make predictions.",
    "FastAPI is a Python framework for building high-performance APIs.",
    "Redis is an in-memory data store commonly used for caching.",
    "FAISS is a library for efficient similarity search over vectors.",
]


async def create_index():
    response = await client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=DOCUMENTS,
    )

    vectors = np.array(
        [item.embedding for item in response.data],
        dtype="float32",
    )

    faiss.normalize_L2(vectors)

    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    return index, vectors


async def generate_embedding(query: str):
    response = await client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query,
    )

    vector = np.array(
        [response.data[0].embedding],
        dtype="float32",
    )

    faiss.normalize_L2(vector)

    return vector


async def search_faiss(index, vector):
    scores, indices = index.search(vector, k=3)

    results = [
        DOCUMENTS[index_value]
        for index_value in indices[0]
        if index_value >= 0
    ]

    return results


def build_prompt(query: str, documents: list[str]) -> str:
    context = "\n".join(
        f"- {document}"
        for document in documents
    )

    return f"""
Answer the user's question using the provided context.

Context:
{context}

Question:
{query}

Give a concise and factual answer.
""".strip()


async def generate_response(prompt: str):
    response = await client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
    )

    return response.choices[0].message.content


def format_response(
    query: str,
    answer: str,
    timings: list[dict],
) -> dict:
    return {
        "query": query,
        "answer": answer,
        "timings": timings,
    }


async def run_pipeline(query: str):
    profiler = PipelineProfiler()

    # Embedding
    start = profiler.start("embedding")
    vector = await generate_embedding(query)
    profiler.end("embedding", start)

    # FAISS search
    start = profiler.start("faiss_search")
    index, _ = await create_index()
    documents = await search_faiss(index, vector)
    profiler.end("faiss_search", start)

    # Prompt construction
    start = profiler.start("prompt_construction")
    prompt = build_prompt(query, documents)
    profiler.end("prompt_construction", start)

    # LLM generation
    start = profiler.start("llm_generation")
    answer = await generate_response(prompt)
    profiler.end("llm_generation", start)

    # Response formatting
    start = profiler.start("response_formatting")
    result = format_response(
        query,
        answer,
        profiler.breakdown(),
    )
    profiler.end("response_formatting", start)

    return result


async def main():
    result = await run_pipeline(
        "How is artificial intelligence used in healthcare?"
    )

    print("\nAnswer:")
    print(result["answer"])

    print("\nTiming:")
    for timing in result["timings"]:
        print(timing)

    print(
        f"\nTotal pipeline time: "
        f"{sum(item['time_seconds'] for item in result['timings']):.4f}s"
    )


if __name__ == "__main__":
    asyncio.run(main())