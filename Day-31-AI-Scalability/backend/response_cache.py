import json
import math
import uuid

from redis_client import redis_client


RESPONSE_CACHE_PREFIX = "response_cache:"
SIMILARITY_THRESHOLD = 0.95
CACHE_TTL = 3600


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    """
    Calculate cosine similarity between two vectors.
    """

    if not vector_a or not vector_b:
        return 0.0

    if len(vector_a) != len(vector_b):
        return 0.0

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (
        magnitude_a * magnitude_b
    )


def cache_response(
    query: str,
    embedding: list[float],
    response: str,
) -> str:
    """
    Store query embedding and generated response in Redis.
    """

    cache_id = str(uuid.uuid4())

    key = f"{RESPONSE_CACHE_PREFIX}{cache_id}"

    data = {
        "query": query,
        "embedding": embedding,
        "response": response,
    }

    redis_client.setex(
        key,
        CACHE_TTL,
        json.dumps(data),
    )

    return cache_id


def find_cached_response(
    query_embedding: list[float],
) -> dict | None:
    """
    Search all cached responses and return the
    most similar response if similarity > 0.95.
    """

    best_match = None
    best_similarity = 0.0

    keys = redis_client.scan_iter(
        match=f"{RESPONSE_CACHE_PREFIX}*"
    )

    for key in keys:

        cached = redis_client.get(key)

        if not cached:
            continue

        try:
            data = json.loads(cached)

            similarity = cosine_similarity(
                query_embedding,
                data["embedding"],
            )

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = {
                    "query": data["query"],
                    "response": data["response"],
                    "similarity": similarity,
                }

        except (json.JSONDecodeError, KeyError):
            continue

    if (
        best_match
        and best_match["similarity"] >= SIMILARITY_THRESHOLD
    ):
        print(
            f"[RESPONSE CACHE HIT] "
            f"Similarity: {best_match['similarity']:.4f}"
        )

        return best_match

    print("[RESPONSE CACHE MISS]")

    return None