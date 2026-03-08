"""
XSS (Cross-Site Scripting) test logic.

Checks for reflective XSS by injecting payloads and looking for
reflection in the response body.
"""

from typing import TYPE_CHECKING

from rmlw.workbench.payloads import XSS_PROBES

if TYPE_CHECKING:
    from rmlw.workbench.core import WebAttackWorkbench


def test_xss(workbench: "WebAttackWorkbench", url: str, param: str) -> None:
    """
    Run XSS probes on the given endpoint and parameter.

    For each payload, sends a request and checks if the payload
    appears in the response body (reflection). Records findings
    when reflection is detected.

    Args:
        workbench: The WebAttackWorkbench instance.
        url: Endpoint URL.
        param: Parameter name to inject.
    """
    for payload in XSS_PROBES:
        try:
            target = workbench._inject_query_param(url, param, payload)
            r = workbench.session.get(
                target,
                timeout=workbench.config.request_timeout,
                verify=workbench.config.verify_tls,
            )
        except Exception:  # nosec B112 - resilience per payload, log handled elsewhere
            continue

        if payload in r.text:
            workbench._record(
                "xss_reflection",
                url,
                param,
                payload,
                {"status_code": r.status_code, "length": len(r.text)},
            )
