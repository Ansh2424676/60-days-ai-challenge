# Day 11 — Build Your First Document Retrieval System

## Overview

This project implements a mini document retrieval engine using Python, NumPy, and scikit-learn.

The system accepts a user query, compares it against a knowledge base of documents using TF-IDF and cosine similarity, and returns the most relevant documents ranked by similarity score.

A relevance threshold is also implemented so that the system can honestly reject queries when no sufficiently relevant document is found.

---

## Technologies Used

* Python
* NumPy
* scikit-learn
* TF-IDF Vectorization
* Cosine Similarity

---

## Knowledge Base

The retrieval system contains **22 text documents** covering topics such as:

* Machine Learning
* Supervised Learning
* Unsupervised Learning
* Deep Learning
* Natural Language Processing
* Text Classification
* Sentiment Analysis
* Computer Vision
* Python
* SQL
* Data Science
* Artificial Intelligence
* Neural Networks
* Cloud Computing
* Cybersecurity
* Encryption
* Authentication
* Recommendation Systems
* Big Data
* Information Retrieval
* Search Engines
* Database Indexing

The documents are stored as a Python list in `retrieval_engine.py`.

---

## Retrieval Architecture

```text
                 USER QUERY
                     |
                     v
          +---------------------+
          | PreprocessingModule |
          |     (Day 10)        |
          +---------------------+
                     |
                     v
             Cleaned Query
                     |
                     v
          +---------------------+
          | VectorizerModule    |
          |     (Day 10)        |
          +---------------------+
                     |
                     v
              Query TF-IDF
                  Vector
                     |
                     v
          +---------------------+
          | Cosine Similarity   |
          +---------------------+
                     |
                     v
          Compare with stored
             TF-IDF matrix
                     |
                     v
          +---------------------+
          | Relevance Threshold |
          |      >= 0.10        |
          +---------------------+
                /          \
              YES           NO
               |             |
               v             v
        Rank Top K       No relevant
         Documents        document
               |
               v
       Document + Score
```

---

## Reusing the Day 10 Pipeline

The retrieval system reuses the preprocessing and vectorization components developed during Day 10.

The following modules are imported from the Day 10 project:

```python
from nlp_pipeline import PreprocessingModule, VectorizerModule
```

The knowledge-base documents are preprocessed before being converted into TF-IDF vectors.

The resulting TF-IDF matrix is stored in:

```python
corpus_matrix
```

This matrix is then reused for every incoming query.

---

## TF-IDF Vectorization

TF-IDF represents each document as a numerical vector based on the importance of its words.

Common words receive lower importance, while words that are more specific to individual documents receive higher importance.

The knowledge base is fitted once:

```python
vectorizer.fit(processed_documents)

corpus_matrix = vectorizer.corpus_vectors
```

The resulting matrix is reused during retrieval instead of rebuilding it for every query.

---

## `retrieve()` Function

The main retrieval function is:

```python
retrieve(query, corpus_matrix, top_k=3)
```

### Parameters

**query**

The user's raw text query.

**corpus_matrix**

The stored TF-IDF matrix representing the knowledge-base documents.

**top_k**

The number of highest-ranked documents to return. The default value is `3`.

### Output

The function returns:

```text
(document_index, similarity_score, document)
```

Results are sorted from the highest similarity score to the lowest.

---

## Cosine Similarity

Cosine similarity measures the similarity between the query vector and each document vector.

A score closer to `1.0` indicates stronger similarity.

A score closer to `0.0` indicates little or no lexical similarity.

The retrieval engine calculates similarity using:

```python
cosine_similarity(
    query_vector,
    corpus_matrix
)
```

---

## Relevance Threshold

A minimum relevance threshold of:

```text
0.10
```

is implemented.

The system first finds the highest similarity score across all documents.

If:

```text
highest_score < 0.10
```

the system returns:

```text
No relevant document found
```

This prevents the retrieval engine from presenting an apparently relevant result when all similarity scores are extremely low.

---

## Ten Query Tests

The retrieval system was tested using ten different queries.

### Query 1 — Normal

```text
how do machines learn from examples?
```

Expected topic:

```text
Supervised learning
```

### Query 2 — Normal

```text
understanding human language with computers
```

Expected topic:

```text
Natural language processing
```

### Query 3 — Normal

```text
protecting networks from hackers
```

Expected topic:

```text
Cybersecurity
```

### Query 4 — Normal

```text
finding relevant documents from a search
```

Expected topic:

```text
Information retrieval
```

### Query 5 — Ambiguous

```text
Python
```

Expected topic:

```text
Python programming
```

This is intentionally ambiguous because the query contains only one meaningful keyword.

