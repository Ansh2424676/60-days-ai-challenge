from typing import Any

from app.rag_pipeline import RAGPipeline


def reproduce_failure(
    pipeline: RAGPipeline,
    failure: dict[str, Any],
) -> dict[str, Any]:
    """Reproduce a previously recorded RAG failure."""

    query = failure.get("query")

    if not query:
        raise ValueError(
            "Failure record must contain a query."
        )

    expected = failure.get("expected")

    result = pipeline.query(query)

    actual = result["answer"]

    return {
        "query": query,
        "expected": expected,
        "actual": actual,
        "reproduced": (
            expected is not None
            and expected not in actual
        ),
        "trace_id": result["trace_id"],
        "retrieved_documents": result[
            "retrieved_documents"
        ],
    }