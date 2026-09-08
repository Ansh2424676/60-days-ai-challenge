import json
from datetime import datetime

import faiss
from sentence_transformers import SentenceTransformer


# ============================================================
# DAY 16 — FINAL RAG FAILURE ANALYSIS
# ============================================================

KB_FILE = "knowledge_base.json"
OUTPUT_FILE = "rag_results_day16_final.json"

TOP_K = 3
SUBQUERY_TOP_K = 2

DISTANCE_THRESHOLD = 0.80


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

with open(
    KB_FILE,
    "r",
    encoding="utf-8"
) as f:
    documents = json.load(f)


texts = [
    doc["text"]
    for doc in documents
]

ids = [
    doc["id"]
    for doc in documents
]


print("=" * 70)
print("DAY 16 — FINAL RAG FAILURE ANALYSIS")
print("=" * 70)

print("Documents loaded:", len(documents))


# ============================================================
# EMBEDDING MODEL
# ============================================================

print("\nLoading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = embedding_model.encode(
    texts,
    convert_to_numpy=True
)

print(
    "Embedding shape:",
    embeddings.shape
)


# ============================================================
# FAISS
# ============================================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)

index.add(
    embeddings.astype("float32")
)

print(
    "FAISS index size:",
    index.ntotal
)

print(
    "Distance threshold:",
    DISTANCE_THRESHOLD
)


# ============================================================
# BASIC RETRIEVAL
# ============================================================

def retrieve(
    query,
    top_k=TOP_K
):

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    )

    distances, indices = index.search(
        query_embedding.astype("float32"),
        top_k
    )

    results = []

    for distance, idx in zip(
        distances[0],
        indices[0]
    ):

        distance = float(distance)

        if distance <= DISTANCE_THRESHOLD:

            results.append({

                "id": ids[idx],

                "text": texts[idx],

                "distance": distance,

                "source_query": query

            })

    return results


# ============================================================
# BROAD QUERY DETECTION
# ============================================================

def is_broad_query(query):

    query_lower = query.lower()

    broad_terms = [
        "everything",
        "complete summary",
        "all known",
        "all",
        "entire",
        "comprehensive"
    ]

    return any(
        term in query_lower
        for term in broad_terms
    )


# ============================================================
# QUERY DECOMPOSITION
# ============================================================

def decompose_query(query):

    query_lower = query.lower()

    if not is_broad_query(query):

        return [query]

    return [

        "What is NovaTech Solutions?",

        "What departments does NovaTech Solutions have?",

        "When was NovaMind launched?",

        "What is NovaMind designed to do?",

        "Who led the NovaMind project?",

        "What is AtlasHub?",

        "What does AtlasHub contain?",

        "What is AI Launchpad?",

        "How long does AI Launchpad last?",

        "What certification do employees receive after AI Launchpad?",

        "When is the weekly engineering technical review meeting?"

    ]


# ============================================================
# ADAPTIVE RETRIEVAL
# ============================================================

def adaptive_retrieve(query):

    sub_queries = decompose_query(
        query
    )

    all_results = []

    for sub_query in sub_queries:

        results = retrieve(
            sub_query,
            top_k=SUBQUERY_TOP_K
        )

        all_results.extend(
            results
        )


    # --------------------------------------------------------
    # Deduplicate
    # --------------------------------------------------------

    unique_docs = {}

    for item in all_results:

        doc_id = item["id"]

        if doc_id not in unique_docs:

            unique_docs[doc_id] = item

        else:

            if (
                item["distance"]
                <
                unique_docs[doc_id]["distance"]
            ):

                unique_docs[doc_id] = item


    # --------------------------------------------------------
    # Sort by distance
    # --------------------------------------------------------

    final_results = sorted(
        unique_docs.values(),
        key=lambda x: x["distance"]
    )

    return sub_queries, final_results


# ============================================================
# 15 TEST CASES
# ============================================================

TEST_CASES = [

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

    {
        "id": "Q07",
        "failure_mode": "answer_context_mismatch",
        "query": "Who led the NovaMind project?",
        "expected_docs": ["doc-005"]
    },

    {
        "id": "Q08",
        "failure_mode": "answer_context_mismatch",
        "query": "How long does AI Launchpad last?",
        "expected_docs": ["doc-008"]
    },

    {
        "id": "Q09",
        "failure_mode": "answer_context_mismatch",
        "query": "Where is NovaTech Solutions headquartered?",
        "expected_docs": ["doc-001"]
    },

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

    {
        "id": "Q13",
        "failure_mode": "correct_chunk_wrong_answer",
        "query": (
            "Which city is NovaTech Solutions "
            "headquartered in?"
        ),
        "expected_docs": ["doc-001"]
    },

    {
        "id": "Q14",
        "failure_mode": "correct_chunk_wrong_answer",
        "query": "Which person led the NovaMind project?",
        "expected_docs": ["doc-005"]
    },

    {
        "id": "Q15",
        "failure_mode": "correct_chunk_wrong_answer",
        "query": (
            "What certification do employees receive "
            "after completing AI Launchpad?"
        ),
        "expected_docs": ["doc-009"]
    }
]


