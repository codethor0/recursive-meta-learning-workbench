#!/usr/bin/env bash
# Pre-push sanity check. Run from repo root. All commands must exit 0.
# Usage: ./scripts/pre-push-check.sh

set -e
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "1. Install (editable + dev)..."
pip install -e .[dev]

echo "2. Black (format check on src + tests)..."
black --check src tests

echo "3. Ruff (lint)..."
ruff check src tests

echo "4. Mypy..."
mypy src

echo "5. Bandit (security scan)..."
bandit -r src

echo "6. Pytest..."
pytest -v

echo "All checks passed. Before pushing, run: git status && git diff"
echo "Skim for: no secrets, no emojis, no .cursor or prompt artifacts in tracked files."
echo "Optional: grep -R 'file://' -n src || true   (no unsafe schemes in src)"
