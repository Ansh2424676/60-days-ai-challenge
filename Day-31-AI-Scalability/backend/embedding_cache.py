import json
import hashlib
from datetime import timedelta

from openai import OpenAI

from redis_client import redis_client


client = OpenAI()

CACHE_TTL = 3600
EMBEDDING_MODEL = "text-embedding-3-small"


def _cache_key(query: str) -> str:
    """
    Generate a stable Redis key for a query.
    """

    normalized_query = query.strip().lower()

    query_hash = hashlib.sha256(
        normalized_query.encode("utf-8")
    ).hexdigest()

    return f"embedding:{query_hash}"


def get_embedding(query: str) -> list[float]:
    """
    Return cached embedding if available.
    Otherwise generate embedding using OpenAI
    and store it in Redis for one hour.
    """

    key = _cache_key(query)

    cached = redis_client.get(key)

    if cached:
        print("[CACHE HIT] Embedding")
        return json.loads(cached)

    print("[CACHE MISS] Embedding")

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query,
    )

    vector = response.data[0].embedding

    redis_client.setex(
        key,
        timedelta(seconds=CACHE_TTL),
        json.dumps(vector),
    )

    return vector