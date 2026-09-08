import json
from statistics import mean


# ============================================================
# FILE CONFIGURATION
# ============================================================

INPUT_FILE = "rag_results_day16_final.json"
SCORECARD_FILE = "scorecard_day16_final.json"
REPORT_FILE = "failure_analysis_day16.md"


# ============================================================
# LOAD RESULTS
# ============================================================

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

metadata = data["metadata"]
tests = data["tests"]

print("=" * 70)
print("DAY 16 — GENERATING FINAL REPORT")
print("=" * 70)


# ============================================================
# RETRIEVAL QUALITY SCORE
# ============================================================

def calculate_retrieval_score(test):

    coverage = test["retrieval_coverage"]
    expected_docs = test["expected_docs"]
    retrieval_success = test["retrieval_success"]

    # Unsupported query
    if len(expected_docs) == 0:

        if retrieval_success:
            return 5
        else:
            return 1

    # Supported query
    if coverage >= 1.0:
        return 5

    elif coverage >= 0.75:
        return 4

    elif coverage >= 0.50:
        return 3

    elif coverage > 0:
        return 2

    else:
        return 1


# ============================================================
# DIAGNOSES
# ============================================================

diagnoses = {

    "Q01":
        "The distance threshold correctly rejected the unsupported vacation-policy query.",

    "Q02":
        "The distance threshold correctly rejected the unsupported production-database query.",

    "Q03":
        "The retriever still returned semantically similar company chunks for the unsupported CFO query, creating a false-positive retrieval.",

    "Q04":
        "Query decomposition improved multi-topic retrieval coverage to 90%, although AtlasHub's platform-description chunk was still missed.",

    "Q05":
        "Query decomposition improved broad-query coverage to 90%, but one expected document was still not retrieved.",

    "Q06":
        "Query decomposition improved broad-query coverage to 88%, but some documents outside the requested internal topics were also retrieved.",

    "Q07":
        "The correct project-lead chunk was retrieved, so any answer mismatch would occur during generation rather than retrieval.",

    "Q08":
        "The correct AI Launchpad duration chunk was retrieved, so generation is the remaining evaluation stage.",

    "Q09":
        "The correct headquarters chunk was retrieved, although an unrelated department chunk was also included.",

    "Q10":
        "NovaMind retrieval was relevant but incomplete because the project-lead document was not retrieved.",

    "Q11":
        "AtlasHub retrieval was incomplete because only the documentation-content chunk was retrieved.",

    "Q12":
        "AI Launchpad retrieval was incomplete because the certification document was not retrieved.",

    "Q13":
        "The correct headquarters chunk was retrieved, so a wrong answer would be a generation-level failure.",

    "Q14":
        "The correct NovaMind project-lead chunk was retrieved, so this test isolates the generation stage.",

    "Q15":
        "The correct certification chunk was retrieved, so any wrong answer would be a generation-level failure."
}


# ============================================================
# PROCESS ALL TESTS
# ============================================================

processed_tests = []

for test in tests:

    test_id = test["test_id"]

    retrieval_score = calculate_retrieval_score(test)

    processed_tests.append({
        "test_id": test_id,
        "failure_mode": test["failure_mode"],
        "query": test["query"],
        "expected_docs": test["expected_docs"],
        "retrieved_ids": test["retrieved_ids"],
        "retrieval_success": test["retrieval_success"],
        "retrieval_coverage": test["retrieval_coverage"],
        "best_distance": test["best_distance"],
        "retrieval_quality": retrieval_score,
        "generated_answer": test["generated_answer"],
        "answer_quality": test["answer_quality"],
        "diagnosis": diagnoses.get(
            test_id,
            "No diagnosis available."
        )
    })


# ============================================================
# SUMMARY METRICS
# ============================================================

total_tests = len(processed_tests)

successful_retrievals = sum(
    1
    for test in processed_tests
    if test["retrieval_success"]
)

retrieval_success_rate = (
    successful_retrievals / total_tests
)

average_coverage = mean(
    test["retrieval_coverage"]
    for test in processed_tests
)

average_retrieval_quality = mean(
    test["retrieval_quality"]
    for test in processed_tests
)

# Answer quality is unavailable because generation
# was not executed due to exhausted API credits.

answer_quality_values = [
    test["answer_quality"]
    for test in processed_tests
    if test["answer_quality"] is not None
]

if answer_quality_values:
    average_answer_quality = mean(answer_quality_values)
else:
    average_answer_quality = None


# ============================================================
# SCORECARD JSON
# ============================================================

