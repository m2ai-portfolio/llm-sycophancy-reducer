

<p align="center">
  <img src="assets/infographic.png" alt="LLM‑SyCophancy Reducer: Shared Custom Prompt Library" width="800">
</p>

<h3 align="center">A collection of optimized custom instructions and prompt templates that lower latency and compute cost when deploying large language models.</h3>

<p align="center">
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#features">Features</a> &bull;
  <a href="#examples">Examples</a> &bull;
  <a href="#contributing">Contributing</a>
</p>

## What is this?
LLM‑SyCophancy Reducer is a local command‑line utility that lets AI/ML researchers and prompt engineers store, reuse, and apply optimized prompt templates to reduce sycophancy, lower latency, and cut compute costs. It works entirely offline, so no external API calls are needed.

```
$ echo "Please say hello in a friendly way." | llmsyc optimize
Please say hello concisely.
```

## Problem
Teams spend too much time figuring out how to reduce LLM sycophancy; there is no standard set of instructions, leading to duplicated effort and higher expenses.

## Features
| Feature | Description |
|---------|-------------|
| Library Management | Add, list, remove, and view custom prompt templates stored locally in JSON (or SQLite). |
| Prompt Optimization | Apply the highest‑priority matching template to a prompt, outputting the optimized version to stdout. |
| Local Telemetry | `--stats` flag reports templates count, optimization attempts, hits, and estimated token savings. |
| Offline Operation | All processing uses local files or in‑memory stores; no external network calls. |
| CLI Interface | Built with Click for intuitive subcommands (`add`, `list`, `rm`, `show`, `optimize`, `stats`). |
| Tested Core | Pytest suite validates core functionality with ≥80% pass rate in an isolated environment. |

## Quick Start
1. Clone the repository:  
   `git clone https://github.com/your-org/llm-sycophancy-reducer.git`
2. Enter the project directory:  
   `cd llm-sycophancy-reducer`
3. Install the package in editable mode:  
   `pip install -e .`
4. Try a quick workflow:  
   ```
   llmsyc add friendly "Respond politely and briefly."
   echo "Please be friendly when answering." | llmsyc optimize
   ```
   Expected output:  
   ```
   Template 'friendly' added.
   Please be polite when answering.
   ```

## Examples
**Add a new prompt template**  
Command: `llmsyc add concise "Give a short answer."`  
Output: `Template 'concise' added.`

**Optimize a prompt via stdin**  
Command: `echo "Can you give a short answer about the weather?" | llmsyc optimize`  
Output: `Can you give a short answer about the weather?` (no match)  
After adding a matching template:  
```
llmsyc add weather "Give a short answer about the weather."
echo "Can you give a short answer about the weather?" | llmsyc optimize
```
Output: `Give a short answer about the weather.`

**View statistics after optimization**  
Command:  
```
llmsyc stats
```
Output after the previous example:  
```
Templates: 2, Attempts: 1, Hits: 1, Saved tokens: 12
```

## File Structure
```
LLM‑SyCophancy Reducer: Shared Custom Prompt Library/
├── assets/
│   └── infographic.png
├── llmsyc/
│   ├── __init__.py
│   ├── cli.py          # Click command groups and subcommands
│   ├── lib.py          # JSON persistence layer
│   ├── models.py       # Pydantic data models
│   ├── optimizer.py    # Matching and replacement logic
│   └── stats.py        # In‑memory counters
├── tests/
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_lib.py
│   ├── test_optimizer.py
│   └── test_stats.py
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements.txt
└── spec.md
```

## Tech Stack
| Technology | Purpose |
|------------|---------|
| Python 3.11+ | Core language |
| Click | CLI framework |
| Pytest | Testing suite |
| JSON / SQLite | Local template storage |

## Contributing
Please fork the repository, make your changes, run the test suite with `pytest`, and submit a pull request. Ensure your code follows the existing style and includes tests for new functionality.

## License
MIT

## Author
Matthew Snow -- [M2AI](https://m2ai.co) | [@m2ai-portfolio](https://github.com/m2ai-portfolio)