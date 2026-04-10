"""Substring matching and replacement logic for prompt optimization."""

from __future__ import annotations

import re
from typing import Optional

from .models import PromptTemplate


def find_best_match(
    text: str, templates: dict[str, PromptTemplate]
) -> Optional[PromptTemplate]:
    """Find the template whose trigger is the longest substring match in text.

    Matching is case-insensitive. Returns None if no trigger matches.
    """
    best: Optional[PromptTemplate] = None
    best_len = 0
    text_lower = text.lower()

    for tmpl in templates.values():
        trigger_lower = tmpl.trigger.lower()
        if trigger_lower in text_lower and len(trigger_lower) > best_len:
            best = tmpl
            best_len = len(trigger_lower)

    return best


def apply_replacements(
    text: str, templates: dict[str, PromptTemplate]
) -> tuple[str, int]:
    """Apply all matching templates to text, longest trigger first.

    Returns (optimized_text, saved_token_estimate).
    Token estimate is based on whitespace-split word count delta.
    """
    if not text:
        return ("", 0)

    # Sort templates by trigger length descending so longest matches first
    sorted_templates = sorted(
        templates.values(), key=lambda t: len(t.trigger), reverse=True
    )

    original_word_count = len(text.split())
    result = text

    for tmpl in sorted_templates:
        # Case-insensitive replacement of the first occurrence
        pattern = re.compile(re.escape(tmpl.trigger), re.IGNORECASE)
        result = pattern.sub(tmpl.replacement, result, count=1)

    new_word_count = len(result.split())
    saved = max(0, original_word_count - new_word_count)

    return (result, saved)
