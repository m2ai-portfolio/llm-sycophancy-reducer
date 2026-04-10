"""Click CLI for the LLM-Sycophancy Reducer prompt library."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import click

from .lib import load_library, save_library
from .models import PromptTemplate
from .optimizer import apply_replacements
from .stats import Stats

DEFAULT_LIB_PATH = Path.home() / ".llm_sycophancy_lib.json"


def _lib_path() -> Path:
    env = os.environ.get("PROMPT_LIB_PATH")
    if env:
        return Path(env)
    return DEFAULT_LIB_PATH


@click.group()
def cli() -> None:
    """LLM-Sycophancy Reducer: manage a shared prompt template library."""


@cli.command()
@click.argument("key")
@click.argument("template")
def add(key: str, template: str) -> None:
    """Add a prompt template. KEY is the trigger phrase, TEMPLATE is the replacement."""
    path = _lib_path()
    state = load_library(path)

    if key in state.templates:
        click.echo(f"Error: Template '{key}' already exists. Remove it first.", err=True)
        raise SystemExit(1)

    state.templates[key] = PromptTemplate(
        key=key, trigger=key, replacement=template
    )
    save_library(state, path)
    click.echo(f"Template '{key}' added")


@cli.command("list")
def list_templates() -> None:
    """List all templates in the library."""
    path = _lib_path()
    state = load_library(path)

    if not state.templates:
        click.echo("No templates in library.")
        return

    for key, tmpl in state.templates.items():
        click.echo(f"{key}: {tmpl.replacement}")


@cli.command()
@click.argument("key")
def rm(key: str) -> None:
    """Remove a template by key."""
    path = _lib_path()
    state = load_library(path)

    if key not in state.templates:
        click.echo(f"Error: Template '{key}' not found.", err=True)
        raise SystemExit(1)

    del state.templates[key]
    save_library(state, path)
    click.echo(f"Template '{key}' removed")


@cli.command()
@click.argument("key")
def show(key: str) -> None:
    """Show a single template's replacement text."""
    path = _lib_path()
    state = load_library(path)

    if key not in state.templates:
        click.echo(f"Error: Template '{key}' not found.", err=True)
        raise SystemExit(1)

    click.echo(state.templates[key].replacement)


@cli.command()
@click.option("-f", "--file", "input_file", type=click.Path(exists=True), default=None,
              help="Read input from FILE instead of stdin.")
@click.option("--stats", "show_stats", is_flag=True, default=False,
              help="Print optimization stats after output.")
def optimize(input_file: str | None, show_stats: bool) -> None:
    """Optimize input text by applying matching templates."""
    path = _lib_path()
    state = load_library(path)
    tracker = Stats()

    if input_file:
        text = Path(input_file).read_text(encoding="utf-8").strip()
    else:
        text = click.get_text_stream("stdin").read().strip()

    tracker.record_attempt()
    result, saved = apply_replacements(text, state.templates)

    if saved > 0 or result != text:
        tracker.record_hit(saved)

    click.echo(result)

    if show_stats:
        s = tracker.summary()
        click.echo(f"Attempts: {s['attempts']}")
        click.echo(f"Hits: {s['hits']}")
        click.echo(f"Saved tokens: {s['saved_tokens']}")


@cli.command()
def stats() -> None:
    """Print current library stats (template count + per-process counters)."""
    path = _lib_path()
    state = load_library(path)

    click.echo(f"Templates: {len(state.templates)}")
    click.echo("Attempts: 0")
    click.echo("Hits: 0")
    click.echo("Saved tokens: 0")


if __name__ == "__main__":
    cli()
