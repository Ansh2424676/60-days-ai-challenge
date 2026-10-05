from pathlib import Path
from datetime import datetime


PROCESSED_DIR = Path("data/processed")


def extract_metadata(file_path: Path):

    text = file_path.read_text(encoding="utf-8")

    lines = text.splitlines()

    title = file_path.stem
    category = "Unknown"

    for line in lines:

        if line.startswith("Title:"):
            title = line.replace("Title:", "").strip()

        if line.startswith("Category:"):
            category = line.replace("Category:", "").strip()

    return {
        "source": file_path.name,
        "title": title,
        "category": category,
        "document_type": file_path.suffix.replace(".", ""),
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }


def build_metadata():

    metadata = []

    for file_path in PROCESSED_DIR.glob("*.txt"):

        document_metadata = extract_metadata(file_path)

        metadata.append(document_metadata)

    return metadata


if __name__ == "__main__":

    documents = build_metadata()

    print("=" * 60)
    print("METADATA")
    print("=" * 60)

    print(f"Total documents: {len(documents)}")

    for document in documents[:5]:

        print("-" * 60)

        for key, value in document.items():
            print(f"{key}: {value}")

    print("=" * 60)