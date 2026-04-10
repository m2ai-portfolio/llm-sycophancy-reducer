"""JSON file persistence for the prompt template library."""

import json
from pathlib import Path

from .models import LibraryState, PromptTemplate


def load_library(path: Path) -> LibraryState:
    """Load library from a JSON file. Returns empty state if file doesn't exist."""
    if not path.exists():
        return LibraryState()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return LibraryState(**data)
    except (json.JSONDecodeError, Exception):
        return LibraryState()


def save_library(state: LibraryState, path: Path) -> None:
    """Save library state to a JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(state.model_dump(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
