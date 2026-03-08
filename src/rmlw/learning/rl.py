"""
RL-based test selection for RMLW.

Simple Q-learning to choose which vulnerability test family to prioritise.
"""

import random
from typing import Any

from rmlw.learning.env_model import EnvironmentModel


class RLPathOptimizer:
    """
    Q-learning based test selector.

    State: coarse encoding from EnvironmentModel.
    Actions: test families (xss, sqli, lfi, cmdi, ssrf).
    """

    def __init__(
        self,
        learning_rate: float = 0.1,
        discount: float = 0.9,
        exploration: float = 0.2,
    ) -> None:
        self.q_table: dict[tuple[Any, ...], float] = {}
        self.lr = learning_rate
        self.gamma = discount
        self.epsilon = exploration

    def _state_from_env(self, env: EnvironmentModel) -> tuple[Any, ...]:
        """Encode environment as a coarse state tuple."""
        return env.state_tuple()

    def select_test(self, env: EnvironmentModel, available_tests: list[str]) -> str:
        """
        Select which test family to run.

        With probability epsilon, explores randomly. Otherwise
        chooses the test with highest Q-value for current state.

        Args:
            env: Current environment model.
            available_tests: List of test names.

        Returns:
            Selected test name.
        """
        if not available_tests:
            raise ValueError("available_tests cannot be empty")

        state = self._state_from_env(env)

        if random.random() < self.epsilon:  # nosec B311 - RL exploration, not crypto
            return random.choice(available_tests)  # nosec B311

        best_test = available_tests[0]
        best_value = float("-inf")

        for t in available_tests:
            key = (state, t)
            value = self.q_table.get(key, 0.0)
            if value > best_value:
                best_value = value
                best_test = t

        return best_test

    def update(
        self,
        env_before: EnvironmentModel,
        test_name: str,
        reward: float,
        env_after: EnvironmentModel,
        available_tests: list[str],
    ) -> None:
        """
        Update Q-value using Q-learning.

        Q(s,a) <- Q(s,a) + lr * (r + gamma * max_a' Q(s',a') - Q(s,a))

        Args:
            env_before: State before the test.
            test_name: Test that was run.
            reward: Observed reward.
            env_after: State after the test.
            available_tests: Available actions in next state.
        """
        s = self._state_from_env(env_before)
        s_next = self._state_from_env(env_after)

        old_q = self.q_table.get((s, test_name), 0.0)
        next_q_values = [self.q_table.get((s_next, t), 0.0) for t in available_tests]
        max_next_q = max(next_q_values) if next_q_values else 0.0

        new_q = old_q + self.lr * (reward + self.gamma * max_next_q - old_q)
        self.q_table[(s, test_name)] = new_q
