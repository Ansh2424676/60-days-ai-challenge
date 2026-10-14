import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from robustness import out_of_scope_response

QUERIES = [
    "Who won the latest cricket match?",
    "Give me a chocolate cake recipe.",
    "Diagnose my headache.",
    "Predict tomorrow's stock market.",
    "Plan a holiday in Paris."
]

def main():
    passed = 0
    for i, query in enumerate(QUERIES, 1):
        response = out_of_scope_response()
        ok = (
            "please" in response.lower()
            and ("ask" in response.lower() or "consult" in response.lower())
        )
        passed += int(ok)
        print(f"\nTest {i}: {query}")
        print(f"Response: {response}")
        print(f"Result: {'PASS' if ok else 'FAIL'}")
    print(f"\nSummary: {passed}/{len(QUERIES)} refusal-message checks passed.")

if __name__ == "__main__":
    main()
