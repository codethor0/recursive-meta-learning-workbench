# Contributing to RMLW

Thank you for your interest in contributing.

## Development Setup

```bash
git clone <repo>
cd recursive-meta-learning-workbench
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install .[dev]
pre-commit install
```

## Build and Run Docker

```bash
docker build -t rmlw .
docker run -e TARGET_URL=http://localhost:8080 rmlw
```

## Code Style

- **Black** for formatting
- **Ruff** for linting
- **mypy** for type checking
- **bandit** for security scanning

Run before committing (same as CI):

```bash
black --check .
ruff check .
mypy src
bandit -r src
pytest -v
```

To fix formatting: `black .` (then re-run `black --check .` to verify).

## Pull Request Process

1. Create a branch from `main`
2. Make changes with tests
3. Ensure all checks pass
4. Submit PR with clear description
5. Address review feedback

## Scope

- Bug fixes and improvements to existing functionality
- New vulnerability tests (with tests and documentation)
- Documentation improvements
- Performance optimisations

For larger features (LLM integration, Fisher-Rao merging), please open an issue first to discuss.
