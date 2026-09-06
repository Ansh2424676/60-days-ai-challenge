# Day 14 — Build a Semantic Search Engine

## Objective

Build a semantic search engine using OpenAI embeddings and FAISS,
then compare semantic retrieval with a simple keyword-search baseline.

## Technologies

- Python
- OpenAI `text-embedding-3-small`
- FAISS
- NumPy
- Pandas

## Dataset

The project uses a small technical-document corpus covering:

- Artificial Intelligence and Machine Learning
- Cloud Computing
- Databases
- Software Engineering
- Cybersecurity
- Data Engineering

The corpus contains more than 50 short documents.

## Semantic Search Pipeline

The semantic search pipeline follows these steps:

1. Prepare the document corpus.
2. Generate embeddings using OpenAI `text-embedding-3-small`.
3. Convert embeddings to NumPy `float32`.
4. Store the vectors in a FAISS index.
5. Embed the user's query.
6. Search for the nearest vectors using FAISS.
7. Return the most relevant documents and distances.

## FAISS Index

The implementation uses:

```python
faiss.IndexFlatL2