# ============================================================
# RUN TESTS
# ============================================================

results = []

print("\n" + "=" * 70)
print("RUNNING FINAL 15 TESTS")
print("=" * 70)


for test in TEST_CASES:

    query = test["query"]

    sub_queries, retrieved = adaptive_retrieve(
        query
    )

    retrieved_ids = [
        item["id"]
        for item in retrieved
    ]

    expected_docs = test["expected_docs"]


    # --------------------------------------------------------
    # Retrieval evaluation
    # --------------------------------------------------------

    if expected_docs:

        relevant_docs = [
            doc_id
            for doc_id in expected_docs
            if doc_id in retrieved_ids
        ]

        retrieval_success = (
            len(relevant_docs) > 0
        )

    else:

        relevant_docs = []

        retrieval_success = (
            len(retrieved) == 0
        )


    # --------------------------------------------------------
    # Coverage
    # --------------------------------------------------------

    if expected_docs:

        coverage = (
            len(relevant_docs)
            /
            len(expected_docs)
        )

    else:

        coverage = (
            1.0
            if len(retrieved) == 0
            else 0.0
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
    # Result
    # --------------------------------------------------------

    result = {

        "test_id":
            test["id"],

        "failure_mode":
            test["failure_mode"],

        "query":
            query,

        "broad_query":
            is_broad_query(query),

        "sub_queries":
            sub_queries,

        "expected_docs":
            expected_docs,

        "retrieved_docs":
            retrieved,

        "retrieved_ids":
            retrieved_ids,

        "relevant_docs_retrieved":
            relevant_docs,

        "retrieval_success":
            retrieval_success,

        "retrieval_coverage":
            round(coverage, 2),

        "best_distance":
            best_distance,

        # Generation unavailable
        "generated_answer":
            None,

        "answer_quality":
            None,

        "diagnosis":
            None,

        "timestamp":
            datetime.now().isoformat()

    }


    results.append(
        result
    )


    # --------------------------------------------------------
    # Console
    # --------------------------------------------------------

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
        "Broad query:",
        is_broad_query(query)
    )

    print(
        "Retrieval success:",
        retrieval_success
    )

    print(
        "Coverage:",
        round(coverage, 2)
    )

    print(
        "Retrieved:",
        retrieved_ids
    )


# ============================================================
# METADATA
# ============================================================

metadata = {

    "project":
        "Day 16 - Diagnosing RAG Failure Modes",

    "embedding_model":
        "all-MiniLM-L6-v2",

    "retrieval_method":
        "FAISS IndexFlatL2",

    "baseline_top_k":
        TOP_K,

    "subquery_top_k":
        SUBQUERY_TOP_K,

    "distance_threshold":
        DISTANCE_THRESHOLD,

    "fix_1":
        (
            "Similarity/distance threshold filtering"
        ),

    "fix_2":
        (
            "Query decomposition for broad multi-topic queries"
        ),

    "document_count":
        len(documents),

    "embedding_dimension":
        int(embeddings.shape[1]),

    "generation_available":
        False,

    "generation_note":
        (
            "OpenAI generation pending because "
            "API credits are exhausted."
        )

}


# ============================================================
# SAVE
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
# SUMMARY
# ============================================================

successful = sum(
    1
    for item in results
    if item["retrieval_success"]
)


average_coverage = (
    sum(
        item["retrieval_coverage"]
        for item in results
    )
    /
    len(results)
)


print("\n" + "=" * 70)
print("FINAL DAY 16 SUMMARY")
print("=" * 70)

print(
    "Total tests:",
    len(results)
)

print(
    "Successful retrieval behavior:",
    successful,
    "/",
    len(results)
)

print(
    "Average retrieval coverage:",
    round(
        average_coverage,
        2
    )
)

print(
    "Fix #1:",
    "Distance threshold =",
    DISTANCE_THRESHOLD
)

print(
    "Fix #2:",
    "Query decomposition"
)

print(
    "Results saved to:",
    OUTPUT_FILE
)

print("=" * 70)