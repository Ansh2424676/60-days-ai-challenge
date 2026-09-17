import json
import faiss
from sentence_transformers import SentenceTransformer


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

with open("knowledge_base.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

texts = [doc["text"] for doc in documents]
ids = [doc["id"] for doc in documents]


# ============================================================
# EMBEDDINGS
# ============================================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = model.encode(
    texts,
    convert_to_numpy=True
)


# ============================================================
# FAISS
# ============================================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(
    embeddings.astype("float32")
)


# ============================================================
# RETRIEVAL WITH THRESHOLD
# ============================================================

def retrieve_with_threshold(
    query,
    k=3,
    threshold=0.80
):

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    distances, indices = index.search(
        query_embedding.astype("float32"),
        k
    )

    results = []

    for distance, idx in zip(
        distances[0],
        indices[0]
    ):

        distance = float(distance)

        if distance <= threshold:

            results.append({
                "id": ids[idx],
                "text": texts[idx],
                "distance": distance
            })

    return results


# ============================================================
# FAILURE QUERIES
# ============================================================

TEST_QUERIES = [
    "What is NovaTech's employee vacation policy?",
    "What database technology does NovaTech use in production?",
    "Who is the Chief Financial Officer of NovaTech Solutions?",
    "Who led the NovaMind project?",
    "Where is NovaTech Solutions headquartered?"
]


# ============================================================
# TEST
# ============================================================

for query in TEST_QUERIES:

    print("\n" + "=" * 70)

    print("QUERY:")
    print(query)

    results = retrieve_with_threshold(
        query,
        k=3,
        threshold=0.80
    )

    if not results:

        print("\nNO RELEVANT DOCUMENT FOUND")

    else:

        print("\nRETRIEVED:")

        for item in results:

            print(
                f"{item['id']} "
                f"| distance={item['distance']:.4f}"
            )

            print(
                item["text"]
            )