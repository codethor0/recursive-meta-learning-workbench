# Getting Started

## Prerequisites

- Python 3.10+
- Docker (optional, for containerized runs)
- Git

## Clone and Install

```bash
git clone https://github.com/codethor0/recursive-meta-learning-workbench.git
cd recursive-meta-learning-workbench
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install .
```

For development (tests, linting):

```bash
pip install .[dev]
```

## Run a Baseline Scan

Baseline mode runs the Web Attack Workbench without learning:

```bash
rmlw scan --target http://localhost:8080 --mode baseline --format human
```

With JSON output:

```bash
rmlw scan --target http://localhost:8080 --mode baseline --output findings.json
```

## Run Learning Mode

Learning mode uses the MetaController for adaptive testing:

```bash
rmlw scan --target http://localhost:8080 --mode learn --iterations 10 --output findings.json
```

## Docker

Build:

```bash
docker build -t rmlw:local .
```

Run (TARGET_URL required):

```bash
docker run --rm -e TARGET_URL=http://localhost:8080 rmlw:local
```

Run tests inside the container:

```bash
docker run --rm rmlw:local pytest -v
```

## Docker Compose with DVWA

1. Uncomment the `dvwa` service in `docker-compose.yml`
2. Start DVWA:

```bash
docker compose up -d dvwa
```

3. Log in at the DVWA URL (default admin/password), set security to Low
4. Run RMLW:

```bash
docker compose run --rm -e TARGET_URL=http://dvwa rmlw rmlw scan --target http://dvwa --mode baseline --format human
```

## Troubleshooting

- **Docker network issues with DVWA**: Ensure RMLW and DVWA are on the same Docker network. Use `docker compose` so both services share the default network, or use `--network host` when running RMLW against a host-published DVWA.
- **Connection refused**: Verify the target URL is correct and the target is running. For DVWA, confirm you have logged in and set security level.
- **No findings**: Baseline mode uses a fixed set of endpoints. If your target has different paths, you may need to configure endpoints programmatically or wait for crawler support.
