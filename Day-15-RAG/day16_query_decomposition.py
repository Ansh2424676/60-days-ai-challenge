import json

import faiss
from sentence_transformers import SentenceTransformer


# ============================================================
# DAY 16 — FIX #2
# QUERY DECOMPOSITION RETRIEVAL
# ============================================================

KB_FILE = "knowledge_base.json"

TOP_K_PER_QUERY = 2

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
print("DAY 16 — FIX #2")
print("QUERY DECOMPOSITION RETRIEVAL")
print("=" * 70)

print(
    "Documents:",
    len(documents)
)


# ============================================================
# EMBEDDING MODEL
# ============================================================

print("\nLoading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


embeddings = model.encode(
    texts,
    convert_to_numpy=True
)


print(
    "Embedding shape:",
    embeddings.shape
)


# ============================================================
# FAISS INDEX
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


# ============================================================
# NORMAL RETRIEVAL
# ============================================================

def retrieve(
    query,
    top_k=TOP_K_PER_QUERY,
    threshold=DISTANCE_THRESHOLD
):

    query_embedding = model.encode(
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


        if distance <= threshold:

            results.append({

                "id":
                    ids[idx],

                "text":
                    texts[idx],

                "distance":
                    distance,

                "source_query":
                    query

            })


    return results


# ============================================================
# QUERY DECOMPOSITION
# ============================================================

def decompose_query(query):

    query_lower = query.lower()


    # Broad multi-topic queries
    if (
        "everything" in query_lower
        or "complete summary" in query_lower
        or "all known" in query_lower
    ):

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


    # Normal focused query
    return [query]


# ============================================================
# ADAPTIVE RETRIEVAL
# ============================================================

def retrieve_adaptive(query):

    sub_queries = decompose_query(
        query
    )


    all_results = []


    for sub_query in sub_queries:

        results = retrieve(
            sub_query
        )

        all_results.extend(
            results
        )


    # --------------------------------------------------------
    # Deduplicate documents
    # --------------------------------------------------------

    unique = {}


    for item in all_results:

        doc_id = item["id"]


        if doc_id not in unique:

            unique[doc_id] = item

        else:

            # Keep the best distance
            if (
                item["distance"]
                <
                unique[doc_id]["distance"]
            ):

                unique[doc_id] = item


    # --------------------------------------------------------
    # Sort by distance
    # --------------------------------------------------------

    final_results = sorted(
        unique.values(),
        key=lambda x: x["distance"]
    )


    return sub_queries, final_results


# ============================================================
# TEST
# ============================================================

TEST_QUERIES = [

    (
        "Tell me everything about NovaTech Solutions, "
        "NovaMind, AtlasHub, AI Launchpad, and the "
        "engineering team's weekly meeting."
    ),

    (
        "Give a complete summary covering the company, "
        "departments, NovaMind, AtlasHub, training, "
        "certification, and engineering meetings."
    ),

    (
        "Explain all known NovaTech internal systems, "
        "projects, documentation, training programs, "
        "certifications, and recurring meetings."
    ),

    (
        "Who led the NovaMind project?"
    ),

    (
        "What certification do employees receive "
        "after completing AI Launchpad?"
    ),

    (
        "What is NovaTech's employee vacation policy?"
    )
]


# ============================================================
# RUN
# ============================================================

for query in TEST_QUERIES:

    print("\n" + "=" * 70)

    print("ORIGINAL QUERY:")

    print(query)


    sub_queries, results = retrieve_adaptive(
        query
    )


    print("\nSUB-QUERIES:")

    for sub_query in sub_queries:

        print(
            " -",
            sub_query
        )


    if not results:

        print(
            "\nNO RELEVANT DOCUMENT FOUND"
        )

        continue


    print(
        f"\nRetrieved {len(results)} unique documents:"
    )


    for item in results:

        print(
            f"\n{item['id']} "
            f"| distance="
            f"{item['distance']:.4f}"
        )

        print(
            "Source query:",
            item["source_query"]
        )

        print(
            item["text"]
        )


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)

print("FIX #2 SUMMARY")

print("=" * 70)

print(
    "Baseline: one embedding + Top-3 retrieval"
)

print(
    "Fix #1: Top-3 + distance threshold"
)

print(
    "Fix #2: query decomposition + Top-2 per sub-query "
    "+ distance threshold"
)

print(
    "Distance threshold:",
    DISTANCE_THRESHOLD
)

print("=" * 70)