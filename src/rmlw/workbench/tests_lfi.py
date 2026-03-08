"""
LFI / directory traversal test logic.

Attempts to read /etc/passwd via traversal payloads and
looks for known markers in the response.
"""

from typing import TYPE_CHECKING

from rmlw.workbench.payloads import TRAVERSAL_PROBES

if TYPE_CHECKING:
    from rmlw.workbench.core import WebAttackWorkbench


def test_traversal(workbench: "WebAttackWorkbench", url: str, param: str) -> None:
    """
    Run LFI/traversal probes.

    Sends traversal payloads targeting /etc/passwd and checks
    for the marker "root:x:0:0" in the response.

    Args:
        workbench: The WebAttackWorkbench instance.
        url: Endpoint URL.
        param: Parameter name to inject.
    """
    for payload in TRAVERSAL_PROBES:
        try:
            r = workbench.session.get(
                url,
                params={param: payload},
                timeout=workbench.config.request_timeout,
                verify=workbench.config.verify_tls,
            )
        except Exception:  # nosec B112 - resilience per payload, log handled elsewhere
            continue

        if "root:x:0:0" in r.text:
            workbench._record(
                "lfi_passwd",
                url,
                param,
                payload,
                {"status_code": r.status_code, "length": len(r.text)},
            )
            break
