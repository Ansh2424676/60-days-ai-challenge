from pathlib import Path


DOCUMENTS_DIR = Path("data/documents")
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)


documents = [
    {
        "title": "Retrieval Augmented Generation",
        "category": "RAG",
        "content": """
Retrieval Augmented Generation combines information retrieval with large language models.
A RAG system retrieves relevant information from an external knowledge base before generating
an answer. The main stages are ingestion, preprocessing, chunking, embedding generation,
vector indexing, retrieval, prompt construction, and answer generation.
"""
    },
    {
        "title": "RAG Retrieval Pipeline",
        "category": "RAG",
        "content": """
A RAG retrieval pipeline converts a user query into an embedding and compares it with
document embeddings stored in a vector index. The most similar chunks are returned as
context for the language model.
"""
    },
    {
        "title": "RAG Hallucination Reduction",
        "category": "RAG",
        "content": """
RAG can reduce hallucination by providing external evidence to the language model.
However, retrieval quality directly affects answer quality. Incorrect retrieved context
can cause the model to generate incorrect answers.
"""
    },
    {
        "title": "Chunking Strategies for RAG",
        "category": "RAG",
        "content": """
Document chunking divides large documents into smaller pieces that can be embedded and
retrieved independently. Chunk size should preserve enough context while remaining
specific enough for accurate retrieval.
"""
    },
    {
        "title": "Semantic Search",
        "category": "RAG",
        "content": """
Semantic search retrieves documents based on meaning rather than exact keyword matches.
Embedding models represent text as vectors, allowing similar concepts to be identified
even when different words are used.
"""
    },
    {
        "title": "RAG Context Window",
        "category": "RAG",
        "content": """
The context window determines how much retrieved information can be passed to an LLM.
Too much irrelevant context can reduce answer quality, while too little context may omit
important evidence.
"""
    },
    {
        "title": "RAG Evaluation",
        "category": "RAG",
        "content": """
RAG systems should be evaluated separately for retrieval and generation. Retrieval
evaluation checks whether relevant chunks are returned, while generation evaluation
checks whether the final answer is correct and grounded.
"""
    },
    {
        "title": "Hybrid Search",
        "category": "RAG",
        "content": """
Hybrid search combines semantic vector search with keyword-based search. This approach
can improve retrieval when exact terms, identifiers, or domain-specific terminology
are important.
"""
    },
    {
        "title": "Metadata Filtering in RAG",
        "category": "RAG",
        "content": """
Metadata can be attached to every document chunk. Fields such as source, category,
date, and document type can be used to filter retrieval results before semantic search.
"""
    },
    {
        "title": "Retrieval Top K",
        "category": "RAG",
        "content": """
Top K controls how many candidate chunks are returned by a retriever. A small K can
miss useful context while a large K may introduce irrelevant information.
"""
    },

    {
        "title": "Vector Embeddings",
        "category": "Embeddings",
        "content": """
Embeddings convert text into numerical vectors representing semantic meaning. Similar
texts generally produce vectors that are close together in embedding space.
"""
    },
    {
        "title": "Embedding Similarity",
        "category": "Embeddings",
        "content": """
Cosine similarity is commonly used to compare embedding vectors. Higher similarity
indicates that two vectors are more semantically related.
"""
    },
    {
        "title": "Embedding Models",
        "category": "Embeddings",
        "content": """
Embedding models transform text into fixed-dimensional numerical representations.
The choice of embedding model affects retrieval accuracy, latency, and cost.
"""
    },
    {
        "title": "Embedding Batch Processing",
        "category": "Embeddings",
        "content": """
Batching multiple texts into one embedding request can improve ingestion efficiency.
Batch sizes should respect API limits and application memory constraints.
"""
    },
    {
        "title": "Embedding Cost Optimization",
        "category": "Embeddings",
        "content": """
Embedding cost depends on the number of tokens processed and the pricing of the
embedding model. Removing duplicate or low-quality documents before embedding can
reduce unnecessary cost.
"""
    },
    {
        "title": "Embedding Dimensions",
        "category": "Embeddings",
        "content": """
Embedding dimensionality determines the number of numerical values in each vector.
Higher dimensions may represent more information but require more memory and computation.
"""
    },
    {
        "title": "Vector Normalization",
        "category": "Embeddings",
        "content": """
Vector normalization scales embeddings to a consistent magnitude. Normalized vectors
are commonly used when similarity is measured using cosine similarity or inner product.
"""
    },
    {
        "title": "Embedding Drift",
        "category": "Embeddings",
        "content": """
Embedding drift can occur when an embedding model changes or when the underlying
document distribution changes. Consistent embedding models help maintain retrieval
quality over time.
"""
    },

    {
        "title": "FAISS Vector Search",
        "category": "FAISS",
        "content": """
FAISS is a library for efficient similarity search over dense vectors. It can index
large collections of embeddings and retrieve vectors that are closest to a query vector.
"""
    },
    {
        "title": "FAISS IndexFlatL2",
        "category": "FAISS",
        "content": """
IndexFlatL2 performs exact nearest-neighbor search using Euclidean distance. It is
simple and useful for smaller datasets where exact retrieval is acceptable.
"""
    },
    {
        "title": "FAISS IndexFlatIP",
        "category": "FAISS",
        "content": """
IndexFlatIP performs inner-product similarity search. With normalized embeddings,
inner product can be used to approximate cosine similarity.
"""
    },
    {
        "title": "FAISS Index Persistence",
        "category": "FAISS",
        "content": """
FAISS indexes can be written to disk and loaded later. Persisting the index avoids
rebuilding embeddings every time an application starts.
"""
    },
    {
        "title": "FAISS Scalability",
        "category": "FAISS",
        "content": """
FAISS provides multiple index types for scaling vector search. Approximate nearest
neighbor indexes can improve search performance for very large collections.
"""
    },
    {
        "title": "FAISS Metadata Management",
        "category": "FAISS",
        "content": """
FAISS primarily stores vectors. Applications commonly maintain a separate metadata
mapping that connects vector positions with source documents and chunk information.
"""
    },
    {
        "title": "FAISS Incremental Updates",
        "category": "FAISS",
        "content": """
New vectors can be added to compatible FAISS indexes using add operations. This allows
applications to update their knowledge base without rebuilding the entire index.
"""
    },
    {
        "title": "Vector Database Architecture",
        "category": "FAISS",
        "content": """
A vector search system normally contains embeddings, an index, metadata, and retrieval
logic. The metadata layer allows retrieved vectors to be mapped back to source content.
"""
    },

    {
        "title": "FastAPI Introduction",
        "category": "FastAPI",
        "content": """
FastAPI is a Python framework for building APIs. It provides automatic validation,
OpenAPI documentation, asynchronous support, and strong integration with Python type
hints.
"""
    },
    {
        "title": "FastAPI Pydantic Validation",
        "category": "FastAPI",
        "content": """
FastAPI uses Pydantic models to validate incoming request data. Validation errors can
be automatically returned to API clients in a structured format.
"""
    },
    {
        "title": "FastAPI Async Endpoints",
        "category": "FastAPI",
        "content": """
Async endpoints allow FastAPI applications to handle I/O-bound operations efficiently.
They are useful when applications communicate with databases, APIs, or external services.
"""
    },
    {
        "title": "FastAPI Health Checks",
        "category": "FastAPI",
        "content": """
Health endpoints provide a simple way to determine whether an application and its
critical dependencies are functioning correctly.
"""
    },
    {
        "title": "FastAPI Error Handling",
        "category": "FastAPI",
        "content": """
Production APIs should handle expected errors consistently. FastAPI supports custom
HTTP exceptions and centralized exception handling.
"""
    },
    {
        "title": "FastAPI Streaming",
        "category": "FastAPI",
        "content": """
Streaming responses allow an API to send generated content incrementally instead of
waiting for the complete response. This can improve perceived latency in AI applications.
"""
    },

    {
        "title": "Prompt Engineering",
        "category": "Prompt Engineering",
        "content": """
Prompt engineering involves designing instructions that guide language model behavior.
Clear objectives, relevant context, constraints, and expected output formats improve
reliability.
"""
    },
    {
        "title": "Few Shot Prompting",
        "category": "Prompt Engineering",
        "content": """
Few-shot prompting provides examples of desired input-output behavior. Examples help
language models infer formatting and reasoning patterns without model fine-tuning.
"""
    },
    {
        "title": "Structured LLM Output",
        "category": "Prompt Engineering",
        "content": """
Structured output constrains language model responses to a predictable schema. JSON
schemas and typed validation can make downstream processing more reliable.
"""
    },
    {
        "title": "Prompt Injection",
        "category": "AI Safety",
        "content": """
Prompt injection occurs when untrusted content attempts to manipulate an AI system's
instructions. Applications should separate trusted instructions from untrusted retrieved
content and validate tool actions.
"""
    },
    {
        "title": "Indirect Prompt Injection",
        "category": "AI Safety",
        "content": """
Indirect prompt injection occurs when malicious instructions are hidden inside external
documents, web pages, or retrieved content. RAG systems must treat retrieved content
as untrusted data.
"""
    },

    {
        "title": "LLM System Architecture",
        "category": "LLM Architecture",
        "content": """
A production LLM application commonly contains an API layer, orchestration layer,
retrieval system, model provider, storage, monitoring, and caching infrastructure.
"""
    },
    {
        "title": "LLM Application Latency",
        "category": "LLM Architecture",
        "content": """
LLM latency can come from retrieval, network requests, model generation, and database
operations. Caching, streaming, batching, and smaller prompts can reduce latency.
"""
    },
    {
        "title": "LLM Cost Management",
        "category": "LLM Architecture",
        "content": """
LLM costs depend on token usage, model selection, request frequency, and prompt size.
Applications should monitor token consumption and optimize repeated requests.
"""
    },
    {
        "title": "AI Observability",
        "category": "Monitoring",
        "content": """
AI observability involves tracking latency, errors, token usage, retrieval quality,
user feedback, and model outputs. These metrics help identify production problems.
"""
    },
    {
        "title": "LLM Evaluation",
        "category": "Evaluation",
        "content": """
LLM evaluation measures system quality using representative queries and expected
answers. Evaluation should cover correctness, relevance, groundedness, and retrieval
quality.
"""
    },

    {
        "title": "Redis Caching",
        "category": "Caching",
        "content": """
Redis is an in-memory data store commonly used for caching. AI applications can cache
expensive retrieval results, embeddings, or frequently requested responses.
"""
    },
    {
        "title": "Semantic Response Cache",
        "category": "Caching",
        "content": """
Semantic caching stores responses for queries that are sufficiently similar in meaning.
It can reduce repeated LLM calls and improve application latency.
"""
    },
    {
        "title": "Cache Invalidation",
        "category": "Caching",
        "content": """
Cache invalidation ensures stale data does not remain available after the underlying
knowledge changes. Time-based expiration and versioning are common approaches.
"""
    },
    {
        "title": "AI Reliability",
        "category": "Reliability",
        "content": """
Reliable AI applications use timeouts, retries, circuit breakers, health checks,
logging, and graceful failure handling for external dependencies.
"""
    },
    {
        "title": "Circuit Breaker Pattern",
        "category": "Reliability",
        "content": """
A circuit breaker temporarily stops requests to a failing dependency. This prevents
cascading failures and gives the dependency time to recover.
"""
    },
    {
        "title": "Retry Strategies",
        "category": "Reliability",
        "content": """
Retries can recover from temporary network or API failures. Exponential backoff and
maximum retry limits prevent excessive repeated requests.
"""
    },

    {
        "title": "AI Feedback Systems",
        "category": "Product",
        "content": """
User feedback such as thumbs-up and thumbs-down can provide evidence about AI product
quality. Feedback should be stored with query and response metadata for analysis.
"""
    },
    {
        "title": "AI Product Metrics",
        "category": "Product",
        "content": """
AI products should track metrics such as retrieval success, response latency, error
rate, user feedback, token consumption, and task completion.
"""
    },
    {
        "title": "Knowledge Base Quality",
        "category": "Data Engineering",
        "content": """
Knowledge base quality strongly influences retrieval quality. Duplicate, outdated,
irrelevant, or poorly formatted documents can reduce the usefulness of an AI system.
"""
    },
    {
        "title": "Document Preprocessing",
        "category": "Data Engineering",
        "content": """
Document preprocessing cleans source content before embedding. Common operations
include whitespace normalization, removing boilerplate, stripping HTML, and handling
page breaks.
"""
    },
    {
        "title": "Data Ingestion Pipeline",
        "category": "Data Engineering",
        "content": """
A reliable ingestion pipeline loads source documents, validates them, preprocesses
content, chunks documents, generates embeddings, stores vectors, and records metadata.
"""
    },
]


def create_documents():
    for index, document in enumerate(documents, start=1):
        filename = f"{index:02d}_{document['category'].lower().replace(' ', '_')}.txt"
        file_path = DOCUMENTS_DIR / filename

        content = (
            f"Title: {document['title']}\n"
            f"Category: {document['category']}\n\n"
            f"{document['content'].strip()}\n"
        )

        file_path.write_text(content, encoding="utf-8")

    print(f"Created {len(documents)} documents.")


if __name__ == "__main__":
    create_documents()