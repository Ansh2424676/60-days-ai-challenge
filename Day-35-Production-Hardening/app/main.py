import logging

import faiss
import numpy as np
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.health import HealthChecker
from app.logging_config import configure_logging
from app.retrieval import ProductionRetriever


configure_logging(level="INFO")

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Production Hardened AI Assistant",
    version="1.0.0",
)


# --------------------------------------------------
# FAISS TEST INDEX
# --------------------------------------------------

TEST_DIMENSION = 384

faiss_index = faiss.IndexFlatL2(
    TEST_DIMENSION
)

test_vector = np.zeros(
    (1, TEST_DIMENSION),
    dtype="float32",
)

faiss_index.add(test_vector)


# --------------------------------------------------
# KNOWLEDGE BASE
# --------------------------------------------------

DOCUMENTS = [
    "Python is a programming language used for software development.",
    "FastAPI is a Python framework for building APIs.",
    "FAISS is a library for efficient vector similarity search.",
    "Redis is an in-memory data store commonly used for caching.",
]


# --------------------------------------------------
# RETRIEVAL
# --------------------------------------------------

retriever = ProductionRetriever(
    documents=DOCUMENTS,
    faiss_index=None,
    embedding_function=None,
)


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

health_checker = HealthChecker(
    faiss_index=faiss_index
)


# --------------------------------------------------
# REQUEST MODEL
# --------------------------------------------------

class ChatRequest(BaseModel):
    query: str


# --------------------------------------------------
# MOCKABLE OPENAI FUNCTION
# --------------------------------------------------

def generate_answer(
    query: str,
    context: list[str],
) -> str:
    """
    Generate an answer using OpenAI.

    This function is intentionally separated so
    integration tests can mock it.
    """

    from openai import OpenAI
    import os

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    context_text = "\n".join(context)

    response = client.responses.create(
        model="gpt-4o-mini",
        input=(
            f"Context:\n{context_text}\n\n"
            f"Question: {query}"
        ),
        max_output_tokens=100,
    )

    return response.output_text


# --------------------------------------------------
# ROOT
# --------------------------------------------------

@app.get("/")
def root():

    logger.info(
        "Root endpoint requested"
    )

    return {
        "message": (
            "Production Hardened "
            "AI Assistant is running"
        )
    }


# --------------------------------------------------
# HEALTH
# --------------------------------------------------

@app.get("/health")
def health():

    logger.info(
        "Health check requested"
    )

    result = health_checker.run_all_checks()

    status_code = (
        200
        if result["status"] == "healthy"
        else 503
    )

    return JSONResponse(
        status_code=status_code,
        content=result,
    )


# --------------------------------------------------
# CHAT
# --------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    logger.info(
        "Chat request received"
    )

    retrieval = retriever.search(
        query=request.query,
        top_k=3,
    )

    answer = generate_answer(
        query=request.query,
        context=retrieval["results"],
    )

    return {
        "answer": answer,
        "retrieval_method": retrieval["method"],
        "fallback": retrieval["fallback"],
        "context": retrieval["results"],
    }