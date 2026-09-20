import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")

llm = ChatOpenAI(
    model=MODEL,
    temperature=0
)


# ============================================================
# STEP 1 — SEARCH SOURCES
# ============================================================

def search_sources(topic: str) -> list[dict]:
    """
    Retrieve relevant source chunks for the given topic.
    """

    sources = [
        {
            "title": "Artificial Intelligence",
            "content": (
                "Artificial intelligence enables computer systems "
                "to perform tasks that normally require human intelligence, "
                "including reasoning, learning, and pattern recognition."
            ),
        },
        {
            "title": "Machine Learning",
            "content": (
                "Machine learning is a subset of AI where systems "
                "learn patterns from data and use those patterns "
                "to make predictions or decisions."
            ),
        },
        {
            "title": "AI Agents",
            "content": (
                "AI agents combine language models, tools, memory, "
                "and workflows to perform multi-step tasks."
            ),
        },
        {
            "title": "Retrieval-Augmented Generation",
            "content": (
                "Retrieval-Augmented Generation combines retrieval "
                "of relevant information with language generation "
                "to improve grounded responses."
            ),
        },
        {
            "title": "FastAPI",
            "content": (
                "FastAPI is a Python framework for building APIs "
                "using Python type hints and automatic validation."
            ),
        },
    ]

    topic_words = set(topic.lower().split())

    matched = []

    for source in sources:
        text = (
            source["title"] + " " + source["content"]
        ).lower()

        score = sum(
            1 for word in topic_words
            if word in text
        )

        if score > 0:
            matched.append(
                {
                    **source,
                    "score": score
                }
            )

    matched.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    if not matched:
        matched = sources[:3]

    return matched[:3]


# ============================================================
# STEP 2 — EXTRACT KEY POINTS
# ============================================================

def extract_key_points(chunks: list[dict]) -> list[str]:
    """
    Extract important research points from retrieved chunks.
    """

    if not chunks:
        raise ValueError(
            "No source chunks available."
        )

    context = "\n\n".join(
        f"Source: {chunk['title']}\n"
        f"{chunk['content']}"
        for chunk in chunks
    )

    prompt = f"""
Extract the most important research points from
the following source material.

Return 4 to 6 concise factual bullet points.

Do not invent information.

SOURCE MATERIAL:

{context}
"""

    response = llm.invoke(prompt)

    text = response.content

    points = [
        line.strip("- •")
        for line in text.splitlines()
        if line.strip()
    ]

    return points[:6]


# ============================================================
# STEP 3 — SYNTHESISE FINDINGS
# ============================================================

def synthesise_findings(points: list[str]) -> str:
    """
    Combine extracted research points into a coherent synthesis.
    """

    if not points:
        raise ValueError(
            "No extracted points available."
        )

    joined_points = "\n".join(
        f"- {point}"
        for point in points
    )

    prompt = f"""
Synthesize the following research points
into a coherent research summary.

Requirements:

- Do not invent facts.
- Preserve important details.
- Identify common themes.
- Mention important differences when relevant.
- Use clear professional language.
- Produce approximately 3 to 5 paragraphs.

Research points:

{joined_points}
"""

    response = llm.invoke(prompt)

    return response.content


# ============================================================
# STEP 4 — FORMAT REPORT
# ============================================================

def format_report(synthesis: str) -> str:
    """
    Convert the synthesis into a structured research report.
    """

    if not synthesis:
        raise ValueError(
            "Synthesis is empty."
        )

    prompt = f"""
Convert the following synthesis into a
professional research report.

Use exactly this structure:

# Research Report

## Executive Summary

## Key Findings

## Analysis

## Conclusion

SYNTHESIS:

{synthesis}
"""

    response = llm.invoke(prompt)

    return response.content