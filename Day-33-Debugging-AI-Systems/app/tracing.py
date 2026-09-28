import logging
import time
import uuid
from contextlib import contextmanager
from typing import Any, Generator


logger = logging.getLogger(__name__)


@contextmanager
def trace_operation(
    operation: str,
    metadata: dict[str, Any] | None = None,
) -> Generator[str, None, None]:
    """Trace an operation with timing and metadata."""

    trace_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    logger.info(
        "TRACE_START | trace_id=%s | operation=%s | metadata=%s",
        trace_id,
        operation,
        metadata or {},
    )

    try:
        yield trace_id

    except Exception as exc:
        elapsed = time.perf_counter() - start_time

        logger.exception(
            "TRACE_ERROR | trace_id=%s | operation=%s | "
            "elapsed=%.4fs | error=%s",
            trace_id,
            operation,
            elapsed,
            exc,
        )

        raise

    finally:
        elapsed = time.perf_counter() - start_time

        logger.info(
            "TRACE_END | trace_id=%s | operation=%s | elapsed=%.4fs",
            trace_id,
            operation,
            elapsed,
        )