# RMLW Learning Lab – DVWA via Docker

End-to-end lab workflow to run RMLW against DVWA and demonstrate that the learning layer is active. For authorised testing only; use only on targets you own or have permission to test.

## Prerequisites

- Docker and Docker Compose (v2)
- Repo at `recursive-meta-learning-workbench/` with Dockerfile and `docker-compose.yml`
- DVWA service uncommented in `docker-compose.yml` when you want to use it

## Quick run: lab script

From the repo root:

```bash
./scripts/run-dvwa-lab.sh [iterations]
```

- Builds the image as `rmlw:local`, brings up DVWA, runs one baseline scan and one learn-mode run (default 30 iterations), then tears down DVWA.
- Optional argument: number of learn iterations (e.g. `./scripts/run-dvwa-lab.sh 10`).
- If the script fails, ensure the `dvwa` service block in `docker-compose.yml` is uncommented.

## Manual steps (copy-paste)

Use these when you want full control or to capture a single proof run.

### Step 0 – Build the image

From the repo root:

```bash
cd recursive-meta-learning-workbench
docker build -t rmlw:local .
```

### Step 1 – Bring up DVWA

If DVWA is commented out in `docker-compose.yml`, uncomment the DVWA service block, then:

```bash
docker compose up -d dvwa
```

- DVWA is reachable as `http://dvwa` (or `http://dvwa:80`) from the RMLW container on the same Docker network.
- From the host, DVWA is usually on `http://localhost:8080`. Log in (e.g. admin/password) and set security level to Low before running learning.

### Step 2 – Baseline scan (sanity check)

Use the same Docker network as the compose project (default: `recursive-meta-learning-workbench_default`; if your repo directory has a different name, the network is `<dirname>_default`):

```bash
docker run --rm \
  --network recursive-meta-learning-workbench_default \
  -e TARGET_URL=http://dvwa \
  rmlw:local \
  rmlw scan \
    --target http://dvwa \
    --mode baseline \
    --format human
```

This confirms URL scoping and readiness. You should see a small number of findings (e.g. ssrf_candidate, xss, sqli) depending on discovery.

JSON output to a file (from host, use a path inside the container or mount a volume to get the file out):

```bash
docker run --rm \
  --network recursive-meta-learning-workbench_default \
  -e TARGET_URL=http://dvwa \
  rmlw:local \
  rmlw scan \
    --target http://dvwa \
    --mode baseline \
    --format json \
    --output /tmp/dvwa-baseline-findings.json
```

### Step 3 – Learning session (prove “it’s actually learning”)

```bash
docker run --rm \
  --network recursive-meta-learning-workbench_default \
  -e TARGET_URL=http://dvwa \
  rmlw:local \
  rmlw scan \
    --target http://dvwa \
    --mode learn \
    --iterations 30 \
    --format human
```

What to look for:

- **Meta-controller logs**: Strategy choices per iteration (baseline, rl, evolution, archive_reuse).
- **RL logs**: Which test families are prioritised over time (e.g. `RL selected test: xss`).
- **Evolution logs**: When the evolution mechanism is selected, payload population changes (e.g. `Evolution: population P -> Q ...`).
- **Findings variation**: Over 20–30 iterations you should see different vuln families getting chosen, not just one fixed pattern. The RL branch uses environment state (successful payloads, WAF hints) to shift which tests it prefers.

### Step 4 – Capture one proof run as evidence

Run a single learning run and capture stdout and stderr. You can use either the compose `rmlw` service or a standalone `rmlw:local` container.

**Using the compose `rmlw` service (recommended when DVWA is already up via compose):**

```bash
docker compose up -d dvwa
docker compose run --rm rmlw \
  rmlw scan \
    --target http://dvwa \
    --mode learn \
    --iterations 30 \
    --format human \
  1> /tmp/rmlw_learn_stdout.txt \
  2> /tmp/rmlw_learn_stderr.txt
docker compose down
```

**Using standalone `rmlw:local`** (after `docker build -t rmlw:local .` and with DVWA on the same network):

```bash
docker run --rm \
  --network recursive-meta-learning-workbench_default \
  -e TARGET_URL=http://dvwa \
  rmlw:local \
  rmlw scan \
    --target http://dvwa \
    --mode learn \
    --iterations 30 \
    --format human \
  1> /tmp/rmlw_learn_stdout.txt \
  2> /tmp/rmlw_learn_stderr.txt
```

Then summarise the run (e.g. in `docs/learning-proof-run.md`):

- Iterations 1/30 … 30/30.
- Mechanism choices (UCB -> rl vs evolution vs archive_reuse vs baseline).
- Test family variation (xss, cmdi, sqli, ssrf).
- Reward function behaviour (e.g. `reward=N findings=N` per iteration).

That summary is your “this system is learning, not just looping” exhibit.

## Proof-of-learning: how to read the logs

| What to check | What you see |
|---------------|--------------|
| Iterations ran | `Starting iteration 1/N` … `Starting iteration N/N`. |
| Mechanism selection | `Selected mechanism: rl` (or evolution, archive_reuse, baseline) each iteration. |
| RL test choice | When mechanism is rl: `RL selected test: xss` (or sqli, cmdi, ssrf, lfi). |
| RL variation | Different tests across iterations show the policy is not fixed. |
| Evolution | When mechanism is evolution: `Evolution: population P -> Q (survivors=S, children=C)`. |
| End-of-run summary | `Learn run complete: mechanism counts: rl=X, evolution=Y, ...`. |
| Reward | Each iteration: `Iteration complete: reward=R findings=F`. |

If mechanism choices and/or RL test choices change over iterations, or reward/state drive different behaviour, that is evidence the learning layer is active. For a reusable checklist and more detail, see [learning-evidence.md](learning-evidence.md). For an example proof run, see [learning-proof-run.md](learning-proof-run.md).

## Tear down

```bash
docker compose down
```

## Checklist: learning layer is working if you see

- **Iteration loop**: Log lines `Starting iteration 1/N` through `Starting iteration N/N` for the chosen N.
- **Mechanism selection**: Each iteration has a line like `Selected mechanism: rl` (or `evolution`, `archive_reuse`, `baseline`).
- **RL behavior**: When mechanism is `rl`, lines like `RL selected test: xss` (or sqli, cmdi, ssrf, lfi); across iterations, more than one test family appears.
- **Reward updates**: Each iteration logs `Iteration complete: reward=R findings=F`.
- **End-of-run summary**: A final line `Learn run complete: mechanism counts: rl=X, evolution=Y, ...`.

If these appear (or the relevant subset for the mechanisms selected), the learning layer is active. For a proof-run recipe and more detail, see [learning-proof-run.md](learning-proof-run.md) and [learning-evidence.md](learning-evidence.md).

## References

- [learning-evidence.md](learning-evidence.md) – Checklist and what “learning” means in RMLW.
- [learning-proof-run.md](learning-proof-run.md) – Example proof run and interpretation.
- [usage.md](usage.md) – CLI options and evaluation harness overview.
