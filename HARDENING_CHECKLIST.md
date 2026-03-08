# RMLW Hardening Checklist

Use this checklist before considering a release or major change complete. Mirrors the quality gates and safety requirements from the project spec.

## Quality Gates (all must pass)

```bash
black --check .
ruff check .
mypy src
bandit -r src
pytest -v
```

## Docker

```bash
docker build -t rmlw .
docker run --rm rmlw
# Expected: exit non-zero, clear usage message (TARGET_URL required)

docker run --rm -e TARGET_URL=http://localhost:8080 rmlw
# Expected: scan runs to completion, no unhandled exceptions
```

## Hygiene

- [ ] No emojis in code, tests, docs, or config
- [ ] No prompt artifacts (master prompts, agent transcripts, LLM instructions) in repo
- [ ] README and SECURITY.md include "Authorized Testing Only" messaging
- [ ] Scope enforcement documented (http/https only, url_in_scope, no file:///javascript:///data:///ftp://)

## Pre-commit (optional)

```bash
pre-commit run --all-files
```

## CI

After pushing, verify GitHub Actions CI workflow passes (lint-and-test, docker-build).

## Cursor prompt workflow (local .cursor/ only)

Three prompts support different workflows. Paste into Cursor Agent at repo root as needed:

| Prompt | When to use |
|--------|-------------|
| **Master** (`rmlw-master-prompt.txt`) | Fresh clone, full re-audit, or major reshape. Inspects tree first, runs all gates and Docker, evolves existing code to match spec. |
| **Runtime** (`rmlw-runtime-prompt.txt`) | Day-to-day: bug fixes, small features, test/doc tweaks. Keeps changes minimal and aligned with existing architecture. |
| **Live Docker test** (`rmlw-live-docker-test-prompt.txt`) | End-to-end verification: rebuild image, spin up DVWA, run baseline + learning scans, tests in container. Use before cutting a release. |

Suggested flow: Runtime for incremental work; Master after several edits or big changes; Live Docker test before tagging v0.1.1, v0.2.0, etc.
