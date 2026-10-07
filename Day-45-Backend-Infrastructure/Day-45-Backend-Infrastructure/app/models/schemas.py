from typing import Any, Optional
from pydantic import BaseModel, Field


# -----------------------------
# Session Schemas
# -----------------------------

class CreateSessionResponse(BaseModel):
    session_id: str
    message: str


# -----------------------------
# Ask / Research Schemas
# -----------------------------

class AskRequest(BaseModel):
    session_id: str = Field(
        ...,
        description="Unique UUID of the user session"
    )
    query: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Technical research question"
    )


class AskResponse(BaseModel):
    session_id: str
    query: str
    answer: str
    sources: list[Any] = []
    retrieval_score: Optional[float] = None
    latency_ms: float


# -----------------------------
# Conversation History
# -----------------------------

class HistoryResponse(BaseModel):
    session_id: str
    history: list[dict[str, Any]]


# -----------------------------
# Feedback Schemas
# -----------------------------

class FeedbackRequest(BaseModel):
    session_id: str
    query: str = Field(
        ...,
        min_length=1,
        max_length=2000
    )
    rating: str = Field(
        ...,
        description="positive or negative"
    )
    correct: bool
    grounded: bool
    source_quality: int = Field(
        ...,
        ge=1,
        le=5,
        description="Source quality rating from 1 to 5"
    )
    comment: Optional[str] = Field(
        default=None,
        max_length=1000
    )


class FeedbackResponse(BaseModel):
    message: str
    feedback_id: int


# -----------------------------
# Health Check
# -----------------------------

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str