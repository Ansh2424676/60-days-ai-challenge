from prompt_reliability import validate_response_format

def test_valid_response():
    response = (
        "Answer: Python is a language.\n"
        "Evidence: The context describes Python.\n"
        "Status: answered"
    )
    assert validate_response_format(response)[0]

def test_missing_section():
    assert not validate_response_format(
        "Answer: Python is a language.\nStatus: answered"
    )[0]

def test_invalid_status():
    response = (
        "Answer: Python is a language.\n"
        "Evidence: The context describes Python.\n"
        "Status: definitely_correct"
    )
    assert not validate_response_format(response)[0]

def test_empty_response():
    assert not validate_response_format("")[0]
