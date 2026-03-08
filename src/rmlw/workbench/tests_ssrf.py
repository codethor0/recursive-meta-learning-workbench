"""
SSRF (Server-Side Request Forgery) test logic.

Probes with internal IP/host aliases and records soft responses
that suggest the server may have processed the request.
"""

from typing import TYPE_CHECKING

from rmlw.workbench.payloads import IP_ALIASES

if TYPE_CHECKING:
    from rmlw.workbench.core import WebAttackWorkbench


def test_ssrf_basic(workbench: "WebAttackWorkbench", url: str, param: str) -> None:
    """
    Run SSRF probes with internal address aliases.

    For each alias (127.0.0.1, localhost, decimal, hex, IPv6),
    sends a request with the URL in the parameter. Records
    responses that do not immediately fail with common errors.

    Args:
        workbench: The WebAttackWorkbench instance.
        url: Endpoint URL.
        param: Parameter name to inject.
    """
    for alias in IP_ALIASES:
        try:
            r = workbench.session.get(
                url,
                params={param: f"http://{alias}/"},
                timeout=workbench.config.request_timeout,
                verify=workbench.config.verify_tls,
            )
        except Exception:  # nosec B112 - resilience per payload, log handled elsewhere
            continue

        if r.status_code not in (400, 404, 500, 501, 502, 503):
            workbench._record(
                "ssrf_candidate",
                url,
                param,
                alias,
                {"status_code": r.status_code, "length": len(r.text)},
            )
