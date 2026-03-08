# RMLW Usage Guide

## Fresh Clone Workflow

For a new contributor or user:

```bash
git clone <repo-url>
cd recursive-meta-learning-workbench
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install .[dev]
pytest tests -v
rmlw scan --target http://example.com --format human
```

Or with Docker:

```bash
docker build -t rmlw .
docker run -e TARGET_URL=http://example.com rmlw
```

## Installation

```bash
pip install .
# With dev dependencies (tests, linting):
pip install .[dev]
```

## CLI Commands

### Baseline Scan

Run the Web Attack Workbench without learning:

```bash
rmlw scan --target http://localhost:8080 --mode baseline
```

With JSON output to file:

```bash
rmlw scan --target http://localhost:8080 --mode baseline --output findings.json
```

### Learning Mode

Run the MetaController for N iterations:

```bash
rmlw scan --target http://localhost:8080 --mode learn --iterations 10 --output findings.json
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--target` | Base URL of target (required) | - |
| `--mode` | `baseline` or `learn` | `baseline` |
| `--iterations` | Number of learning iterations (learn mode) | 5 |
| `--output` | Output file for findings (always JSON, regardless of --format) | stdout |
| `--format` | `human` (succinct summary) or `json` (machine-readable) | `human` |

## Docker

### Build

```bash
docker build -t rmlw .
```

The image includes dev dependencies (pytest, black, ruff, mypy, bandit). To run tests inside the container:

```bash
docker run --rm rmlw pytest -v
```

### Run

TARGET_URL is required. The container exits with a usage message if not set:

```bash
docker run -e TARGET_URL=http://your-target:80 rmlw
```

To scan a Dockerized DVWA (with explicit permission):

```bash
docker run -d -p 8080:80 --name dvwa vulnerables/web-dvwa
# Log in at http://localhost:8080, set security to Low
docker run --network host -e TARGET_URL=http://localhost:8080 rmlw
```

Or use docker-compose:

```bash
# Uncomment dvwa service in docker-compose.yml, then:
docker compose up -d dvwa
docker compose run rmlw
```

### Docker Compose with DVWA

1. Uncomment the DVWA service in `docker-compose.yml` if needed
2. Run:

```bash
docker compose up
```

The workbench will scan `http://dvwa:80` (or the configured `TARGET_URL`).

## Example Output

### Baseline Scan (JSON)

```json
[
  {
    "ftype": "xss_reflection",
    "url": "http://localhost:8080/vulnerabilities/xss_r/",
    "param": "name",
    "payload": "<script>alert(1)</script>",
    "detail": {"status_code": 200, "length": 1234}
  }
]
```

### Learning Mode Logs

```
INFO  MetaController: Starting iteration 1/5
INFO  MetaController: Selected mechanism: rl
INFO  RLPathOptimizer: Selected test: xss
INFO  WebAttackWorkbench: Running tests on 4 endpoints
INFO  MetaController: Reward=2, new findings=2
INFO  MetaController: UCB stats: rl=0.5, evolution=0.0, archive_reuse=0.0
```

## DVWA Setup

1. Start DVWA: `docker run -d -p 8080:80 vulnerables/web-dvwa`
2. Log in (admin/password), set security to "Low"
3. Configure crawl in Workbench or use explicit endpoints:

```python
workbench = WebAttackWorkbench("http://localhost:8080")
workbench.endpoints.add("http://localhost:8080/vulnerabilities/xss_r/?name=test")
workbench.endpoints.add("http://localhost:8080/vulnerabilities/sqli/?id=1")
# ...
findings = workbench.run()
```

## Programmatic Usage

```python
from rmlw.workbench import WebAttackWorkbench, Finding

workbench = WebAttackWorkbench("http://localhost:8080")
findings = workbench.run()

for f in findings:
    print(f"{f.ftype} @ {f.url} param={f.param}")
```

With learning:

```python
from rmlw.workbench import WebAttackWorkbench
from rmlw.learning import MetaController

workbench = WebAttackWorkbench("http://localhost:8080")
controller = MetaController(workbench)
controller.run_iterations(5)
```
