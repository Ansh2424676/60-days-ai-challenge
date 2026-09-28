import logging
import os


LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)


def configure_logging(
    level: str | None = None,
) -> None:
    """
    Configure application-wide logging.

    Supported levels:
    DEBUG, INFO, WARNING, ERROR, CRITICAL
    """

    log_level = (
        level
        or os.getenv("LOG_LEVEL", "INFO")
    ).upper()

    numeric_level = getattr(
        logging,
        log_level,
        logging.INFO,
    )

    logging.basicConfig(
        level=numeric_level,
        format=LOG_FORMAT,
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """Return a module-specific logger."""
    return logging.getLogger(name)