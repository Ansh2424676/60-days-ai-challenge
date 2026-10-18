import logging

from app.logging_config import configure_logging


def test_warning_level_suppresses_debug_and_info(
    caplog,
):
    configure_logging("WARNING")

    logger = logging.getLogger(
        "production_test"
    )

    with caplog.at_level(
        logging.WARNING,
        logger="production_test",
    ):
        logger.debug(
            "Debug message"
        )

        logger.info(
            "Info message"
        )

        logger.warning(
            "Warning message"
        )

        logger.error(
            "Error message"
        )

    messages = [
        record.message
        for record in caplog.records
    ]

    assert "Debug message" not in messages
    assert "Info message" not in messages

    assert "Warning message" in messages
    assert "Error message" in messages