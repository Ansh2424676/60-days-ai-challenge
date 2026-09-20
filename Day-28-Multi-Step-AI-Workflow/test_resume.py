from workflow import run_workflow


def main():
    topic = "AI Agents"

    # ========================================================
    # PHASE 1 — INTENTIONAL FAILURE
    # ========================================================

    print("=" * 60)
    print("PHASE 1 — INTENTIONAL FAILURE")
    print("=" * 60)

    failed_state = run_workflow(
        topic,
        resume=False,
        fail_at_step="synthesise_findings",
    )

    print("\nCompleted before failure:")
    print(failed_state.completed_steps)

    assert "search_sources" in failed_state.completed_steps
    assert "extract_key_points" in failed_state.completed_steps

    assert "synthesise_findings" not in (
        failed_state.completed_steps
    )

    print("\nResume checkpoint created successfully.")

    # ========================================================
    # PHASE 2 — RESUME
    # ========================================================

    print("\n" + "=" * 60)
    print("PHASE 2 — RESUME")
    print("=" * 60)

    resumed_state = run_workflow(
        topic,
        resume=True,
    )

    print("\nCompleted after resume:")
    print(resumed_state.completed_steps)

    assert "search_sources" in resumed_state.completed_steps
    assert "extract_key_points" in resumed_state.completed_steps
    assert "synthesise_findings" in resumed_state.completed_steps
    assert "format_report" in resumed_state.completed_steps

    print("\n" + "=" * 60)
    print("RESUME TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()