import os
import pickle
import time
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from chunker import create_chunks


load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in .env file")


VECTORSTORE_DIR = Path("vectorstore")
VECTORSTORE_DIR.mkdir(exist_ok=True)


def build_faiss_index():

    start_time = time.time()

    print("=" * 60)
    print("BUILDING FAISS KNOWLEDGE BASE")
    print("=" * 60)

    # Load chunks
    chunks = create_chunks()

    print(f"Total chunks: {len(chunks)}")

    if not chunks:
        raise ValueError("No chunks found.")

    # Prepare texts
    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    # Prepare metadata
    metadatas = [
        {
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"],
            "document_type": "txt"
        }
        for chunk in chunks
    ]

    # OpenAI embedding model
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    print("Generating embeddings...")

    # Build FAISS
    vectorstore = FAISS.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas
    )

    # Save index
    vectorstore.save_local(
        str(VECTORSTORE_DIR)
    )

    # Save chunk metadata
    with open(
        VECTORSTORE_DIR / "chunks.pkl",
        "wb"
    ) as file:

        pickle.dump(
            chunks,
            file
        )

    elapsed_time = time.time() - start_time

    total_characters = sum(
        len(chunk["text"])
        for chunk in chunks
    )

    average_chunk_size = (
        total_characters / len(chunks)
    )

    print("\n" + "=" * 60)
    print("INGESTION COMPLETE")
    print("=" * 60)

    print(
        f"Total documents: "
        f"{len(set(chunk['source'] for chunk in chunks))}"
    )

    print(
        f"Total chunks: "
        f"{len(chunks)}"
    )

    print(
        f"Average chunk size: "
        f"{average_chunk_size:.2f} characters"
    )

    print(
        f"Total ingestion time: "
        f"{elapsed_time:.2f} seconds"
    )

    print(
        f"Index location: "
        f"{VECTORSTORE_DIR}"
    )

    print("=" * 60)


if __name__ == "__main__":
    build_faiss_index()