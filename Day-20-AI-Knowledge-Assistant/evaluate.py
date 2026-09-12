import json
from pathlib import Path

from rag_pipeline import answer_query, retrieve


BASE_DIR = Path(__file__).resolve().parent

TESTS = [
    {
        "id": "Q01",
        "difficulty": "easy",
        "query": "Where is NovaTech Solutions headquartered?",
        "expected_ids": ["doc-001"],
        "reference_answer": "NovaTech Solutions is headquartered in Noida, India.",
    },
    {
        "id": "Q02",
        "difficulty": "easy",
        "query": "When was NovaMind launched?",
        "expected_ids": ["doc-003"],
        "reference_answer": "NovaMind was launched in February 2026.",
    },
    {
        "id": "Q03",
        "difficulty": "easy",
        "query": "Who led the NovaMind project?",
        "expected_ids": ["doc-005"],
        "reference_answer": "The NovaMind project was led by Priya Mehta, the fictional Head of Artificial Intelligence.",
    },
    {
        "id": "Q04",
        "difficulty": "easy",
        "query": "What platform stores NovaTech engineering documentation?",
        "expected_ids": ["doc-006"],
        "reference_answer": "AtlasHub stores NovaTech engineering documentation.",
    },
    {
        "id": "Q05",
        "difficulty": "easy",
        "query": "How long does the AI Launchpad program last?",
        "expected_ids": ["doc-008"],
        "reference_answer": "AI Launchpad lasts six weeks.",
    },
    {
        "id": "Q06",
        "difficulty": "medium",
        "query": "What departments does NovaTech Solutions have?",
        "expected_ids": ["doc-002"],
        "reference_answer": "Artificial Intelligence, Data Engineering, and Cloud Infrastructure.",
    },
    {
        "id": "Q07",
        "difficulty": "medium",
        "query": "What is NovaMind designed to do?",
        "expected_ids": ["doc-004"],
        "reference_answer": "NovaMind answers employee questions about policies, projects, internal documentation, and technical procedures.",
    },
    {
        "id": "Q08",
        "difficulty": "medium",
        "query": "What kinds of documentation are in AtlasHub?",
        "expected_ids": ["doc-007"],
        "reference_answer": "AtlasHub contains API, deployment, incident response, and internal coding standards documentation.",
    },
    {
        "id": "Q09",
        "difficulty": "medium",
        "query": "What certification do employees receive after AI Launchpad?",
        "expected_ids": ["doc-009"],
        "reference_answer": "They receive the fictional Nova AI Engineer Level 1 certification.",
    },
    {
        "id": "Q10",
        "difficulty": "medium",
        "query": "When is the weekly technical review meeting?",
        "expected_ids": ["doc-010"],
        "reference_answer": "The weekly technical review is every Friday at 4 PM.",
    },
    {
        "id": "Q11",
        "difficulty": "hard",
        "query": "What is NovaMind and when was it launched?",
        "expected_ids": ["doc-003", "doc-004"],
        "reference_answer": "NovaMind is NovaTech's internal AI assistant, launched in February 2026.",
    },
    {
        "id": "Q12",
        "difficulty": "hard",
        "query": "Which platform stores engineering docs and what does it contain?",
        "expected_ids": ["doc-006", "doc-007"],
        "reference_answer": "AtlasHub stores engineering documentation and contains API, deployment, incident response, and coding standards documentation.",
    },
    {
        "id": "Q13",
        "difficulty": "hard",
        "query": "Summarize AI Launchpad including its duration, topics, and certification.",
        "expected_ids": ["doc-008", "doc-009"],
        "reference_answer": "AI Launchpad lasts six weeks, covers Python, embeddings, vector databases, RAG, and AI agents, and leads to the fictional Nova AI Engineer Level 1 certification.",
    },
    {
        "id": "Q14",
        "difficulty": "hard",
        "query": "What is NovaTech's organizational structure and which department led NovaMind?",
        "expected_ids": ["doc-002", "doc-005"],
        "reference_answer": "NovaTech has Artificial Intelligence, Data Engineering, and Cloud Infrastructure departments; NovaMind was led by Priya Mehta, Head of Artificial Intelligence.",
    },
    {
        "id": "Q15",
        "difficulty": "hard",
        "query": "Give the known facts about NovaMind, including its purpose, launch, and project lead.",
        "expected_ids": ["doc-003", "doc-004", "doc-005"],
        "reference_answer": "NovaMind is an internal AI assistant for employee questions, launched in February 2026; the project was led by Priya Mehta.",
    },
]


