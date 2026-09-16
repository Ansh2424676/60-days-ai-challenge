import asyncio
import json
import uuid

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, StreamingResponse

from models import (
    ChatRequest,
    ChatResponse,
    ErrorResponse
)

from services import (
    retrieve_documents,
    generate_answer,
    stream_answer,
    simulate_slow_pipeline
)


# ==================================================
# FASTAPI APPLICATION
# ==================================================

app = FastAPI(
    title="Production-Ready AI API",
    description=(
        "Day 22 - Production-grade AI API with "
        "validation, structured errors, retry logic, "
        "streaming and timeout handling."
    ),
    version="1.0.0"
)


# ==================================================
# CONFIGURATION
# ==================================================

REQUEST_TIMEOUT = 15


# ==================================================
# STRUCTURED ERROR RESPONSE
# ==================================================

def create_error_response(
    code: str,
    message: str,
    request_id: str,
    http_status: int
):
    """
    Create a consistent structured error response.
    """

    return JSONResponse(
        status_code=http_status,
        content={
            "code": code,
            "message": message,
            "request_id": request_id
        }
    )


# ==================================================
# INPUT VALIDATION ERROR HANDLER
# ==================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    """
    Convert FastAPI/Pydantic validation errors
    into our structured INPUT_INVALID response.
    """

    request_id = (
        f"req_{uuid.uuid4().hex[:12]}"
    )

    messages = []

    for error in exc.errors():

        message = error.get(
            "msg",
            "Invalid request."
        )

        messages.append(message)

    final_message = " ".join(messages)

    return create_error_response(
        code="INPUT_INVALID",
        message=final_message,
        request_id=request_id,
        http_status=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


# ==================================================
# HEALTH CHECK
# ==================================================

@app.get("/health")
async def health():
    """
    Health check endpoint.
    """

    return {
        "status": "healthy",
        "service": "production-ai-api",
        "version": "1.0.0"
    }


# ==================================================
# NORMAL CHAT ENDPOINT
# ==================================================

@app.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        422: {
            "model": ErrorResponse
        },
        500: {
            "model": ErrorResponse
        },
        504: {
            "model": ErrorResponse
        }
    }
)
async def chat(request: ChatRequest):
    """
    Main AI endpoint.

    Pipeline:

    User Query
        ↓
    Validation
        ↓
    Retrieval
        ↓
    Context
        ↓
    LLM
        ↓
    Response
    """

    request_id = (
        f"req_{uuid.uuid4().hex[:12]}"
    )

    try:

        # ------------------------------------------
        # STEP 1: RETRIEVAL
        # ------------------------------------------

        documents = await retrieve_documents(
            request.query
        )

        if not documents:

            return create_error_response(
                code="RETRIEVAL_FAILURE",
                message=(
                    "No relevant documents were "
                    "retrieved from the knowledge base."
                ),
                request_id=request_id,
                http_status=500
            )

        # ------------------------------------------
        # STEP 2: BUILD CONTEXT
        # ------------------------------------------

        context = "\n\n".join(
            document["content"]
            for document in documents
        )

        sources = [
            document["id"]
            for document in documents
        ]

        # ------------------------------------------
        # STEP 3: LLM WITH 15 SECOND TIMEOUT
        # ------------------------------------------

        answer = await asyncio.wait_for(
            generate_answer(
                request.query,
                context
            ),
            timeout=REQUEST_TIMEOUT
        )

        # ------------------------------------------
        # STEP 4: STRUCTURED SUCCESS RESPONSE
        # ------------------------------------------

        return ChatResponse(
            answer=answer,
            request_id=request_id,
            sources=sources
        )

    # ----------------------------------------------
    # TIMEOUT ERROR
    # ----------------------------------------------

    except asyncio.TimeoutError:

        return create_error_response(
            code="LLM_TIMEOUT",
            message=(
                "The AI generation pipeline exceeded "
                "the 15-second request timeout."
            ),
            request_id=request_id,
            http_status=504
        )

    # ----------------------------------------------
    # RETRIEVAL / PIPELINE FAILURE
    # ----------------------------------------------

    except RuntimeError as exc:

        return create_error_response(
            code="RETRIEVAL_FAILURE",
            message=str(exc),
            request_id=request_id,
            http_status=500
        )

    # ----------------------------------------------
    # UNEXPECTED ERROR
    # ----------------------------------------------

    except Exception as exc:

        return create_error_response(
            code="RETRIEVAL_FAILURE",
            message=(
                f"Unexpected pipeline error: {str(exc)}"
            ),
            request_id=request_id,
            http_status=500
        )


# ==================================================
# STREAMING CHAT ENDPOINT
# ==================================================

@app.post(
    "/chat/stream"
)
async def chat_stream(request: ChatRequest):
    """
    Streaming AI endpoint.

    Uses FastAPI StreamingResponse so that
    generated content can reach the client
    incrementally.
    """

    request_id = (
        f"req_{uuid.uuid4().hex[:12]}"
    )

    try:

        # ------------------------------------------
        # RETRIEVAL
        # ------------------------------------------

        documents = await retrieve_documents(
            request.query
        )

        if not documents:

            return create_error_response(
                code="RETRIEVAL_FAILURE",
                message=(
                    "No relevant documents were "
                    "retrieved."
                ),
                request_id=request_id,
                http_status=500
            )

        # ------------------------------------------
        # CONTEXT
        # ------------------------------------------

        context = "\n\n".join(
            document["content"]
            for document in documents
        )

        # ------------------------------------------
        # STREAM GENERATOR
        # ------------------------------------------

        async def response_generator():

            try:

                async for chunk in stream_answer(
                    request.query,
                    context
                ):

                    yield chunk

            except asyncio.TimeoutError:

                error = {
                    "code": "LLM_TIMEOUT",
                    "message": (
                        "Streaming generation "
                        "exceeded the timeout."
                    ),
                    "request_id": request_id
                }

                yield (
                    "\n"
                    + json.dumps(error)
                )

            except Exception as exc:

                error = {
                    "code": "RETRIEVAL_FAILURE",
                    "message": str(exc),
                    "request_id": request_id
                }

                yield (
                    "\n"
                    + json.dumps(error)
                )

        # ------------------------------------------
        # STREAM RESPONSE
        # ------------------------------------------

        return StreamingResponse(
            response_generator(),
            media_type="text/plain",
            headers={
                "X-Request-ID": request_id
            }
        )

    except Exception as exc:

        return create_error_response(
            code="RETRIEVAL_FAILURE",
            message=str(exc),
            request_id=request_id,
            http_status=500
        )


# ==================================================
# DELIBERATE TIMEOUT TEST
# ==================================================

@app.post("/test/timeout")
async def test_timeout():
    """
    Deliberately triggers the 15-second timeout
    so that LLM_TIMEOUT can be verified.
    """

    request_id = (
        f"req_{uuid.uuid4().hex[:12]}"
    )

    try:

        await asyncio.wait_for(
            simulate_slow_pipeline(),
            timeout=REQUEST_TIMEOUT
        )

        return {
            "message": "Unexpected completion."
        }

    except asyncio.TimeoutError:

        return create_error_response(
            code="LLM_TIMEOUT",
            message=(
                "The simulated AI pipeline "
                "exceeded the 15-second timeout."
            ),
            request_id=request_id,
            http_status=504
        )


# ==================================================
# DELIBERATE RETRIEVAL FAILURE TEST
# ==================================================

@app.post("/test/retrieval-failure")
async def test_retrieval_failure():
    """
    Deliberately triggers RETRIEVAL_FAILURE.
    """

    request_id = (
        f"req_{uuid.uuid4().hex[:12]}"
    )

    try:

        await retrieve_documents(
            "trigger retrieval failure"
        )

        return {
            "message": "Unexpected completion."
        }

    except RuntimeError as exc:

        return create_error_response(
            code="RETRIEVAL_FAILURE",
            message=str(exc),
            request_id=request_id,
            http_status=500
        )