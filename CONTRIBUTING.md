# Contributing to RMLW

Thank you for your interest in contributing.

## Getting Started for Contributors

Follow this walkthrough from a clean clone to confirm the repo is in good shape and you can run the CLI and checks. All steps assume you have Python 3.10+ and (for the Docker step) Docker installed.

1. **Clone and enter the repo**

   ```bash
   git clone https://github.com/codethor0/recursive-meta-learning-workbench.git
   cd recursive-meta-learning-workbench
   ```

2. **Create a virtualenv and install with dev extras**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install .[dev]
   ```

3. **Run the quality gates (same as CI)**

   All of the following should exit 0:

   ```bash
   black --check .
   ruff check .
   mypy src
   bandit -r src
   pytest -v
   ```

   If anything fails, fix it before pushing (see Quality Gates below for fix hints).

4. **Run a sample scan**

   Confirm the CLI works (this does not hit a real lab target; it uses a safe example URL):

   ```bash
   rmlw scan --target http://example.com --mode baseline --format human
   ```

   You should see either "No findings." or a short list of findings. Then try JSON output:

   ```bash
   rmlw scan --target http://example.com --mode baseline --format json
   ```

5. **Optional: run with Docker**

   ```bash
   docker build -t rmlw:local .
   docker run --rm -e TARGET_URL=http://example.com rmlw:local
   ```

   The container should run a baseline scan and exit 0. If you omit `TARGET_URL`, it should exit non-zero with a clear message.

Once this walkthrough succeeds, you are ready to make changes. Use the Quality Gates and Pre-push checklist below before committing and pushing.

## Development Setup

```bash
git clone https://github.com/codethor0/recursive-meta-learning-workbench.git
cd recursive-meta-learning-workbench
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install .[dev]
pre-commit install
```

Run a quick baseline scan to confirm the CLI works:

```bash
rmlw scan --target http://example.com --mode baseline --format human
```

## Quality Gates (run before committing)

Same as CI. All must pass:

```bash
black --check .
ruff check .
mypy src
bandit -r src
pytest -v
```

To fix formatting: `black .` then re-run `black --check .` to verify.

To fix ruff issues: `ruff check .` shows problems; fix manually or use `ruff check . --fix` where safe.

## Pre-push sanity checklist

Before pushing to GitHub, run from the repo root:

```bash
pip install -e .[dev]
black --check src tests
ruff check src tests
mypy src
bandit -r src
pytest -v
```

All must exit 0. Then run `git status` and `git diff` and skim for: no secrets, no emojis, no stray prompt files or `.cursor` artifacts in tracked files. Optional extra checks:

```bash
grep -R "file://" -n src || echo "No unsafe schemes referenced"
```

Alternatively, run the script: `./scripts/pre-push-check.sh` (same checks, then follow with manual git review).

## Pull Request Process

1. Create a branch from `main`
2. Make changes with tests
3. Run all quality gates locally
4. Submit PR with clear description
5. Address review feedback

## Do Not Commit

- `.cursor/` or any local prompt files
- Prompt text, agent transcripts, or LLM instructions
- Emojis in code or docs
- Secrets or credentials

## Cursor: Learning Lab instructions

For sessions focused only on the DVWA learning lab and proof-of-learning (no core architecture changes), paste the contents of [docs/cursor-learning-lab-instructions.md](docs/cursor-learning-lab-instructions.md) into Cursor's Agent / Instructions panel as the workspace instruction. That keeps the agent in-bounds for lab harness, docs, and evidence only.

## Scope

- Bug fixes and improvements to existing functionality
- New vulnerability tests (with tests and documentation)
- Documentation improvements
- Performance optimisations

For larger features (LLM integration, Fisher-Rao merging), please open an issue first to discuss.
