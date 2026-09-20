from dataclasses import dataclass, field
from typing import Any


@dataclass
class WorkflowState:
    topic: str

    retrieved_chunks: list[dict[str, Any]] = field(default_factory=list)

    extracted_points: list[str] = field(default_factory=list)

    synthesis_text: str = ""

    final_report: str = ""

    current_step: str = "start"

    error: str | None = None

    completed_steps: list[str] = field(default_factory=list)