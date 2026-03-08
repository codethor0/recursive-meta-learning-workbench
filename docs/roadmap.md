# RMLW Roadmap

## Implemented (PoC)

- [x] Web Attack Workbench (XSS, SQLi, LFI, CMDi, SSRF)
- [x] EnvironmentModel
- [x] RLPathOptimizer (Q-learning)
- [x] EvolutionaryPayloadGenerator
- [x] PersistentArchive
- [x] MetaController with UCB bandit
- [x] CLI (baseline + learn modes)
- [x] Docker + docker-compose

## Phase 1 – Foundation (Weeks 1–2) ✓

- [x] Web Attack Workbench with core tests
- [x] Minimal environment model
- [x] JSON log format for findings

## Phase 2 – RL and Evolution (Weeks 3–5) ✓

- [x] RLPathOptimizer for test selection
- [x] EvolutionaryPayloadGenerator
- [x] Environment model integration

## Phase 3 – LLM Integration (Weeks 6–8)

- [ ] Prompt templates for payload generation
- [ ] Sandbox for validating generated code
- [ ] Human-in-the-loop review workflow
- [ ] Interface: `LLMPayloadGenerator.generate(env_summary, archive_sample) -> list[str]`
- [ ] Interface: `LLMStrategyGenerator.propose_test(env, logs) -> Optional[TestFunction]`

## Phase 4 – Meta-Controller Enhancements (Weeks 9–10)

- [ ] Richer reward functions (novelty, diversity)
- [ ] Per-target mechanism preference metrics
- [ ] Configurable UCB parameters

## Phase 5 – Recursive Improvement (Weeks 11–12)

- [ ] Fisher-Rao agent merging (stub exists)
  - Convert agents to output distributions
  - Compute Karcher mean on manifold
  - Fit merged agent
- [ ] Meta-controller self-modification pipeline
  - LLM suggests changes → sandbox test → adopt if metrics improve
- [ ] Learning curve and archive visualisations

## Future Extensions

### Discovery

- Proxy import (Burp, ZAP, HAR)
- HTML form and link discovery
- JavaScript analysis for dynamic endpoints
- OpenAPI/Swagger integration
- GraphQL introspection

### Vulnerability Classes

- XXE (XML External Entity)
- SSTI (Server-Side Template Injection)
- Deserialisation
- BAC/IDOR (multi-session comparison)
- Race conditions

### Integration

- CI/CD pipelines with risk gating
- Headless browser for dynamic XSS
- Telemetry from production/honeypots into archive
