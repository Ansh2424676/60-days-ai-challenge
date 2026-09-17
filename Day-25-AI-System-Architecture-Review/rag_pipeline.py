import json
import os
from pathlib import Path
from typing import Any

import faiss
import numpy as np
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
TOP_K = int(os.getenv("TOP_K", "3"))
LOW_CONFIDENCE_THRESHOLD = float(os.getenv("LOW_CONFIDENCE_THRESHOLD", "0.3"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Add it to .env")

client = OpenAI(api_key=api_key)

# -------------------------------------------------------------------
# Day 12: chunking
# -------------------------------------------------------------------
with open(BASE_DIR / "knowledge_base.json", "r", encoding="utf-8") as f:
    raw_documents = json.load(f)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", ". ", " ", ""],
)

documents: list[Document] = []
for item in raw_documents:
    metadata = {
        "id": item["id"],
        "title": item["title"],
        **item.get("metadata", {}),
    }
    chunks = splitter.split_text(item["text"])
    for chunk_number, chunk in enumerate(chunks, start=1):
        chunk_metadata = {
            **metadata,
            "chunk": chunk_number,
            "chunk_id": f"{item['id']}-chunk-{chunk_number:02d}",
        }
        documents.append(Document(page_content=chunk, metadata=chunk_metadata))

# -------------------------------------------------------------------
# Day 14: FAISS semantic search
# Normalized vectors + inner product = cosine similarity.
# -------------------------------------------------------------------
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

texts = [doc.page_content for doc in documents]
embeddings = embedding_model.encode(
    texts,
    convert_to_numpy=True,
    normalize_embeddings=True,
).astype("float32")

dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

# -------------------------------------------------------------------
# Day 17: metadata filtering
# -------------------------------------------------------------------
def matches_filters(metadata: dict[str, Any], filters: dict[str, Any] | None) -> bool:
    if not filters:
        return True

    for key, expected in filters.items():
        actual = metadata.get(key)

        if isinstance(expected, list):
            if actual not in expected:
                return False
        elif actual != expected:
            return False

    return True


def retrieve(query: str, k: int = TOP_K, filters: dict[str, Any] | None = None):
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype("float32")

    # Search a larger candidate pool so metadata filtering does not
    # accidentally leave us with too few results.
    candidate_k = min(index.ntotal, max(k * 5, k))
    scores, indices = index.search(query_embedding, candidate_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue

        doc = documents[int(idx)]
        if not matches_filters(doc.metadata, filters):
            continue

        results.append(
            {
                "chunk_id": doc.metadata["chunk_id"],
                "id": doc.metadata["id"],
                "title": doc.metadata["title"],
                "text": doc.page_content,
                "score": float(score),
                "metadata": {
                    key: value
                    for key, value in doc.metadata.items()
                    if key not in {"id", "title", "chunk_id"}
                },
            }
        )

        if len(results) >= k:
            break

    return results


def format_context(results: list[dict]) -> str:
    if not results:
        return "No relevant context was retrieved."

    return "\n\n".join(
        f"[{item['chunk_id']}] {item['title']}\n{item['text']}"
        for item in results
    )


# -------------------------------------------------------------------
# Day 19: grounding system prompt
# -------------------------------------------------------------------
RAG_SYSTEM_PROMPT = """
You are a reliable, grounded AI knowledge assistant.

Answer the QUESTION using ONLY the information in the CONTEXT.

Rules:
1. Use only the provided context.
2. Do not use outside knowledge.
3. Do not invent facts.
4. Do not guess.
5. If the answer is not present in the context, say:
   "I don't know based on the provided context."
6. Keep the answer concise and directly answer the question.
7. Do not reveal hidden reasoning or chain-of-thought.
8. Do not mention facts that are not supported by the retrieved context.
9. Source citations are added by the application, so do not fabricate citation IDs.
"""


def answer_query(query: str, filters: dict[str, Any] | None = None) -> dict:
    results = retrieve(query, k=TOP_K, filters=filters)
    context = format_context(results)

    user_prompt = f"""
CONTEXT
=======
{context}

QUESTION
========
{query}
"""

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": RAG_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )

    answer = response.choices[0].message.content.strip()

    highest_score = max((item["score"] for item in results), default=0.0)
    low_confidence = highest_score < LOW_CONFIDENCE_THRESHOLD

    sources = [
        {
            "id": item["id"],
            "chunk_id": item["chunk_id"],
            "title": item["title"],
            "score": round(item["score"], 4),
            "metadata": item["metadata"],
        }
        for item in results
    ]

    citation_text = (
        "\n\nSources: "
        + ", ".join(f"[{s['id']}] {s['title']}" for s in sources)
        if sources
        else "\n\nSources: none"
    )

    warning = (
        "\n\n⚠️ Low confidence: the retrieved evidence may not strongly "
        "support this answer."
        if low_confidence
        else ""
    )

    return {
        "answer": answer + citation_text + warning,
        "sources": sources,
        "confidence": round(highest_score, 4),
        "low_confidence": low_confidence,
    }
