import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gpt-4o-mini"
)

TEMPERATURE = float(
    os.getenv("TEMPERATURE", "0")
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)

DEBUG_MODE = os.getenv(
    "DEBUG_MODE",
    "false"
).lower() == "true"


def validate_config() -> None:
    """Validate required configuration."""

    if not OPENAI_API_KEY:
        print(
            "WARNING: OPENAI_API_KEY is not configured."
        )