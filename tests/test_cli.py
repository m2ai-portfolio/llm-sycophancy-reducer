"""CLI integration tests using Click CliRunner."""

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from llmsyc.cli import cli


@pytest.fixture()
def lib_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Set PROMPT_LIB_PATH to a temp file and return the path."""
    p = tmp_path / "lib.json"
    monkeypatch.setenv("PROMPT_LIB_PATH", str(p))
    return p


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()


# ---------- add ----------


def test_add_template(runner: CliRunner, lib_path: Path) -> None:
    result = runner.invoke(cli, ["add", "hello", "Say hello concisely"])
    assert result.exit_code == 0
    assert "Template 'hello' added" in result.output

    data = json.loads(lib_path.read_text())
    assert "hello" in data["templates"]
    assert data["templates"]["hello"]["replacement"] == "Say hello concisely"


def test_add_template_duplicate_key(runner: CliRunner, lib_path: Path) -> None:
    runner.invoke(cli, ["add", "hello", "Say hello concisely"])
    result = runner.invoke(cli, ["add", "hello", "New replacement"])
    assert result.exit_code != 0 or "Error" in result.output or "already exists" in result.output


# ---------- list ----------


def test_list_templates(runner: CliRunner, lib_path: Path) -> None:
    runner.invoke(cli, ["add", "hello", "Say hello concisely"])
    runner.invoke(cli, ["add", "world", "Explain the world in one sentence."])

    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "hello: Say hello concisely" in result.output
    assert "world: Explain the world in one sentence." in result.output


# ---------- rm ----------


def test_remove_template(runner: CliRunner, lib_path: Path) -> None:
    runner.invoke(cli, ["add", "hello", "Say hello concisely"])
    result = runner.invoke(cli, ["rm", "hello"])
    assert result.exit_code == 0
    assert "Template 'hello' removed" in result.output

    data = json.loads(lib_path.read_text())
    assert "hello" not in data["templates"]


# ---------- show ----------


def test_show_template(runner: CliRunner, lib_path: Path) -> None:
    runner.invoke(cli, ["add", "world", "Explain the world in one sentence."])
    result = runner.invoke(cli, ["show", "world"])
    assert result.exit_code == 0
    assert "Explain the world in one sentence." in result.output


# ---------- optimize ----------


def test_optimize_no_match(runner: CliRunner, lib_path: Path) -> None:
    runner.invoke(cli, ["add", "hello", "Say hello concisely"])
    result = runner.invoke(cli, ["optimize"], input="Random input.\n")
    assert result.exit_code == 0
    assert result.output.strip() == "Random input."


def test_optimize_single_match(runner: CliRunner, lib_path: Path) -> None:
    runner.invoke(cli, ["add", "hello", "Say hello concisely"])
    result = runner.invoke(cli, ["optimize"], input="Please say hello in a friendly way.\n")
    assert result.exit_code == 0
    assert "Say hello concisely" in result.output
    # The original trigger should be replaced
    assert "hello" not in result.output.lower().replace("say hello concisely", "")


def test_optimize_multiple_matches(runner: CliRunner, lib_path: Path) -> None:
    runner.invoke(cli, ["add", "hello", "Say hello concisely"])
    runner.invoke(cli, ["add", "world", "Explain the world in one sentence."])
    result = runner.invoke(cli, ["optimize"], input="Say hello and also explain the world.\n")
    assert result.exit_code == 0
    assert "Say hello concisely" in result.output
    assert "Explain the world in one sentence." in result.output


def test_optimize_from_file(runner: CliRunner, lib_path: Path, tmp_path: Path) -> None:
    runner.invoke(cli, ["add", "world", "Explain the world in one sentence."])
    pf = tmp_path / "pf.txt"
    pf.write_text("Explain the world in one sentence please.", encoding="utf-8")
    result = runner.invoke(cli, ["optimize", "-f", str(pf)])
    assert result.exit_code == 0
    assert "Explain the world in one sentence." in result.output


# ---------- stats ----------


def test_stats_initial(runner: CliRunner, lib_path: Path) -> None:
    result = runner.invoke(cli, ["stats"])
    assert result.exit_code == 0
    assert "Templates: 0" in result.output
    assert "Attempts: 0" in result.output
    assert "Hits: 0" in result.output
    assert "Saved tokens: 0" in result.output


def test_stats_after_add(runner: CliRunner, lib_path: Path) -> None:
    runner.invoke(cli, ["add", "test", "Test replacement"])
    result = runner.invoke(cli, ["stats"])
    assert "Templates: 1" in result.output
    assert "Attempts: 0" in result.output


def test_stats_after_optimize(runner: CliRunner, lib_path: Path) -> None:
    runner.invoke(cli, ["add", "test", "Test replacement"])
    result = runner.invoke(cli, ["optimize", "--stats"], input="Please test this.\n")
    assert result.exit_code == 0
    assert "Test replacement" in result.output
    assert "Attempts: 1" in result.output
    assert "Hits: 1" in result.output


def test_stats_after_remove(runner: CliRunner, lib_path: Path) -> None:
    runner.invoke(cli, ["add", "test", "Test replacement"])
    runner.invoke(cli, ["rm", "test"])
    result = runner.invoke(cli, ["stats"])
    assert "Templates: 0" in result.output
