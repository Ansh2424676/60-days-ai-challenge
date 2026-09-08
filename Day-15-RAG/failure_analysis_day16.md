# Day 16 — Diagnosing RAG Failure Modes

## 1. Objective

The goal of Day 16 was to diagnose common RAG failure modes using a
15-query test suite and identify improvements to the Day 15 RAG pipeline.

The five targeted failure modes were:

1. Retrieval failure
2. Context window / multi-topic retrieval pressure
3. Answer-context mismatch
4. Vague context retrieved
5. Correct chunk retrieved but wrong answer generated

---

## 2. RAG Configuration

| Component | Configuration |
|---|---|
| Knowledge Base Documents | 10 |
| Embedding Model | all-MiniLM-L6-v2 |
| Embedding Dimension | 384 |
| Vector Index | FAISS IndexFlatL2 |
| Baseline Top-K | 3 |
| Sub-query Top-K | 2 |
| Distance Threshold | 0.8 |

---

## 3. Test Results

| ID | Failure Mode | Query | Expected Docs | Retrieved Docs | Coverage | Retrieval Quality | Diagnosis |
|---|---|---|---|---|---:|---:|---|
| Q01 | retrieval_failure | What is NovaTech's employee vacation policy? | None | None | 1.00 | 5/5 | The distance threshold correctly rejected the unsupported vacation-policy query. |
| Q02 | retrieval_failure | What database technology does NovaTech use in production? | None | None | 1.00 | 5/5 | The distance threshold correctly rejected the unsupported production-database query. |
| Q03 | retrieval_failure | Who is the Chief Financial Officer of NovaTech Solutions? | None | doc-001, doc-002 | 0.00 | 1/5 | The retriever still returned semantically similar company chunks for the unsupported CFO query, creating a false-positive retrieval. |
| Q04 | context_window_overflow | Tell me everything about NovaTech Solutions, NovaMind, AtlasHub, AI Launchpad, and the engineering team's weekly meeting. | doc-001, doc-002, doc-003, doc-004, doc-005, doc-006, doc-007, doc-008, doc-009, doc-010 | doc-002, doc-001, doc-009, doc-005, doc-003, doc-010, doc-004, doc-008, doc-007 | 0.90 | 4/5 | Query decomposition improved multi-topic retrieval coverage to 90%, although AtlasHub's platform-description chunk was still missed. |
| Q05 | context_window_overflow | Give a complete summary covering the company, departments, NovaMind, AtlasHub, training, certification, and engineering meetings. | doc-001, doc-002, doc-003, doc-004, doc-005, doc-006, doc-007, doc-008, doc-009, doc-010 | doc-002, doc-001, doc-009, doc-005, doc-003, doc-010, doc-004, doc-008, doc-007 | 0.90 | 4/5 | Query decomposition improved broad-query coverage to 90%, but one expected document was still not retrieved. |
| Q06 | context_window_overflow | Explain all known NovaTech internal systems, projects, documentation, training programs, certifications, and recurring meetings. | doc-003, doc-004, doc-005, doc-006, doc-007, doc-008, doc-009, doc-010 | doc-002, doc-001, doc-009, doc-005, doc-003, doc-010, doc-004, doc-008, doc-007 | 0.88 | 4/5 | Query decomposition improved broad-query coverage to 88%, but some documents outside the requested internal topics were also retrieved. |
| Q07 | answer_context_mismatch | Who led the NovaMind project? | doc-005 | doc-005, doc-003 | 1.00 | 5/5 | The correct project-lead chunk was retrieved, so any answer mismatch would occur during generation rather than retrieval. |
| Q08 | answer_context_mismatch | How long does AI Launchpad last? | doc-008 | doc-008 | 1.00 | 5/5 | The correct AI Launchpad duration chunk was retrieved, so generation is the remaining evaluation stage. |
| Q09 | answer_context_mismatch | Where is NovaTech Solutions headquartered? | doc-001 | doc-001, doc-002 | 1.00 | 5/5 | The correct headquarters chunk was retrieved, although an unrelated department chunk was also included. |
| Q10 | vague_context_retrieved | Tell me about NovaMind. | doc-003, doc-004, doc-005 | doc-004, doc-003 | 0.67 | 3/5 | NovaMind retrieval was relevant but incomplete because the project-lead document was not retrieved. |
| Q11 | vague_context_retrieved | Tell me about AtlasHub. | doc-006, doc-007 | doc-007 | 0.50 | 3/5 | AtlasHub retrieval was incomplete because only the documentation-content chunk was retrieved. |
| Q12 | vague_context_retrieved | Tell me about AI Launchpad. | doc-008, doc-009 | doc-008 | 0.50 | 3/5 | AI Launchpad retrieval was incomplete because the certification document was not retrieved. |
| Q13 | correct_chunk_wrong_answer | Which city is NovaTech Solutions headquartered in? | doc-001 | doc-001, doc-002 | 1.00 | 5/5 | The correct headquarters chunk was retrieved, so a wrong answer would be a generation-level failure. |
| Q14 | correct_chunk_wrong_answer | Which person led the NovaMind project? | doc-005 | doc-005, doc-003 | 1.00 | 5/5 | The correct NovaMind project-lead chunk was retrieved, so this test isolates the generation stage. |
| Q15 | correct_chunk_wrong_answer | What certification do employees receive after completing AI Launchpad? | doc-009 | doc-009, doc-008 | 1.00 | 5/5 | The correct certification chunk was retrieved, so any wrong answer would be a generation-level failure. |

