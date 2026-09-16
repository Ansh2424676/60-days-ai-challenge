from typing import TypedDict


class Message(TypedDict):
    role: str
    content: str


class ConversationHistory:
    """
    Stores conversation messages for a single session.
    """

    def __init__(self, max_turns: int = 10):
        self.messages: list[Message] = []
        self.max_turns = max_turns

    def append(self, role: str, content: str) -> None:
        """
        Add a user or assistant message to the conversation.
        """
        self.messages.append(
            {
                "role": role,
                "content": content,
            }
        )

    def get_context(self, last_turns: int = 5) -> list[Message]:
        """
        Return only the most recent conversation turns.

        One turn consists of a user message + assistant response.
        """
        max_messages = last_turns * 2

        return self.messages[-max_messages:]

    def clear(self) -> None:
        """
        Clear the complete conversation history.
        """
        self.messages.clear()

    def turn_count(self) -> int:
        """
        Return the number of complete conversation turns.
        """
        return len(self.messages) // 2

    def should_summarize(self) -> bool:
        """
        Check whether the conversation has exceeded the memory window.
        """
        return self.turn_count() > self.max_turns