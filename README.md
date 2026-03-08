# Recursive Meta-Learning Workbench (RMLW)

RMLW is a transparent, research-focused proof of concept for web application security testing. It combines:

- A **Web Attack Workbench** that runs targeted, explainable tests for common vulnerability classes (XSS, SQL injection, LFI/traversal, command injection, SSRF) against explicitly scoped targets.
- A **Recursive Meta-Learning layer** that models the environment, uses reinforcement learning to prioritize tests, evolves payloads over time, and stores successful strategies in an archive.

RMLW is designed for authorized lab and training environments, not for indiscriminate scanning. It emphasizes clarity, reproducibility, and extensibility rather than being a black-box scanner.

## Authorized Testing Only

**Do not use on systems you do not own or have explicit permission to test.** This tool is for authorised testing in controlled environments only. Unauthorised access to computer systems is illegal. The authors assume no liability for misuse.

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
