@'
SCORING_DIMENSIONS = [
    "correctness",
    "groundedness",
    "completeness",
    "relevance",
    "safe_abstention",
]

def calculate_overall(scores):
    if not scores:
        raise ValueError("Scores cannot be empty.")
    if any(not isinstance(v, (int, float)) or not 1 <= v <= 5 for v in scores.values()):
        raise ValueError("Every score must be between 1 and 5.")
    return round(sum(scores.values()) / len(scores), 2)

def validate_judge_result(result):
    missing = set(SCORING_DIMENSIONS) - set(result)
    if missing:
        raise ValueError(f"Missing scoring dimensions: {sorted(missing)}")
    return calculate_overall({k: result[k] for k in SCORING_DIMENSIONS})
'@ | Set-Content -Encoding UTF8 evaluator.py