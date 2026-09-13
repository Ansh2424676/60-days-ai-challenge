import csv
import statistics
import sys
import time
from pathlib import Path


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DAY20_DIR = BASE_DIR.parent / "Day-20-AI-Knowledge-Assistant"

if not DAY20_DIR.exists():
    raise FileNotFoundError(
        f"Day 20 project not found at: {DAY20_DIR}"
    )

# Allow Python to import Day 20 pipeline
sys.path.insert(0, str(DAY20_DIR))


# ============================================================
# IMPORT DAY 20 PIPELINE
# ============================================================

from rag_pipeline import (
    OPENAI_MODEL,
    TOP_K,
    LOW_CONFIDENCE_THRESHOLD,
    answer_query,
    retrieve,
    format_context,
)


# ============================================================
# OUTPUT DIRECTORY
# ============================================================

OUT = BASE_DIR / "results"
OUT.mkdir(exist_ok=True)


# ============================================================
# PRODUCT QUALITY DEFINITIONS
# ============================================================

QUALITY_DEFINITIONS = {
    "accuracy": (
        "The system gives answers that are correct and supported "
        "by the available knowledge base."
    ),
    "latency": (
        "The system responds quickly enough to provide a useful "
        "experience for its intended users."
    ),
    "reliability": (
        "The system consistently completes requests without "
        "crashes, exceptions, or unstable behavior."
    ),
    "transparency": (
        "The system clearly explains where an answer came from "
        "so a non-technical user can understand and verify it."
    ),
    "graceful_degradation": (
        "When relevant knowledge is unavailable, the system "
        "communicates uncertainty honestly instead of inventing facts."
    ),
}


# ============================================================
# 10 ACCURACY / RELIABILITY / TRANSPARENCY TESTS
# ============================================================

GROUNDED_TESTS = [
    (
        "A01",
        "Where is NovaTech Solutions headquartered?",
        "Noida, India",
        ["doc-001"],
    ),
    (
        "A02",
        "Who led the NovaMind project?",
        "Priya Mehta",
        ["doc-005"],
    ),
    (
        "A03",
        "When was NovaMind launched?",
        "February 2026",
        ["doc-003"],
    ),
    (
        "A04",
        "What is NovaTech's internal documentation platform?",
        "AtlasHub",
        ["doc-006"],
    ),
    (
        "A05",
        "How long does AI Launchpad last?",
        "six weeks",
        ["doc-008"],
    ),
    (
        "A06",
        "What departments does NovaTech Solutions have?",
        "Artificial Intelligence, Data Engineering, and Cloud Infrastructure",
        ["doc-002"],
    ),
    (
        "A07",
        "What does NovaMind help employees with?",
        "company policies, projects, internal documentation, and technical procedures",
        ["doc-004"],
    ),
    (
        "A08",
        "What certification do employees receive after AI Launchpad?",
        "Nova AI Engineer Level 1",
        ["doc-009"],
    ),
    (
        "A09",
        "When is the weekly technical review meeting?",
        "Friday at 4 PM",
        ["doc-010"],
    ),
    (
        "A10",
        "What does AtlasHub contain?",
        "APIs, deployment procedures, incident response processes, and internal coding standards",
        ["doc-007"],
    ),
]


# ============================================================
# 10 OUT-OF-DOMAIN / UNKNOWN TESTS
# ============================================================

OOD_TESTS = [
    (
        "G01",
        "What is the weather in Delhi today?",
    ),
    (
        "G02",
        "Who won the latest FIFA World Cup?",
    ),
    (
        "G03",
        "How do I cook paneer butter masala?",
    ),
    (
        "G04",
        "What is the current price of Bitcoin?",
    ),
    (
        "G05",
        "How can I renew my Indian passport?",
    ),
    (
        "G06",
        "What is the capital of Australia?",
    ),
    (
        "G07",
        "Can you explain photosynthesis?",
    ),
    (
        "G08",
        "What are the best tourist places in Japan?",
    ),
    (
        "G09",
        "How do I calculate compound interest?",
    ),
    (
        "G10",
        "Who is the current CEO of Microsoft?",
    ),
]


# ============================================================
# 10 NATURAL USER-STYLE QUERIES
# ============================================================

