import re


INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?prior\s+instructions",
    r"forget\s+(all\s+)?previous\s+instructions",
    r"your\s+system\s+prompt\s+is",
    r"reveal\s+(your\s+)?system\s+prompt",
    r"show\s+(your\s+)?system\s+prompt",
    r"reveal\s+hidden\s+instructions",
    r"developer\s+instructions",
    r"override\s+(your\s+)?instructions",
    r"override\s+(your\s+)?role",
    r"you\s+are\s+now\s+",
    r"act\s+as\s+an?\s+unrestricted",
]


def detect_injection(text: str) -> list[str]:
    """Return injection patterns detected in the input."""

    detected = []

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            detected.append(pattern)

    return detected


def sanitize_input(text: str) -> tuple[bool, str]:
    """
    Check user input for known prompt-injection patterns.

    Returns:
        (allowed, message)
    """

    detected = detect_injection(text)

    if detected:
        return (
            False,
            "Request blocked: potential prompt injection detected.",
        )

    return True, text