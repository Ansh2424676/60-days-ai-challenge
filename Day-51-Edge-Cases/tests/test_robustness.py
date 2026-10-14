import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from robustness import normalize_input, safe_error_message

def test_empty_input():
    assert normalize_input("   ")["ok"] is False

def test_whitespace():
    result = normalize_input("  hello    world  ")
    assert result["ok"] and result["query"] == "hello world"

def test_unicode_normalization():
    result = normalize_input("  Ｈｅｌｌｏ？ ")
    assert result["ok"] and result["query"] == "Hello?"

def test_long_input():
    assert normalize_input("x" * 4001)["ok"] is False

def test_safe_error():
    message = safe_error_message("processing")
    assert "try again" in message.lower()
    assert "Traceback" not in message
