import json
import os
from datetime import datetime
from pathlib import Path
from dataset import EVAL_DATASET

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

def score_response(question, answer, expected):
    """Temporary baseline checks; replace with the Day 29 LLM judge."""
    answer = (answer or "").strip()
    if not answer:
        return {"accuracy": 0, "relevance": 0, "grounding": 0, "reasoning": 0}
    unsupported = any(x in answer.lower() for x in ["i guarantee", "100% accurate", "never makes mistakes"])
    score = 2 if unsupported else 3
    return {"accuracy": score, "relevance": score, "grounding": score, "reasoning": score}

def evaluate():
    results = []
    for item in EVAL_DATASET:
        answer = "NOT RUN: connect your actual product pipeline and Day 29 LLM judge."
        scores = score_response(item["question"], answer, item["expected"])
        results.append({**item, "answer": answer, "scores": scores})
    return results

def regression_test_runner():
    results = evaluate()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = RESULTS / f"eval_{stamp}.json"
    path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Saved: {path}")
    print(f"Questions: {len(results)}")
    print("FAIL: Real product pipeline and Day 29 LLM judge are not connected.")
    return results

if __name__ == "__main__":
    regression_test_runner()
