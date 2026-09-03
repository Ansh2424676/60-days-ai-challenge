import sys
from pathlib import Path
from typing import List, Tuple

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# REUSE DAY 10 NLP MODULES
# ============================================================

DAY10_PATH = (
    Path(__file__).resolve().parent.parent
    / "Day-10-NLP-Pipeline"
)

sys.path.insert(0, str(DAY10_PATH))

from nlp_pipeline import PreprocessingModule, VectorizerModule


# ============================================================
# KNOWLEDGE BASE
# ============================================================

KNOWLEDGE_BASE = [
    "Machine learning algorithms learn patterns from data and make predictions.",
    "Supervised learning trains models using labelled training examples.",
    "Unsupervised learning discovers hidden patterns in data without labels.",
    "Deep learning uses neural networks with multiple layers to learn complex patterns.",
    "Natural language processing enables computers to understand and process human language.",
    "Text classification assigns documents or messages to predefined categories.",
    "Sentiment analysis identifies whether text expresses positive negative or neutral opinions.",
    "Computer vision enables machines to analyze and understand images and videos.",
    "Python is widely used for machine learning data science and artificial intelligence.",
    "SQL is a language used to query and manage structured databases.",
    "Data science combines statistics programming and machine learning to extract insights from data.",
    "Artificial intelligence allows computer systems to perform tasks that normally require human intelligence.",
    "Neural networks are computing models inspired by interconnected neurons in the human brain.",
    "Cloud computing provides computing storage and software resources over the internet.",
    "Cybersecurity protects systems networks applications and data from unauthorized access and attacks.",
    "Encryption converts readable information into encoded data to protect sensitive information.",
    "Authentication verifies the identity of a user before granting access to a system.",
    "Recommendation systems suggest products movies music or other content based on user behavior.",
    "Big data technologies process very large and complex datasets efficiently.",
    "Information retrieval finds and ranks relevant documents in response to a user query.",
    "Search engines use information retrieval techniques to find relevant web pages for user queries.",
    "Database indexing improves the speed of searching and retrieving records from databases.",
]


# ============================================================
# RETRIEVAL CONFIGURATION
# ============================================================

RELEVANCE_THRESHOLD = 0.10
DEFAULT_TOP_K = 3


# ============================================================
# INITIALIZE NLP MODULES
# ============================================================

preprocessor = PreprocessingModule()
vectorizer = VectorizerModule()


# ============================================================
# PREPROCESS KNOWLEDGE BASE
# ============================================================

processed_documents = [
    preprocessor.transform(document)
    for document in KNOWLEDGE_BASE
]


# ============================================================
# CREATE AND STORE TF-IDF MATRIX
# ============================================================

vectorizer.fit(processed_documents)

# Stored TF-IDF matrix for the complete knowledge base
corpus_matrix = vectorizer.corpus_vectors


# ============================================================
# RETRIEVAL FUNCTION
# ============================================================

