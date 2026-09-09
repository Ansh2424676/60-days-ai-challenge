"""
Day 17 - Improve RAG Precision with Metadata Filtering

Features:
- Loads metadata-enriched knowledge base
- Creates LangChain Documents with metadata
- Uses local HuggingFace embeddings
- Builds FAISS vector store
- Supports metadata filtering
- Supports category filtering
- Supports date cutoff filtering
- Handles missing metadata safely
- Compares filtered vs unfiltered retrieval
"""

import json
from datetime import datetime
from pathlib import Path

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
KB_PATH = BASE_DIR / "knowledge_base.json"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

DEFAULT_K = 3


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

def load_knowledge_base():
    """Load knowledge base JSON file."""

    if not KB_PATH.exists():
        raise FileNotFoundError(
            f"Knowledge base not found: {KB_PATH}"
        )

    with open(KB_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(
            "knowledge_base.json must contain a JSON list."
        )

    print(f"Loaded documents: {len(data)}")

    return data


# ============================================================
# CREATE LANGCHAIN DOCUMENTS
# ============================================================

def create_documents(data):
    """
    Convert knowledge base records into LangChain Documents.

    Metadata:
    - id
    - source
    - category
    - date
    - document_type
    """

    documents = []

    for item in data:

        if "id" not in item:
            print("WARNING: Document missing id. Skipping.")
            continue

        if "text" not in item:
            print(
                f"WARNING: {item['id']} missing text. Skipping."
            )
            continue

        metadata = item.get("metadata", {})

        document = Document(
            page_content=item["text"],
            metadata={
                "id": item["id"],
                "source": metadata.get("source"),
                "category": metadata.get("category"),
                "date": metadata.get("date"),
                "document_type": metadata.get("document_type"),
            },
        )

        documents.append(document)

    print(f"Created LangChain Documents: {len(documents)}")

    return documents


# ============================================================
# METADATA VALIDATION
# ============================================================

def validate_metadata(documents):
    """Validate required metadata fields."""

    print("\n" + "=" * 70)
    print("METADATA VALIDATION")
    print("=" * 70)

    required_fields = [
        "source",
        "category",
        "date",
        "document_type",
    ]

    print(f"Total documents: {len(documents)}")

    valid_count = 0

    for document in documents:

        doc_id = document.metadata.get("id", "unknown")

        missing = [
            field
            for field in required_fields
            if not document.metadata.get(field)
        ]

        if missing:

            print(
                f"WARNING: {doc_id} missing {missing}"
            )

        else:

            print(
                f"OK: {doc_id} | "
                f"{document.metadata['category']} | "
                f"{document.metadata['date']} | "
                f"{document.metadata['document_type']}"
            )

            valid_count += 1

    print(
        f"\nMetadata validation: "
        f"{valid_count}/{len(documents)} documents valid"
    )

    return valid_count == len(documents)


# ============================================================
# CREATE FAISS VECTOR STORE
# ============================================================

def create_vector_store(documents):
    """
    Create FAISS vector store using local HuggingFace embeddings.

    No OpenAI API is required for embeddings.
    """

    print("\nCreating FAISS vector store with local embeddings...")

    print(
        f"Embedding model: {EMBEDDING_MODEL}"
    )

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vector_store = FAISS.from_documents(
        documents,
        embeddings
    )

    print("FAISS vector store created successfully.")

    return vector_store


# ============================================================
# NORMAL RETRIEVAL
# ============================================================

def retrieve(vector_store, query, k=DEFAULT_K):
    """Perform normal similarity retrieval."""

    return vector_store.similarity_search(
        query,
        k=k
    )


# ============================================================
# METADATA FILTER MATCHING
# ============================================================

def matches_filters(document, filters):
    """
    Check whether a document matches supplied metadata filters.

    Supported filters:

    category
    source
    document_type
    date_after

    Example:

    {
        "category": "ai",
        "date_after": "2025-12-31"
    }
    """

    if not filters:
        return True

    metadata = document.metadata

    # --------------------------------------------------------
    # Category filter
    # --------------------------------------------------------

    if "category" in filters:

        expected_category = filters["category"]

        actual_category = metadata.get("category")

        if actual_category != expected_category:
            return False

    # --------------------------------------------------------
    # Source filter
    # --------------------------------------------------------

    if "source" in filters:

        expected_source = filters["source"]

        actual_source = metadata.get("source")

        if actual_source != expected_source:
            return False

    # --------------------------------------------------------
    # Document type filter
    # --------------------------------------------------------

    if "document_type" in filters:

        expected_type = filters["document_type"]

        actual_type = metadata.get("document_type")

        if actual_type != expected_type:
            return False

    # --------------------------------------------------------
    # Date cutoff filter
    # --------------------------------------------------------

    if "date_after" in filters:

        cutoff_string = filters["date_after"]

        document_date_string = metadata.get("date")

        # Missing date cannot pass a date filter
        if not document_date_string:
            return False

        try:

            cutoff_date = datetime.strptime(
                cutoff_string,
                "%Y-%m-%d"
            ).date()

            document_date = datetime.strptime(
                document_date_string,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            print(
                f"WARNING: Invalid date format. "
                f"Expected YYYY-MM-DD."
            )

            return False

        # Only documents strictly newer than cutoff
        if document_date <= cutoff_date:
            return False

    return True


# ============================================================
# FILTERED RETRIEVAL
# ============================================================

def filtered_retrieve(
    vector_store,
    query,
    filters=None,
    k=DEFAULT_K,
):
    """
    Retrieve documents using semantic similarity
    followed by metadata filtering.

    The vector search first finds candidates.
    Metadata filters then remove irrelevant candidates.
    """

    if filters is None:
        filters = {}

    # Search more candidates because some may
    # be removed by metadata filtering.
    fetch_k = max(k * 4, 10)

    candidates = vector_store.similarity_search(
        query,
        k=fetch_k
    )

    filtered_results = []

    for document in candidates:

        if matches_filters(
            document,
            filters
        ):

            filtered_results.append(document)

        if len(filtered_results) >= k:
            break

    return filtered_results


# ============================================================
# PRINT RETRIEVAL RESULTS
# ============================================================

def print_results(
    title,
    results
):
    """Print retrieved documents."""

    print("\n" + "-" * 70)
    print(title)
    print("-" * 70)

    if not results:

        print("No documents retrieved.")
        return

    for index, document in enumerate(
        results,
        start=1
    ):

        metadata = document.metadata

        print(
            f"\n[{index}] "
            f"{metadata.get('id')}"
        )

        print(
            f"Category: "
            f"{metadata.get('category')}"
        )

        print(
            f"Source: "
            f"{metadata.get('source')}"
        )

        print(
            f"Date: "
            f"{metadata.get('date')}"
        )

        print(
            f"Document Type: "
            f"{metadata.get('document_type')}"
        )

        print(
            f"Text: "
            f"{document.page_content}"
        )


# ============================================================
# PRECISION CALCULATION
# ============================================================

def calculate_precision(
    results,
    relevant_ids
):
    """
    Calculate Precision@K.

    Precision =
    relevant retrieved documents /
    total retrieved documents
    """

    if not results:
        return 0.0

    retrieved_ids = [
        document.metadata.get("id")
        for document in results
    ]

    relevant_count = sum(
        1
        for doc_id in retrieved_ids
        if doc_id in relevant_ids
    )

    return relevant_count / len(results)


# ============================================================
# FIVE QUERY EVALUATION
# ============================================================

def run_evaluation(vector_store):
    """
    Run five queries with and without metadata filters.

    Precision is calculated against manually defined
    relevant document IDs.
    """

    test_cases = [

        {
            "query": "When was NovaMind launched?",
            "filters": {
                "category": "ai",
                "date_after": "2025-12-31",
            },
            "relevant_ids": {"doc-003"},
        },

        {
            "query": (
                "What is NovaMind designed to help "
                "employees with?"
            ),
            "filters": {
                "category": "ai",
                "document_type": "technical_reference",
            },
            "relevant_ids": {"doc-004"},
        },

        {
            "query": "What does AtlasHub contain?",
            "filters": {
                "category": "engineering",
                "document_type": "technical_reference",
                "date_after": "2024-12-31",
            },
            "relevant_ids": {"doc-007"},
        },

        {
            "query": "What is AI Launchpad?",
            "filters": {
                "category": "training",
            },
            "relevant_ids": {
                "doc-008",
                "doc-009",
            },
        },

        {
            "query": (
                "When is the weekly technical "
                "review meeting?"
            ),
            "filters": {
                "category": "engineering",
                "date_after": "2025-12-31",
            },
            "relevant_ids": {"doc-010"},
        },
    ]

    print("\n")
    print("=" * 70)
    print("FIVE-QUERY PRECISION EVALUATION")
    print("=" * 70)

    evaluation_results = []

    for index, test in enumerate(
        test_cases,
        start=1
    ):

        query = test["query"]
        filters = test["filters"]
        relevant_ids = test["relevant_ids"]

        # ----------------------------------------------------
        # Unfiltered
        # ----------------------------------------------------

        unfiltered_results = retrieve(
            vector_store,
            query,
            k=DEFAULT_K
        )

        unfiltered_precision = calculate_precision(
            unfiltered_results,
            relevant_ids
        )

        # ----------------------------------------------------
        # Filtered
        # ----------------------------------------------------

        filtered_results = filtered_retrieve(
            vector_store,
            query,
            filters,
            k=DEFAULT_K
        )

        filtered_precision = calculate_precision(
            filtered_results,
            relevant_ids
        )

        improvement = (
            filtered_precision -
            unfiltered_precision
        )

        print("\n" + "-" * 70)

        print(
            f"Query {index}: {query}"
        )

        print(
            f"Filters: {filters}"
        )

        print(
            f"Expected relevant IDs: "
            f"{sorted(relevant_ids)}"
        )

        print(
            "\nUnfiltered results:"
        )

        for document in unfiltered_results:

            print(
                f"  - "
                f"{document.metadata.get('id')}"
            )

        print(
            f"Unfiltered Precision@{DEFAULT_K}: "
            f"{unfiltered_precision:.2f}"
        )

        print(
            "\nFiltered results:"
        )

        for document in filtered_results:

            print(
                f"  - "
                f"{document.metadata.get('id')}"
            )

        print(
            f"Filtered Precision@{DEFAULT_K}: "
            f"{filtered_precision:.2f}"
        )

        print(
            f"Improvement: "
            f"{improvement:+.2f}"
        )

        evaluation_results.append(
            {
                "query": query,
                "filters": filters,
                "unfiltered_precision": (
                    unfiltered_precision
                ),
                "filtered_precision": (
                    filtered_precision
                ),
                "improvement": improvement,
                "unfiltered_ids": [
                    d.metadata.get("id")
                    for d in unfiltered_results
                ],
                "filtered_ids": [
                    d.metadata.get("id")
                    for d in filtered_results
                ],
            }
        )

    # --------------------------------------------------------
    # Average precision
    # --------------------------------------------------------

    if evaluation_results:

        avg_unfiltered = sum(
            item["unfiltered_precision"]
            for item in evaluation_results
        ) / len(evaluation_results)

        avg_filtered = sum(
            item["filtered_precision"]
            for item in evaluation_results
        ) / len(evaluation_results)

        avg_improvement = (
            avg_filtered -
            avg_unfiltered
        )

        print("\n")
        print("=" * 70)
        print("PRECISION SUMMARY")
        print("=" * 70)

        print(
            f"Average Unfiltered Precision: "
            f"{avg_unfiltered:.2f}"
        )

        print(
            f"Average Filtered Precision:   "
            f"{avg_filtered:.2f}"
        )

        print(
            f"Average Improvement:           "
            f"{avg_improvement:+.2f}"
        )

    return evaluation_results


# ============================================================
# EDGE CASE TESTS
# ============================================================

def test_edge_cases(documents):
    """
    Test metadata filtering edge cases.

    Edge cases:
    1. Missing metadata
    2. Conflicting categories
    """

    print("\n")
    print("=" * 70)
    print("EDGE CASE TESTS")
    print("=" * 70)

    # --------------------------------------------------------
    # Edge Case 1: Missing metadata
    # --------------------------------------------------------

    print("\n1. Missing metadata")

    test_document = Document(
        page_content="Example document",
        metadata={
            "id": "test-missing",
            "category": "ai",
            "source": None,
            "date": None,
            "document_type": None,
        },
    )

    result = matches_filters(
        test_document,
        {
            "category": "ai",
            "date_after": "2025-01-01",
        },
    )

    print(
        f"Document with missing date "
        f"passes date filter: {result}"
    )

    print(
        "Expected: False"
    )

    # --------------------------------------------------------
    # Edge Case 2: Conflicting category
    # --------------------------------------------------------

    print("\n2. Conflicting category")

    conflicting_document = Document(
        page_content="Example document",
        metadata={
            "id": "test-conflict",
            "category": "training",
            "source": "example.pdf",
            "date": "2026-01-01",
            "document_type": "technical_reference",
        },
    )

    result = matches_filters(
        conflicting_document,
        {
            "category": "ai",
        },
    )

    print(
        f"Training document with AI filter passes: "
        f"{result}"
    )

    print(
        "Expected: False"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("DAY 17 - METADATA FILTERING RAG")
    print("=" * 70)

    # --------------------------------------------------------
    # Load data
    # --------------------------------------------------------

    data = load_knowledge_base()

    # --------------------------------------------------------
    # Create LangChain documents
    # --------------------------------------------------------

    documents = create_documents(data)

    # --------------------------------------------------------
    # Validate metadata
    # --------------------------------------------------------

    validate_metadata(documents)

    # --------------------------------------------------------
    # Create FAISS vector store
    # --------------------------------------------------------

    vector_store = create_vector_store(
        documents
    )

    # --------------------------------------------------------
    # Basic retrieval test
    # --------------------------------------------------------

    query = "What is NovaMind?"

    print("\n")
    print("=" * 70)
    print("BASIC RETRIEVAL TEST")
    print("=" * 70)

    results = retrieve(
        vector_store,
        query,
        k=3
    )

    print_results(
        "Normal Similarity Search",
        results
    )

    # --------------------------------------------------------
    # Category filter test
    # --------------------------------------------------------

    filtered_results = filtered_retrieve(
        vector_store,
        query,
        filters={
            "category": "ai"
        },
        k=3
    )

    print_results(
        "Category Filter: ai",
        filtered_results
    )

    # --------------------------------------------------------
    # Category + date filter test
    # --------------------------------------------------------

    filtered_results = filtered_retrieve(
        vector_store,
        query,
        filters={
            "category": "engineering",
            "date_after": "2024-12-31",
        },
        k=3
    )

    print_results(
        "Engineering + Date Filter",
        filtered_results
    )

    # --------------------------------------------------------
    # Five-query evaluation
    # --------------------------------------------------------

    run_evaluation(
        vector_store
    )

    # --------------------------------------------------------
    # Edge cases
    # --------------------------------------------------------

    test_edge_cases(
        documents
    )

    # --------------------------------------------------------
    # Complete
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("DAY 17 PIPELINE COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()