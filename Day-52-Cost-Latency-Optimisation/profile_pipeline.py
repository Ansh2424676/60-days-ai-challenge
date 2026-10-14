import json
import time
from datetime import datetime
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

# Replace these sample prompts with representative queries from your product.
SAMPLE_QUERIES = [
    "What is the product's purpose?",
    "Who is the target user?",
    "What are the main features?",
    "Explain the system architecture.",
    "How does retrieval work?",
    "What are the known limitations?",
    "How is a response generated?",
    "What happens when context is missing?",
    "How is quality evaluated?",
    "Explain the data ingestion process.",
    "How does the API handle requests?",
    "What is the role of the knowledge base?",
    "How are errors handled?",
    "How does the system handle long inputs?",
    "What makes an answer reliable?",
    "How should unsupported questions be handled?",
    "How can latency be measured?",
    "How can token usage be reduced?",
    "What should regression tests verify?",
    "Summarise the product's main workflow."
]

def record_step(name, duration_ms):
    return {"step": name, "duration_ms": round(duration_ms, 3)}

def estimate_cost(input_tokens, output_tokens, input_price_per_million, output_price_per_million):
    return (
        input_tokens * input_price_per_million
        + output_tokens * output_price_per_million
    ) / 1_000_000

def monthly_cost(avg_cost_per_query, queries_per_day):
    return avg_cost_per_query * queries_per_day * 30

def run_profile(query_fn=None):
    rows = []
    for index, query in enumerate(SAMPLE_QUERIES, 1):
        started = time.perf_counter()
        steps = []
        if query_fn is None:
            # No model call is made in demo mode.
            answer = None
            status = "NOT_RUN: connect actual product pipeline"
        else:
            try:
                step_start = time.perf_counter()
                answer = query_fn(query)
                steps.append(record_step("complete_pipeline", (time.perf_counter() - step_start) * 1000))
                status = "measured"
            except Exception as exc:
                answer = None
                status = f"ERROR: {type(exc).__name__}"
        rows.append({
            "query_id": index,
            "query": query,
            "status": status,
            "answer": answer,
            "steps": steps,
            "total_latency_ms": round((time.perf_counter() - started) * 1000, 3),
            "input_tokens": None,
            "output_tokens": None,
            "cost_usd": None
        })

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = RESULTS / f"profile_{stamp}.json"
    path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Queries listed: {len(rows)}")
    print(f"Report saved: {path}")
    print("Reminder: token/cost fields require actual API usage metadata and configured model pricing.")
    print("Reminder: demo mode does not measure real AI latency or quality.")

if __name__ == "__main__":
    run_profile()
