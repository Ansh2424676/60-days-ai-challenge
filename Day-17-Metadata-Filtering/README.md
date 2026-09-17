\# Day 17 - Improve RAG Precision with Metadata Filtering



\## Overview



Day 17 extends the RAG pipeline by introducing metadata-aware retrieval.



Instead of relying only on semantic similarity, documents are enriched with

structured metadata such as:



\- Source

\- Category

\- Date

\- Document type



The metadata remains attached to each LangChain `Document` and is used to

filter retrieved candidates.



The goal is to reduce irrelevant retrievals and improve retrieval precision.



\---



\## Objectives



The Day 17 pipeline implements:



1\. Metadata-enriched knowledge base

2\. LangChain Documents with metadata

3\. FAISS vector store

4\. Local HuggingFace embeddings

5\. Category filtering

6\. Source filtering

7\. Document-type filtering

8\. Date cutoff filtering

9\. Five-query retrieval evaluation

10\. Precision comparison

11\. Metadata edge-case handling

12\. Updated RAG architecture



\---



\## Project Structure



```text

Day-17-Metadata-Filtering/

│

├── knowledge\_base.json

├── rag\_metadata.py

├── requirements.txt

├── precision\_comparison.md

├── edge\_cases.md

├── architecture\_day17.md

├── README.md

└── .gitignore

