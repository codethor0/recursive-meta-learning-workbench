"""
HTTP readiness check for RMLW lab targets.

Waits for a target URL to return HTTP 200 before scans run.
Useful for Docker-based workflows where targets (e.g. DVWA) may
take a few seconds to become ready.
"""

import time

import requests
from requests import RequestException

from rmlw.logging_utils import get_logger

logger = get_logger(__name__)


class ReadinessTimeoutError(Exception):
    """Raised when target does not become ready within max_wait."""

    pass


def wait_for_http_ready(
    url: str,
    max_wait: float = 30.0,
    interval: float = 2.0,
    timeout_per_request: float = 5.0,
) -> None:
    """
    Wait for target URL to return HTTP 200.

    Retries at fixed intervals until ready or max_wait exceeded.
    Logs INFO when waiting and when ready.

    Args:
        url: Base URL to check (e.g. http://dvwa or http://localhost:8080).
        max_wait: Maximum seconds to wait. Default 30.
        interval: Seconds between retries. Default 2.
        timeout_per_request: Request timeout per attempt. Default 5.

    Raises:
        ReadinessTimeoutError: If target never returns 200 within max_wait.
    """
    elapsed = 0.0
    attempt = 0
    while elapsed < max_wait:
        attempt += 1
        try:
            resp = requests.get(url, timeout=timeout_per_request)
            if resp.status_code == 200:
                logger.info("Target ready: %s (HTTP 200 after %.1fs)", url, elapsed)
                return
            logger.info(
                "Waiting for target %s (attempt %d, HTTP %d, %.1fs elapsed)",
                url,
                attempt,
                resp.status_code,
                elapsed,
            )
        except RequestException as e:
            logger.info(
                "Waiting for target %s (attempt %d, error: %s, %.1fs elapsed)",
                url,
                attempt,
                type(e).__name__,
                elapsed,
            )
        time.sleep(interval)
        elapsed += interval

    raise ReadinessTimeoutError(
        f"Target {url} did not return HTTP 200 within {max_wait:.0f}s. "
        "Ensure the target is running (e.g. docker compose up -d dvwa) and retry."
    )
