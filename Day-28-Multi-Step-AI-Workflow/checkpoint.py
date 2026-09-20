import json
from dataclasses import asdict
from pathlib import Path

from state import WorkflowState


CHECKPOINT_DIR = Path("checkpoints")


def ensure_checkpoint_directory():
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)


def checkpoint_path(step_name: str) -> Path:
    return CHECKPOINT_DIR / f"{step_name}.json"


def save_checkpoint(state: WorkflowState, step_name: str):
    ensure_checkpoint_directory()

    state.current_step = step_name

    path = checkpoint_path(step_name)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            asdict(state),
            file,
            indent=2,
            ensure_ascii=False
        )

    print(f"[CHECKPOINT SAVED] {path}")


def load_checkpoint(step_name: str) -> WorkflowState | None:
    path = checkpoint_path(step_name)

    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return WorkflowState(**data)


def checkpoint_exists(step_name: str) -> bool:
    return checkpoint_path(step_name).exists()