import re

ALLOWED_STATUSES = {
    "answered",
    "partially_answered",
    "needs_clarification",
    "conflicting_evidence",
    "insufficient_context",
}

def validate_response_format(response: str) -> tuple[bool, str]:
    if not isinstance(response, str) or not response.strip():
        return False, "Response is empty."

    pattern = (
        r"(?s)^Answer:\s*(.*?)\nEvidence:\s*(.*?)"
        r"\nStatus:\s*(answered|partially_answered|"
        r"needs_clarification|conflicting_evidence|"
        r"insufficient_context)\s*$"
    )
    match = re.match(pattern, response.strip())

    if not match:
        return False, "Required sections or status are invalid."

    if not match.group(1).strip():
        return False, "Answer section is empty."

    if not match.group(2).strip():
        return False, "Evidence section is empty."

    return True, "Response format is valid."

def generate_validated_response(client, context: str, question: str, model: str, prompt: str) -> str:
    """Generate a response and retry once if its format is invalid."""

    messages = [
        {"role": "system", "content": prompt},
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion:\n{question}",
        },
    ]

    for attempt in range(2):
        result = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
        )

        response = result.choices[0].message.content or ""
        is_valid, error = validate_response_format(response)

        if is_valid:
            return response

        if attempt == 0:
            messages.extend([
                {"role": "assistant", "content": response},
                {
                    "role": "user",
                    "content": (
                        f"Your response failed validation: {error}\n"
                        "Retry once. Use exactly these sections:\n"
                        "Answer: ...\nEvidence: ...\nStatus: ...\n"
                        "Status must be one of the allowed values."
                    ),
                },
            ])

    return (
        "Answer: Unable to produce a valid response.\n"
        "Evidence: Response validation failed after one retry.\n"
        "Status: insufficient_context"
    )
