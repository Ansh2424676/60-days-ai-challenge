import logging
from dataclasses import dataclass
from typing import Any

from app.tracing import trace_operation


logger = logging.getLogger(__name__)


@dataclass
class Document:
    """Simple document representation."""

    doc_id: str
    text: str
    metadata: dict[str, Any]


class RAGPipeline:
    """Small RAG pipeline designed for debugging and testing."""

    def __init__(self, documents: list[Document] | None = None):
        self.documents = documents or []

    def add_document(
        self,
        doc_id: str,
        text: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Add a document to the knowledge base."""

        if not text.strip():
            raise ValueError("Document text cannot be empty.")

        self.documents.append(
            Document(
                doc_id=doc_id,
                text=text,
                metadata=metadata or {},
            )
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[Document]:
        """Retrieve documents using simple keyword matching."""

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        query_words = set(query.lower().split())

        scored_documents = []

        for document in self.documents:
            document_words = set(document.text.lower().split())

            score = len(query_words & document_words)

            scored_documents.append(
                (score, document)
            )

        scored_documents.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        results = [
            document
            for score, document in scored_documents
            if score > 0
        ][:top_k]

        logger.info(
            "RETRIEVAL | query=%r | candidates=%d | results=%d",
            query,
            len(self.documents),
            len(results),
        )

        return results

    def generate_answer(
        self,
        query: str,
        documents: list[Document],
    ) -> str:
        """Generate a deterministic grounded answer."""

        if not documents:
            return (
                "I could not find relevant information "
                "in the knowledge base."
            )

        context = " ".join(
            document.text for document in documents
        )

        return (
            f"Based on the retrieved context: {context}"
        )

    def query(
        self,
        query: str,
        top_k: int = 3,
    ) -> dict[str, Any]:
        """Run retrieval and answer generation with tracing."""

        with trace_operation(
            "rag_query",
            {"query": query, "top_k": top_k},
        ) as trace_id:

            documents = self.retrieve(
                query,
                top_k,
            )

            answer = self.generate_answer(
                query,
                documents,
            )

            return {
                "trace_id": trace_id,
                "query": query,
                "answer": answer,
                "retrieved_documents": [
                    {
                        "doc_id": document.doc_id,
                        "text": document.text,
                        "metadata": document.metadata,
                    }
                    for document in documents
                ],
            }