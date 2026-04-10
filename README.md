

<p align="center">
  <img src="assets/infographic.png" alt="LLM‑SyCophancy Reducer: Shared Custom Prompt Library" width="800">
</p>

<h3 align="center">A command-line tool for managing and optimizing LLM prompts using a shared library of custom templates to reduce sycophancy and improve efficiency.</h3>

<p align="center">
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#features">Features</a> &bull;
  <a href="#examples">Examples</a> &bull;
  <a href="#contributing">Contributing</a>
</p>

### What is this?
LLM‑SyCophancy Reducer is a local command-line utility that enables AI/ML researchers and prompt engineers to store, retrieve, and apply optimized prompt templates from a shared library. It reduces redundant prompt engineering (sycophancy) by providing high‑priority matching templates that transform input prompts into concise, effective outputs, all without external API calls.

### Features
| Feature | Description |
|---------|-------------|
| Library Management | Add, list, remove, and view prompt templates stored in a local JSON backend with unique keys and priorities. |
| Prompt Optimization | Transform input prompts by applying the highest‑priority matching template from the library, outputting the optimized prompt to stdout; if no match, emit the original prompt unchanged. |
| Statistics & Telemetry | Provide a `--stats` flag that reports library size, hit/miss counts, and average token reduction for the current session, persisted only in memory and reset on exit. |
| Offline Operation | All processing uses local files or in‑memory stores; no external API calls are made. |
| Case‑Insensitive Matching | Template matching is case‑insensitive and based on substring containment of the trigger phrase. |
| Longest Trigger Wins | When multiple templates match, the one with the longest trigger phrase is selected. |

### Quick Start
1. Clone the repository: `git clone https://github.com/m2ai-portfolio/llmsyc.git`
2. Install the package: `pip install llmsyc/`
3. Run the help command: `llmsyc --help` to see available subcommands.
4. Add a prompt template: `llmsyc add hello "Say hello concisely"`
5. Optimize a prompt: `echo "Please say hello in a friendly way." | llmsyc optimize`

### Examples
**Example 1: Adding a greeting template**
- **Title**: Storing a concise greeting prompt
- **Command**: `llmsyc add hello "Say hello concisely"`
- **Output**: `Template 'hello' added.`

**Example 2: Optimizing a friendly prompt**
- **Title**: Transforming a wordy greeting into a concise version
- **Command**: `echo "Please say hello in a friendly way." | llmsyc optimize`
- **Output**: `Please say hello concisely.`

**Example 3: Using the world template**
- **Title**: Applying a template that explains the world in one sentence
- **Command**: `llmsyc optimize -f pf.txt` (assuming `pf.txt` contains "Explain the world in one sentence please.")
- **Output**: `Explain the world in one sentence.`

### File Structure
LLM‑SyCophancy Reducer: Shared Custom Prompt Library/
├── llmsyc/
│   ├── __init__.py
│   ├── cli.py               # Click command groups and subcommands
│   ├── lib.py               # Library persistence (JSON file)
│   ├── optimizer.py         # Matching and replacement logic
│   ├── stats.py             # In‑memory counters
│   ├── models.py            # Pydantic models
└── tests/
    ├── test_cli.py
    ├── test_lib.py
    ├── test_optimizer.py
    └── test_stats.py

### Tech Stack
| Technology | Purpose |
|------------|---------|
| Python 3.11+ | Core interpreter |
| Click | Building the command-line interface |
| Pytest | Testing framework |

### Contributing
We welcome contributions! Please fork the repository, create a feature branch, and submit a pull request. For major changes, open an issue first to discuss what you would like to contribution.

### License
MIT

### Author
Matthew Snow -- [M2AI](https://m2ai.co) | [@m2ai-portfolio](https://github.com/m2ai-portfolio)