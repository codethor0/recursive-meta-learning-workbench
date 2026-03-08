# Recursive Meta-Learning Workbench (RMLW)

A self-improving architecture for web application security testing. RMLW combines a transparent **Web Attack Workbench** with a **Recursive Meta-Learning** layer that learns from testing outcomes.

RMLW is NOT a black-box scanner. It is a transparent, extensible PoC for security professionals to run against lab targets.

## Authorized Testing Only

**Do not use on systems you do not own or have explicit permission to test.** This tool is for authorised testing in controlled environments only. Unauthorised access to computer systems is illegal. The authors assume no liability for misuse.

## Overview

RMLW provides two layers:

1. **Web Attack Workbench** – A transparent, extensible Python library that:
   - Models a web app as HTTP endpoints with parameters
   - Runs targeted tests for XSS, SQLi, LFI, command injection, and SSRF
   - Collects structured findings with payload and evidence

2. **Recursive Meta-Learning Layer** – Wraps the Workbench with:
   - Environment model (WAF hints, filters, successes/failures)
   - RL-based test selection
   - Evolutionary payload generation
   - Persistent archive of successful payloads
   - Meta-controller (multi-armed bandit) to orchestrate strategies

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Meta-Controller (UCB Bandit)                  │
│  Chooses: RL test selection | Evolution | Archive recombination  │
└─────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌───────────────┐         ┌─────────────────┐         ┌──────────────┐
│ RLPathOptimizer│         │ EvolutionaryPayload│       │ PersistentArchive│
│ (Q-learning)   │         │ Generator          │       │ (successes)   │
└───────────────┘         └─────────────────┘         └──────────────┘
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    ▼
                    ┌───────────────────────────────┐
                    │     Web Attack Workbench       │
                    │  XSS | SQLi | LFI | CMDi | SSRF│
                    └───────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │     Target Web Application    │
                    └───────────────────────────────┘
```

See [docs/architecture.md](docs/architecture.md) for details.

## Quickstart

### Install

```bash
pip install .
# or with dev dependencies:
pip install .[dev]
```

### Run a baseline scan

```bash
rmlw scan --target http://localhost:8080 --mode baseline --output findings.json
```

Human-readable output:

```bash
rmlw scan --target http://localhost:8080 --format human
```

### Run learning mode

```bash
rmlw scan --target http://localhost:8080 --mode learn --iterations 5 --output findings.json
```

### Docker

```bash
docker build -t rmlw .
docker run -e TARGET_URL=http://dvwa:80 rmlw
```

With docker-compose (see `docker-compose.yml` for DVWA setup):

```bash
docker compose up
```

## Project Structure

```
recursive-meta-learning-workbench/
├── src/rmlw/
│   ├── workbench/     # Web Attack Workbench
│   ├── learning/      # RMLW learning layer
│   └── cli/           # CLI entry point
├── tests/
├── docs/
├── Dockerfile
└── docker-compose.yml
```

## Documentation

- [Architecture](docs/architecture.md) – Design and component diagrams
- [Usage](docs/usage.md) – Commands and examples
- [Security Model](docs/security_model.md) – Threat model and safety
- [Roadmap](docs/roadmap.md) – Planned extensions

## Community

- [Contributing](CONTRIBUTING.md) - How to contribute
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community guidelines

## License

MIT License. See [LICENSE](LICENSE) for details.
