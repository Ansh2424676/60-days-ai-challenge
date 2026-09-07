import os
import json
import faiss
import pandas as pd

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from openai import OpenAI


# ============================================================
# 1. ENVIRONMENT
# ============================================================

load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env")

client = OpenAI(api_key=api_key)

MODEL_NAME = "gpt-5.6-luna"

print("OpenAI client initialized successfully")


# ============================================================
# 2. LOAD KNOWLEDGE BASE
# ============================================================

with open("knowledge_base.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

texts = [doc["text"] for doc in documents]
ids = [doc["id"] for doc in documents]

print("Documents loaded:", len(documents))


# ============================================================
# 3. EMBEDDING MODEL
# ============================================================

print("\nLoading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = embedding_model.encode(
    texts,
    convert_to_numpy=True
)

print("Embedding shape:", embeddings.shape)


# ============================================================
# 4. FAISS INDEX
# ============================================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(
    embeddings.astype("float32")
)

print("FAISS index size:", index.ntotal)


# ============================================================
# 5. RETRIEVAL
# ============================================================

def retrieve_top_k(query, k=3):

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    )

    distances, indices = index.search(
        query_embedding.astype("float32"),
        k
    )

    results = []

    for distance, idx in zip(
        distances[0],
        indices[0]
    ):

        results.append({
            "id": ids[idx],
            "text": texts[idx],
            "distance": float(distance)
        })

    return results


# ============================================================
# 6. FORMAT CONTEXT
# ============================================================

def format_context(results):

    return "\n\n".join(
        f"[{item['id']}]\n{item['text']}"
        for item in results
    )


# ============================================================
# 7. NO-RAG
# ============================================================

def generate_without_rag(query):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": """
You are a helpful assistant.

Answer the user's question normally.

You do NOT have access to the private
NovaTech Solutions knowledge base.

Do not invent private company facts.
"""
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )

    return response.choices[0].message.content


# ============================================================
# 8. RAG SYSTEM PROMPT
# ============================================================

RAG_SYSTEM_PROMPT = """
You are a grounded question-answering assistant.

Answer the QUESTION using ONLY the information
provided in the CONTEXT.

Rules:

1. Use only the provided context.
2. Do not use outside knowledge.
3. Do not invent facts.
4. Do not guess.
5. If the answer is not present in the context,
   say:

   I don't know based on the provided context.

6. Keep the answer concise.
"""


# ============================================================
# 9. RAG
# ============================================================

def generate_with_rag(query):

    retrieved_docs = retrieve_top_k(
        query,
        k=3
    )

    context = format_context(
        retrieved_docs
    )

    user_prompt = f"""
CONTEXT
=======

{context}

QUESTION
========

{query}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": RAG_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return {
        "answer": response.choices[0].message.content,
        "retrieved": retrieved_docs,
        "context": context
    }


# ============================================================
# 10. RETRIEVAL TEST
# ============================================================

print("\n" + "=" * 70)
print("RETRIEVAL TEST")
print("=" * 70)

query = "Who led the NovaMind project?"

results = retrieve_top_k(query)

print("QUERY:", query)

for item in results:

    print(f"\nID: {item['id']}")
    print(f"Distance: {item['distance']:.4f}")
    print(f"Text: {item['text']}")


# ============================================================
# 11. FIVE TEST QUERIES
# ============================================================

TEST_QUERIES = [
    "Where is NovaTech Solutions headquartered?",
    "Who led the NovaMind project?",
    "When was NovaMind launched?",
    "What is the name of NovaTech's internal documentation platform?",
    "How long does the AI Launchpad training program last?"
]


# ============================================================
# 12. RETRIEVAL ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("RETRIEVAL ANALYSIS")
print("=" * 70)

for question in TEST_QUERIES:

    results = retrieve_top_k(
        question,
        k=3
    )

    print("\nQuestion:")
    print(question)

    print("Retrieved:")

    for item in results:

        print(
            f"  {item['id']} "
            f"(distance={item['distance']:.4f})"
        )


# ============================================================
# 13. FAILURE TRACE FUNCTION
# ============================================================

