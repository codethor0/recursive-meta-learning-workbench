"""
Command injection test logic (timing-based).

Uses a sleep payload to detect command injection via timing channel.
"""

import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rmlw.workbench.core import WebAttackWorkbench


def test_cmd_injection(workbench: "WebAttackWorkbench", url: str, param: str) -> None:
    """
    Run timing-based command injection probe.

    Sends a payload with "sleep 5" and measures elapsed time.
    If elapsed > threshold (default 4s), records a cmd_time finding.

    Args:
        workbench: The WebAttackWorkbench instance.
        url: Endpoint URL.
        param: Parameter name to inject.
    """
    payload = "test; sleep 5"
    try:
        start = time.time()
        workbench.session.get(
            url,
            params={param: payload},
            timeout=10,
            verify=workbench.config.verify_tls,
        )
        elapsed = time.time() - start
    except Exception:
        return

    if elapsed > workbench.config.cmd_sleep_threshold:
        workbench._record(
            "cmd_time",
            url,
            param,
            payload,
            {"elapsed": elapsed},
        )
