from app.moderation import check_moderation
from app.output_validator import validate_output
from app.sanitizer import sanitize_input


def run_security_checks(
    user_input: str,
) -> dict:
    """
    Run all pre-LLM security checks.

    Order:
    1. Input sanitisation
    2. Moderation
    """

    allowed, sanitization_message = sanitize_input(
        user_input
    )

    if not allowed:
        return {
            "allowed": False,
            "blocked_by": "input_sanitization",
            "message": sanitization_message,
        }

    moderation = check_moderation(user_input)

    if not moderation["allowed"]:
        return {
            "allowed": False,
            "blocked_by": "moderation",
            "message": (
                "Request blocked by safety moderation."
            ),
            "moderation": moderation,
        }

    return {
        "allowed": True,
        "blocked_by": None,
        "message": "Input passed security checks.",
        "moderation": moderation,
    }


def validate_llm_response(
    response: str,
) -> dict:
    """Validate an LLM response before returning it."""

    validation = validate_output(response)

    if not validation["safe"]:
        return {
            "allowed": False,
            "blocked_by": "output_validation",
            "message": (
                "Response blocked by output validation."
            ),
            "validation": validation,
        }

    return {
        "allowed": True,
        "blocked_by": None,
        "message": "Response passed output validation.",
        "validation": validation,
    }