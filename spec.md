

# LLM‑SyCophancy Reducer: Shared Custom Prompt Library - App Specification

## Overview
This tool provides a local command‑line interface for managing and applying a shared library of optimized prompt templates that reduce LLM sycophancy, lower latency, and cut compute cost. AI/ML researchers and prompt engineers can store, retrieve, and transform prompts without any external service calls.

**Problem Statement**: Teams waste time and money reinventing prompt‑engineering tricks to curb LLM sycophancy.  
**Target Audience**: AI/ML researchers, LLM engineers, and prompt engineers who need a reusable, offline prompt‑optimization utility.

## Tech Stack
- Python 3.11+
- Click (for CLI)
- Pytest (for testing)

## Environment Setup

### Prerequisites
- Python 3.11+ interpreter
- Pip (standard tool)

### Configuration
| Environment Variable | Default | Description |
|----------------------|---------|-------------|
| `PROMPT_LIB_PATH`    | `~/.llm_sycophancy_lib.json` | Path to the JSON file storing the prompt template library |
| `OPTIMIZE_VERBOSE`   | `0`     | Set to `1` to emit debug info during optimization |

## Architecture
```
+-------------------+
|   CLI Entrypoint  |
+----------+--------+
           |
   +------v------+      +------------------+
   |  Command    |      |  Prompt Library  |
   |  Router     |<-----|  (JSON/SQLite)  |
   +------+------+      +------------------+
           |
   +------v------+
   |  Optimizer  |
   +------+------+
           |
   +------v------+
   |  Output (stdout) |
   +------------------+
```

## Core Features
### Feature 1: Library Management
**Description**: Add, list, remove, and view custom prompt templates stored in a local JSON (or SQLite) backend.  
**Requirements**:
- `add` subcommand stores a new template with a unique key and returns success.
- `list` subcommand prints all stored keys and their associated templates.
- `rm` subcommand deletes a template by key and confirms removal.
- `show` subcommand displays the full template for a given key.
**Test Steps**:
1. `llmsyc add hello "Say hello concisely"` -> `Template 'hello' added.`
2. `llmsyc list` -> `hello: Say hello concisely`
3. `llmsyc rm hello` -> `Template 'hello' removed.`
4. `llmsyc add world "Explain the world in one sentence."` -> `Template 'world' added.`
5. `llmsyc show world` -> `Explain the world in one sentence.`

### Feature 2: Prompt Optimization
**Description**: Transform an input prompt by applying the highest‑priority matching template from the library, outputting the optimized prompt to stdout.  
**Requirements**:
- If no template matches, the original prompt is emitted unchanged.
- Matching is case‑insensitive and based on substring containment of the template’s trigger phrase.
- When multiple templates match, the longest trigger phrase wins.
- The tool reads the prompt from either a file argument or stdin.
**Test Steps**:
1. `echo "Please say hello in a friendly way." | llmsyc optimize` -> `Please say hello concisely.` *(assuming "hello" template replaces "say hello in a friendly way")*
2. `llmsyc optimize -f pf.txt` *(pf.txt contains "Explain the world in one sentence please.")* -> `Explain the world in one sentence.` *(world template applied)*
3. `echo "Random input." | llmsyc optimize` -> `Random input.` *(no match)*
4. `llmsyc optimize -f empty.txt` *(empty file)* -> *(empty output)*
5. `echo "Say hello and also explain the world." | llmsyc optimize` -> `Say hello concisely and also explain the world in one sentence.` *(both templates applied, longest triggers first)*