def retrieve(
    query: str,
    corpus_matrix,
    top_k: int = DEFAULT_TOP_K
) -> List[Tuple[int, float, str]]:
    """
    Retrieve the most relevant documents for a query.

    Args:
        query (str):
            User's search query.

        corpus_matrix:
            TF-IDF matrix containing vectors for the
            knowledge-base documents.

        top_k (int):
            Number of top results to return.

    Returns:
        List of tuples:
            (document_index, similarity_score, document)

        If the highest similarity score is below 0.10,
        an empty list is returned.

    Raises:
        ValueError:
            If the query is empty, invalid, or top_k is invalid.
    """

    if not isinstance(query, str):
        raise TypeError("Query must be a string.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    # Preprocess query using Day 10 preprocessing module
    processed_query = preprocessor.transform(query)

    # Convert query into TF-IDF vector
    query_vector = vectorizer.vectorizer.transform(
        [processed_query]
    )

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(
        query_vector,
        corpus_matrix
    )[0]

    # Find highest similarity
    highest_score = float(np.max(similarity_scores))

    # Relevance threshold
    if highest_score < RELEVANCE_THRESHOLD:
        return []

    # Sort documents by similarity score
    ranked_indices = np.argsort(
        similarity_scores
    )[::-1]

    results = []

    for index in ranked_indices[:top_k]:

        score = float(similarity_scores[index])

        results.append(
            (
                int(index),
                score,
                KNOWLEDGE_BASE[index]
            )
        )

    return results


# ============================================================
# DISPLAY RETRIEVAL RESULTS
# ============================================================

def display_results(query: str):
    """
    Display retrieval results for a query.
    """

    print("\n" + "=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    try:
        results = retrieve(
            query,
            corpus_matrix,
            top_k=3
        )

        if not results:
            print("No relevant document found")
            return

        for rank, (index, score, document) in enumerate(
            results,
            start=1
        ):
            print(
                f"{rank}. "
                f"Score: {score:.4f} | "
                f"Document {index + 1}: {document}"
            )

    except (ValueError, TypeError) as error:
        print(f"Query error: {error}")


# ============================================================
# TEN QUERY TESTS
# ============================================================

TEST_QUERIES = [
    {
        "query": "how do machines learn from examples?",
        "type": "Normal",
        "expected": "Supervised learning"
    },
    {
        "query": "understanding human language with computers",
        "type": "Normal",
        "expected": "Natural language processing"
    },
    {
        "query": "protecting networks from hackers",
        "type": "Normal",
        "expected": "Cybersecurity"
    },
    {
        "query": "finding relevant documents from a search",
        "type": "Normal",
        "expected": "Information retrieval"
    },
    {
        "query": "Python",
        "type": "Ambiguous",
        "expected": "Python programming"
    },
    {
        "query": "data",
        "type": "Ambiguous",
        "expected": "Data science"
    },
    {
        "query": "machine intelligence",
        "type": "Ambiguous",
        "expected": "Artificial intelligence"
    },
    {
        "query": "best pizza recipe for dinner",
        "type": "Out-of-domain",
        "expected": "No relevant document"
    },
    {
        "query": "latest football match score",
        "type": "Out-of-domain",
        "expected": "No relevant document"
    },
    {
        "query": "encrypting sensitive information",
        "type": "Normal",
        "expected": "Encryption"
    },
]


# ============================================================
# FAILURE ANALYSIS
# ============================================================

def analyse_failure(query_data, results):
    """
    Provide a one-sentence diagnosis for retrieval failures.
    """

    query = query_data["query"]
    query_type = query_data["type"]

    if not results:
        if query_type == "Out-of-domain":
            return (
                "Correct threshold rejection: the query is outside "
                "the knowledge-base vocabulary."
            )

        return (
            "The query produced no relevant result because its "
            "important vocabulary did not sufficiently overlap "
            "with the document vocabulary."
        )

    top_document = results[0][2].lower()

    expected = query_data["expected"].lower()

    # Simple expected-topic check
    expected_keywords = expected.split()

    if any(keyword in top_document for keyword in expected_keywords):
        return "No retrieval failure detected."

    if query_type == "Ambiguous":
        return (
            "The query is ambiguous, so keyword overlap caused "
            "a document from a related but unintended topic to rank first."
        )

    return (
        "The top result is incorrect because TF-IDF relies on "
        "lexical word overlap rather than semantic meaning."
    )


# ============================================================
# RUN ALL TEN TESTS
# ============================================================

def run_tests():
    """
    Run all ten retrieval queries and print results.
    """

    print("\n")
    print("#" * 80)
    print("DAY 11 - DOCUMENT RETRIEVAL SYSTEM")
    print("#" * 80)

    print(f"\nKnowledge base size: {len(KNOWLEDGE_BASE)} documents")

    print(
        f"TF-IDF matrix shape: {corpus_matrix.shape}"
    )

    print(
        f"Relevance threshold: {RELEVANCE_THRESHOLD}"
    )

    for number, query_data in enumerate(
        TEST_QUERIES,
        start=1
    ):

        query = query_data["query"]

        print("\n" + "-" * 80)
        print(f"TEST {number}/10")
        print(f"Type: {query_data['type']}")
        print(f"Query: {query}")
        print(f"Expected: {query_data['expected']}")
        print("-" * 80)

        try:
            results = retrieve(
                query,
                corpus_matrix,
                top_k=3
            )

            if not results:
                print(
                    "Result: No relevant document found"
                )

            else:
                for rank, (
                    index,
                    score,
                    document
                ) in enumerate(results, start=1):

                    print(
                        f"{rank}. "
                        f"Score: {score:.4f} | "
                        f"Document {index + 1}: {document}"
                    )

            diagnosis = analyse_failure(
                query_data,
                results
            )

            print(
                f"\nFailure analysis: {diagnosis}"
            )

        except (ValueError, TypeError) as error:
            print(f"Error: {error}")


# ============================================================
# THRESHOLD TEST
# ============================================================

def test_threshold():
    """
    Explicitly test the 0.10 relevance threshold.
    """

    print("\n")
    print("#" * 80)
    print("RELEVANCE THRESHOLD TEST")
    print("#" * 80)

    query = "ancient ocean dinosaur recipe"

    print(f"\nQuery: {query}")
    print(f"Threshold: {RELEVANCE_THRESHOLD}")

    try:
        results = retrieve(
            query,
            corpus_matrix,
            top_k=3
        )

        if not results:
            print(
                "PASS: No relevant document found"
            )
        else:
            print(
                "Unexpected relevant result:"
            )

            for result in results:
                print(result)

    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


# ============================================================
# VOCABULARY MISMATCH DEMONSTRATION
# ============================================================

def vocabulary_mismatch_demo():
    """
    Demonstrate a limitation of TF-IDF:
    synonyms may have little or no lexical overlap.
    """

    print("\n")
    print("#" * 80)
    print("VOCABULARY MISMATCH DEMONSTRATION")
    print("#" * 80)

    query = "protecting computers from intruders"

    print(f"\nSynonym-style query: {query}")

    try:
        results = retrieve(
            query,
            corpus_matrix,
            top_k=3
        )

        if not results:
            print(
                "No relevant document found."
            )
            print(
                "Diagnosis: TF-IDF cannot reliably connect "
                "'intruders' with terms such as 'attacks' "
                "or 'unauthorized access'."
            )

        else:
            for rank, (
                index,
                score,
                document
            ) in enumerate(results, start=1):

                print(
                    f"{rank}. "
                    f"Score: {score:.4f} | "
                    f"Document {index + 1}: {document}"
                )

    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    run_tests()

    test_threshold()

    vocabulary_mismatch_demo()
