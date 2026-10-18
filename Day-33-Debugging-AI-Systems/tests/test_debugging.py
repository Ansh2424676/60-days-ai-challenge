from app.rag_pipeline import RAGPipeline
from debugging.compare_results import compare_answers, compare_results
from debugging.isolation_test import (
    test_generation_isolation,
    test_retrieval_isolation,
)
from debugging.reproduce_failures import reproduce_failure
from debugging.select_failures import (
    select_failures,
    summarize_failures,
)


def create_pipeline() -> RAGPipeline:
    pipeline = RAGPipeline()

    pipeline.add_document(
        "doc1",
        "Python is a programming language",
        {"source": "test"},
    )

    pipeline.add_document(
        "doc2",
        "FastAPI is a Python web framework",
        {"source": "test"},
    )

    return pipeline


def test_select_failures():
    results = [
        {"id": 1, "passed": True},
        {
            "id": 2,
            "passed": False,
            "category": "retrieval",
        },
    ]

    failures = select_failures(results)

    assert len(failures) == 1
    assert failures[0]["id"] == 2


def test_summarize_failures():
    failures = [
        {"category": "retrieval"},
        {"category": "retrieval"},
        {"category": "generation"},
    ]

    summary = summarize_failures(failures)

    assert summary["retrieval"] == 2
    assert summary["generation"] == 1


def test_retrieval_isolation():
    pipeline = create_pipeline()

    result = test_retrieval_isolation(
        pipeline,
        "Python",
    )

    assert result["retrieval_success"] is True
    assert result["document_count"] == 2


def test_generation_isolation():
    pipeline = create_pipeline()

    result = test_generation_isolation(
        pipeline,
        "Python",
    )

    assert result["generation_success"] is True
    assert result["context_documents"] == 2


def test_reproduce_failure():
    pipeline = create_pipeline()

    failure = {
        "query": "Python",
        "expected": "JavaScript",
    }

    result = reproduce_failure(
        pipeline,
        failure,
    )

    assert result["reproduced"] is True
    assert result["trace_id"]


def test_compare_results():
    expected = {
        "answer": "A",
        "score": 1,
    }

    actual = {
        "answer": "B",
        "score": 1,
    }

    result = compare_results(
        expected,
        actual,
    )

    assert result["match"] is False
    assert "answer" in result["differences"]


def test_compare_answers():
    result = compare_answers(
        "Python is a language",
        "Python is a language",
    )

    assert result["match"] is True


def test_rag_query():
    pipeline = create_pipeline()

    result = pipeline.query("Python")

    assert result["trace_id"]
    assert result["answer"]
    assert len(result["retrieved_documents"]) == 2