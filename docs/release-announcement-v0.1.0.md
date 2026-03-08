# Recursive Meta-Learning Workbench (RMLW) v0.1.0 – Initial PoC Release

RMLW (Recursive Meta-Learning Workbench) is a transparent, research-focused proof of concept for web application security testing.

Instead of a black-box scanner, RMLW gives you:

- A **Web Attack Workbench** that runs targeted, explainable tests for common vulnerability classes (XSS, SQLi, LFI/traversal, command injection, SSRF) against explicitly scoped targets.
- A **meta-learning layer** that models the environment, uses reinforcement learning to prioritize tests, evolves payloads over time, and stores successful strategies in an archive for reuse.

This project is designed for authorized lab and training environments only. It is not a spray-and-pray scanner. The emphasis is on clarity, reproducibility, and extensibility so researchers and security engineers can see exactly what is being tested and why.

## Key features in v0.1.0

- **Python package** with clean layout under `src/rmlw/`
- **Web Attack Workbench** with:
  - Scope enforcement and URL validation utilities
  - Test modules for XSS, SQLi, LFI/traversal, command injection, SSRF
  - Structured `Finding` dataclass with JSON-serializable output
- **Learning layer** with:
  - `EnvironmentModel` to capture target behavior
  - `RLPathOptimizer` for test selection
  - `EvolutionaryPayloadGenerator` for payload mutation
  - `MetaController` using a UCB bandit strategy
- **CLI**: `rmlw scan --target http://dvwa --mode baseline|learn --format human|json --output findings.json`
- **Docker**:
  - Dockerfile with dev dependencies and tests baked in
  - docker-compose.yml with a DVWA service for local lab testing
- **Quality gates**: black, ruff, mypy, bandit -r src, pytest -v all green locally and in CI
- **Docs**: Architecture overview, usage guide with Docker examples, security model, hardening checklist, contribution guidelines

## Example DVWA workflow

```bash
# Clone and install
git clone https://github.com/codethor0/recursive-meta-learning-workbench.git
cd recursive-meta-learning-workbench
python -m venv .venv
source .venv/bin/activate
pip install .[dev]

# Run tests
pytest -v

# Docker lab with DVWA (uncomment dvwa service in docker-compose.yml first)
docker compose up -d dvwa
docker compose run --rm -e TARGET_URL=http://dvwa rmlw \
    rmlw scan --target http://dvwa --mode baseline --format human
```

## Future work (tracked in the roadmap)

- Richer discovery beyond a single base URL
- Stronger archive reuse in learning mode
- Additional vulnerability classes (SSTI, XXE, deserialization)
- Example reports and analysis tooling under `examples/`

**As always: do not use this tool on systems you do not own or lack explicit permission to test.**
