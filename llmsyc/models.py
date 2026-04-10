"""Pydantic data models for the prompt template library."""

from pydantic import BaseModel, Field


class PromptTemplate(BaseModel):
    """A single prompt template with trigger and replacement text."""

    key: str
    trigger: str
    replacement: str
    priority: int = 0


class LibraryState(BaseModel):
    """Top-level state: a dict of templates plus aggregate counters."""

    templates: dict[str, PromptTemplate] = Field(default_factory=dict)
    attempts: int = 0
    hits: int = 0
    saved_tokens: int = 0
