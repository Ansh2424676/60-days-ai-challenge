from validator import validate_arguments


def run_validation_tests():

    tests = [
        (
            "Missing query",
            "search_documents",
            {},
        ),
        (
            "Wrong top_k type",
            "search_documents",
            {
                "query": "RAG",
                "top_k": "three",
            },
        ),
        (
            "Missing expression",
            "calculate",
            {},
        ),
        (
            "Valid weather",
            "get_weather_stub",
            {
                "city": "Kanpur",
            },
        ),
    ]

    for name, tool, arguments in tests:

        valid, message = validate_arguments(
            tool,
            arguments
        )

        print(
            f"{name}: "
            f"{'PASS' if valid else 'CAUGHT'} "
            f"→ {message}"
        )


if __name__ == "__main__":
    run_validation_tests()