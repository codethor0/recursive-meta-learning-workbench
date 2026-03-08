# RMLW Wiki

## Purpose

The Recursive Meta-Learning Workbench (RMLW) is a security research tool for web vulnerability testing in authorized lab environments. It combines a static Web Attack Workbench (XSS, SQLi, LFI, CMDi, SSRF) with a recursive meta-learning layer that adapts payloads and test strategies based on target feedback.

## High-Level Architecture

RMLW has two main layers:

1. **Web Attack Workbench** – Runs vulnerability tests against configured endpoints. Tests include XSS (reflection), SQLi (boolean logic), LFI (file inclusion), CMDi (command injection), and SSRF (internal access probes).

2. **Recursive Meta-Learning Layer** – Orchestrates the workbench using:
   - **EnvironmentModel**: Captures target characteristics (WAF, filters, successful payloads)
   - **RLPathOptimizer**: Q-learning to choose test families
   - **EvolutionaryPayloadGenerator**: Mutates and evolves payloads
   - **PersistentArchive**: Stores successful payloads for reuse
   - **MetaController**: UCB bandit selects which mechanism to apply

The MetaController selects a mechanism (RL, evolution, archive, or baseline), the workbench runs tests, findings update the model and archive, and the cycle repeats.

## Wiki Pages

- **Getting-Started** – Prerequisites, install, baseline scan, learning mode, troubleshooting
- **Architecture** – Detailed component overview and data flow
- **Contributing** – How to run tests, coding style, PR process
- **Security-and-Scope** – Authorized use, scope, assumptions
