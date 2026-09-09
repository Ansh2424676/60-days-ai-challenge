\# Day 17 - Metadata Filtering Precision Comparison



\## Objective



The objective of this experiment is to improve RAG retrieval precision by

using document metadata such as category, date, source, and document type.



The same five queries were executed twice:



1\. Without metadata filtering

2\. With metadata filtering



Precision@3 was used to compare retrieval quality.



\---



\## Evaluation Method



Precision@K is calculated as:



Precision@K = Relevant Retrieved Documents / Total Retrieved Documents



The evaluation uses manually defined relevant document IDs for each query.



The metadata filters are applied after semantic similarity retrieval to remove

documents that do not match the requested metadata constraints.



\---



\## Test Results



| Query | Unfiltered Precision@3 | Filtered Precision@3 | Improvement |

|---|---:|---:|---:|

| When was NovaMind launched? | 0.33 | 0.33 | +0.00 |

| What is NovaMind designed to help employees with? | 0.33 | 1.00 | +0.67 |

| What does AtlasHub contain? | 0.33 | 1.00 | +0.67 |

| What is AI Launchpad? | 0.67 | 1.00 | +0.33 |

| When is the weekly technical review meeting? | 0.33 | 1.00 | +0.67 |

| \*\*Average\*\* | \*\*0.40\*\* | \*\*0.87\*\* | \*\*+0.47\*\* |



\---



\## Query 1



\### Query



> When was NovaMind launched?



\### Filters



```text

category = ai

date\_after = 2025-12-31