def retrieval_score(expected_ids, retrieved_ids):
    expected = set(expected_ids)
    retrieved = list(retrieved_ids)

    if not expected:
        return 5.0 if not retrieved else 1.0

    hits = sum(1 for doc_id in expected if doc_id in retrieved)
    coverage = hits / len(expected)

    # Ranking-aware score:
    # 5 = all expected docs and best expected doc at rank 1
    # 4 = all expected docs in top-k
    # 3 = at least half of expected docs
    # 2 = one hit
    # 1 = no hits
    best_rank = min(
        (retrieved.index(doc_id) + 1 for doc_id in expected if doc_id in retrieved),
        default=None,
    )

    if coverage == 1 and best_rank == 1:
        return 5.0
    if coverage == 1:
        return 4.0
    if coverage >= 0.5:
        return 3.0
    if hits > 0:
        return 2.0
    return 1.0


def heuristic_answer_score(answer, reference_answer):
    """
    Local fallback score. The primary submission score should be the
    LLM-judge score when an API call is available.

    5: answer contains the key facts from the reference
    4: mostly correct
    3: partially correct
    2: weak
    1: unsupported/incorrect
    """
    answer_l = answer.lower()
    ref_l = reference_answer.lower()

    # Extract meaningful words; this is intentionally simple and transparent.
    stop = {
        "the", "a", "an", "is", "are", "was", "were", "and", "or", "to",
        "of", "in", "for", "with", "its", "this", "that", "called",
    }
    keywords = {
        word.strip(".,!?():;")
        for word in ref_l.split()
        if len(word.strip(".,!?():;")) >= 4
        and word.strip(".,!?():;") not in stop
    }

    if not keywords:
        return 1.0

    overlap = len([w for w in keywords if w in answer_l]) / len(keywords)

    if overlap >= 0.85:
        return 5.0
    if overlap >= 0.65:
        return 4.0
    if overlap >= 0.45:
        return 3.0
    if overlap >= 0.20:
        return 2.0
    return 1.0


def main():
    results = []

    print("=" * 78)
    print("DAY 20 - 15 QUERY EVALUATION")
    print("=" * 78)

    for test in TESTS:
        retrieved = retrieve(test["query"], k=3)
        retrieved_ids = [item["id"] for item in retrieved]
        best_score = max((item["score"] for item in retrieved), default=0.0)

        output = answer_query(test["query"])
        local_answer_score = heuristic_answer_score(
            output["answer"],
            test["reference_answer"],
        )
        r_score = retrieval_score(test["expected_ids"], retrieved_ids)

        row = {
            **test,
            "retrieved_ids": retrieved_ids,
            "retrieval_scores": [round(item["score"], 4) for item in retrieved],
            "best_similarity": round(best_score, 4),
            "retrieval_quality": r_score,
            "answer": output["answer"],
            "answer_quality_local": local_answer_score,
            "low_confidence": output["low_confidence"],
        }
        results.append(row)

        print(f"\n{test['id']} [{test['difficulty']}]")
        print("Query:", test["query"])
        print("Expected:", test["expected_ids"])
        print("Retrieved:", retrieved_ids)
        print("Best similarity:", round(best_score, 4))
        print("Retrieval quality:", f"{r_score:.1f}/5")
        print("Answer quality (local):", f"{local_answer_score:.1f}/5")
        print("Low confidence:", output["low_confidence"])

    avg_retrieval = sum(r["retrieval_quality"] for r in results) / len(results)
    avg_answer = sum(r["answer_quality_local"] for r in results) / len(results)

    report = {
        "project": "Day 20 - AI Knowledge Assistant",
        "evaluation_count": len(results),
        "retrieval_quality_average": round(avg_retrieval, 2),
        "answer_quality_average_local": round(avg_answer, 2),
        "note": "Run with your OpenAI API key. The local answer score is a transparent fallback; for a stronger submission, add an LLM judge if desired.",
        "tests": results,
    }

    output_path = BASE_DIR / "results" / "evaluation_results.json"
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print(f"Average retrieval quality: {avg_retrieval:.2f}/5")
    print(f"Average answer quality (local): {avg_answer:.2f}/5")
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