---

## 4. Fix #1 — Similarity / Distance Threshold Filtering

### Problem

The original Day 15 retriever used fixed Top-3 retrieval.

This meant that even unsupported queries could receive the nearest
available documents.

For example, unsupported questions could still return semantically
similar company information.

### Implementation

A FAISS distance threshold of **0.80** was introduced.

Only retrieved chunks satisfying:

`distance <= 0.80`

are accepted.

### Result

The threshold successfully rejected the unsupported vacation-policy
and production-database queries.

However, Q03 still retrieved two semantically similar company chunks,
demonstrating that a threshold alone cannot perfectly determine whether
a document actually answers a question.

---

## 5. Fix #2 — Query Decomposition

### Problem

A broad query containing multiple topics was represented using a
single query embedding.

With fixed Top-K retrieval, some topics could be missed.

### Implementation

Broad queries are decomposed into focused sub-queries.

Each sub-query retrieves Top-2 documents.

Results are then deduplicated.

### Result

The broad-query tests achieved:

- Q04 → 90% retrieval coverage
- Q05 → 90% retrieval coverage
- Q06 → 88% retrieval coverage

This improved multi-topic retrieval coverage compared with the original
fixed Top-K approach.

---

## 6. Root Cause Analysis

### Root Cause 1 — Fixed Top-K Retrieval

The original Day 15 retrieval strategy always returned the nearest
documents.

Vector similarity produces a ranking even when the knowledge base does
not contain an answer.

This caused false-positive retrieval for unsupported questions.

### Root Cause 2 — Single Embedding for Broad Queries

A broad multi-topic query was represented by one semantic embedding.

Because retrieval was restricted to a small Top-K, some relevant topics
were not retrieved.

Query decomposition gives each topic an independent retrieval
opportunity.

---

## 7. Chunking and Embedding Analysis

The Day 15 knowledge base consists of small atomic documents.

This improves precision for focused questions.

However, atomic chunks combined with a single broad-query embedding can
reduce multi-topic recall.

The main issue was therefore the combination of:

**atomic chunks + single broad-query embedding + fixed Top-K**

rather than oversized chunks.

Query decomposition improves recall without unnecessarily combining
unrelated facts into large chunks.

---

## 8. Scorecard

| Metric | Result |
|---|---:|
| Total Tests | 15 |
| Successful Retrieval Behavior | 14/15 |
| Retrieval Success Rate | 93% |
| Average Retrieval Coverage | 0.82 |
| Average Retrieval Quality | 4.13/5 |
| Average Answer Quality | Pending |

---

## 9. Answer Quality Evaluation

Answer generation was not completed because the OpenAI API credits
were exhausted during testing.

The Day 16 results therefore contain:

- `generated_answer: null`
- `answer_quality: null`

No answer-quality scores were fabricated.

Therefore Q07–Q15 can confirm retrieval behavior, but generation-level
failure cannot yet be experimentally confirmed.

---

## 10. Final Findings

### Improvements

- Distance threshold reduced false-positive retrieval.
- Query decomposition improved multi-topic retrieval coverage.
- Most focused queries retrieved their expected documents.
- All 15 tests were logged.
- Retrieval behavior achieved 14/15.

### Remaining Issues

- The 0.80 threshold can cause false negatives.
- Q03 still demonstrates semantic false-positive retrieval.
- Vague queries can retrieve incomplete context.
- Generation-level answer quality remains pending.

---

## 11. Final Conclusion

The Day 16 experiment identified two major weaknesses in the Day 15
RAG system:

1. False-positive retrieval caused by fixed Top-K retrieval.
2. Poor multi-topic recall caused by a single broad-query embedding.

Two fixes were implemented:

1. Similarity / distance threshold filtering.
2. Query decomposition with per-sub-query Top-2 retrieval.

Final retrieval metrics:

- **14/15 successful retrieval behavior**
- **93% retrieval success rate**
- **0.82 average retrieval coverage**
- **4.13/5 average retrieval quality**

Answer-quality evaluation remains pending until OpenAI API generation
is available.

---

## 12. Submission Files

- `day16_final.py`
- `day16_report.py`
- `rag_results_day16_final.json`
- `scorecard_day16_final.json`
- `failure_analysis_day16.md`
