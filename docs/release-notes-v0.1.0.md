# RMLW v0.1.0 – Initial Proof-of-Concept Release

This is the initial public proof-of-concept release of the Recursive Meta-Learning Workbench (RMLW): a transparent, self-improving framework for web application security testing in authorized lab environments.

## Highlights

### 1. Web Attack Workbench (Static Layer)

- Models a target as a set of HTTP endpoints with parameters.
- Implements targeted tests for core vulnerability classes:
  - Cross-Site Scripting (XSS) via reflection checks.
  - Boolean-based SQL injection.
  - Local file inclusion / directory traversal using `/etc/passwd` markers.
  - Command injection via timing-based `sleep` probes.
  - Basic SSRF checks using internal address aliases (127.0.0.1, localhost, etc.).
- Enforces strict scope:
  - Only `http://` and `https://` schemes are allowed.
  - Rejects dangerous schemes such as `file://`, `javascript://`, `data://`, and `ftp://`.
  - Skips endpoints whose host does not match the configured base URL.
- Produces structured `Finding` objects with:
  - `ftype`, `url`, `param`, `payload`, and a `detail` evidence dictionary.
- Handles network errors and timeouts gracefully without crashing the scan.

### 2. Recursive Meta-Learning Workbench (Learning Layer)

- `EnvironmentModel` tracks:
  - WAF hints from response headers.
  - Simple input filtering behavior (e.g., blocking, sanitization).
  - Successful and failed payloads per vulnerability type.
- `RLPathOptimizer`:
  - Tabular Q-learning for choosing which test families to prioritize.
  - Epsilon-greedy policy with unit tests covering selection and updates.
- `EvolutionaryPayloadGenerator`:
  - Maintains a population of payloads with fitness scores.
  - Supports mutation and crossover operators.
  - Accepts an optional RNG for deterministic testing.
- `PersistentArchive`:
  - Stores successful payloads plus context and timestamps.
  - Exposes `recent()` for retrieving recent successes.
- `MetaController`:
  - Implements a simple multi-armed bandit (UCB) over strategies (baseline, RL-focused, evolution-focused, archive reuse).
  - Orchestrates calls into the workbench and learning components.
  - Logs strategy decisions, rewards, and basic metrics.

### 3. CLI and Docker

- `rmlw` CLI (via `rmlw.cli.main:main`):
  - `rmlw scan --target URL --mode baseline|learn --iterations N --format human|json --output FILE`
  - Validates and normalizes the target URL before scanning.
  - `--format human` prints concise, human-readable lines:
    - `[ftype] url=... param=... payload='...'`
  - `--format json` prints a JSON array of findings to stdout and, optionally, to `--output`.
  - Exits with a clear error and non-zero status for invalid URLs or fatal issues.
- Docker:
  - `Dockerfile` builds a slim image with RMLW installed.
  - Runtime requires `TARGET_URL`; missing `TARGET_URL` results in a clear usage message and exit.
  - Supports running baseline scans or short learning runs in containers.
  - Documentation includes an example workflow with DVWA or similar lab targets.

### 4. Security, Quality, and Tooling

- Strict scope enforcement and URL validation utilities (`url_utils.py`).
- No use of `eval`, `exec`, or unsafe deserialization.
- No subprocess-based target interaction; all probing is via HTTP requests with explicit timeouts.
- No emojis and no prompt artifacts committed to the repository.
- Tooling and CI:
  - `black` for formatting.
  - `ruff` for linting.
  - `mypy` for static type checking.
  - `bandit` for static security analysis.
  - `pytest` for tests (58 tests across workbench, learning layer, CLI, and utilities).
- Documentation:
  - `README.md` with quickstart and "Authorized Testing Only" guidance.
  - `docs/architecture.md` describing the Web Attack Workbench and RMLW layers.
  - `docs/usage.md` with CLI and Docker examples.
  - `docs/security_model.md` outlining scope, threat model, and limitations.
  - `docs/roadmap.md` capturing future directions (richer discovery, more vuln classes, LLM/Fisher-Rao extensions, and CI/CD integration).

## Intended Use

RMLW v0.1.0 is a research and training tool. It is intended **only** for use against systems and applications where you have explicit, written permission to test. It is not a point-and-shoot scanner and is not designed for unauthorized hacking or internet-wide scanning.
