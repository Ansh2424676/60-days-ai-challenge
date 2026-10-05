from pathlib import Path
import time

from chunker import create_chunks


DOCUMENTS_DIR = Path("data/documents")


def calculate_metrics():

    start = time.time()

    documents = list(
        DOCUMENTS_DIR.glob("*.txt")
    )

    chunks = create_chunks()

    total_characters = sum(
        len(chunk["text"])
        for chunk in chunks
    )

    average_chunk_size = (
        total_characters / len(chunks)
        if chunks
        else 0
    )

    elapsed = time.time() - start

    print("=" * 60)
    print("DAY 43 INGESTION METRICS")
    print("=" * 60)

    print(
        f"Total document count: "
        f"{len(documents)}"
    )

    print(
        f"Total chunk count: "
        f"{len(chunks)}"
    )

    print(
        f"Average chunk size: "
        f"{average_chunk_size:.2f} characters"
    )

    print(
        f"Metric calculation time: "
        f"{elapsed:.4f} seconds"
    )

    print("=" * 60)


if __name__ == "__main__":
    calculate_metrics()