USER_STYLE_TESTS = [
    (
        "U01",
        "hey can u tell me where novatech is based?",
    ),
    (
        "U02",
        "Who was the person behind that NovaMind project again?",
    ),
    (
        "U03",
        "so like when did NovaMind actually start?",
    ),
    (
        "U04",
        "what's that internal docs thing called at NovaTech?",
    ),
    (
        "U05",
        "AI Launchpad is for what exactly and how long is it?",
    ),
    (
        "U06",
        "can you just tell me the departments there, like all of them",
    ),
    (
        "U07",
        "I'm trying to understand NovaMind — what does it actually do for employees?",
    ),
    (
        "U08",
        "after finishing that AI Launchpad training, do people get some certificate?",
    ),
    (
        "U09",
        "when do the engineering folks have their weekly tech review?",
    ),
    (
        "U10",
        "what kind of stuff can I find inside AtlasHub?",
    ),
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def contains_expected(answer: str, expected: str) -> bool:
    """
    Flexible accuracy check.
    """

    answer_lower = answer.lower()

    if expected == (
        "Artificial Intelligence, Data Engineering, and Cloud Infrastructure"
    ):
        required = [
            "artificial intelligence",
            "data engineering",
            "cloud infrastructure",
        ]

        return all(item in answer_lower for item in required)

    if expected == (
        "company policies, projects, internal documentation, and technical procedures"
    ):
        required = [
            "company policies",
            "projects",
            "internal documentation",
            "technical procedures",
        ]

        return all(item in answer_lower for item in required)

    if expected == (
        "APIs, deployment procedures, incident response processes, and internal coding standards"
    ):
        required = [
            "apis",
            "deployment procedures",
            "incident response",
            "coding standards",
        ]

        return all(item in answer_lower for item in required)

    return expected.lower() in answer_lower


def has_honest_uncertainty(answer: str) -> bool:
    """
    Detect whether the assistant honestly communicates uncertainty.
    """

    if not answer:
        return False

    answer_lower = answer.lower()

    uncertainty_phrases = [
        "i don't know",
        "i do not know",
        "not in the provided context",
        "not provided in the context",
        "cannot be confirmed",
        "can't confirm",
        "insufficient information",
        "information is not available",
        "not available in the knowledge base",
        "based on the provided context",
        "does not contain",
        "not present in the context",
        "not supported by the provided context",
    ]

    return any(
        phrase in answer_lower
        for phrase in uncertainty_phrases
    )


def has_source_citation(answer: str) -> bool:
    """
    Check whether the final user-visible answer contains
    a readable source citation.
    """

    if not answer:
        return False

    answer_lower = answer.lower()

    has_source_word = (
        "source:" in answer_lower
        or "sources:" in answer_lower
        or "reference:" in answer_lower
        or "citation:" in answer_lower
    )

    has_doc_id = any(
        f"doc-{i:03d}" in answer_lower
        for i in range(1, 100)
    )

    return has_source_word and has_doc_id


def score_1_to_5(pass_rate: float) -> float:
    """
    Convert pass rate to a 1-5 score.
    0% = 1
    100% = 5
    """

    return round(1 + (4 * pass_rate), 2)


def run_single_query(query: str):
    """
    Run the actual Day 20 answer_query() function.
    """

    start = time.perf_counter()

    try:
        result = answer_query(query)

        total_latency = time.perf_counter() - start

        return {
            "success": True,
            "answer": result.get("answer", ""),
            "sources": result.get("sources", []),
            "confidence": result.get("confidence", 0.0),
            "low_confidence": result.get(
                "low_confidence",
                False,
            ),
            "latency_s": total_latency,
            "error": "",
        }

    except Exception as exc:

        total_latency = time.perf_counter() - start

        return {
            "success": False,
            "answer": "",
            "sources": [],
            "confidence": 0.0,
            "low_confidence": False,
            "latency_s": total_latency,
            "error": f"{type(exc).__name__}: {exc}",
        }


# ============================================================
# ACCURACY / RELIABILITY / TRANSPARENCY
# ============================================================

def run_grounded_tests():

    rows = []

    print("\n" + "=" * 70)
    print("1. ACCURACY / RELIABILITY / TRANSPARENCY TESTS")
    print("=" * 70)

    for test_id, query, expected, expected_docs in GROUNDED_TESTS:

        print(f"\nRunning {test_id}: {query}")

        result = run_single_query(query)

        answer = result["answer"]

        retrieved_ids = [
            source.get("id", "")
            for source in result["sources"]
        ]

        expected_doc_pass = any(
            doc in retrieved_ids
            for doc in expected_docs
        )

        accuracy_pass = (
            result["success"]
            and contains_expected(
                answer,
                expected,
            )
            and expected_doc_pass
        )

        reliability_pass = (
            result["success"]
            and bool(answer.strip())
        )

        transparency_pass = has_source_citation(answer)

        rows.append(
            {
                "test_id": test_id,
                "dimension": "accuracy",
                "query": query,
                "expected": expected,
                "answer": answer,
                "retrieved_ids": ",".join(retrieved_ids),
                "confidence": result["confidence"],
                "latency_s": round(
                    result["latency_s"],
                    4,
                ),
                "pass": accuracy_pass,
                "error": result["error"],
            }
        )

        rows.append(
            {
                "test_id": test_id,
                "dimension": "reliability",
                "query": query,
                "expected": "successful response without exception",
                "answer": answer,
                "retrieved_ids": ",".join(retrieved_ids),
                "confidence": result["confidence"],
                "latency_s": round(
                    result["latency_s"],
                    4,
                ),
                "pass": reliability_pass,
                "error": result["error"],
            }
        )

        rows.append(
            {
                "test_id": test_id,
                "dimension": "transparency",
                "query": query,
                "expected": "readable source citation in final answer",
                "answer": answer,
                "retrieved_ids": ",".join(retrieved_ids),
                "confidence": result["confidence"],
                "latency_s": round(
                    result["latency_s"],
                    4,
                ),
                "pass": transparency_pass,
                "error": result["error"],
            }
        )

        print(
            f"  Accuracy:      {'PASS' if accuracy_pass else 'FAIL'}"
        )

        print(
            f"  Reliability:   {'PASS' if reliability_pass else 'FAIL'}"
        )

        print(
            f"  Transparency:  {'PASS' if transparency_pass else 'FAIL'}"
        )

    return rows


# ============================================================
# GRACEFUL DEGRADATION
# ============================================================

def run_graceful_degradation_tests():

    rows = []

    print("\n" + "=" * 70)
    print("2. GRACEFUL DEGRADATION TESTS")
    print("=" * 70)

    for test_id, query in OOD_TESTS:

        print(f"\nRunning {test_id}: {query}")

        result = run_single_query(query)

        answer = result["answer"]

        honest = has_honest_uncertainty(answer)

        no_exception = result["success"]

        passed = (
            honest
            and no_exception
        )

        retrieved_ids = [
            source.get("id", "")
            for source in result["sources"]
        ]

        rows.append(
            {
                "test_id": test_id,
                "dimension": "graceful_degradation",
                "query": query,
                "expected": "honest uncertainty / no invented answer",
                "answer": answer,
                "retrieved_ids": ",".join(retrieved_ids),
                "confidence": result["confidence"],
                "low_confidence": result["low_confidence"],
                "latency_s": round(
                    result["latency_s"],
                    4,
                ),
                "pass": passed,
                "error": result["error"],
            }
        )

        print(
            f"  Honest uncertainty: "
            f"{'PASS' if honest else 'FAIL'}"
        )

        print(
            f"  No exception: "
            f"{'PASS' if no_exception else 'FAIL'}"
        )

    return rows


# ============================================================
# LATENCY TEST
# ============================================================

def run_latency_tests():

    rows = []

    print("\n" + "=" * 70)
    print("3. LATENCY TEST — 10 QUERIES")
    print("=" * 70)

    for test_id, query, _, _ in GROUNDED_TESTS:

        print(f"\nTiming {test_id}: {query}")

        total_start = time.perf_counter()

        # ----------------------------------------------------
        # Component 1: Retrieval
        # ----------------------------------------------------

        retrieval_start = time.perf_counter()

        retrieved = retrieve(
            query,
            k=TOP_K,
        )

        retrieval_s = (
            time.perf_counter()
            - retrieval_start
        )

        # ----------------------------------------------------
        # Component 2: Context formatting
        # ----------------------------------------------------

        context_start = time.perf_counter()

        context = format_context(
            retrieved
        )

        context_s = (
            time.perf_counter()
            - context_start
        )

        # ----------------------------------------------------
        # Component 3: LLM generation
        # ----------------------------------------------------

        user_prompt = f"""
CONTEXT
=======

{context}

QUESTION
========

{query}
"""

        generation_start = time.perf_counter()

        error = ""

        try:

            from rag_pipeline import client, RAG_SYSTEM_PROMPT

            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": RAG_SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature=0,
            )

            _ = response.choices[0].message.content

        except Exception as exc:

            error = (
                f"{type(exc).__name__}: {exc}"
            )

        generation_s = (
            time.perf_counter()
            - generation_start
        )

        # ----------------------------------------------------
        # End-to-end
        # ----------------------------------------------------

        total_s = (
            time.perf_counter()
            - total_start
        )

        rows.append(
            {
                "test_id": test_id,
                "query": query,
                "retrieval_s": round(
                    retrieval_s,
                    4,
                ),
                "context_formatting_s": round(
                    context_s,
                    4,
                ),
                "generation_s": round(
                    generation_s,
                    4,
                ),
                "end_to_end_s": round(
                    total_s,
                    4,
                ),
                "error": error,
            }
        )

        print(
            f"  Retrieval: {retrieval_s:.3f}s"
        )

        print(
            f"  Context:   {context_s:.3f}s"
        )

        print(
            f"  Generation:{generation_s:.3f}s"
        )

        print(
            f"  Total:     {total_s:.3f}s"
        )

    return rows


