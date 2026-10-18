import logging
import sys

from app.config import LOG_LEVEL


def setup_logging() -> logging.Logger:
    """Configure application-wide logging."""

    logger = logging.getLogger()

    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger