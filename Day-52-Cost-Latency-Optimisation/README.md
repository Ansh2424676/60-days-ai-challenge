# Day 52 — Optimise Your Product for Speed and Cost

## Objective
Measure AI pipeline cost and latency, implement semantic caching, and reduce unnecessary context.

## Implemented modules
- `profile_pipeline.py` — 20 representative queries and timestamped profiling report scaffold.
- `semantic_cache.py` — Redis-backed response cache with cosine similarity threshold greater than 0.92.
- `context_optimizer.py` — configurable limits on retrieved context chunks and characters.
- `tests/test_context_optimizer.py` — context optimiser unit tests.

## Profiling requirements
For each actual API call, record:
- Model name and token usage
- Input/output token cost using the applicable model prices
- Per-step latency in milliseconds
- Cache hit/miss status

## Monthly cost projection
For average cost C USD per query:
- 1,000 queries/day: C × 30,000 USD/month
- 10,000 queries/day: C × 300,000 USD/month
- 100,000 queries/day: C × 3,000,000 USD/month

## Quality guardrail
Run the Day 50 evaluation baseline before optimisation and after each optimisation. Stop if any evaluation dimension drops by more than 0.3 points.

## Current status
Initial profiler, cache module, and context optimiser scaffolds are present. Actual pipeline integration, Redis server verification, measured cost/latency results, and quality comparisons must be completed before claiming verified improvements.

## Run
```powershell
python .\Day-52-Cost-Latency-Optimisation\profile_pipeline.py
python -m pytest .\Day-52-Cost-Latency-Optimisation\tests -q
```