# ============================================================
# NATURAL LANGUAGE USER TEST
# ============================================================

def run_user_style_tests():

    rows = []

    print("\n" + "=" * 70)
    print("4. NATURAL USER-STYLE QUERIES")
    print("=" * 70)

    for test_id, query in USER_STYLE_TESTS:

        print(f"\nRunning {test_id}: {query}")

        result = run_single_query(query)

        answer = result["answer"]

        retrieved_ids = [
            source.get("id", "")
            for source in result["sources"]
        ]

        rows.append(
            {
                "test_id": test_id,
                "query": query,
                "answer": answer,
                "retrieved_ids": ",".join(
                    retrieved_ids
                ),
                "confidence": result["confidence"],
                "low_confidence": result["low_confidence"],
                "latency_s": round(
                    result["latency_s"],
                    4,
                ),
                "success": result["success"],
                "error": result["error"],
            }
        )

        print(
            f"  Success: "
            f"{'YES' if result['success'] else 'NO'}"
        )

        print(
            f"  Confidence: "
            f"{result['confidence']}"
        )

    return rows


# ============================================================
# CSV WRITER
# ============================================================

def write_csv(path: Path, rows: list[dict]):

    if not rows:
        return

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=list(rows[0].keys()),
        )

        writer.writeheader()
        writer.writerows(rows)