### Query 6 — Ambiguous

```text
data
```

Expected topic:

```text
Data science
```

This is ambiguous because many documents contain or relate to the concept of data.

### Query 7 — Ambiguous

```text
machine intelligence
```

Expected topic:

```text
Artificial intelligence
```

This query tests how TF-IDF handles related terminology.

### Query 8 — Out-of-domain

```text
best pizza recipe for dinner
```

Expected result:

```text
No relevant document
```

### Query 9 — Out-of-domain

```text
latest football match score
```

Expected result:

```text
No relevant document
```

### Query 10 — Normal

```text
encrypting sensitive information
```

Expected topic:

```text
Encryption
```

---

## Retrieval Failure Analysis

The system deliberately includes ambiguous queries to expose limitations of lexical retrieval.

### Ambiguous queries

For queries such as:

```text
Python
```

or:

```text
data
```

multiple documents can contain related vocabulary.

TF-IDF may therefore rank a technically related document first even when it is not the intended meaning of the query.

### Vocabulary mismatch

TF-IDF depends heavily on shared words between the query and documents.

For example, a document may discuss cybersecurity using terms such as:

```text
attacks
unauthorized access
security
```

while a user may search for:

```text
protecting computers from intruders
```

The concepts are related, but the exact vocabulary differs.

Because TF-IDF primarily measures lexical overlap, the correct document may receive a low similarity score.

### Diagnosis

The specific limitation is that TF-IDF does not understand semantic relationships between words.

It treats different words such as:

```text
intruders
attackers
hackers
```

as different vocabulary unless the words themselves appear in the documents.

---

## Why Embeddings Are Needed

The vocabulary-mismatch problem demonstrates an important limitation of traditional TF-IDF retrieval.

TF-IDF answers approximately:

> "Which documents use words similar to the words in my query?"

Semantic embeddings can instead represent the meaning of text in a vector space.

This makes it possible to retrieve documents even when the query and document use different but semantically related vocabulary.

For example:

```text
Query:
protecting computers from intruders

Document:
Cybersecurity protects systems from unauthorized access and attacks.
```

The words are not identical, but the concepts are closely related.

This is one reason modern retrieval systems often use embeddings and vector databases instead of relying only on keyword overlap.

---

## Relevance Threshold Test

The retrieval engine includes an explicit threshold test using an out-of-domain query:

```text
ancient ocean dinosaur recipe
```

If the highest similarity score is below:

```text
0.10
```

the engine returns:

```text
No relevant document found
```

This prevents low-quality matches from being returned simply because the retrieval system must produce a result.

---

## Project Structure

```text
Day-11-Document-Retrieval/
│
├── retrieval_engine.py
├── README.md
└── requirements.txt
```

---

## How to Run

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the retrieval engine:

```bash
python retrieval_engine.py
```

The program will:

1. Load the 22-document knowledge base.
2. Preprocess all documents.
3. Create and store the TF-IDF matrix.
4. Process ten test queries.
5. Calculate cosine similarity.
6. Return the top three results.
7. Apply the 0.10 relevance threshold.
8. Print failure analysis.
9. Demonstrate the vocabulary-mismatch limitation.

---

## Key Learning

The main lesson from this project is that **retrieval quality depends not only on ranking but also on how relevance is represented**.

TF-IDF provides a simple and interpretable baseline, but it is limited by vocabulary mismatch and lack of semantic understanding.

The failure cases show why modern AI retrieval systems move toward semantic embeddings for better meaning-based search.

---

## Conclusion

This project demonstrates a complete mini information-retrieval system built on top of the modular NLP components from Day 10.

The system stores a reusable TF-IDF representation of a knowledge base, retrieves the top-K documents for a query, ranks them using cosine similarity, and rejects low-quality matches using a relevance threshold.

The experiments also demonstrate an important limitation of keyword-based retrieval: **matching words is not the same as matching meaning.**

This provides the foundation for moving from TF-IDF retrieval toward embedding-based semantic search in future projects.

````

### Step 9 — Save and run again

Save `README.md`.

Then run:

```powershell
python retrieval_engine.py
````

**Important:** abhi Git add/commit/push mat karo.

Jo **complete terminal output** aayega, mujhe bhejo. Main specifically check karunga:

1. `Knowledge base size: 22`
2. TF-IDF matrix successfully created
3. 10/10 queries execute hui
4. Ambiguous queries work kar rahi hain
5. 2 out-of-domain queries threshold se reject ho rahi hain
6. Failure analysis sensible hai
7. Vocabulary mismatch test run hua

Uske baad final **GitHub commit + push + Day 11 submission + LinkedIn caption** karenge.
