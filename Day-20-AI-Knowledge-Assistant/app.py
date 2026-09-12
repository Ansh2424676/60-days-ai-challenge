from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from rag_pipeline import answer_query


app = FastAPI(
    title="Day 20 - AI Knowledge Assistant",
    description="Grounded RAG assistant using LangChain chunking, FAISS retrieval, metadata filtering, and OpenAI generation.",
    version="1.0.0",
)


class AskRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Question for the knowledge assistant")
    filters: dict[str, Any] | None = Field(
        default=None,
        description="Optional exact metadata filters, e.g. {'category': 'training'}",
    )


class Source(BaseModel):
    id: str
    chunk_id: str
    title: str
    score: float
    metadata: dict[str, Any]


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]
    confidence: float
    low_confidence: bool


@app.get("/")
def root():
    return {
        "message": "Day 20 AI Knowledge Assistant is running.",
        "docs": "/docs",
        "endpoint": "POST /ask",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    try:
        return answer_query(request.query, request.filters)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
