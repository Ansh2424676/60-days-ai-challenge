from app.retrieval import ProductionRetriever


DOCUMENTS = [
    "Python is a programming language.",
    "FastAPI is a Python web framework.",
    "FAISS is used for vector similarity search.",
    "Redis is an in-memory data store.",
]


def test_faiss_success_path():

    class FakeRetriever(ProductionRetriever):

        def search_faiss(self, query, top_k=3):
            return [
                "FAISS is used for vector similarity search."
            ]

    retriever = FakeRetriever(DOCUMENTS)

    result = retriever.search("vector search")

    assert result["method"] == "faiss"
    assert result["fallback"] is False
    assert len(result["results"]) > 0


def test_faiss_failure_uses_tfidf():

    class BrokenFAISSRetriever(ProductionRetriever):

        def search_faiss(self, query, top_k=3):
            raise RuntimeError("FAISS index crashed")

    retriever = BrokenFAISSRetriever(DOCUMENTS)

    result = retriever.search(
        "Python programming language"
    )

    assert result["method"] == "tfidf"
    assert result["fallback"] is True
    assert len(result["results"]) > 0


def test_tfidf_returns_relevant_document():

    retriever = ProductionRetriever(DOCUMENTS)

    result = retriever.search_tfidf(
        "Python programming"
    )

    assert result
    assert "Python" in result[0]