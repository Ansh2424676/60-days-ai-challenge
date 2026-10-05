import os
import time
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()


VECTORSTORE_DIR = Path("vectorstore")
NEW_DOCUMENTS_DIR = Path("data/new_documents")


def load_existing_index():

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vectorstore = FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


def preprocess(text):

    text = text.replace("\r\n", "\n")
    text = text.strip()

    return text


def create_chunks(text):

    splitter = RecursiveCharacterTextSplitter(
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

    return splitter.split_text(text)


def incremental_update(new_docs):

    start_time = time.time()

    vectorstore = load_existing_index()

    documents = []

    for file_path in new_docs:

        print(f"Processing: {file_path.name}")

        raw_text = file_path.read_text(
            encoding="utf-8"
        )

        cleaned_text = preprocess(raw_text)

        chunks = create_chunks(cleaned_text)

        for index, chunk in enumerate(chunks):

            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source": file_path.name,
                        "chunk_index": index,
                        "document_type": "txt",
                        "update_type": "incremental"
                    }
                )
            )

    if not documents:

        print("No new documents found.")

        return

    print(
        f"New chunks to add: "
        f"{len(documents)}"
    )

    vectorstore.add_documents(
        documents
    )

    vectorstore.save_local(
        str(VECTORSTORE_DIR)
    )

    elapsed = time.time() - start_time

    print("=" * 60)
    print("INCREMENTAL UPDATE COMPLETE")
    print("=" * 60)

    print(
        f"New documents: "
        f"{len(new_docs)}"
    )

    print(
        f"New chunks: "
        f"{len(documents)}"
    )

    print(
        f"Update time: "
        f"{elapsed:.2f} seconds"
    )

    print(
        "Existing FAISS index was updated "
        "without rebuilding it."
    )

    print("=" * 60)


if __name__ == "__main__":

    NEW_DOCUMENTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    new_files = list(
        NEW_DOCUMENTS_DIR.glob("*.txt")
    )

    print(
        f"New documents detected: "
        f"{len(new_files)}"
    )

    incremental_update(
        new_files
    )