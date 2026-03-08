"""
Stub interfaces for future RMLW extensions.

These define clean interfaces for LLM integration and Fisher-Rao merging
as documented in docs/roadmap.md. No implementation required for PoC.
"""

from typing import Any, Protocol


class LLMPayloadGenerator(Protocol):
    """
    Interface for LLM-based payload generation.

    Future: Given environment summary and archive sample, generate
    new payload candidates. Would be called by MetaController when
    mechanism is 'llm' or similar.
    """

    def generate(
        self, env_summary: dict[str, Any], archive_sample: list[dict[str, Any]]
    ) -> list[str]:
        """Generate new payload strings. Returns empty list for stub."""
        ...


class LLMStrategyGenerator(Protocol):
    """
    Interface for LLM-based test strategy generation.

    Future: Given environment and performance logs, propose new
    test functions or algorithm modifications. Would require
    sandbox validation before adoption.
    """

    def propose_test(self, env: dict[str, Any], logs: list[dict[str, Any]]) -> Any | None:
        """Propose a new test function or None. Returns None for stub."""
        ...


class FisherRaoMerger(Protocol):
    """
    Interface for Fisher-Rao-style agent merging.

    Future: Combine multiple specialised agents (e.g. from archive)
    into a merged agent via Karcher mean on the manifold of
    output distributions. Preserves functionality better than
    naive parameter averaging.
    """

    def merge(self, agents: list[Any], weights: list[float] | None = None) -> Any:
        """Merge agents into single agent. Returns first agent for stub."""
        ...
