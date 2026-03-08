# Architecture

## Overview

RMLW has two main layers: the Web Attack Workbench (static foundation) and the Recursive Meta-Learning Layer (self-improving orchestration).

## Web Attack Workbench

The workbench runs vulnerability tests against HTTP endpoints.

### Test Families

| Test | Signal | Heuristic |
|------|--------|-----------|
| XSS | Payload reflection | Payload appears in response body |
| SQLi | Boolean logic | True/false conditions produce different responses |
| LFI | File content | /etc/passwd markers in response |
| CMDi | Timing | sleep N causes measurable delay |
| SSRF | Internal access | Non-error response to internal IP probes |

### Data Model

- **Endpoint**: (method, url, params, headers, body)
- **Parameter**: (name, location, baseline_value) – query, path, header, or body
- **Finding**: (ftype, url, param, payload, detail)

Parameters are extracted from the query string. For URLs without query params, a default "q" is used.

## Learning Layer

### EnvironmentModel

Captures target characteristics:

- waf_detected: WAF presence from headers
- input_filtering: Per-parameter filter behaviour
- successful_payloads: Payloads that triggered findings
- failed_payloads: Payloads that did not

### RLPathOptimizer

- State: Coarse encoding from EnvironmentModel
- Actions: Test families (xss, sqli, lfi, cmdi, ssrf)
- Algorithm: Tabular Q-learning

### EvolutionaryPayloadGenerator

- Population: Payload strings
- Fitness: Based on findings
- Operators: Mutation (encoding, case, quotes), crossover

### PersistentArchive

- Stores successful payloads with context
- Supports recent(n) and diversity retrieval
- Feeds recombination and novelty search

### MetaController

- UCB Bandit: Chooses which mechanism to apply
- Strategies: RL-driven, evolution, archive, baseline
- Reward: New findings, novelty

## Runtime Flow

1. MetaController selects mechanism (UCB)
2. Mechanism influences Workbench (payloads, test order)
3. Workbench runs tests against target
4. Findings update EnvironmentModel and Archive
5. RL/Evolution update based on reward
6. Repeat

## URL Utilities

Target URLs are validated and scoped:

- validate_target_url: Rejects disallowed schemes (file, javascript, data, etc.)
- normalize_url: Structural normalization
- url_in_scope: Ensures endpoints match the configured host

All scans are restricted to the host of the configured base URL.
