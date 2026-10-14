from typing import Iterable

DEFAULT_MAX_CHUNKS = 4
DEFAULT_MAX_CHARS_PER_CHUNK = 1500

def optimise_context(
    chunks: Iterable[str],
    max_chunks: int = DEFAULT_MAX_CHUNKS,
    max_chars_per_chunk: int = DEFAULT_MAX_CHARS_PER_CHUNK
) -> list[str]:
    """Limit retrieved context before constructing the model prompt."""
    if max_chunks < 1 or max_chars_per_chunk < 1:
        raise ValueError("Context limits must be positive integers.")

    result = []
    for chunk in chunks:
        if not isinstance(chunk, str):
            continue
        text = " ".join(chunk.split())
        if not text:
            continue
        result.append(text[:max_chars_per_chunk])
        if len(result) >= max_chunks:
            break
    return result

def estimate_context_chars(chunks: Iterable[str]) -> int:
    return sum(len(chunk) for chunk in chunks)
