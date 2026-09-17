import json
from datetime import datetime

import faiss
from sentence_transformers import SentenceTransformer


# ============================================================
# DAY 16 — RAG FAILURE MODE DIAGNOSTICS
# ============================================================

KB_FILE = "knowledge_base.json"
OUTPUT_FILE = "rag_results_day16.json"

TOP_K = 3

# Fix #1:
# Reject retrieved chunks whose FAISS L2 distance
# is greater than this threshold.
DISTANCE_THRESHOLD = 0.80


# ============================================================
# 1. LOAD KNOWLEDGE BASE
# ============================================================

with open(KB_FILE, "r", encoding="utf-8") as f:
    documents = json.load(f)

texts = [doc["text"] for doc in documents]
ids = [doc["id"] for doc in documents]

print("=" * 70)
print("DAY 16 — RAG FAILURE MODE DIAGNOSTICS")
print("=" * 70)

print("Documents loaded:", len(documents))


# ============================================================
# 2. LOAD EMBEDDING MODEL
# Same model used in Day 15
# ============================================================

print("\nLoading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = embedding_model.encode(
    texts,
    convert_to_numpy=True
)

print("Embedding shape:", embeddings.shape)


# ============================================================
# 3. BUILD FAISS INDEX
# Same method used in Day 15
# ============================================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(
    embeddings.astype("float32")
)

print("FAISS index size:", index.ntotal)

print("Distance threshold:", DISTANCE_THRESHOLD)


# ============================================================
# 4. RETRIEVAL FUNCTION
# ============================================================

def retrieve_top_k(
    query,
    k=TOP_K,
    distance_threshold=DISTANCE_THRESHOLD
):

    # --------------------------------------------------------
    # Convert query into embedding
    # --------------------------------------------------------

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    )

    # --------------------------------------------------------
    # FAISS search
    # --------------------------------------------------------

    distances, indices = index.search(
        query_embedding.astype("float32"),
        k
    )

    results = []

    # --------------------------------------------------------
    # Apply distance threshold
    # --------------------------------------------------------

    for distance, idx in zip(
        distances[0],
        indices[0]
    ):

        distance = float(distance)

        # Only accept sufficiently similar chunks
        if distance <= distance_threshold:

            results.append({
                "id": ids[idx],
                "text": texts[idx],
                "distance": distance
            })

    return results


# ============================================================
# 5. TEST SUITE
# 15 TEST QUERIES
# ============================================================

TEST_CASES = [

    # ========================================================
    # FAILURE MODE 1
    # RETRIEVAL FAILURE
    # ========================================================

    {
        "id": "Q01",
        "failure_mode": "retrieval_failure",
        "query": "What is NovaTech's employee vacation policy?",
        "expected_docs": []
    },

    {
        "id": "Q02",
        "failure_mode": "retrieval_failure",
        "query": "What database technology does NovaTech use in production?",
        "expected_docs": []
    },

    {
        "id": "Q03",
        "failure_mode": "retrieval_failure",
        "query": "Who is the Chief Financial Officer of NovaTech Solutions?",
        "expected_docs": []
    },


    # ========================================================
    # FAILURE MODE 2
    # CONTEXT WINDOW / CONTEXT PRESSURE
    # ========================================================

    {
        "id": "Q04",
        "failure_mode": "context_window_overflow",
        "query": (
            "Tell me everything about NovaTech Solutions, "
            "NovaMind, AtlasHub, AI Launchpad, and the "
            "engineering team's weekly meeting."
        ),
        "expected_docs": [
            "doc-001",
            "doc-002",
            "doc-003",
            "doc-004",
            "doc-005",
            "doc-006",
            "doc-007",
            "doc-008",
            "doc-009",
            "doc-010"
        ]
    },

    {
        "id": "Q05",
        "failure_mode": "context_window_overflow",
        "query": (
            "Give a complete summary covering the company, "
            "departments, NovaMind, AtlasHub, training, "
            "certification, and engineering meetings."
        ),
        "expected_docs": [
            "doc-001",
            "doc-002",
            "doc-003",
            "doc-004",
            "doc-005",
            "doc-006",
            "doc-007",
            "doc-008",
            "doc-009",
            "doc-010"
        ]
    },

    {
        "id": "Q06",
        "failure_mode": "context_window_overflow",
        "query": (
            "Explain all known NovaTech internal systems, "
            "projects, documentation, training programs, "
            "certifications, and recurring meetings."
        ),
        "expected_docs": [
            "doc-003",
            "doc-004",
            "doc-005",
            "doc-006",
            "doc-007",
            "doc-008",
            "doc-009",
            "doc-010"
        ]
    },


    # ========================================================
    # FAILURE MODE 3
    # ANSWER-CONTEXT MISMATCH
    # ========================================================

    {
        "id": "Q07",
        "failure_mode": "answer_context_mismatch",
        "query": "Who led the NovaMind project?",
        "expected_docs": [
            "doc-005"
        ]
    },

    {
        "id": "Q08",
        "failure_mode": "answer_context_mismatch",
        "query": "How long does AI Launchpad last?",
        "expected_docs": [
            "doc-008"
        ]
    },

    {
        "id": "Q09",
        "failure_mode": "answer_context_mismatch",
        "query": "Where is NovaTech Solutions headquartered?",
        "expected_docs": [
            "doc-001"
        ]
    },


    # ========================================================
    # FAILURE MODE 4
    # VAGUE CONTEXT RETRIEVED
    # ========================================================

    {
        "id": "Q10",
        "failure_mode": "vague_context_retrieved",
        "query": "Tell me about NovaMind.",
        "expected_docs": [
            "doc-003",
            "doc-004",
            "doc-005"
        ]
    },

    {
        "id": "Q11",
        "failure_mode": "vague_context_retrieved",
        "query": "Tell me about AtlasHub.",
        "expected_docs": [
            "doc-006",
            "doc-007"
        ]
    },

    {
        "id": "Q12",
        "failure_mode": "vague_context_retrieved",
        "query": "Tell me about AI Launchpad.",
        "expected_docs": [
            "doc-008",
            "doc-009"
        ]
    },


    # ========================================================
    # FAILURE MODE 5
    # CORRECT CHUNK BUT WRONG ANSWER GENERATED
    # ========================================================

    {
        "id": "Q13",
        "failure_mode": "correct_chunk_wrong_answer",
        "query": (
            "Which city is NovaTech Solutions "
            "headquartered in?"
        ),
        "expected_docs": [
            "doc-001"
        ]
    },

    {
        "id": "Q14",
        "failure_mode": "correct_chunk_wrong_answer",
        "query": "Which person led the NovaMind project?",
        "expected_docs": [
            "doc-005"
        ]
    },

    {
        "id": "Q15",
        "failure_mode": "correct_chunk_wrong_answer",
        "query": (
            "What certification do employees receive "
            "after completing AI Launchpad?"
        ),
        "expected_docs": [
            "doc-009"
        ]
    }
]


