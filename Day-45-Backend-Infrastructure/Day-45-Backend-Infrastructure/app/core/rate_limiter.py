import time
from collections import defaultdict


class RateLimiter:
    """
    In-memory rate limiter.

    Each session is allowed a maximum number of requests
    within a fixed time window.
    """

    def __init__(
        self,
        max_requests: int = 20,
        window_seconds: int = 3600
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

        # session_id -> list of request timestamps
        self.requests = defaultdict(list)

    def _cleanup(self, session_id: str) -> None:
        """
        Remove request timestamps that are outside
        the current rate-limit window.
        """

        current_time = time.time()

        valid_requests = [
            timestamp
            for timestamp in self.requests[session_id]
            if current_time - timestamp < self.window_seconds
        ]

        self.requests[session_id] = valid_requests

    def is_allowed(self, session_id: str) -> bool:
        """
        Check whether the session is allowed to make
        another request.
        """

        self._cleanup(session_id)

        return len(self.requests[session_id]) < self.max_requests

    def record_request(self, session_id: str) -> None:
        """
        Record a new request for the session.
        """

        self._cleanup(session_id)

        self.requests[session_id].append(time.time())

    def get_remaining_requests(self, session_id: str) -> int:
        """
        Return the number of requests remaining
        in the current window.
        """

        self._cleanup(session_id)

        return max(
            0,
            self.max_requests - len(self.requests[session_id])
        )


# Global rate limiter instance
rate_limiter = RateLimiter(
    max_requests=20,
    window_seconds=3600
)