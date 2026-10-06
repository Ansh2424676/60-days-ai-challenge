import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def retrieve_context(user_input: str):
    """
    Retrieves relevant context from the knowledge base.

    Day 43 retrieval implementation can be connected here.
    """
    return []


def core_ai_loop(user_input: str) -> dict:
    """
    Main AI loop.

    Takes a user question, retrieves relevant context,
    generates a grounded answer, and returns sources.
    """

    if not user_input or not user_input.strip():
        raise ValueError("Question cannot be empty.")

    # Retrieve relevant context
    retrieved_docs = retrieve_context(user_input)

    context = "\n\n".join(
        doc.get("text", "")
        for doc in retrieved_docs
    )

    sources = [
        doc.get("source", "Unknown")
        for doc in retrieved_docs
    ]

    # Grounded AI prompt
    prompt = f"""
You are ResearchMate AI, an evidence-grounded
technical research assistant.

Answer the user's question using the provided context.

Rules:
1. Give a direct and technically accurate answer.
2. Prefer the provided context.
3. Do not invent information.
4. If the context is insufficient, clearly say so.
5. Keep the answer useful and structured.
6. Do not create fake citations.

CONTEXT:
{context}

USER QUESTION:
{user_input}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a reliable technical research assistant."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": sources
    }