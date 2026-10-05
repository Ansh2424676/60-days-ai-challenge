import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


load_dotenv()


VECTORSTORE_DIR = "vectorstore"


def load_vectorstore():

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vectorstore = FAISS.load_local(
        VECTORSTORE_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


def search(query, k=3):

    vectorstore = load_vectorstore()

    results = vectorstore.similarity_search_with_score(
        query,
        k=k
    )

    return results


if __name__ == "__main__":

    queries = [
        "What is Retrieval Augmented Generation?",
        "How does semantic search work?",
        "How should documents be chunked for RAG?",
        "How does FAISS perform vector search?",
        "What is prompt injection?",
        "How can Redis improve AI application performance?",
        "How can FastAPI stream AI responses?",
        "What metrics should be used to evaluate an LLM application?",
        "How can AI application latency be reduced?",
        "How can embedding costs be optimized?"
    ]

    print("=" * 70)
    print("DAY 43 RETRIEVAL EVALUATION")
    print("=" * 70)

    for number, query in enumerate(queries, start=1):

        print(f"\nQUERY {number}")
        print("-" * 70)
        print(query)

        results = search(query, k=3)

        for rank, (document, score) in enumerate(
            results,
            start=1
        ):

            print(f"\nRank {rank}")
            print(f"Score: {score:.4f}")
            print(
                f"Source: "
                f"{document.metadata.get('source')}"
            )

            print(
                "Content:"
            )

            print(
                document.page_content[:500]
            )

    print("\n" + "=" * 70)