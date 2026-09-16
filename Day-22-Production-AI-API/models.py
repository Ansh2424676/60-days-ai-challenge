from pydantic import BaseModel, Field, field_validator
import re


class ChatRequest(BaseModel):
    query: str = Field(
        ...,
        description="User question for the AI assistant",
        examples=[
            "What is retrieval augmented generation?"
        ]
    )

    stream: bool = Field(
        default=False,
        description="Whether to stream the AI response"
    )

    @field_validator("query")
    @classmethod
    def validate_query(cls, value: str) -> str:
        value = value.strip()

        # Less than 5 characters
        if len(value) < 5:
            raise ValueError(
                "Query must contain at least 5 characters."
            )

        # More than 1000 characters
        if len(value) > 1000:
            raise ValueError(
                "Query must not exceed 1000 characters."
            )

        # Only whitespace/special characters
        if not re.search(r"[A-Za-z0-9]", value):
            raise ValueError(
                "Query must contain at least one letter or number."
            )

        return value


class ErrorResponse(BaseModel):
    code: str = Field(
        ...,
        description="Structured application error code",
        examples=["INPUT_INVALID"]
    )

    message: str = Field(
        ...,
        description="Human-readable error message",
        examples=[
            "Query must contain at least 5 characters."
        ]
    )

    request_id: str = Field(
        ...,
        description="Unique request identifier",
        examples=["req_123456789"]
    )


class ChatResponse(BaseModel):
    answer: str = Field(
        ...,
        description="AI generated answer"
    )

    request_id: str = Field(
        ...,
        description="Unique request identifier",
        examples=["req_123456789"]
    )

    sources: list[str] = Field(
        default_factory=list,
        description="Retrieved document identifiers"
    )