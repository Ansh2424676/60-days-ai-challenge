from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter


PROCESSED_DIR = Path("data/processed")


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)


def create_chunks():

    all_chunks = []

    for file_path in PROCESSED_DIR.glob("*.txt"):

        text = file_path.read_text(
            encoding="utf-8"
        )

        chunks = text_splitter.split_text(text)

        for index, chunk in enumerate(chunks):

            all_chunks.append({
                "source": file_path.name,
                "chunk_index": index,
                "text": chunk
            })

    return all_chunks


if __name__ == "__main__":

    chunks = create_chunks()

    print("=" * 60)
    print("CHUNKING RESULTS")
    print("=" * 60)

    print(f"Total chunks: {len(chunks)}")

    if chunks:

        total_characters = sum(
            len(chunk["text"])
            for chunk in chunks
        )

        average_size = (
            total_characters / len(chunks)
        )

        print(
            f"Average chunk size: "
            f"{average_size:.2f} characters"
        )

        print("\nSample chunk:")
        print("-" * 60)
        print(chunks[0]["text"])
        print("-" * 60)

    print("=" * 60)