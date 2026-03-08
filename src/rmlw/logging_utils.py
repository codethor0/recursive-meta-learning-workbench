"""
Logging utilities for RMLW.

Provides structured logging suitable for security tooling.
"""

import logging
import sys
from typing import Any


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Get a configured logger for the given module name.

    Args:
        name: Logger name (typically __name__).
        level: Logging level.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(level)
    return logger


def log_finding(logger: logging.Logger, ftype: str, url: str, param: str) -> None:
    """Log a finding in a parseable format."""
    logger.info("Finding: %s url=%s param=%s", ftype, url, param)


def log_metrics(logger: logging.Logger, metrics: dict[str, Any]) -> None:
    """Log structured metrics."""
    parts = " ".join(f"{k}={v}" for k, v in metrics.items())
    logger.info("Metrics: %s", parts)
