"""
Meta-controller for RMLW.

Orchestrates learning mechanisms using a UCB multi-armed bandit.
"""

import math
from typing import TYPE_CHECKING

from rmlw.learning.archive import PersistentArchive
from rmlw.learning.env_model import EnvironmentModel
from rmlw.learning.evolution import EvolutionaryPayloadGenerator
from rmlw.learning.rl import RLPathOptimizer
from rmlw.logging_utils import get_logger
from rmlw.workbench.payloads import (
    IP_ALIASES,
    TRAVERSAL_PROBES,
    XSS_PROBES,
)

if TYPE_CHECKING:
    from rmlw.workbench.core import Finding, WebAttackWorkbench

logger = get_logger(__name__)

MECHANISMS = ["rl", "evolution", "archive_reuse", "baseline"]


class MetaController:
    """
    Orchestrates Workbench and learning components.

    Uses UCB bandit to select which mechanism to apply each iteration:
        - rl: RL-driven test selection
        - evolution: Evolutionary payload refinement
        - archive_reuse: Reuse high-fitness payloads from archive
        - baseline: Standard workbench run

    Logs metrics for observability.
    """

    def __init__(
        self,
        workbench: "WebAttackWorkbench",
        seed_payloads: list[str] | None = None,
        ucb_beta: float = 1.0,
    ) -> None:
        """
        Initialise MetaController.

        Args:
            workbench: WebAttackWorkbench instance.
            seed_payloads: Payloads for evolutionary generator.
            ucb_beta: UCB exploration parameter.
        """
        self.workbench = workbench
        self.env = EnvironmentModel()
        self.rl = RLPathOptimizer()
        payloads = seed_payloads or (XSS_PROBES + TRAVERSAL_PROBES + IP_ALIASES[:2])
        self.evo = EvolutionaryPayloadGenerator(payloads)
        self.archive = PersistentArchive()
        self.ucb_beta = ucb_beta
        self.available_tests = ["xss", "sqli", "lfi", "cmdi", "ssrf"]

        # UCB state: mechanism -> (total_reward, count)
        self._ucb_rewards: dict[str, float] = dict.fromkeys(MECHANISMS, 0.0)
        self._ucb_counts: dict[str, int] = dict.fromkeys(MECHANISMS, 0)
        self._ucb_total_selections = 0

    def _select_mechanism(self) -> str:
        """Select mechanism using UCB."""
        scores: dict[str, float] = {}
        for m in MECHANISMS:
            n = self._ucb_counts[m] + 1
            mu = self._ucb_rewards[m] / max(1, self._ucb_counts[m])
            ucb = mu + self.ucb_beta * math.sqrt(math.log(self._ucb_total_selections + 2) / n)
            scores[m] = ucb

        best = max(MECHANISMS, key=lambda x: scores[x])
        return best

    def _run_workbench(self) -> list["Finding"]:
        """Run workbench and return findings."""
        return self.workbench.run()

    def run_iteration(self) -> list["Finding"]:
        """
        Run one meta-controller iteration.

        1. Select mechanism via UCB
        2. Run workbench (mechanism influences via RL/evolution in future)
        3. Update env, archive, fitness, RL
        4. Update UCB stats
        5. Return findings

        Returns:
            List of findings from this iteration.
        """
        mechanism = self._select_mechanism()
        self._ucb_total_selections += 1
        self._ucb_counts[mechanism] += 1

        logger.info("Selected mechanism: %s", mechanism)

        test_choice = ""
        env_before = self.env.copy()
        if mechanism == "rl":
            test_choice = self.rl.select_test(self.env, self.available_tests)
            logger.info("RL selected test: %s", test_choice)

        findings = self._run_workbench()
        reward = float(len(findings))

        for f in findings:
            self.env.update_from_finding(f)
            self.archive.add_success(f.ftype, f.payload, f.detail)
            if f.payload in self.evo.fitness:
                self.evo.fitness[f.payload] += 1.0

        if mechanism == "archive_reuse":
            pass
        elif mechanism == "evolution":
            self.evo.evolve()
            logger.info("Evolved population: %d payloads", len(self.evo.population))

        if mechanism == "rl" and test_choice:
            self.rl.update(env_before, test_choice, reward, self.env, self.available_tests)

        self._ucb_rewards[mechanism] += reward

        logger.info(
            "Iteration complete: reward=%.0f findings=%d",
            reward,
            len(findings),
        )
        return findings

    def run_iterations(self, n: int) -> list["Finding"]:
        """
        Run N iterations and return all findings.

        Args:
            n: Number of iterations.

        Returns:
            Combined list of findings from all iterations.
        """
        all_findings: list[Finding] = []
        for i in range(n):
            logger.info("Starting iteration %d/%d", i + 1, n)
            findings = self.run_iteration()
            all_findings.extend(findings)
        return all_findings
