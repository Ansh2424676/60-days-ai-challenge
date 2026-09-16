from memory import ConversationHistory


def test_append():
    history = ConversationHistory()

    history.append("user", "Hello")
    history.append("assistant", "Hi! How can I help you?")

    assert len(history.messages) == 2


def test_get_context():
    history = ConversationHistory()

    for i in range(7):
        history.append("user", f"Question {i}")
        history.append("assistant", f"Answer {i}")

    context = history.get_context(last_turns=5)

    assert len(context) == 10
    assert context[0]["content"] == "Question 2"


def test_clear():
    history = ConversationHistory()

    history.append("user", "Hello")
    history.append("assistant", "Hi")

    history.clear()

    assert len(history.messages) == 0


def test_turn_count():
    history = ConversationHistory()

    history.append("user", "Question 1")
    history.append("assistant", "Answer 1")

    history.append("user", "Question 2")
    history.append("assistant", "Answer 2")

    assert history.turn_count() == 2


def test_should_summarize():
    history = ConversationHistory(max_turns=10)

    for i in range(11):
        history.append("user", f"Question {i}")
        history.append("assistant", f"Answer {i}")

    assert history.should_summarize() is True