# ============================================================
# REPORT GENERATION
# ============================================================

def make_report(
    quality_rows,
    graceful_rows,
    latency_rows,
    user_rows,
):

    def dimension_stats(dimension):

        subset = [
            row
            for row in quality_rows
            if row["dimension"] == dimension
        ]

        passed = sum(
            bool(row["pass"])
            for row in subset
        )

        total = len(subset)

        rate = (
            passed / total
            if total
            else 0
        )

        return (
            total,
            passed,
            rate,
            score_1_to_5(rate),
        )

    accuracy = dimension_stats(
        "accuracy"
    )

    reliability = dimension_stats(
        "reliability"
    )

    transparency = dimension_stats(
        "transparency"
    )

    graceful_total = len(
        graceful_rows
    )

    graceful_passes = sum(
        bool(row["pass"])
        for row in graceful_rows
    )

    graceful_rate = (
        graceful_passes / graceful_total
        if graceful_total
        else 0
    )

    graceful_score = score_1_to_5(
        graceful_rate
    )

    # --------------------------------------------------------
    # Latency statistics
    # --------------------------------------------------------

    e2e_values = [
        row["end_to_end_s"]
        for row in latency_rows
    ]

    retrieval_values = [
        row["retrieval_s"]
        for row in latency_rows
    ]

    context_values = [
        row["context_formatting_s"]
        for row in latency_rows
    ]

    generation_values = [
        row["generation_s"]
        for row in latency_rows
    ]

    avg_e2e = statistics.mean(
        e2e_values
    )

    avg_retrieval = statistics.mean(
        retrieval_values
    )

    avg_context = statistics.mean(
        context_values
    )

    avg_generation = statistics.mean(
        generation_values
    )

    p95_e2e = sorted(
        e2e_values
    )[
        min(
            len(e2e_values) - 1,
            int(
                0.95 * len(e2e_values)
            ),
        )
    ]

    components = {
        "Retrieval / embedding + FAISS":
            avg_retrieval,

        "Context formatting":
            avg_context,

        "LLM generation":
            avg_generation,
    }

    bottleneck = max(
        components,
        key=components.get,
    )

    # --------------------------------------------------------
    # Latency score
    # --------------------------------------------------------

    if avg_e2e <= 2:
        latency_score = 5
    elif avg_e2e <= 4:
        latency_score = 4
    elif avg_e2e <= 7:
        latency_score = 3
    elif avg_e2e <= 10:
        latency_score = 2
    else:
        latency_score = 1

    # --------------------------------------------------------
    # User style success
    # --------------------------------------------------------

    user_successes = sum(
        bool(row["success"])
        for row in user_rows
    )

    user_total = len(
        user_rows
    )

    user_success_rate = (
        user_successes / user_total
        if user_total
        else 0
    )

    # --------------------------------------------------------
    # Overall score
    # --------------------------------------------------------

    all_scores = [
        accuracy[3],
        latency_score,
        reliability[3],
        transparency[3],
        graceful_score,
    ]

    overall_score = round(
        statistics.mean(all_scores),
        2,
    )

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    report = f"""# Day 21 — AI Product Quality Audit

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
| Accuracy | {QUALITY_DEFINITIONS["accuracy"]} |
| Latency | {QUALITY_DEFINITIONS["latency"]} |
| Reliability | {QUALITY_DEFINITIONS["reliability"]} |
| Transparency | {QUALITY_DEFINITIONS["transparency"]} |
| Graceful degradation | {QUALITY_DEFINITIONS["graceful_degradation"]} |

---

## 3. System Under Test

**Model:** `{OPENAI_MODEL}`

**Embedding model:** `all-MiniLM-L6-v2`

**Retrieval:** FAISS semantic search

**Top-K:** `{TOP_K}`

**Low-confidence threshold:** `{LOW_CONFIDENCE_THRESHOLD}`

The Day 20 assistant retrieves relevant knowledge-base chunks,
formats them as context, sends them to the LLM using a grounding
prompt, and appends source information to the final answer.

---

## 4. Quality Scores

| Dimension | Tests | Passes | Pass Rate | Score |
|---|---:|---:|---:|---:|
| Accuracy | {accuracy[0]} | {accuracy[1]} | {accuracy[2] * 100:.1f}% | {accuracy[3]}/5 |
| Latency | 10 | — | — | {latency_score}/5 |
| Reliability | {reliability[0]} | {reliability[1]} | {reliability[2] * 100:.1f}% | {reliability[3]}/5 |
| Transparency | {transparency[0]} | {transparency[1]} | {transparency[2] * 100:.1f}% | {transparency[3]}/5 |
| Graceful degradation | {graceful_total} | {graceful_passes} | {graceful_rate * 100:.1f}% | {graceful_score}/5 |

### Overall Product Quality Score

**{overall_score}/5**

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
| Retrieval / embedding + FAISS | {avg_retrieval:.3f}s |
| Context formatting | {avg_context:.3f}s |
| LLM generation | {avg_generation:.3f}s |
| **End-to-end** | **{avg_e2e:.3f}s** |

### P95 End-to-End Latency

**{p95_e2e:.3f}s**

### Largest latency contributor

**{bottleneck}**

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

**{user_successes}/{user_total} ({user_success_rate * 100:.1f}%)**

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

**AI Product Quality Score: {overall_score}/5**

Day 21 completed through structured product-quality evaluation.
"""


    report_path = (
        OUT / "DAY21_PRODUCT_QUALITY_REPORT.md"
    )

    report_path.write_text(
        report,
        encoding="utf-8",
    )

    return report_path


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("DAY 21 — AI PRODUCT QUALITY AUDIT")
    print("=" * 70)

    print(
        f"\nDay 20 directory: {DAY20_DIR}"
    )

    print(
        f"Model: {OPENAI_MODEL}"
    )

    print(
        f"Top-K: {TOP_K}"
    )

    # --------------------------------------------------------
    # Run evaluations
    # --------------------------------------------------------

    quality_rows = run_grounded_tests()

    graceful_rows = (
        run_graceful_degradation_tests()
    )

    latency_rows = run_latency_tests()

    user_rows = run_user_style_tests()

    # --------------------------------------------------------
    # Save CSV files
    # --------------------------------------------------------

    write_csv(
        OUT / "quality_test_results.csv",
        quality_rows,
    )

    write_csv(
        OUT / "graceful_degradation_results.csv",
        graceful_rows,
    )

    write_csv(
        OUT / "latency_results.csv",
        latency_rows,
    )

    write_csv(
        OUT / "user_style_results.csv",
        user_rows,
    )

    # --------------------------------------------------------
    # Generate final report
    # --------------------------------------------------------

    report_path = make_report(
        quality_rows,
        graceful_rows,
        latency_rows,
        user_rows,
    )

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("DAY 21 AUDIT COMPLETED")
    print("=" * 70)

    print("\nGenerated files:")

    print(
        "  results/quality_test_results.csv"
    )

    print(
        "  results/graceful_degradation_results.csv"
    )

    print(
        "  results/latency_results.csv"
    )

    print(
        "  results/user_style_results.csv"
    )

    print(
        "  results/DAY21_PRODUCT_QUALITY_REPORT.md"
    )

    print(
        f"\nReport: {report_path}"
    )

    print("\nDone!")