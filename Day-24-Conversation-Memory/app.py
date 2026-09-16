import os
import uuid
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, Field
from openai import AsyncOpenAI

from memory import ConversationHistory

load_dotenv()

app = FastAPI(
    title="Conversation Memory AI API",
    description="Day 24 - Stateful AI conversations with session-based memory.",
    version="1.0.0",
)

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Separate memory for every session
sessions: dict[str, ConversationHistory] = {}


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1)
    session_id: Optional[str] = None
    memory_enabled: bool = True


class ChatResponse(BaseModel):
    answer: str
    session_id: str
    memory_enabled: bool
    context_turns: int


def get_or_create_session(session_id: str) -> ConversationHistory:
    if session_id not in sessions:
        sessions[session_id] = ConversationHistory(max_turns=10)

    return sessions[session_id]


async def generate_answer(
    query: str,
    context: list,
) -> str:

    conversation_context = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in context
    )

    prompt = f"""
You are a helpful AI assistant.

Use the conversation history below to understand follow-up
questions and pronouns correctly.

Conversation history:
{conversation_context}

Current user question:
{query}

Answer the current question clearly and accurately.
"""

    response = await client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        input=prompt,
    )

    return response.output_text


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "conversation-memory-api",
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    session_id = request.session_id or f"session_{uuid.uuid4().hex[:12]}"

    history = get_or_create_session(session_id)

    # Get only the latest five turns when memory is enabled
    if request.memory_enabled:
        context = history.get_context(last_turns=5)
    else:
        context = []

    answer = await generate_answer(
        request.query,
        context,
    )

    # Store both sides of the conversation
    history.append(
        "user",
        request.query,
    )

    history.append(
        "assistant",
        answer,
    )

    return ChatResponse(
        answer=answer,
        session_id=session_id,
        memory_enabled=request.memory_enabled,
        context_turns=len(context) // 2,
    )


@app.delete("/chat/{session_id}")
async def clear_session(session_id: str):

    if session_id in sessions:
        sessions[session_id].clear()

        return {
            "message": "Conversation memory cleared.",
            "session_id": session_id,
        }

    return {
        "message": "Session not found.",
        "session_id": session_id,
    }