# ============================================================
# 6. RUN ALL TESTS
# ============================================================

results = []

print("\n" + "=" * 70)
print("RUNNING 15 DIAGNOSTIC QUERIES")
print("=" * 70)


for test in TEST_CASES:

    query = test["query"]

    retrieved = retrieve_top_k(
        query
    )

    retrieved_ids = [
        item["id"]
        for item in retrieved
    ]

    expected_docs = test["expected_docs"]


    # --------------------------------------------------------
    # Check retrieval success
    # --------------------------------------------------------

    if expected_docs:

        relevant_retrieved = [
            doc_id
            for doc_id in expected_docs
            if doc_id in retrieved_ids
        ]

        retrieval_success = (
            len(relevant_retrieved) > 0
        )

    else:

        # For unsupported queries, successful behavior
        # means returning no documents.
        relevant_retrieved = []

        retrieval_success = (
            len(retrieved) == 0
        )


    # --------------------------------------------------------
    # Best distance
    # --------------------------------------------------------

    if retrieved:

        best_distance = min(
            item["distance"]
            for item in retrieved
        )

    else:

        best_distance = None


    # --------------------------------------------------------
    # Result record
    # --------------------------------------------------------

    result = {

        "test_id": test["id"],

        "failure_mode": test["failure_mode"],

        "query": query,

        "expected_docs": expected_docs,

        "retrieved_docs": retrieved,

        "retrieved_ids": retrieved_ids,

        "relevant_docs_retrieved":
            relevant_retrieved,

        "retrieval_success":
            retrieval_success,

        "best_distance":
            best_distance,

        # OpenAI generation is currently unavailable
        "generated_answer": None,

        "answer_quality": None,

        "diagnosis": None,

        "timestamp":
            datetime.now().isoformat()

    }

    results.append(result)


    # ========================================================
    # PRINT RESULT
    # ========================================================

    print("\n" + "-" * 70)

    print(
        test["id"],
        "|",
        test["failure_mode"]
    )

    print(
        "Query:",
        query
    )

    print(
        "Expected:",
        expected_docs
    )

    print(
        "Retrieval success:",
        retrieval_success
    )


    if retrieved:

        print("Retrieved:")

        for item in retrieved:

            print(
                f"  {item['id']} "
                f"| distance={item['distance']:.4f}"
            )

            print(
                f"    {item['text']}"
            )

    else:

        print(
            "  NO RELEVANT DOCUMENT FOUND"
        )


# ============================================================
# 7. METADATA
# ============================================================

metadata = {

    "project":
        "Day 16 - Diagnosing RAG Failure Modes",

    "embedding_model":
        "all-MiniLM-L6-v2",

    "retrieval_method":
        "FAISS IndexFlatL2",

    "top_k":
        TOP_K,

    "distance_threshold":
        DISTANCE_THRESHOLD,

    "document_count":
        len(documents),

    "embedding_dimension":
        int(embeddings.shape[1]),

    "generation_available":
        False,

    "generation_note":
        (
            "OpenAI generation is pending because "
            "the API account currently has no remaining credits."
        )

}


# ============================================================
# 8. SAVE RESULTS
# ============================================================

output = {

    "metadata":
        metadata,

    "tests":
        results

}


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        output,
        f,
        indent=2,
        ensure_ascii=False
    )


# ============================================================
# 9. FINAL SUMMARY
# ============================================================

successful_retrievals = sum(
    1
    for item in results
    if item["retrieval_success"]
)


print("\n" + "=" * 70)
print("DAY 16 DIAGNOSTICS COMPLETED")
print("=" * 70)

print(
    "Total tests:",
    len(results)
)

print(
    "Successful retrieval behavior:",
    successful_retrievals,
    "/",
    len(results)
)

print(
    "Distance threshold:",
    DISTANCE_THRESHOLD
)

print(
    "Results saved to:",
    OUTPUT_FILE
)

print("=" * 70)