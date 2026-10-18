import re


LEAKAGE_PATTERNS = [
    r"system\s+prompt",
    r"developer\s+instructions",
    r"hidden\s+instructions",
    r"internal\s+instructions",
]

PERSONA_PATTERNS = [
    r"i\s+am\s+now\s+an?\s+unrestricted",
    r"my\s+new\s+role\s+is",
    r"i\s+will\s+ignore\s+my\s+instructions",
    r"i\s+will\s+follow\s+the\s+new\s+instructions",
]


def validate_output(text: str) -> dict:
    """Detect possible instruction leakage or persona adoption."""

    leakage_matches = []

    for pattern in LEAKAGE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            leakage_matches.append(pattern)

    persona_matches = []

    for pattern in PERSONA_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            persona_matches.append(pattern)

    safe = not leakage_matches and not persona_matches

    return {
        "safe": safe,
        "system_prompt_leak_detected": bool(leakage_matches),
        "persona_change_detected": bool(persona_matches),
        "leakage_matches": leakage_matches,
        "persona_matches": persona_matches,
    }