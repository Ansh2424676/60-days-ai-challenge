from datetime import date
from typing import Any


KNOWLEDGE_BASE = [
    {
        "title": "RAG",
        "content": "Retrieval-Augmented Generation combines document retrieval with language generation.",
        "category": "AI",
    },
    {
        "title": "FAISS",
        "content": "FAISS is a library for efficient similarity search and clustering of dense vectors.",
        "category": "AI",
    },
    {
        "title": "AI Agents",
        "content": "AI agents can reason about tasks, select tools, execute actions, and use returned observations.",
        "category": "AI",
    },
    {
        "title": "FastAPI",
        "content": "FastAPI is a Python framework for building APIs using type hints.",
        "category": "Backend",
    },
    {
        "title": "Machine Learning",
        "content": "Machine learning allows systems to learn patterns from data and make predictions.",
        "category": "ML",
    },
]


def search_documents(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    """
    Search the local knowledge base using simple keyword matching.
    """

    query_words = set(query.lower().split())

    scored = []

    for document in KNOWLEDGE_BASE:
        text = (
            document["title"] + " " + document["content"]
        ).lower()

        score = sum(1 for word in query_words if word in text)

        if score > 0:
            scored.append((score, document))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [doc for _, doc in scored[:top_k]]


def get_weather_stub(city: str) -> dict[str, Any]:
    """
    Return deterministic fake weather data for testing.
    """

    weather_data = {
        "kanpur": {
            "city": "Kanpur",
            "temperature_c": 31,
            "condition": "Sunny",
        },
        "delhi": {
            "city": "Delhi",
            "temperature_c": 30,
            "condition": "Partly Cloudy",
        },
        "mumbai": {
            "city": "Mumbai",
            "temperature_c": 29,
            "condition": "Cloudy",
        },
    }

    return weather_data.get(
        city.lower(),
        {
            "city": city,
            "temperature_c": 28,
            "condition": "Clear",
        },
    )


def calculate(expression: str) -> float:
    """
    Evaluate a basic mathematical expression.
    """

    allowed_chars = set(
        "0123456789+-*/(). %"
    )

    if not set(expression).issubset(allowed_chars):
        raise ValueError("Expression contains unsupported characters.")

    result = eval(expression, {"__builtins__": {}}, {})

    return float(result)


def get_today() -> dict[str, str]:
    """
    Return today's date.
    """

    today = date.today()

    return {
        "date": today.isoformat(),
        "day": today.strftime("%A"),
    }


TOOL_REGISTRY = {
    "search_documents": search_documents,
    "get_weather_stub": get_weather_stub,
    "calculate": calculate,
    "get_today": get_today,
}