scorecard = {

    "project":
        "Day 16 - Diagnosing RAG Failure Modes",

    "total_tests":
        total_tests,

    "successful_retrieval_behavior":
        f"{successful_retrievals}/{total_tests}",

    "retrieval_success_rate":
        round(retrieval_success_rate, 2),

    "average_retrieval_coverage":
        round(average_coverage, 2),

    "average_retrieval_quality":
        round(average_retrieval_quality, 2),

    "average_answer_quality":
        average_answer_quality,

    "answer_evaluation_status":
        "Pending — OpenAI generation unavailable because API credits are exhausted.",

    "embedding_model":
        metadata["embedding_model"],

    "embedding_dimension":
        metadata["embedding_dimension"],

    "retrieval_method":
        metadata["retrieval_method"],

    "baseline_top_k":
        metadata["baseline_top_k"],

    "subquery_top_k":
        metadata["subquery_top_k"],

    "distance_threshold":
        metadata["distance_threshold"],

    "fix_1":
        metadata["fix_1"],

    "fix_2":
        metadata["fix_2"]
}


with open(
    SCORECARD_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        scorecard,
        f,
        indent=2,
        ensure_ascii=False
    )


# ============================================================
# FAILURE TABLE
# ============================================================

table_rows = []

for test in processed_tests:

    retrieved = ", ".join(test["retrieved_ids"])

    if not retrieved:
        retrieved = "None"

    expected = ", ".join(test["expected_docs"])

    if not expected:
        expected = "None"

    row = (
        f"| {test['test_id']} "
        f"| {test['failure_mode']} "
        f"| {test['query']} "
        f"| {expected} "
        f"| {retrieved} "
        f"| {test['retrieval_coverage']:.2f} "
        f"| {test['retrieval_quality']}/5 "
        f"| {test['diagnosis']} |"
    )

    table_rows.append(row)

failure_table = "\n".join(table_rows)


# ============================================================
# MARKDOWN REPORT
# ============================================================

report = f"""# Day 16 — Diagnosing RAG Failure Modes

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
| Knowledge Base Documents | {metadata["document_count"]} |
| Embedding Model | {metadata["embedding_model"]} |
| Embedding Dimension | {metadata["embedding_dimension"]} |
| Vector Index | {metadata["retrieval_method"]} |
| Baseline Top-K | {metadata["baseline_top_k"]} |
| Sub-query Top-K | {metadata["subquery_top_k"]} |
| Distance Threshold | {metadata["distance_threshold"]} |

---

## 3. Test Results

| ID | Failure Mode | Query | Expected Docs | Retrieved Docs | Coverage | Retrieval Quality | Diagnosis |
|---|---|---|---|---|---:|---:|---|
{failure_table}

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
| Total Tests | {total_tests} |
| Successful Retrieval Behavior | {successful_retrievals}/{total_tests} |
| Retrieval Success Rate | {retrieval_success_rate:.0%} |
| Average Retrieval Coverage | {average_coverage:.2f} |
| Average Retrieval Quality | {average_retrieval_quality:.2f}/5 |
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
- Retrieval behavior achieved {successful_retrievals}/{total_tests}.

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

- **{successful_retrievals}/{total_tests} successful retrieval behavior**
- **{retrieval_success_rate:.0%} retrieval success rate**
- **{average_coverage:.2f} average retrieval coverage**
- **{average_retrieval_quality:.2f}/5 average retrieval quality**

Answer-quality evaluation remains pending until OpenAI API generation
is available.

---

## 12. Submission Files

- `day16_final.py`
- `day16_report.py`
- `rag_results_day16_final.json`
- `scorecard_day16_final.json`
- `failure_analysis_day16.md`
"""


with open(
    REPORT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(report)


# ============================================================
# FINAL OUTPUT
# ============================================================

print("=" * 70)
print("DAY 16 REPORT GENERATED SUCCESSFULLY")
print("=" * 70)

print(f"Total tests: {total_tests}")

print(
    f"Successful retrieval behavior: "
    f"{successful_retrievals}/{total_tests}"
)

print(
    f"Retrieval success rate: "
    f"{retrieval_success_rate:.0%}"
)

print(
    f"Average retrieval coverage: "
    f"{average_coverage:.2f}"
)

print(
    f"Average retrieval quality: "
    f"{average_retrieval_quality:.2f}/5"
)

print("Average answer quality: PENDING")

print()
print(f"Created: {SCORECARD_FILE}")
print(f"Created: {REPORT_FILE}")

print("=" * 70)