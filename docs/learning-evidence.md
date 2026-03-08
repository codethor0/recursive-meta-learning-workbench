# How We Know RMLW Is Learning

This document explains how to run learning experiments and what to look for to confirm the meta-learning layer is active. All testing must be against authorized lab targets only.

## Quick checklist

After running `rmlw scan --mode learn --iterations N` (or the equivalent via Docker):

| Check | What to look for |
|-------|------------------|
| Iterations run | Log lines `Starting iteration 1/N` through `Starting iteration N/N`. |
| Mechanism selection | Log line `Selected mechanism: <rl|evolution|archive_reuse|baseline>` each iteration. |
| RL activity | When mechanism is `rl`, log line `RL selected test: <xss|sqli|lfi|cmdi|ssrf>`. |
| RL variation | Different tests chosen across iterations (e.g. xss in one, ssrf in another). |
| Evolution activity | When mechanism is `evolution`, log line `Evolution: population P -> Q (survivors=S, children=C)`. |
| End-of-run summary | Log line `Learn run complete: mechanism counts: rl=X, evolution=Y, ...`. |
| Reward updates | Each iteration logs `Iteration complete: reward=R findings=F`. |
| Unit tests | `pytest tests/test_learning_*.py tests/test_*_rl.py` pass (RL, evolution, archive, meta-controller). |

If all of the above appear (or the relevant subset for the mechanisms that were selected), the learning layer is active.

## What "learning" means here

- **Meta-controller**: Picks a mechanism each iteration via UCB. Counts and mean rewards per mechanism are updated; over time the bandit can favor higher-reward mechanisms.
- **RL (RLPathOptimizer)**: Maintains Q-values over (state, test) pairs. Epsilon-greedy selection can change which test is chosen as the state (environment model) changes. Different test names in the logs across iterations show the policy is not fixed.
- **Evolution (EvolutionaryPayloadGenerator)**: When selected, evolves the payload population (survivors + children). Population size and fitness change over generations; logs show population before/after.
- **Archive**: Successful (vuln_type, payload, detail) are stored. The archive grows during a run; it is used for archive_reuse and can influence evolution when that mechanism is used.
- **Environment model**: Updated from findings (e.g. WAF hints, successful payloads). Its state feeds into RL state; so even if reward is constant (e.g. 5 findings every time on a simple target), internal state and thus RL choices can still change.

So "proof" of learning is: (1) mechanisms and RL test choices vary or respond to reward, (2) evolution logs appear when evolution is selected, (3) end-of-run mechanism counts reflect that multiple mechanisms were tried or one dominated in a way consistent with UCB.

## How to run a learning experiment

**With Docker and DVWA** (see [learning-lab-dvwa.md](learning-lab-dvwa.md)):

1. Uncomment the `dvwa` service in `docker-compose.yml`, then: `docker compose up -d dvwa`
2. Wait for DVWA to be ready (e.g. `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080` returns 200)
3. Run:  
   `docker compose run --rm rmlw rmlw scan --target http://dvwa --mode learn --iterations 10 --format human`  
   Or with JSON: add `--format json --output examples/dvwa-learn-findings.json`
4. Inspect stderr for the log lines in the checklist above. Inspect stdout (or the JSON file) for findings.

**Local (no Docker)** against a lab target on localhost:

```bash
rmlw scan --target http://localhost:8080 --mode learn --iterations 10 --format json --output examples/local-learn-findings.json
```

Then review logs (stderr) and `examples/local-learn-findings.json`.

## Increasing mechanism diversity

If every iteration shows `Selected mechanism: rl` and you want to see evolution or archive_reuse:

- Increase `--iterations` (e.g. 20 or 50) so UCB explores other mechanisms.
- In code, increase the UCB exploration constant (e.g. `ucb_beta` in `MetaController`) so exploration is stronger; run tests after any change.

## References

- [learning-lab-dvwa.md](learning-lab-dvwa.md) – Example DVWA lab run and results.
- [architecture.md](architecture.md) – RMLW architecture and data flow.
- [usage.md](usage.md) – CLI and Docker usage.
