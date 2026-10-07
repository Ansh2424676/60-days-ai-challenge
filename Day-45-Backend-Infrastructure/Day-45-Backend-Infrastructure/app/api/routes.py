import time

from fastapi import APIRouter, Depends, HTTPException, status
from httpcore2 import request

from app.core.auth import verify_api_key
from app.core.rate_limiter import rate_limiter
from app.db.database import log_request, save_feedback
from app.models.schemas import (
    AskRequest,
    AskResponse,
    CreateSessionResponse,
    FeedbackRequest,
    FeedbackResponse,
    HealthResponse,
    HistoryResponse,
)
from app.services.session_manager import session_manager


router = APIRouter()


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@router.get(
    "/health",
    response_model=HealthResponse,
)
def health_check(
    _: bool = Depends(verify_api_key)
):
    return {
        "status": "healthy",
        "service": "ResearchMate AI",
        "version": "1.0.0",
    }


# --------------------------------------------------
# Create Session
# --------------------------------------------------

@router.post(
    "/session",
    response_model=CreateSessionResponse,
)
def create_session(
    _: bool = Depends(verify_api_key)
):
    session_id = session_manager.create_session()

    return {
        "session_id": session_id,
        "message": "Session created successfully",
    }


# --------------------------------------------------
# Get Conversation History
# --------------------------------------------------

@router.get(
    "/session/{session_id}/history",
    response_model=HistoryResponse,
)
def get_history(
    session_id: str,
    _: bool = Depends(verify_api_key)
):
    if not session_manager.session_exists(session_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found.",
        )

    return {
        "session_id": session_id,
        "history": session_manager.get_history(session_id),
    }


# --------------------------------------------------
# Ask ResearchMate AI
# --------------------------------------------------

@router.post(
    "/ask",
    response_model=AskResponse,
)
def ask_question(
    request: AskRequest,
    _: bool = Depends(verify_api_key)
):
    # 1. Check session
    if not session_manager.session_exists(request.session_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found. Please create a session first.",
        )

    # 2. Check rate limit
    if not rate_limiter.is_allowed(request.session_id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=(
                "Rate limit exceeded. You can make up to "
                "20 requests per hour. Please try again later."
            ),
        )

    # 3. Record request
    rate_limiter.record_request(request.session_id)

    # 4. Start latency timer
    start_time = time.perf_counter()

    # --------------------------------------------------
    # Temporary AI response
    # Day 44 core_ai_loop will be connected here.
    # --------------------------------------------------

    answer = (
        f"ResearchMate AI received your question: "
        f"{request.query}"
    )

    sources = []

    retrieval_score = None

    # 5. Calculate latency
    latency_ms = (time.perf_counter() - start_time) * 1000

    # 6. Store conversation
    session_manager.add_message(
        request.session_id,
        "user",
        request.query,
    )

    session_manager.add_message(
        request.session_id,
        "assistant",
        answer,
    )

    # 7. Log request
    log_request(
        session_id=request.session_id,
        query=request.query,
        response_excerpt=answer[:500],
        latency_ms=latency_ms,
        retrieval_score=retrieval_score,
    )

    # 8. Return response
    return {
        "session_id": request.session_id,
        "query": request.query,
        "answer": answer,
        "sources": sources,
        "retrieval_score": retrieval_score,
        "latency_ms": round(latency_ms, 2),
    }


# --------------------------------------------------
# Feedback
# --------------------------------------------------

@router.post(
    "/feedback",
    response_model=FeedbackResponse,
)
def submit_feedback(
    request: FeedbackRequest,
    _: bool = Depends(verify_api_key)
):
    if not session_manager.session_exists(request.session_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found.",
        )

    if request.rating not in ["positive", "negative"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be either positive or negative.",
        )

    feedback_id = save_feedback(
        session_id=request.session_id,
        query=request.query,
        rating=request.rating,
        correct=request.correct,
        grounded=request.grounded,
        source_quality=request.source_quality,
        comment=request.comment,
    )

    return {
        "message": "Feedback recorded successfully.",
        "feedback_id": feedback_id,
    }
# --------------------------------------------------
# Temporary AI response
# Day 44 core_ai_loop will be connected here.
# --------------------------------------------------

answer = (
    f"ResearchMate AI received your question: "
    f"{request.query}"
)

sources = []

retrieval_score = None