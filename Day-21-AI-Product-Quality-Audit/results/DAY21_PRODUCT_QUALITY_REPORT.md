# Day 21 — AI Product Quality Audit

## 1. Objective

This audit evaluates the Day 20 AI Knowledge Assistant from a real
AI-product quality perspective rather than judging a single response.

The evaluation covers:

- Accuracy
- Latency
- Reliability
- Transparency
- Graceful degradation
- Natural-language user experience

The tests were executed against the actual Day 20 RAG pipeline.

---

## 2. Product Quality Dimensions

| Dimension | Definition |
|---|---|
| Accuracy | The system gives answers that are correct and supported by the available knowledge base. |
| Latency | The system responds quickly enough to provide a useful experience for its intended users. |
| Reliability | The system consistently completes requests without crashes, exceptions, or unstable behavior. |
| Transparency | The system clearly explains where an answer came from so a non-technical user can understand and verify it. |
| Graceful degradation | When relevant knowledge is unavailable, the system communicates uncertainty honestly instead of inventing facts. |

---

## 3. System Under Test

**Model:** `gpt-5.6-luna`

**Embedding model:** `all-MiniLM-L6-v2`

**Retrieval:** FAISS semantic search

**Top-K:** `3`

**Low-confidence threshold:** `0.3`

The Day 20 assistant retrieves relevant knowledge-base chunks,
formats them as context, sends them to the LLM using a grounding
prompt, and appends source information to the final answer.

---

## 4. Quality Scores

| Dimension | Tests | Passes | Pass Rate | Score |
|---|---:|---:|---:|---:|
| Accuracy | 10 | 0 | 0.0% | 1.0/5 |
| Latency | 10 | — | — | 5/5 |
| Reliability | 10 | 0 | 0.0% | 1.0/5 |
| Transparency | 10 | 0 | 0.0% | 1.0/5 |
| Graceful degradation | 10 | 0 | 0.0% | 1.0/5 |

### Overall Product Quality Score

**1.8/5**

---

## 5. Accuracy Evaluation

Ten factual questions were tested against known facts in the Day 20
knowledge base.

The evaluation checks:

1. Whether the expected fact appears in the answer.
2. Whether the expected source document was retrieved.
3. Whether the system successfully returned a response.

Detailed evidence is available in:

`results/quality_test_results.csv`

---

## 6. Reliability Evaluation

Reliability was evaluated across the same ten grounded questions.

A test passes when:

- the request completes successfully,
- no Python exception occurs,
- the assistant returns a non-empty answer.

This evaluates repeatable system behavior rather than the quality of
one individual answer.

---

## 7. Transparency Evaluation

A transparency test passes when the final user-visible response
contains a readable source citation.

For example:

`Sources: doc-001 — Company Overview`

This matters because a non-technical user should be able to understand
where the answer came from without seeing the internal retrieval
pipeline.

The detailed transparency results are included in:

`results/quality_test_results.csv`

---

## 8. Latency Evaluation

Ten independent grounded queries were measured end-to-end using
Python's `time.perf_counter()`.

### Average latency

| Pipeline Component | Average |
|---|---:|
| Retrieval / embedding + FAISS | 0.020s |
| Context formatting | 0.000s |
| LLM generation | 0.342s |
| **End-to-end** | **0.362s** |

### P95 End-to-End Latency

**0.408s**

### Largest latency contributor

**LLM generation**

This component should be the first target for performance
optimization.

Detailed measurements:

`results/latency_results.csv`

---

## 9. Graceful Degradation Evaluation

Ten questions about topics completely outside the NovaTech knowledge
base were tested.

The tests covered:

- Weather
- FIFA
- Cooking
- Bitcoin
- Passport renewal
- Geography
- Photosynthesis
- Tourism
- Compound interest
- Microsoft leadership

A pass required the assistant to communicate uncertainty rather than
inventing a knowledge-base answer.

Detailed results:

`results/graceful_degradation_results.csv`

---

## 10. Natural-Language User Evaluation

Ten user-style questions were intentionally written casually,
vaguely, or verbosely.

Examples include:

- "hey can u tell me where novatech is based?"
- "Who was the person behind that NovaMind project again?"
- "what's that internal docs thing called at NovaTech?"

Successful responses:

**0/10 (0.0%)**

Detailed outputs:

`results/user_style_results.csv`

This test is important because real users generally do not write
perfectly engineered benchmark questions.

---

## 11. What Passed

Based on the automated evaluation, the strongest areas are the
dimensions with the highest scores in the table above.

The Day 20 architecture already provides several useful product
foundations:

- Semantic retrieval through FAISS
- Grounded generation through a dedicated RAG prompt
- Explicit instruction not to invent facts
- Confidence measurement
- Low-confidence detection
- Source information in the final response
- Structured retrieval metadata
- Measurable pipeline components

---

## 12. Product Risks / What Can Fail

### Risk 1 — Retrieval relevance

Top-K retrieval can still return documents for an unrelated question.
A low-confidence threshold exists, but the application should make
abstention behavior a strict product rule.

### Risk 2 — Citation usability

Source IDs are useful for engineering evaluation, but a production
user may need more human-readable citation text explaining why a
source is relevant.

### Risk 3 — API dependency

The assistant depends on the LLM API. Production deployment should
handle timeouts, rate limits, API failures, and temporary outages.

### Risk 4 — Latency

LLM generation is expected to be the major latency contributor in
many RAG workloads. The measured bottleneck should determine the
actual optimization priority.

### Risk 5 — Natural-language ambiguity

Casual queries can produce different retrieval behavior from carefully
engineered benchmark questions.

---

## 13. Top Three Priorities Before Launch

### Priority 1 — Stronger relevance gating and abstention

The system should refuse to answer when retrieved evidence is not
strong enough to support the question.

This reduces hallucination risk.

### Priority 2 — Production-grade citation experience

Every answer should expose a clear, human-readable source that allows
the user to understand and verify the information.

### Priority 3 — Reliability and latency hardening

Add:

- API timeout handling
- Controlled retries
- Failure messages
- Latency monitoring
- Retrieval/generation metrics
- Caching where appropriate

---

## 14. Launch Decision

### Recommendation: NOT READY FOR REAL USERS YET

The Day 20 assistant is a strong engineering prototype, but a real
product launch should require reliable abstention, clear citations,
production error handling, and acceptable latency.

The audit demonstrates why AI product quality is broader than model
accuracy alone.

---

## 15. Evidence Files

Generated automatically by `audit.py`:

- `results/quality_test_results.csv`
- `results/graceful_degradation_results.csv`
- `results/latency_results.csv`
- `results/user_style_results.csv`
- `results/DAY21_PRODUCT_QUALITY_REPORT.md`

---

## 16. Final Score

**AI Product Quality Score: 1.8/5**

Day 21 completed through structured product-quality evaluation.
