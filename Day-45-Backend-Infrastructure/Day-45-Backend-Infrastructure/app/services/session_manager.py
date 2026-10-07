from uuid import uuid4
from typing import Any


class SessionManager:
    """
    Manages user sessions and keeps separate conversation
    history for every session.
    """

    def __init__(self):
        self.sessions: dict[str, list[dict[str, Any]]] = {}

    def create_session(self) -> str:
        """Create a new UUID-based session."""
        session_id = str(uuid4())

        self.sessions[session_id] = []

        return session_id

    def session_exists(self, session_id: str) -> bool:
        """Check whether a session exists."""
        return session_id in self.sessions

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str
    ) -> None:
        """Add a message to a session's conversation history."""

        if not self.session_exists(session_id):
            raise ValueError("Session not found")

        self.sessions[session_id].append({
            "role": role,
            "content": content
        })

    def get_history(
        self,
        session_id: str
    ) -> list[dict[str, Any]]:
        """Return conversation history for a session."""

        if not self.session_exists(session_id):
            raise ValueError("Session not found")

        return self.sessions[session_id]

    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""

        if not self.session_exists(session_id):
            return False

        del self.sessions[session_id]

        return True


# Global session manager instance
session_manager = SessionManager()