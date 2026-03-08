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
