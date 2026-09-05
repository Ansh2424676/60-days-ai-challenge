# Day 12 - Chunking Strategies for Long Document Processing

## Overview

This project explores how different chunking strategies affect retrieval
quality when processing long documents for RAG applications.

## Document

The experiment uses a long Wikipedia article about Artificial Intelligence
as the source document.

## Chunking Strategies

### 1. Manual Fixed-Size Chunking

Implemented manually in Python without LangChain.

The document is divided into fixed character windows using a Python loop.

### 2. Recursive Character Chunking

Implemented using LangChain's:

`RecursiveCharacterTextSplitter`

The splitter was tested with different chunk sizes and overlaps.

## Configurations

### Chunk Sizes

- 100 characters
- 300 characters
- 500 characters
- 1000 characters

### Overlaps

- 0 characters
- 50 characters
- 100 characters

Total configurations:

**12**

## Retrieval

The same retrieval query was used for every configuration:

> What are the goals, capabilities and applications of artificial intelligence?

TF-IDF vectorization and cosine similarity were used to retrieve the most
relevant chunk.

## Evaluation

Configurations were compared using:

- Retrieval similarity
- Contextual completeness
- Overall quality score

## Boundary Failure Analysis

Three examples of sentences being split across fixed-size chunk boundaries
were identified.

Each example includes the exact character position where the boundary
occurred.

## Key Findings

Small chunks can lose surrounding context, while very large chunks may include
unnecessary information.

Overlap improves continuity between neighbouring chunks.

Recursive character splitting generally provides more natural boundaries than
naive fixed-size character splitting.

## Recommendation

For long-form documents, a moderate chunk size with a small overlap is a
strong starting point.

The exact best configuration is reported in the notebook based on the
retrieval experiment.

## Technologies

- Python
- LangChain
- Scikit-learn
- Pandas
- BeautifulSoup
- Jupyter Notebook

## Day 12 Learning Outcomes

- Manual fixed-size chunking
- Recursive character splitting
- Chunk size experimentation
- Chunk overlap experimentation
- Retrieval evaluation
- Boundary failure analysis
- RAG-oriented chunking strategy design