def trace_retrieval(
    query,
    expected_doc_id
):

    results = retrieve_top_k(
        query,
        k=3
    )

    retrieved_ids = [
        item["id"]
        for item in results
    ]

    print("\n" + "=" * 70)
    print("FAILURE TRACE")
    print("=" * 70)

    print("Question:", query)

    print(
        "Expected document:",
        expected_doc_id
    )

    print(
        "Retrieved documents:",
        retrieved_ids
    )

    if expected_doc_id in retrieved_ids:

        print("\nRESULT: Retrieval SUCCESS")

        print(
            "The relevant chunk was retrieved."
        )

        print(
            "If the final answer is wrong, "
            "the problem is likely generation drift."
        )

    else:

        print("\nRESULT: RETRIEVAL FAILURE")

        print(
            "The relevant chunk was NOT "
            "in the top 3."
        )

        print(
            "This is a retrieval problem."
        )

    print("\nRetrieved chunks:")

    for item in results:

        print(
            f"\n{item['id']} "
            f"(distance={item['distance']:.4f})"
        )

        print(item["text"])


# ============================================================
# 14. TWO FAILURE TRACE EXPERIMENTS
# ============================================================

trace_retrieval(
    "Who is responsible for NovaMind?",
    "doc-005"
)

trace_retrieval(
    "Which program teaches employees about embeddings and RAG?",
    "doc-008"
)


# ============================================================
# 15. OPENAI GENERATION TEST
# ============================================================

print("\n" + "=" * 70)
print("OPENAI GENERATION TEST")
print("=" * 70)

try:

    no_rag = generate_without_rag(
        query
    )

    print("\nNO-RAG ANSWER:")
    print(no_rag)

except Exception as e:

    print("\nNO-RAG ERROR:")
    print(type(e).__name__)
    print(e)


try:

    rag = generate_with_rag(
        query
    )

    print("\nRAG ANSWER:")
    print(rag["answer"])

except Exception as e:

    print("\nRAG ERROR:")
    print(type(e).__name__)
    print(e)


# ============================================================
# 16. FIVE QUERY RAG VS NO-RAG
# ============================================================

rows = []

print("\n" + "=" * 70)
print("FIVE QUERY COMPARISON")
print("=" * 70)

for question in TEST_QUERIES:

    print("\nProcessing:")
    print(question)

    # -------------------------------
    # RAG
    # -------------------------------

    try:

        rag_result = generate_with_rag(
            question
        )

        rag_answer = rag_result["answer"]

    except Exception as e:

        rag_answer = (
            f"API ERROR: "
            f"{type(e).__name__}: {e}"
        )

    # -------------------------------
    # NO RAG
    # -------------------------------

    try:

        no_rag_answer = generate_without_rag(
            question
        )

    except Exception as e:

        no_rag_answer = (
            f"API ERROR: "
            f"{type(e).__name__}: {e}"
        )

    # -------------------------------
    # Retrieval
    # -------------------------------

    retrieved = retrieve_top_k(
        question,
        k=3
    )

    retrieved_ids = ", ".join(
        item["id"]
        for item in retrieved
    )

    # -------------------------------
    # Save
    # -------------------------------

    rows.append({
        "Question": question,
        "RAG Answer": rag_answer,
        "Without RAG Answer": no_rag_answer,
        "Retrieved Chunks": retrieved_ids
    })


# ============================================================
# 17. RESULTS TABLE
# ============================================================

df = pd.DataFrame(rows)

pd.set_option(
    "display.max_colwidth",
    120
)

print("\n" + "=" * 100)
print("RAG vs NO-RAG COMPARISON")
print("=" * 100)

print(
    df.to_string(index=False)
)


# ============================================================
# 18. SAVE CSV
# ============================================================

df.to_csv(
    "rag_results.csv",
    index=False,
    encoding="utf-8"
)

print(
    "\nResults saved to: rag_results.csv"
)


# ============================================================
# 19. ARCHITECTURE
# ============================================================

print("\n" + "=" * 70)
print("RAG ARCHITECTURE")
print("=" * 70)

print("""
                 USER QUERY
                      |
                      v
            Sentence Transformer
                      |
                      v
              Query Embedding
                      |
                      v
              FAISS Similarity
                  Search
                      |
                      v
                 Top 3 Chunks
                      |
                      v
              Context Formatter
                      |
                      v
          Structured RAG Prompt
          +-------------------+
          | CONTEXT           |
          | QUESTION          |
          +-------------------+
                      |
                      v
            OpenAI Chat Model
                      |
                      v
              Grounded Answer
""")


# ============================================================
# 20. COMPLETE
# ============================================================

print("\n" + "=" * 70)
print("DAY 15 RAG PIPELINE COMPLETED")
print("=" * 70)