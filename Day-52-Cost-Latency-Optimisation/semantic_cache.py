import json
import math
import os
import hashlib
from redis import Redis

SIMILARITY_THRESHOLD = 0.92
CACHE_PREFIX = "day52:semantic:"
CACHE_TTL_SECONDS = 86400

def cosine_similarity(a, b):
    if len(a) != len(b) or not a:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

class SemanticResponseCache:
    def __init__(self, redis_url=None):
        self.redis = Redis.from_url(
            redis_url or os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            decode_responses=True
        )

    def get(self, query_embedding):
        # Scan stored entries and return only a sufficiently similar match.
        for key in self.redis.scan_iter(match=f"{CACHE_PREFIX}*"):
            item = self.redis.get(key)
            if not item:
                continue
            try:
                entry = json.loads(item)
                score = cosine_similarity(query_embedding, entry["embedding"])
                if score > SIMILARITY_THRESHOLD:
                    return {"answer": entry["answer"], "similarity": score}
            except (ValueError, KeyError, TypeError):
                continue
        return None

    def set(self, query, query_embedding, answer):
        key = CACHE_PREFIX + hashlib.sha256(query.encode("utf-8")).hexdigest()
        self.redis.setex(
            key,
            CACHE_TTL_SECONDS,
            json.dumps({
                "query": query,
                "embedding": query_embedding,
                "answer": answer
            })
        )
