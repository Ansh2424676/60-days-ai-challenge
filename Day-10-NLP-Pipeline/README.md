# Day 10 — Build Your First End-to-End NLP Pipeline

## Overview

This project implements a modular end-to-end NLP similarity pipeline using Python, NLTK, and scikit-learn.

The pipeline takes raw text as input, preprocesses the text, converts documents into TF-IDF vectors, calculates cosine similarity, and returns ranked documents with similarity scores.

## Technologies Used

* Python
* NLTK
* scikit-learn
* TF-IDF Vectorization
* Cosine Similarity

## Project Architecture

```text
Raw Query + Document Corpus
            |
            v
+-------------------------+
|  PreprocessingModule    |
|                         |
| - Lowercase             |
| - Tokenization          |
| - Stopword Removal      |
| - Lemmatization         |
+-------------------------+
            |
            v
+-------------------------+
|    VectorizerModule     |
|                         |
| - TF-IDF Vectorization  |
| - Cosine Similarity     |
+-------------------------+
            |
            v
+-------------------------+
|        Pipeline         |
|                         |
| - Connects modules      |
| - Calculates scores     |
| - Ranks documents       |
+-------------------------+
            |
            v
+-------------------------+
|   Ranked Results        |
| Document + Score        |
+-------------------------+
```

## Module 1 — PreprocessingModule

The `PreprocessingModule` is responsible for cleaning raw text.

It provides:

```python
transform(text)
```

### Processing steps

1. Convert text to lowercase.
2. Extract alphabetic words.
3. Remove English stopwords.
4. Lemmatize words.
5. Return cleaned text.

The module also handles invalid input.

### Error handling

* Empty string
* Single-character input
* Numbers/symbols-only input
* Non-string input
* Text that contains no meaningful words after preprocessing

## Module 2 — VectorizerModule

The `VectorizerModule` handles vectorization and similarity calculation.

It provides:

```python
fit(corpus)
transform(query)
```

TF-IDF is used to represent documents numerically.

Cosine similarity is then used to measure how similar the query is to each document.

Higher similarity scores indicate stronger similarity between the query and document.

## Module 3 — Pipeline

The `Pipeline` class connects the preprocessing and vectorization modules.

It provides a single method:

```python
run(query, corpus)
```

The pipeline performs the following operations:

```text
Raw Query
    ↓
Preprocessing
    ↓
TF-IDF Transformation
    ↓
Cosine Similarity
    ↓
Sorting by Score
    ↓
Ranked Results
```

This keeps the complete NLP workflow reusable and easy to test.

## Test Corpus

The pipeline was tested using a corpus containing 15 documents covering topics such as:

* Machine Learning
* Deep Learning
* Python
* NLP
* Data Science
* Artificial Intelligence
* Computer Vision
* SQL
* Cloud Computing
* Cybersecurity
* Neural Networks
* Text Classification
* Recommendation Systems
* Big Data

## Five Query Tests

### Query 1

```text
machine learning and data
```

Top results:

```text
1. Document 1 — Score: 0.5703
2. Document 5 — Score: 0.5402
3. Document 2 — Score: 0.2046
```

### Query 2

```text
understanding human language
```

Top results:

```text
1. Document 4 — Score: 0.6341
2. Document 11 — Score: 0.2866
3. Document 3 — Score: 0.2443
```

### Query 3

```text
neural networks and deep learning
```

Top results:

```text
1. Document 2 — Score: 0.7044
2. Document 11 — Score: 0.3486
3. Document 1 — Score: 0.1657
```

### Query 4

```text
protecting computer systems
```

Top results:

```text
1. Document 10 — Score: 0.5052
2. Document 13 — Score: 0.2493
3. Document 7 — Score: 0.2134
```

### Query 5

```text
large datasets and cloud computing
```

Top results:

```text
1. Document 9 — Score: 0.5000
2. Document 14 — Score: 0.3688
```

The actual program prints all 15 ranked documents for every query.

## Edge Case Testing

The pipeline was tested against the three required edge cases.

| Input                        | Expected Behavior      | Result |
| ---------------------------- | ---------------------- | ------ |
| Empty string `""`            | Raise validation error | Passed |
| Single character `"A"`       | Raise validation error | Passed |
| Numbers/symbols `"12345!!!"` | Raise validation error | Passed |

Actual test execution confirmed that all three cases were handled correctly.

## Design Decision Note

### Why Modular Components?

The pipeline uses separate classes instead of putting all NLP operations into one large script.

Each module has a single responsibility:

* `PreprocessingModule` → cleans text
* `VectorizerModule` → creates vectors and calculates similarity
* `Pipeline` → coordinates the complete workflow

This modular design makes the system easier to debug because an error can be isolated to a specific component.

For example, if preprocessing produces incorrect output, only the `PreprocessingModule` needs to be inspected. Similarly, vectorization problems can be tested independently without changing the preprocessing logic.

Modularity also makes the project easier to extend.

For example:

* A different tokenizer can be added to preprocessing.
* Another vectorization method can replace TF-IDF.
* A different similarity algorithm can be introduced.
* The pipeline can later be extended to classification or recommendation tasks.

Therefore, separating components according to their responsibilities improves maintainability, testability, debugging, and future extensibility.

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the pipeline:

```bash
python nlp_pipeline.py
```

The program will:

1. Process the 15-document corpus.
2. Run five test queries.
3. Calculate similarity scores.
4. Rank the documents.
5. Test the required edge cases.

## Project Structure

```text
Day-10-NLP-Pipeline/
│
├── nlp_pipeline.py
├── README.md
└── requirements.txt
```

## Conclusion

This project demonstrates how individual NLP operations can be connected into a reusable end-to-end pipeline.

The modular architecture separates preprocessing, vectorization, similarity calculation, and pipeline orchestration, making the system easier to test, debug, maintain, and extend.
