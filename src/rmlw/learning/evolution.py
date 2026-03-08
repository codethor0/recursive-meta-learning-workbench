"""
Evolutionary payload generator for RMLW.

Maintains a population of payloads, mutates and recombines them
based on fitness from test results. State encoding is deterministic
when an optional RNG is provided for testing.
"""

import random


class EvolutionaryPayloadGenerator:
    """
    Evolutionary search over payload strings.

    Population is seeded from static payload lists. Fitness is
    updated externally based on findings. Evolve() performs
    selection, crossover, and mutation.
    """

    def __init__(
        self,
        seed_payloads: list[str],
        rng: random.Random | None = None,
    ) -> None:
        self.population: list[str] = list(seed_payloads)
        self.fitness: dict[str, float] = dict.fromkeys(seed_payloads, 0.0)
        self._rng = rng or random

    def _mutate(self, payload: str) -> str:
        """
        Mutate a payload: flip case or insert quote.

        Returns:
            Mutated payload string.
        """
        if not payload:
            return payload

        p_list = list(payload)
        idx = self._rng.randrange(len(p_list))
        c = p_list[idx]

        if c.isalpha():
            p_list[idx] = c.swapcase()
        else:
            p_list.insert(idx, "'")

        return "".join(p_list)

    def _crossover(self, a: str, b: str) -> str:
        """Combine two payloads at a random cut point."""
        if not a or not b:
            return a or b
        cut = self._rng.randrange(1, min(len(a), len(b)))
        return a[:cut] + b[cut:]

    def evolve(self) -> list[str]:
        """
        Perform one generation: select, crossover, mutate.

        Top half by fitness survive. Children fill the rest.
        New children start with fitness 0.

        Returns:
            Updated population.
        """
        if not self.population:
            return []

        sorted_pop = sorted(
            self.population,
            key=lambda p: self.fitness.get(p, 0.0),
            reverse=True,
        )
        n_survivors = max(1, len(sorted_pop) // 2)
        survivors = sorted_pop[:n_survivors]

        children: list[str] = []
        while len(children) < len(self.population):
            parents = self._rng.sample(survivors, k=min(2, len(survivors)))
            child = self._crossover(parents[0], parents[1]) if len(parents) == 2 else parents[0]
            child = self._mutate(child)
            children.append(child)
            self.fitness.setdefault(child, 0.0)

        self.population = survivors + children
        return self.population
