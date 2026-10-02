class ConversationMemory:
    def __init__(self, max_turns=7):
        self.max_turns = max_turns
        self.messages = []

    def add(self, role, content):
        self.messages.append({"role": role, "content": content})
        self.messages = self.messages[-(self.max_turns * 2):]

    def get_history(self):
        return self.messages


def test_seven_turn_memory():
    memory = ConversationMemory(max_turns=7)

    conversations = [
        ("user", "My project is called HireLens."),
        ("assistant", "Got it."),
        ("user", "It analyzes resumes."),
        ("assistant", "Understood."),
        ("user", "It uses Python."),
        ("assistant", "Yes."),
        ("user", "It also uses FastAPI."),
        ("assistant", "Correct."),
        ("user", "It has a React frontend."),
        ("assistant", "Okay."),
        ("user", "It is deployed online."),
        ("assistant", "Great."),
        ("user", "What is it called?"),
    ]

    for role, content in conversations:
        memory.add(role, content)

    history = memory.get_history()

    assert len(history) <= 14
    assert any("HireLens" in item["content"] for item in history)

    print("PASS: 7-turn memory preserves earlier context.")
    print("Stored messages:", len(history))


if __name__ == "__main__":
    test_seven_turn_memory()
