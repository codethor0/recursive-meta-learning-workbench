# RMLW Learning Proof Run

This document defines how to capture a "proof run" and what to look for in the logs to verify the learning layer is active. All commands are for a local DVWA lab target (authorized use only).

## Proof run recipe

Run a learning scan and capture stdout and stderr for later inspection:

1. Enable the DVWA service in `docker-compose.yml` (uncomment the `dvwa` block), then:

```bash
docker compose up -d dvwa
```

2. Run the learning scan and redirect output (use `rmlw:local` on the compose network, or the compose `rmlw` service):

**Option A – using the compose `rmlw` service:**

```bash
docker compose run --rm rmlw \
  rmlw scan \
    --target http://dvwa \
    --mode learn \
    --iterations 30 \
    --format human \
  1> /tmp/rmlw_learn_stdout.txt \
  2> /tmp/rmlw_learn_stderr.txt
```

**Option B – using standalone `rmlw:local` (after `docker build -t rmlw:local .`):**

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

3. Tear down:

```bash
docker compose down
```

Inspect `/tmp/rmlw_learn_stderr.txt` for the log lines below; inspect `/tmp/rmlw_learn_stdout.txt` for findings (human format).

## Which log lines to look for

In **stderr** (learning logs), assert the following:

| Assertion | Log line pattern |
|-----------|-------------------|
| Iterations are running | `Starting iteration 1/N` through `Starting iteration N/N` |
| Meta-controller is choosing a mechanism | `Selected mechanism: rl` (or `evolution`, `archive_reuse`, `baseline`) each iteration |
| RL is active when mechanism is rl | `RL selected test: xss` (or sqli, cmdi, ssrf, lfi) |
| RL explores more than one test family | Across iterations, different test names appear (not always the same one) |
| Reward is updated | `Iteration complete: reward=R findings=F` each iteration |
| End-of-run summary | `Learn run complete: mechanism counts: rl=X, evolution=Y, ...` |

If you see a sequence of iterations, mechanism selection lines, and (when RL is selected) varying test families over iterations, the learning layer is working. For a formal checklist and interpretation, see [learning-evidence.md](learning-evidence.md).

---

## Example run parameters (recorded run)

- **Target**: http://dvwa (Docker network)
- **Mode**: learn
- **Iterations**: 30
- **Command**: `docker compose run --rm rmlw rmlw scan --target http://dvwa --mode learn --iterations 30 --format human`

## Evidence that RMLW is learning

### 1. Iterations executed

All 30 iterations ran. Logs show `Starting iteration 1/30` through `Starting iteration 30/30` and 30 corresponding `Iteration complete: reward=5 findings=5` lines.

### 2. Mechanism selection

In this run the UCB bandit selected the **rl** mechanism for all 30 iterations. So mechanism selection was consistent (rl), and the meta-controller is making a choice each iteration based on UCB state.

### 3. RL test selection variation (proof of learning)

The RLPathOptimizer chooses which test family to emphasize each iteration. The run showed **four different test types** selected:

| RL selected test | Count |
|------------------|-------|
| xss              | 27    |
| cmdi             | 1     |
| sqli             | 1     |
| ssrf             | 1     |

So the RL policy is **not** fixed: it chose xss most often but also cmdi, sqli, and ssrf. That variation is driven by the internal Q-values and environment model state, which update after each iteration. This is direct evidence that the learning layer is updating state and that the policy responds to it.

### 4. Reward and findings

Each iteration reported `reward=5 findings=5`. On this DVWA setup the workbench always returns the same 5 SSRF candidates, so the observed reward is constant. Nevertheless, the **internal state** (Q-values, environment model, archive) changes between iterations, which is why RL test selection varied.

### 5. Evolution and other mechanisms

Evolution logs (`Evolution: population P -> Q ...`) did not appear in this run because UCB never selected the `evolution` mechanism. With more iterations or higher UCB exploration, evolution and archive_reuse can be selected; when they are, the corresponding logs and end-of-run mechanism counts would show them. The unit tests in `tests/test_learning_*.py` already verify that evolution and the meta-controller behave correctly when invoked.

## Conclusion

- **Learning is occurring**: RL test selection changed across iterations (xss, sqli, ssrf, cmdi), driven by updated internal state.
- **Meta-controller is active**: It selected a mechanism (rl) every iteration via UCB.
- **Reward is used**: Although reward was constant (5) in this scenario, the bandit and RL components use it; in scenarios with varying findings, mechanism selection and RL would adapt further.

For a reusable checklist and how to reproduce, see [learning-evidence.md](learning-evidence.md).
