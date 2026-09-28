import logging
import time
from typing import Callable, Any

logger = logging.getLogger(__name__)


class CircuitBreaker:
    """
    Circuit breaker for unreliable external services.

    States:
    - CLOSED: Requests are allowed.
    - OPEN: Requests are blocked temporarily.
    - HALF_OPEN: One request is allowed to test recovery.
    """

    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: int = 60,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self.failure_count = 0
        self.state = "CLOSED"
        self.opened_at = None

    def _should_attempt_reset(self) -> bool:
        """Check whether the recovery timeout has elapsed."""
        if self.opened_at is None:
            return False

        return time.monotonic() - self.opened_at >= self.recovery_timeout

    def call(self, func: Callable[..., Any], *args, **kwargs) -> Any:
        """
        Execute a function through the circuit breaker.
        """

        # OPEN state
        if self.state == "OPEN":

            if self._should_attempt_reset():
                self.state = "HALF_OPEN"
                logger.warning(
                    "Circuit breaker entering HALF_OPEN state"
                )
            else:
                logger.error(
                    "Circuit breaker is OPEN. Request blocked."
                )
                raise RuntimeError(
                    "Service temporarily unavailable. "
                    "Please try again later."
                )

        try:
            result = func(*args, **kwargs)

            # Successful request
            self.failure_count = 0
            self.state = "CLOSED"
            self.opened_at = None

            logger.info("Circuit breaker request succeeded.")

            return result

        except Exception as exc:
            self.failure_count += 1

            logger.error(
                "External service failure %s/%s: %s",
                self.failure_count,
                self.failure_threshold,
                exc,
            )

            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                self.opened_at = time.monotonic()

                logger.error(
                    "Circuit breaker OPEN after %s consecutive failures.",
                    self.failure_count,
                )

            raise