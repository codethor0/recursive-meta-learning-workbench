"""
Configuration for RMLW.

Holds defaults for timeouts, thresholds, and scope validation.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkbenchConfig:
    """Configuration for the Web Attack Workbench."""

    request_timeout: float = 5.0
    """Timeout in seconds for HTTP requests."""

    cmd_sleep_threshold: float = 4.0
    """Seconds of delay to consider command injection (sleep N)."""

    verify_tls: bool = True
    """Verify TLS certificates. Set False only for lab targets with self-signed certs."""


@dataclass(frozen=True)
class LearningConfig:
    """Configuration for the learning layer."""

    rl_learning_rate: float = 0.1
    rl_discount: float = 0.9
    rl_exploration: float = 0.2
    ucb_beta: float = 1.0
    evolution_population_size: int = 20
