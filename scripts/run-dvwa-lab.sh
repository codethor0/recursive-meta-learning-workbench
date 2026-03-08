#!/usr/bin/env bash
# Run RMLW lab against DVWA via Docker: build image, bring up DVWA, baseline + learn, tear down.
# Authorized testing only. Use only on targets you own or have permission to test. Not run in CI.
# Requires Docker and docker compose. Idempotent: safe to re-run; only affects Docker resources.
# Typical time: ~2–5 min for 10 iterations, ~5–15 min for 30 (depending on host).
# Usage: from repo root, ./scripts/run-dvwa-lab.sh [iterations]
#   iterations: number of learn-mode iterations (default 30)

set -e
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

ITERATIONS="${1:-30}"
# Docker Compose project name is the directory name; network is ${project}_default.
PROJECT_NAME="$(basename "$REPO_ROOT")"
NETWORK="${PROJECT_NAME}_default"

echo "Ensuring DVWA service is uncommented in docker-compose.yml..."
if ! grep -q '^  dvwa:' docker-compose.yml 2>/dev/null; then
  echo "Error: Uncomment the dvwa service block in docker-compose.yml first."
  exit 1
fi

echo "Step 0: Building RMLW image (rmlw:local)..."
docker build -t rmlw:local .

echo "Step 1: Bringing up DVWA on Docker network..."
docker compose up -d dvwa

echo "Waiting for DVWA (http://localhost:8080)..."
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
  if curl -s -o /dev/null -w "%{http_code}" http://localhost:8080 2>/dev/null | grep -q "200"; then
    echo "DVWA ready."
    break
  fi
  if [ "$i" -eq 15 ]; then
    echo "Timeout waiting for DVWA."
    docker compose down
    exit 1
  fi
  sleep 2
done

echo "Step 2: Baseline scan (sanity check)..."
docker run --rm \
  --network "$NETWORK" \
  -e TARGET_URL=http://dvwa \
  rmlw:local \
  rmlw scan \
    --target http://dvwa \
    --mode baseline \
    --format human

echo "Step 3: Learning session ($ITERATIONS iterations)..."
docker run --rm \
  --network "$NETWORK" \
  -e TARGET_URL=http://dvwa \
  rmlw:local \
  rmlw scan \
    --target http://dvwa \
    --mode learn \
    --iterations "$ITERATIONS" \
    --format human

echo "Step 4: Tearing down DVWA..."
docker compose down

echo "Lab run complete. To capture a proof run: re-run with DVWA up and redirect stdout/stderr (see docs/learning-lab-dvwa.md)."
