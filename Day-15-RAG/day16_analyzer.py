import json


INPUT_FILE = "rag_results_day16.json"
OUTPUT_FILE = "scorecard_day16.json"


# ============================================================
# LOAD RESULTS
# ============================================================

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)


tests = data["tests"]


# ============================================================
# ANALYSIS
# ============================================================

analysis_results = []


for item in tests:

    failure_mode = item["failure_mode"]
    retrieved_ids = item["retrieved_ids"]
    expected_docs = item["expected_docs"]

    best_distance = item["best_distance"]


    # --------------------------------------------------------
    # Retrieval quality score: 1–5
    # --------------------------------------------------------

    if failure_mode == "retrieval_failure":

        # Unsupported questions should ideally be rejected.
        # Since our retriever still returns chunks, retrieval
        # confidence is weak.

        retrieval_quality = 1

        diagnosis = (
            "Retrieval failure: the query has no supporting "
            "document, but the retriever still returns unrelated "
            "NovaTech chunks."
        )


    elif failure_mode == "context_window_overflow":

        # Top-3 retrieval cannot cover all requested topics.

        matched = len(
            set(expected_docs) &
            set(retrieved_ids)
        )

        coverage = (
            matched / len(expected_docs)
            if expected_docs
            else 0
        )

        if coverage >= 0.8:
            retrieval_quality = 5
        elif coverage >= 0.6:
            retrieval_quality = 4
        elif coverage >= 0.4:
            retrieval_quality = 3
        elif coverage >= 0.2:
            retrieval_quality = 2
        else:
            retrieval_quality = 1

        diagnosis = (
            f"Context coverage failure: the query requests "
            f"many topics, but top-k retrieval returned only "
            f"{len(retrieved_ids)} chunks."
        )


    elif failure_mode in [
        "answer_context_mismatch",
        "correct_chunk_wrong_answer"
    ]:

        matched = len(
            set(expected_docs) &
            set(retrieved_ids)
        )

        if matched > 0:

            retrieval_quality = 5

            if failure_mode == "answer_context_mismatch":

                diagnosis = (
                    "Retrieval succeeded because the relevant "
                    "chunk was retrieved; any wrong final answer "
                    "would indicate answer-generation mismatch."
                )

            else:

                diagnosis = (
                    "The correct chunk was retrieved, so a wrong "
                    "answer would be a generation-stage failure."
                )

        else:

            retrieval_quality = 1

            diagnosis = (
                "The expected supporting chunk was not retrieved "
                "in the top-k results."
            )


    elif failure_mode == "vague_context_retrieved":

        matched = len(
            set(expected_docs) &
            set(retrieved_ids)
        )

        if matched >= 2:
            retrieval_quality = 4
        elif matched == 1:
            retrieval_quality = 3
        else:
            retrieval_quality = 1

        diagnosis = (
            "The query is broad, so multiple related chunks are "
            "retrieved instead of one sharply targeted passage."
        )


    else:

        retrieval_quality = 3

        diagnosis = (
            "Retrieval behavior requires manual inspection."
        )


    # --------------------------------------------------------
    # Answer quality
    # --------------------------------------------------------

    if item["generated_answer"] is None:

        answer_quality = None

        answer_status = (
            "Pending: OpenAI generation unavailable because "
            "API credits are exhausted."
        )

    else:

        answer_quality = item.get(
            "answer_quality",
            None
        )

        answer_status = "Generated answer available."


    # --------------------------------------------------------
    # Create analysis record
    # --------------------------------------------------------

    analysis_results.append({

        "test_id": item["test_id"],

        "failure_mode": failure_mode,

        "query": item["query"],

        "expected_docs": expected_docs,

        "retrieved_ids": retrieved_ids,

        "best_distance": best_distance,

        "retrieval_quality": retrieval_quality,

        "answer_quality": answer_quality,

        "answer_status": answer_status,

        "diagnosis": diagnosis

    })


# ============================================================
# SCORECARD
# ============================================================

retrieval_scores = [
    item["retrieval_quality"]
    for item in analysis_results
]


answer_scores = [
    item["answer_quality"]
    for item in analysis_results
    if item["answer_quality"] is not None
]


retrieval_average = (
    sum(retrieval_scores) /
    len(retrieval_scores)
)


answer_average = (
    sum(answer_scores) /
    len(answer_scores)
    if answer_scores
    else None
)


# ============================================================
# SUMMARY
# ============================================================

summary = {

    "total_tests": len(analysis_results),

    "retrieval_average_1_to_5":
        round(retrieval_average, 2),

    "answer_average_1_to_5":
        (
            round(answer_average, 2)
            if answer_average is not None
            else None
        ),

    "answer_tests_available":
        len(answer_scores),

    "answer_tests_pending":
        len(analysis_results) - len(answer_scores),

    "generation_status":
        "Pending because OpenAI API credits are exhausted."

}


# ============================================================
# SAVE
# ============================================================

output = {

    "summary": summary,

    "tests": analysis_results

}


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        output,
        f,
        indent=2,
        ensure_ascii=False
    )


# ============================================================
# PRINT SCORECARD
# ============================================================

print("\n" + "=" * 70)

print("DAY 16 SCORECARD")

print("=" * 70)

print(
    f"Total tests: {summary['total_tests']}"
)

print(
    f"Average retrieval quality: "
    f"{summary['retrieval_average_1_to_5']}/5"
)

print(
    f"Average answer quality: "
    f"{summary['answer_average_1_to_5']}/5"
)

print(
    f"Answer tests pending: "
    f"{summary['answer_tests_pending']}"
)

print("=" * 70)

print(
    f"\nSaved to: {OUTPUT_FILE}"
)