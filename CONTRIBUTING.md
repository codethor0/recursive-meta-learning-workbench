# Contributing to RMLW

Thank you for your interest in contributing.

## Development Setup

```bash
git clone https://github.com/codethor0/recursive-meta-learning-workbench.git
cd recursive-meta-learning-workbench
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install .[dev]
pre-commit install
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

## Scope

- Bug fixes and improvements to existing functionality
- New vulnerability tests (with tests and documentation)
- Documentation improvements
- Performance optimisations

For larger features (LLM integration, Fisher-Rao merging), please open an issue first to discuss.
