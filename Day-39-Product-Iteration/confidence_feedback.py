def add_helpfulness_prompt(response: str, retrieval_score: float) -> str:
    """Append a helpfulness prompt when retrieval confidence is low."""
    if retrieval_score < 0.4:
        return (
            response.rstrip()
            + "\n\nIs this answer helpful? Yes or No"
        )
    return response
