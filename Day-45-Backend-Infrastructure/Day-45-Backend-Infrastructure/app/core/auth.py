import os

from fastapi import Header, HTTPException, status
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("API_KEY")


def verify_api_key(
    x_api_key: str | None = Header(default=None)
):
    """
    Verify the API key supplied through the x-api-key header.
    """

    if not API_KEY:
        raise RuntimeError(
            "API_KEY is not configured in the environment."
        )

    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Please provide the x-api-key header."
        )

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key."
        )

    return True