from pathlib import Path
import re


DOCUMENTS_DIR = Path("data/documents")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def normalize_whitespace(text: str) -> str:
    """
    Replace multiple spaces/newlines with clean spacing.
    """
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def remove_boilerplate(text: str) -> str:
    """
    Remove unnecessary document labels from the content.
    """
    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            cleaned_lines.append("")
            continue

        if line.startswith("Title:"):
            continue

        if line.startswith("Category:"):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def preprocess_text(text: str) -> str:
    """
    Complete preprocessing pipeline.
    """
    text = remove_boilerplate(text)
    text = normalize_whitespace(text)

    return text


def process_documents():

    processed_documents = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):

        raw_text = file_path.read_text(encoding="utf-8")

        cleaned_text = preprocess_text(raw_text)

        output_path = PROCESSED_DIR / file_path.name

        output_path.write_text(
            cleaned_text,
            encoding="utf-8"
        )

        processed_documents.append({
            "source": file_path.name,
            "text": cleaned_text,
            "characters": len(cleaned_text)
        })

    return processed_documents


if __name__ == "__main__":

    documents = process_documents()

    print("=" * 60)
    print("DOCUMENT PREPROCESSING")
    print("=" * 60)

    print(f"Documents processed: {len(documents)}")

    total_chars = sum(
        document["characters"]
        for document in documents
    )

    print(f"Total characters: {total_chars}")

    if documents:
        average_chars = total_chars / len(documents)
        print(f"Average characters/document: {average_chars:.2f}")

    print("=" * 60)