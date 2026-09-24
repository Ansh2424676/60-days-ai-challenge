import json
import logging
from pathlib import Path

from checkpoint import (
    checkpoint_exists,
    load_checkpoint,
    save_checkpoint,
)

from state import WorkflowState

from steps import (
    search_sources,
    extract_key_points,
    synthesise_findings,
    format_report,
)


STEPS = [
    "search_sources",
    "extract_key_points",
    "synthesise_findings",
    "format_report",
]


# ============================================================
# LOGGING
# ============================================================

Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    filename="logs/workflow.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


# ============================================================
# STATE SNAPSHOT
# ============================================================

def state_snapshot(state: WorkflowState) -> dict:
    """
    Create a lightweight snapshot of the workflow state.
    """

    return {
        "topic": state.topic,
        "current_step": state.current_step,
        "retrieved_chunks": len(state.retrieved_chunks),
        "extracted_points": len(state.extracted_points),
        "has_synthesis": bool(state.synthesis_text),
        "has_report": bool(state.final_report),
        "completed_steps": state.completed_steps,
        "error": state.error,
    }


# ============================================================
# SAVE PARTIAL RESULTS
# ============================================================

def save_partial_results(state: WorkflowState):
    """
    Save partial workflow results when a step fails.
    """

    Path("reports").mkdir(exist_ok=True)

    safe_topic = (
        state.topic
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
    )

    path = Path("reports") / f"{safe_topic}_partial.json"

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            {
                "state": state_snapshot(state),
                "retrieved_chunks": state.retrieved_chunks,
                "extracted_points": state.extracted_points,
                "synthesis_text": state.synthesis_text,
                "final_report": state.final_report,
            },
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(f"[PARTIAL RESULTS] {path}")


# ============================================================
# SAVE FINAL REPORT
# ============================================================

def save_final_report(state: WorkflowState):
    """
    Save completed report as Markdown.
    """

    Path("reports").mkdir(exist_ok=True)

    safe_topic = (
        state.topic
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
    )

    path = Path("reports") / f"{safe_topic}_report.md"

    with open(path, "w", encoding="utf-8") as file:
        file.write(state.final_report)

    print(f"[REPORT SAVED] {path}")


# ============================================================
# ERROR HANDLER
# ============================================================

def handle_error(
    state: WorkflowState,
    step_name: str,
    exc: Exception,
):
    """
    Handle workflow errors and preserve partial results.
    """

    state.error = str(exc)

    logging.error(
        "Step failed: %s | State: %s | Error: %s",
        step_name,
        state_snapshot(state),
        exc,
    )

    print(f"[ERROR] Step: {step_name}")
    print(f"[ERROR] {exc}")

    save_partial_results(state)

    return state


# ============================================================
# MAIN WORKFLOW
# ============================================================

def run_workflow(
    topic: str,
    resume: bool = True,
    fail_at_step: str | None = None,
):
    """
    Run the complete multi-step AI workflow.

    Parameters
    ----------
    topic:
        Research topic.

    resume:
        Whether to resume from the latest checkpoint.

    fail_at_step:
        Used for testing intentional failures.
    """

    state = None

    # --------------------------------------------------------
    # RESUME FROM LATEST CHECKPOINT
    # --------------------------------------------------------

    if resume:

        for step in reversed(STEPS):

            if checkpoint_exists(step):

                state = load_checkpoint(step)

                print(
                    f"[RESUME] Loaded checkpoint: {step}"
                )

                break

    # --------------------------------------------------------
    # CREATE NEW STATE
    # --------------------------------------------------------

    if state is None:

        state = WorkflowState(
            topic=topic
        )

    # --------------------------------------------------------
    # STEP 1 — SEARCH SOURCES
    # --------------------------------------------------------

    if "search_sources" not in state.completed_steps:

        try:

            state.current_step = "search_sources"

            state.retrieved_chunks = search_sources(
                state.topic
            )

            state.completed_steps.append(
                "search_sources"
            )

            save_checkpoint(
                state,
                "search_sources"
            )

        except Exception as exc:

            return handle_error(
                state,
                "search_sources",
                exc
            )

    # --------------------------------------------------------
    # STEP 2 — EXTRACT KEY POINTS
    # --------------------------------------------------------

    if "extract_key_points" not in state.completed_steps:

        try:

            state.current_step = "extract_key_points"

            state.extracted_points = extract_key_points(
                state.retrieved_chunks
            )

            state.completed_steps.append(
                "extract_key_points"
            )

            save_checkpoint(
                state,
                "extract_key_points"
            )

        except Exception as exc:

            return handle_error(
                state,
                "extract_key_points",
                exc
            )

    # --------------------------------------------------------
    # STEP 3 — SYNTHESISE FINDINGS
    # --------------------------------------------------------

    if "synthesise_findings" not in state.completed_steps:

        try:

            state.current_step = "synthesise_findings"

            # Intentional failure for resume testing
            if fail_at_step == "synthesise_findings":

                raise RuntimeError(
                    "Intentional failure for resume testing."
                )

            state.synthesis_text = synthesise_findings(
                state.extracted_points
            )

            state.completed_steps.append(
                "synthesise_findings"
            )

            save_checkpoint(
                state,
                "synthesise_findings"
            )

        except Exception as exc:

            return handle_error(
                state,
                "synthesise_findings",
                exc
            )

    # --------------------------------------------------------
    # STEP 4 — FORMAT REPORT
    # --------------------------------------------------------

    if "format_report" not in state.completed_steps:

        try:

            state.current_step = "format_report"

            state.final_report = format_report(
                state.synthesis_text
            )

            state.completed_steps.append(
                "format_report"
            )

            save_checkpoint(
                state,
                "format_report"
            )

        except Exception as exc:

            return handle_error(
                state,
                "format_report",
                exc
            )

    # --------------------------------------------------------
    # FINAL REPORT
    # --------------------------------------------------------

    save_final_report(state)

    return state


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":

    topic = input(
        "Enter research topic: "
    ).strip()

    result = run_workflow(topic)

    print("\n" + "=" * 60)
    print("WORKFLOW RESULT")
    print("=" * 60)

    print(
        "Completed steps:",
        result.completed_steps
    )

    if result.error:

        print(
            f"Workflow stopped: {result.error}"
        )

    else:

        print("\nFinal Report:\n")
        print(result.final_report)