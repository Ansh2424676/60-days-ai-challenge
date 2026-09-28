from typing import Any

from app.rag_pipeline import RAGPipeline


def test_retrieval_isolation(
    pipeline: RAGPipeline,
    query: str,
) -> dict[str, Any]:
    """Check retrieval independently from answer generation."""

    documents = pipeline.retrieve(query)

    return {
        "query": query,
        "retrieval_success": bool(documents),
        "document_count": len(documents),
        "documents": [
            {
                "doc_id": document.doc_id,
                "text": document.text,
                "metadata": document.metadata,
            }
            for document in documents
        ],
    }


def test_generation_isolation(
    pipeline: RAGPipeline,
    query: str,
) -> dict[str, Any]:
    """Check answer generation using supplied retrieved context."""

    documents = pipeline.retrieve(query)

    answer = pipeline.generate_answer(
        query,
        documents,
    )

    return {
        "query": query,
        "generation_success": bool(answer.strip()),
        "answer": answer,
        "context_documents": len(documents),
    }