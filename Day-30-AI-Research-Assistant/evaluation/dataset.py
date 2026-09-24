EVALUATION_DATASET = [
    {
        "id": 1,
        "question": "What is artificial intelligence?",
        "context": (
            "Artificial intelligence enables computer systems to perform "
            "tasks that normally require human intelligence, including "
            "reasoning, learning, and pattern recognition."
        ),
        "ground_truth": (
            "Artificial intelligence enables computer systems to perform "
            "tasks that normally require human intelligence, such as "
            "reasoning, learning, and pattern recognition."
        ),
    },
    {
        "id": 2,
        "question": "What is machine learning?",
        "context": (
            "Machine learning is a subset of AI where systems learn "
            "patterns from data and use those patterns to make predictions "
            "or decisions."
        ),
        "ground_truth": (
            "Machine learning is a subset of artificial intelligence in "
            "which systems learn patterns from data and use them to make "
            "predictions or decisions."
        ),
    },
    {
        "id": 3,
        "question": "How is machine learning related to AI?",
        "context": (
            "Machine learning is a subset of artificial intelligence. "
            "It allows systems to learn patterns from data and use those "
            "patterns to make predictions or decisions."
        ),
        "ground_truth": (
            "Machine learning is a subset of artificial intelligence. "
            "It provides a way for AI systems to learn patterns from data "
            "and use those patterns for predictions or decisions."
        ),
    },
    {
        "id": 4,
        "question": "What are AI agents?",
        "context": (
            "AI agents combine language models, tools, memory, and "
            "workflows to perform multi-step tasks."
        ),
        "ground_truth": (
            "AI agents combine language models with tools, memory, and "
            "workflows to perform multi-step tasks."
        ),
    },
    {
        "id": 5,
        "question": "What components can an AI agent use?",
        "context": (
            "AI agents combine language models, tools, memory, and "
            "workflows to perform multi-step tasks."
        ),
        "ground_truth": (
            "An AI agent can use a language model, tools, memory, and "
            "workflows to perform multi-step tasks."
        ),
    },
    {
        "id": 6,
        "question": "What is RAG?",
        "context": (
            "Retrieval-Augmented Generation combines retrieval of relevant "
            "information with language generation to improve grounded "
            "responses."
        ),
        "ground_truth": (
            "Retrieval-Augmented Generation combines retrieval of relevant "
            "information with language generation to produce more grounded "
            "responses."
        ),
    },
    {
        "id": 7,
        "question": "Why is RAG useful?",
        "context": (
            "Retrieval-Augmented Generation combines retrieval of relevant "
            "information with language generation to improve grounded "
            "responses."
        ),
        "ground_truth": (
            "RAG is useful because it retrieves relevant information and "
            "uses it during generation, helping produce more grounded "
            "responses."
        ),
    },
    {
        "id": 8,
        "question": "What does grounded response mean?",
        "context": (
            "Retrieval-Augmented Generation combines retrieval of relevant "
            "information with language generation to improve grounded "
            "responses."
        ),
        "ground_truth": (
            "A grounded response is a response supported by the relevant "
            "information retrieved for the question rather than fabricated "
            "information."
        ),
    },
    {
        "id": 9,
        "question": "What is FastAPI?",
        "context": (
            "FastAPI is a Python framework for building APIs using Python "
            "type hints and automatic validation."
        ),
        "ground_truth": (
            "FastAPI is a Python framework for building APIs using Python "
            "type hints and automatic validation."
        ),
    },
    {
        "id": 10,
        "question": "What are key features of FastAPI?",
        "context": (
            "FastAPI is a Python framework for building APIs using Python "
            "type hints and automatic validation."
        ),
        "ground_truth": (
            "FastAPI provides a Python framework for building APIs and "
            "uses Python type hints and automatic validation."
        ),
    },
    {
        "id": 11,
        "question": "What is semantic search?",
        "context": (
            "Semantic search retrieves information based on meaning and "
            "conceptual similarity rather than relying only on exact "
            "keyword matches."
        ),
        "ground_truth": (
            "Semantic search retrieves information based on meaning and "
            "conceptual similarity rather than only exact keyword matches."
        ),
    },
    {
        "id": 12,
        "question": "How does semantic search differ from keyword search?",
        "context": (
            "Semantic search retrieves information based on meaning and "
            "conceptual similarity rather than relying only on exact "
            "keyword matches."
        ),
        "ground_truth": (
            "Semantic search focuses on meaning and conceptual similarity, "
            "while keyword search primarily relies on matching specific "
            "words or terms."
        ),
    },
    {
        "id": 13,
        "question": "What is a vector embedding?",
        "context": (
            "A vector embedding represents information as numerical values "
            "in a multidimensional vector space so that semantic similarity "
            "can be measured."
        ),
        "ground_truth": (
            "A vector embedding represents information as numerical values "
            "in a multidimensional space, allowing semantic similarity "
            "between items to be measured."
        ),
    },
    {
        "id": 14,
        "question": "Why are embeddings useful for retrieval?",
        "context": (
            "Embeddings represent information numerically and allow systems "
            "to compare semantic similarity between items."
        ),
        "ground_truth": (
            "Embeddings are useful for retrieval because they allow a system "
            "to compare semantic similarity between a query and stored "
            "information."
        ),
    },
    {
        "id": 15,
        "question": "What is a RAG pipeline?",
        "context": (
            "A RAG pipeline retrieves relevant information and then uses "
            "that information as context for language generation."
        ),
        "ground_truth": (
            "A RAG pipeline first retrieves relevant information and then "
            "provides that information as context to a language model for "
            "generation."
        ),
    },
    {
        "id": 16,
        "question": "What is hallucination in an AI system?",
        "context": (
            "A hallucination occurs when an AI system generates information "
            "that is unsupported, fabricated, or not grounded in the "
            "available evidence."
        ),
        "ground_truth": (
            "An AI hallucination is generated information that is "
            "unsupported, fabricated, or not grounded in the available "
            "evidence."
        ),
    },
    {
        "id": 17,
        "question": "How can grounding help reduce hallucinations?",
        "context": (
            "Grounding requires generated answers to be supported by "
            "retrieved information or other available evidence."
        ),
        "ground_truth": (
            "Grounding can reduce hallucinations by requiring generated "
            "answers to be supported by retrieved information or available "
            "evidence."
        ),
    },
    {
        "id": 18,
        "question": "What is a knowledge assistant?",
        "context": (
            "A knowledge assistant uses retrieval and language generation "
            "to answer questions using information from a defined "
            "knowledge base."
        ),
        "ground_truth": (
            "A knowledge assistant uses retrieval and language generation "
            "to answer questions using information from a defined "
            "knowledge base."
        ),
    },
    {
        "id": 19,
        "question": "Why is evaluation important for AI systems?",
        "context": (
            "Evaluation provides measurements that can be used to assess "
            "AI system quality and detect regressions when the system "
            "changes."
        ),
        "ground_truth": (
            "Evaluation is important because it provides measurements of "
            "AI system quality and helps detect regressions when the system "
            "changes."
        ),
    },
    {
        "id": 20,
        "question": "What is regression testing for an AI system?",
        "context": (
            "Regression testing compares current system performance with "
            "a stored baseline to detect meaningful decreases in quality."
        ),
        "ground_truth": (
            "AI regression testing compares current system performance "
            "against a stored baseline to detect meaningful decreases "
            "in quality."
        ),
    },
]


def get_evaluation_dataset():
    """Return the complete labelled evaluation dataset."""
    return EVALUATION_DATASET