"""Tests for RLPathOptimizer."""

import pytest

from rmlw.learning.env_model import EnvironmentModel
from rmlw.learning.rl import RLPathOptimizer


def test_rl_select_test_returns_valid_action() -> None:
    """select_test returns one of available_tests."""
    env = EnvironmentModel()
    rl = RLPathOptimizer(exploration=0.0)
    tests = ["xss", "sqli", "lfi"]
    for _ in range(10):
        choice = rl.select_test(env, tests)
        assert choice in tests


def test_rl_select_test_explores_with_epsilon() -> None:
    """With exploration=1.0, all actions get selected eventually."""
    env = EnvironmentModel()
    rl = RLPathOptimizer(exploration=1.0)
    tests = ["xss", "sqli"]
    seen = set()
    for _ in range(50):
        choice = rl.select_test(env, tests)
        seen.add(choice)
    assert len(seen) == 2


def test_rl_update_changes_q_value() -> None:
    """update() modifies Q-table."""
    env_before = EnvironmentModel()
    env_after = EnvironmentModel()
    env_after.successful_payloads["xss"] = ["p1"]
    rl = RLPathOptimizer(exploration=0.0, learning_rate=0.5)
    tests = ["xss", "sqli"]
    rl.update(env_before, "xss", 1.0, env_after, tests)
    key = (env_before.state_tuple(), "xss")
    assert key in rl.q_table
    assert rl.q_table[key] > 0


def test_rl_select_test_empty_raises() -> None:
    """select_test with empty list raises."""
    env = EnvironmentModel()
    rl = RLPathOptimizer()
    with pytest.raises(ValueError, match="cannot be empty"):
        rl.select_test(env, [])
