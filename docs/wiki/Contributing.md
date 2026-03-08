# Contributing

## How to Get Started

1. Fork and clone the repository
2. Create a virtual environment and install dev dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install .[dev]
pre-commit install
```

3. Create a branch, make changes, run quality gates, open a PR

## Quality Gates (run before every PR)

All must pass:

```bash
black --check .
ruff check .
mypy src
bandit -r src
pytest -v
```

To fix formatting: `black .` then re-run `black --check .`

To fix ruff issues: `ruff check .` shows problems; use `ruff check . --fix` where safe.

## Coding Style and Security

- Black for formatting
- Ruff for linting
- mypy for type checking
- bandit for security scanning

Do not add:

- Prompt artifacts or .cursor content
- Emojis in code or docs
- eval/exec on untrusted input
- shell=True
- Weak randomness for security decisions

## Pull Request Process

1. Create a branch from main
2. Make changes with tests
3. Run all quality gates locally
4. Submit PR with clear description
5. Address review feedback

See the main CONTRIBUTING.md in the repository for full details.
