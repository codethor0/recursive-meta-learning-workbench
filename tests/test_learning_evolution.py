"""Tests for EvolutionaryPayloadGenerator."""

import random

from rmlw.learning.evolution import EvolutionaryPayloadGenerator


def test_evolution_initial_population() -> None:
    """Population is seeded from input."""
    seeds = ["a", "b", "c"]
    evo = EvolutionaryPayloadGenerator(seeds)
    assert set(evo.population) == set(seeds)
    assert all(evo.fitness[p] == 0.0 for p in seeds)


def test_evolution_evolve_returns_population() -> None:
    """evolve() returns list of strings."""
    evo = EvolutionaryPayloadGenerator(["x", "y"])
    result = evo.evolve()
    assert isinstance(result, list)
    assert len(result) >= 2
    assert all(isinstance(p, str) for p in result)


def test_evolution_fitness_affects_selection() -> None:
    """Higher fitness payloads more likely to survive."""
    evo = EvolutionaryPayloadGenerator(["low", "high"])
    evo.fitness["low"] = 0.0
    evo.fitness["high"] = 10.0
    evo.evolve()
    assert "high" in evo.population


def test_evolution_mutate_changes_string() -> None:
    """_mutate produces different string (usually)."""
    evo = EvolutionaryPayloadGenerator(["test"])
    results = {evo._mutate("abc") for _ in range(20)}
    assert len(results) >= 2


def test_evolution_deterministic_with_seeded_rng() -> None:
    """evolve() is deterministic when using seeded RNG."""
    rng = random.Random(42)
    evo = EvolutionaryPayloadGenerator(["a", "b", "c"], rng=rng)
    evo.fitness["a"] = 1.0
    evo.fitness["b"] = 0.5
    evo.fitness["c"] = 0.0
    result1 = evo.evolve()

    rng2 = random.Random(42)
    evo2 = EvolutionaryPayloadGenerator(["a", "b", "c"], rng=rng2)
    evo2.fitness["a"] = 1.0
    evo2.fitness["b"] = 0.5
    evo2.fitness["c"] = 0.0
    result2 = evo2.evolve()

    assert result1 == result2


def test_evolution_evolve_produces_non_empty_payloads() -> None:
    """evolve() never produces empty strings in population."""
    evo = EvolutionaryPayloadGenerator(["ab", "cd"])
    for _ in range(5):
        evo.evolve()
    for p in evo.population:
        assert len(p) > 0


def test_evolution_crossover_combines() -> None:
    """_crossover combines two strings."""
    evo = EvolutionaryPayloadGenerator(["a", "b"])
    result = evo._crossover("hello", "world")
    assert len(result) == 5
    assert result != "hello"
    assert result != "world"
