# Cursor daily-driver prompt (small maintenance tasks)

Use this when you want Cursor to do **incremental work** (fixes, tests, doc updates, small features) without touching the full master spec. Paste into Agent / Instructions for quick sessions. For greenfield or large alignment work, use [cursor-master-prompt-from-scratch.md](cursor-master-prompt-from-scratch.md) or [cursor-master-prompt-continue.md](cursor-master-prompt-continue.md) instead.

---

You are working in `recursive-meta-learning-workbench/`. Do not create or modify files outside that folder.

- **Existing code is the source of truth.** Treat missing pieces as gaps to fill; do not rebuild or replace working modules.
- **Doctrine:** No emojis. No eval/exec or unsafe deserialization. Authorized testing only. URL scope enforced via `url_utils` in both CLI and Workbench; only http/https, no out-of-scope requests.
- **Quality bar:** After any change, run `black`, `ruff`, `mypy`, `bandit`, `pytest` and fix anything that fails. Do not relax existing checks.
- **Tasks:** Stay incremental. Prefer small, focused edits (e.g. "fix failing tests", "align docs/usage.md with CLI", "add tests for X") rather than broad refactors.

When in doubt, run the quality gates and treat the full master prompt (from-scratch or continue) as the canonical spec for architecture and doctrine.
