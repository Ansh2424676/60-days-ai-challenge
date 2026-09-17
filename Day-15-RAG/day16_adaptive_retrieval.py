import json

import faiss
from sentence_transformers import SentenceTransformer


# ============================================================
# DAY 16 — FIX #2
# ADAPTIVE / HIGHER RECALL RETRIEVAL
# ============================================================

KB_FILE = "knowledge_base.json"

BASE_TOP_K = 3
ADAPTIVE_TOP_K = 5

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
print("ADAPTIVE RETRIEVAL EXPERIMENT")
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
# ADAPTIVE RETRIEVAL
# ============================================================

def adaptive_retrieve(
    query,
    top_k=ADAPTIVE_TOP_K,
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
                    distance

            })


    return results


# ============================================================
# TEST QUERIES
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
        "What is NovaTech's employee vacation policy?"
    ),

    (
        "Who led the NovaMind project?"
    ),

    (
        "What certification do employees receive "
        "after completing AI Launchpad?"
    )
]


# ============================================================
# RUN TESTS
# ============================================================

for query in TEST_QUERIES:

    print("\n" + "=" * 70)

    print("QUERY:")

    print(query)


    results = adaptive_retrieve(
        query
    )


    if not results:

        print(
            "\nNO RELEVANT DOCUMENT FOUND"
        )

        continue


    print(
        f"\nRetrieved {len(results)} chunks:"
    )


    for item in results:

        print(
            f"\n{item['id']} "
            f"| distance="
            f"{item['distance']:.4f}"
        )

        print(
            item["text"]
        )


# ============================================================
# COMPARISON
# ============================================================

print("\n" + "=" * 70)

print("RETRIEVAL STRATEGY")

print("=" * 70)

print(
    f"Day 15 baseline: "
    f"Top {BASE_TOP_K}"
)

print(
    f"Fix #1: "
    f"Top {BASE_TOP_K} + distance threshold"
)

print(
    f"Fix #2: "
    f"Top {ADAPTIVE_TOP_K} + distance threshold"
)

print(
    f"Distance threshold: "
    f"{DISTANCE_THRESHOLD}"
)

print("=" * 70)