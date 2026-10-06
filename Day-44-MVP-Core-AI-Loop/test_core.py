from core_ai import core_ai_loop


QUERIES = [
    "What is the difference between RAG and fine-tuning, and when should each be used?",
    "How do FAISS and embeddings work together in a RAG system?",
    "What are the main differences between FastAPI and Flask for building AI APIs?",
    "Why do RAG systems hallucinate and what techniques can reduce hallucinations?",
    "How should chunk size and chunk overlap be selected for a RAG system?",
    "How can Redis caching improve the performance of an AI application?",
    "What are prompt injection attacks and how can an AI application defend against them?",
    "What is the difference between semantic search, keyword search, and hybrid search?",
    "How should a customer-support RAG system be evaluated for quality?",
    "How should an AI research system handle conflicting information from different sources?"
]


if __name__ == "__main__":

    for i, question in enumerate(QUERIES, start=1):

        print("\n" + "=" * 80)
        print(f"QUERY {i}")
        print("=" * 80)

        print("Question:")
        print(question)

        try:
            result = core_ai_loop(question)

            print("\nAnswer:")
            print(result["answer"])

            print("\nSources:")
            if result["sources"]:
                for source in result["sources"]:
                    print(f"- {source}")
            else:
                print("No sources returned.")

        except Exception as e:
            print("\nERROR:")
            print(str(e))
            from core_ai import core_ai_loop


QUERIES = [
    "What is the difference between RAG and fine-tuning, and when should each be used?",
    "How do FAISS and embeddings work together in a RAG system?",
    "What are the main differences between FastAPI and Flask for building AI APIs?",
    "Why do RAG systems hallucinate and what techniques can reduce hallucinations?",
    "How should chunk size and chunk overlap be selected for a RAG system?",
    "How can Redis caching improve the performance of an AI application?",
    "What are prompt injection attacks and how can an AI application defend against them?",
    "What is the difference between semantic search, keyword search, and hybrid search?",
    "How should a customer-support RAG system be evaluated for quality?",
    "How should an AI research system handle conflicting information from different sources?"
]


for i, question in enumerate(QUERIES, 1):

    print("\n" + "=" * 80)
    print(f"QUERY {i}")
    print("=" * 80)

    print(question)

    try:
        result = core_ai_loop(question)

        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCES:")
        if result["sources"]:
            for source in result["sources"]:
                print("-", source)
        else:
            print("No sources returned.")

    except Exception as e:
        print("\nERROR:")
        print(e)