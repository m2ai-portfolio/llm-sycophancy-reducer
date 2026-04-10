"""Unit tests for JSON persistence (load/save library)."""

import json
from pathlib import Path

from llmsyc.lib import load_library, save_library
from llmsyc.models import LibraryState, PromptTemplate


def test_load_library(tmp_path: Path) -> None:
    lib_file = tmp_path / "lib.json"

    # Valid JSON file
    data = {
        "templates": {
            "greet": {
                "key": "greet",
                "trigger": "greet",
                "replacement": "Greet concisely",
                "priority": 0,
            }
        },
        "attempts": 0,
        "hits": 0,
        "saved_tokens": 0,
    }
    lib_file.write_text(json.dumps(data), encoding="utf-8")

    state = load_library(lib_file)
    assert isinstance(state, LibraryState)
    assert state.templates["greet"].replacement == "Greet concisely"
    assert state.templates["greet"].trigger == "greet"

    # Nonexistent path returns empty state (no crash)
    empty_state = load_library(tmp_path / "nonexistent.json")
    assert isinstance(empty_state, LibraryState)
    assert len(empty_state.templates) == 0


def test_save_library(tmp_path: Path) -> None:
    lib_file = tmp_path / "lib.json"
    state = LibraryState(
        templates={
            "demo": PromptTemplate(
                key="demo", trigger="demo", replacement="Demo text"
            )
        }
    )

    save_library(state, lib_file)
    assert lib_file.exists()

    # Verify raw JSON structure
    raw = json.loads(lib_file.read_text(encoding="utf-8"))
    assert "templates" in raw
    assert raw["templates"]["demo"]["replacement"] == "Demo text"

    # Roundtrip
    loaded = load_library(lib_file)
    assert loaded.templates["demo"].replacement == "Demo text"
