# Day 13 — Understanding Embeddings as Semantic Coordinates

## Objective

Explore how dense sentence embeddings represent semantic meaning
and compare them with sparse TF-IDF representations.

## Dataset

20 semantically diverse sentences across four topics:

- Sports
- Technology
- Cooking
- Travel

The dataset also contains five paraphrase pairs designed to demonstrate
the difference between lexical similarity and semantic similarity.

## Experiments

### 1. Sentence Embeddings

Generated dense sentence embeddings for 20 sentences.

Primary experiment target:

- OpenAI `text-embedding-3-small`

Due to exhausted API credits, the final experiment used:

- `all-MiniLM-L6-v2`
- 384-dimensional local sentence embeddings

### 2. TF-IDF vs Embedding Similarity

Cosine similarity was calculated for five paraphrase pairs using:

- TF-IDF
- Dense sentence embeddings

The comparison demonstrates that TF-IDF depends strongly on word overlap,
while embeddings capture semantic similarity even when wording differs.

### 3. Semantic Recommendation

Implemented:

```python
embed_and_recommend(query_sentence, corpus_sentences, top_k=3)