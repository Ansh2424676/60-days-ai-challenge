\# Day 17 - Metadata Filtering RAG Architecture



\## Architecture Overview



The Day 17 pipeline extends the original RAG architecture by adding

metadata enrichment and metadata-based filtering to improve retrieval

precision.



```text

&#x20;                   ┌──────────────────────┐

&#x20;                   │   Knowledge Base     │

&#x20;                   │  knowledge\_base.json │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Metadata Enrichment  │

&#x20;                   │                      │

&#x20;                   │ source               │

&#x20;                   │ category             │

&#x20;                   │ date                 │

&#x20;                   │ document\_type        │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ LangChain Documents  │

&#x20;                   │                      │

&#x20;                   │ page\_content         │

&#x20;                   │ + metadata           │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │ Local Embeddings     │

&#x20;                   │                      │

&#x20;                   │ all-MiniLM-L6-v2     │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌──────────────────────┐

&#x20;                   │   FAISS Vector DB    │

&#x20;                   │                      │

&#x20;                   │ Embeddings +         │

&#x20;                   │ Document Metadata    │

&#x20;                   └──────────┬───────────┘

&#x20;                              │

&#x20;                              │

&#x20;               ┌──────────────┘

&#x20;               │

&#x20;               ▼

&#x20;      ┌──────────────────────┐

&#x20;      │      User Query      │

&#x20;      └──────────┬───────────┘

&#x20;                 │

&#x20;                 ▼

&#x20;      ┌──────────────────────┐

&#x20;      │ Semantic Retrieval   │

&#x20;      │                      │

&#x20;      │ Similarity Search    │

&#x20;      └──────────┬───────────┘

&#x20;                 │

&#x20;                 ▼

&#x20;      ┌──────────────────────┐

&#x20;      │ Metadata Filtering   │

&#x20;      │                      │

&#x20;      │ category             │

&#x20;      │ source               │

&#x20;      │ document\_type        │

&#x20;      │ date\_after           │

&#x20;      └──────────┬───────────┘

&#x20;                 │

&#x20;                 ▼

&#x20;      ┌──────────────────────┐

&#x20;      │ Filtered Context     │

&#x20;      │                      │

&#x20;      │ Relevant Documents   │

&#x20;      └──────────┬───────────┘

&#x20;                 │

&#x20;                 ▼

&#x20;      ┌──────────────────────┐

&#x20;      │      RAG Layer       │

&#x20;      │                      │

&#x20;      │ Context + Query      │

&#x20;      └──────────┬───────────┘

&#x20;                 │

&#x20;                 ▼

&#x20;      ┌──────────────────────┐

&#x20;      │     Final Answer     │

&#x20;      └──────────────────────┘

