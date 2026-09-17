import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


OPENAI_MODEL: str = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.6-luna",
)

EMBEDDING_MODEL: str = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2",
)

TOP_K: int = int(
    os.getenv("TOP_K", "3")
)

LOW_CONFIDENCE_THRESHOLD: float = float(
    os.getenv("LOW_CONFIDENCE_THRESHOLD", "0.3")
)

CHUNK_SIZE: int = int(
    os.getenv("CHUNK_SIZE", "500")
)

CHUNK_OVERLAP: int = int(
    os.getenv("CHUNK_OVERLAP", "50")
)

OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")