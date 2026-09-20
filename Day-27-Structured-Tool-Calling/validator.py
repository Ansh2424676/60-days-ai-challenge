from typing import Any


REQUIRED_ARGUMENTS = {
    "search_documents": ["query"],
    "get_weather_stub": ["city"],
    "calculate": ["expression"],
    "get_today": [],
}


def validate_arguments(
    tool_name: str,
    arguments: dict[str, Any],
) -> tuple[bool, str]:

    if tool_name not in REQUIRED_ARGUMENTS:
        return False, f"Unknown tool: {tool_name}"

    required = REQUIRED_ARGUMENTS[tool_name]

    for argument in required:
        if argument not in arguments:
            return False, f"Missing required argument: {argument}"

        if arguments[argument] in (None, ""):
            return False, f"Argument cannot be empty: {argument}"

    if tool_name == "search_documents":

        if not isinstance(arguments.get("query"), str):
            return False, "query must be a string"

        top_k = arguments.get("top_k", 3)

        if not isinstance(top_k, int):
            return False, "top_k must be an integer"

        if not 1 <= top_k <= 5:
            return False, "top_k must be between 1 and 5"

    elif tool_name == "get_weather_stub":

        if not isinstance(arguments.get("city"), str):
            return False, "city must be a string"

    elif tool_name == "calculate":

        if not isinstance(arguments.get("expression"), str):
            return False, "expression must be a string"

    elif tool_name == "get_today":

        if arguments:
            return False, "get_today does not accept arguments"

    return True, "Valid arguments"