from confidence_feedback import add_helpfulness_prompt


def test_low_confidence():
    result = add_helpfulness_prompt("I am not sure about this.", 0.32)

    assert "Is this answer helpful? Yes or No" in result
    print("PASS: low-confidence response gets helpfulness prompt.")


def test_high_confidence():
    result = add_helpfulness_prompt("Python is a programming language.", 0.82)

    assert "Is this answer helpful? Yes or No" not in result
    print("PASS: high-confidence response is unchanged.")


if __name__ == "__main__":
    test_low_confidence()
    test_high_confidence()
