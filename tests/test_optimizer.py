"""Unit tests for matching and replacement logic."""

from llmsyc.models import PromptTemplate
from llmsyc.optimizer import apply_replacements, find_best_match


def _make_templates() -> dict[str, PromptTemplate]:
    return {
        "hello": PromptTemplate(key="hello", trigger="hello", replacement="Hi"),
        "hello world": PromptTemplate(
            key="hello world", trigger="hello world", replacement="Greetings Earth"
        ),
        "test": PromptTemplate(key="test", trigger="test", replacement="Exam"),
    }


def test_find_best_match() -> None:
    templates = _make_templates()

    # Longest trigger match wins
    match = find_best_match("say hello world now", templates)
    assert match is not None
    assert match.key == "hello world"

    # Simple match
    match2 = find_best_match("just a test", templates)
    assert match2 is not None
    assert match2.key == "test"

    # No match
    assert find_best_match("no match here", templates) is None

    # Case-insensitive
    match3 = find_best_match("Say HELLO", templates)
    assert match3 is not None
    assert match3.key == "hello"


def test_apply_replacement() -> None:
    templates = {
        "hello": PromptTemplate(
            key="hello", trigger="hello", replacement="Say hello concisely"
        ),
        "world": PromptTemplate(
            key="world",
            trigger="world",
            replacement="Explain the world in one sentence.",
        ),
    }

    result_text, saved = apply_replacements(
        "Say hello and explain the world.", templates
    )
    assert "Say hello concisely" in result_text
    assert "Explain the world in one sentence." in result_text

    # No triggers
    text2, saved2 = apply_replacements("No triggers here.", templates)
    assert text2 == "No triggers here."
    assert saved2 == 0

    # Empty input
    text3, saved3 = apply_replacements("", templates)
    assert text3 == ""
    assert saved3 == 0
