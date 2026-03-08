"""
Environment model for RMLW.

Captures WAF hints, input filtering, and successful/failed payloads
to inform RL state and learning decisions.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rmlw.workbench.core import Finding


class EnvironmentModel:
    """
    Models the target environment based on test results.

    Tracks WAF presence, per-parameter filtering behaviour, and
    payload success/failure history per vulnerability type.
    """

    def __init__(self) -> None:
        self.waf_detected: bool = False
        self.framework: str | None = None
        self.input_filtering: dict[str, str] = {}
        self.successful_payloads: dict[str, list[str]] = {}
        self.failed_payloads: dict[str, list[str]] = {}

    def update_from_finding(self, finding: "Finding") -> None:
        """
        Update environment state from a finding.

        Records the payload as successful for its vulnerability type.
        Does not have access to raw response here; WAF/filter updates
        would require response object (handled in update_from_result if needed).

        Args:
            finding: A Finding from the Workbench.
        """
        vuln_type = finding.ftype
        payload = finding.payload
        self.successful_payloads.setdefault(vuln_type, []).append(payload)

    def update_from_result(
        self,
        vuln_type: str,
        param: str,
        payload: str,
        status_code: int,
        headers: dict[str, str],
        payload_in_response: bool,
    ) -> None:
        """
        Update environment from a raw test result (when response is available).

        Checks for WAF headers, 403 filtering, and success/failure.

        Args:
            vuln_type: Vulnerability type.
            param: Parameter name.
            payload: Payload used.
            status_code: HTTP status code.
            headers: Response headers.
            payload_in_response: Whether payload appeared in response.
        """
        header_str = " ".join(f"{k}: {v}" for k, v in headers.items())
        if "ModSecurity" in header_str:
            self.waf_detected = True

        if status_code == 403:
            self.input_filtering[param] = "blocked"

        looks_successful = status_code < 500 and payload_in_response
        if looks_successful:
            self.successful_payloads.setdefault(vuln_type, []).append(payload)
        else:
            self.failed_payloads.setdefault(vuln_type, []).append(payload)

    def copy(self) -> "EnvironmentModel":
        """Return a shallow copy of this environment model."""
        other = EnvironmentModel()
        other.waf_detected = self.waf_detected
        other.framework = self.framework
        other.input_filtering = dict(self.input_filtering)
        other.successful_payloads = {k: list(v) for k, v in self.successful_payloads.items()}
        other.failed_payloads = {k: list(v) for k, v in self.failed_payloads.items()}
        return other

    def state_tuple(self) -> tuple[bool, bool, int]:
        """
        Encode environment as a hashable state for RL.

        Returns:
            Tuple of (waf_detected, any_filtering, count_successes).
        """
        any_filtering = bool(self.input_filtering)
        count_successes = sum(len(payloads) for payloads in self.successful_payloads.values())
        return (self.waf_detected, any_filtering, count_successes)

    def state_key(self) -> tuple[bool, bool, int]:
        """Alias for state_tuple; matches spec naming."""
        return self.state_tuple()
