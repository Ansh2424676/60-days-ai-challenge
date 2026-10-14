import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from context_optimizer import optimise_context

def test_chunk_limit():
    assert len(optimise_context(["a", "b", "c"], max_chunks=2)) == 2

def test_character_limit():
    assert len(optimise_context(["x" * 100], max_chars_per_chunk=10)[0]) == 10

def test_empty_chunks_removed():
    assert optimise_context(["", "  ", "useful"]) == ["useful"]

def test_whitespace_collapsed():
    assert optimise_context(["hello   world"]) == ["hello world"]