### Feature 3: Statistics & Telemetry (local only)
**Description**: Provide a `--stats` flag that reports library size, hit/miss counts, and average token reduction for the current session, persisted only in memory.  
**Requirements**:
- `--stats` prints number of stored templates, number of optimizations attempted, number of hits, and estimated token savings.
- Counters reset only when the process exits; no external storage.
- The flag can be combined with any other subcommand.
**Test Steps**:
1. `llmsyc stats` -> `Templates: 0, Attempts: 0, Hits: 0, Saved tokens: 0`
2. `llmsyc add t "Test"` then `llmsyc stats` -> `Templates: 1, Attempts: 0, Hits: 0, Saved tokens: 0`
3. `echo "Please test this." | llmsyc optimize` then `llmsyc stats` -> `Templates: 1, Attempts: 1, Hits: 1, Saved tokens: 5` *(example)*
4. `llmsyc optimize -f nonexistent.txt 2>/dev/null || llmsyc stats` -> `Templates: 1, Attempts: 2, Hits: 1, Saved tokens: 5`
5. `llmsyc rm t` then `llmsyc stats` -> `Templates: 0, Attempts: 2, Hits: 1, Saved tokens: 5`

## Data Models
```python
# prompt_lib/models.py
from pydantic import BaseModel, Field
from typing import Dict, Optional

class PromptTemplate(BaseModel):
    key: str = Field(..., description="Unique identifier for the template")
    trigger: str = Field(..., description="Substring to match in a prompt")
    replacement: str = Field(..., description="Text to substitute for the trigger")
    priority: int = Field(0, description="Higher priority wins on equal length trigger")

class LibraryState(BaseModel):
    templates: Dict[str, PromptTemplate] = Field(default_factory=dict)
    attempts: int = 0
    hits: int = 0
    saved_tokens: int = 0
```

## File Structure
```
llmsyc/
├── __init__.py
├── cli.py               # Click command groups and subcommands
├── lib.py               # Library persistence (JSON file)
├── optimizer.py         # Matching and replacement logic
├── stats.py             # In‑memory counters
├── models.py            # Pydantic models
└── tests/
    ├── test_cli.py
    ├── test_lib.py
    ├── test_optimizer.py
    └── test_stats.py
```
*(8 files – within the 8‑12 limit; each test file contains multiple test functions)*

## Test Plan
- `tests/test_cli.py::test_add_template`
- `tests/test_cli.py::test_list_templates`
- `tests/test_cli.py::test_remove_template`
- `tests/test_cli.py::test_show_template`
- `tests/test_cli.py::test_optimize_no_match`
- `tests/test_cli.py::test_optimize_single_match`
- `tests/test_cli.py::test_optimize_multiple_matches`
- `tests/test_cli.py::test_optimize_from_file`
- `tests/test_cli.py::test_stats_initial`
- `tests/test_cli.py::test_stats_after_add`
- `tests/test_cli.py::test_stats_after_optimize`
- `tests/test_cli.py::test_stats_after_remove`
- `tests/test_lib.py::test_load_library`
- `tests/test_lib.py::test_save_library`
- `tests/test_optimizer.py::test_find_best_match`
- `tests/test_optimizer.py::test_apply_replacement`
- `tests/test_stats.py::test_counter_increment`
- `tests/test_stats.py::test_counter_reset_on_exit`  
*(≥5 test functions total, each with concrete CLI command assertions)*

## Success Criteria
- The tool compiles and installs with `pip install .` in an isolated environment.
- Running `llmsyc --help` prints a usage message showing subcommands `add`, `list`, `rm`, `show`, `optimize`, and `stats`.
- All core-feature test suites pass (≥80% pass rate) with no external network calls.
- A user can store a prompt template, then pipe a raw prompt through `llmsyc optimize` and receive the expected transformed prompt on stdout.
- The `--stats` flag reports non‑zero hits and saved token counts after at least one successful optimization, demonstrating local telemetry.

## Constraints & Notes
- No external API calls — all processing uses local files or in‑memory stores.
- Target: a working MVP achievable within the 5‑iteration limit for the builder.
- Prioritize **correct behavior** over covering every possible edge case; the library need only support simple substring triggers.
- All dependencies are limited to the Python standard library plus `click` and `pytest`; exact versions are pinned in `requirements.txt`.
- The solution must be buildable by the coding agent with no human intervention and no API keys.