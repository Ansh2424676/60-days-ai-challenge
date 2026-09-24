from embedding_cache import get_embedding
from response_cache import find_cached_response, cache_response


def get_cached_response(query: str):
    """
    Get query embedding from cache/API and check semantic response cache.
    """

    embedding = get_embedding(query)

    cached = find_cached_response(embedding)

    return embedding, cached


def save_response_to_cache(
    query: str,
    embedding: list[float],
    response: str
):
    """
    Store generated response in semantic response cache.
    """

    return cache_response(
        query=query,
        embedding=embedding,
        response=response
    )