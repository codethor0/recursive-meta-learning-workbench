"""
Core Web Attack Workbench.

Models endpoints, runs vulnerability tests, and collects findings.
"""

from dataclasses import asdict, dataclass
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import requests

from rmlw.config import WorkbenchConfig
from rmlw.logging_utils import get_logger
from rmlw.url_utils import url_in_scope
from rmlw.workbench import discovery
from rmlw.workbench.tests_cmdi import test_cmd_injection
from rmlw.workbench.tests_lfi import test_traversal
from rmlw.workbench.tests_sqli import test_sqli_boolean
from rmlw.workbench.tests_ssrf import test_ssrf_basic
from rmlw.workbench.tests_xss import test_xss

logger = get_logger(__name__)


@dataclass
class Finding:
    """
    A candidate vulnerability finding.

    Attributes:
        ftype: Vulnerability type (e.g. xss_reflection, sqli_boolean).
        url: Endpoint URL where the finding was observed.
        param: Parameter name that was probed.
        payload: The probe that triggered the signal.
        detail: Supporting evidence (status codes, lengths, timing, etc.).
    """

    ftype: str
    url: str
    param: str
    payload: str
    detail: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Convert to a JSON-serialisable dictionary."""
        return asdict(self)


class WebAttackWorkbench:
    """
    Web Attack Workbench for targeted vulnerability testing.

    Models a web application as a set of endpoints and parameters,
    runs probes for XSS, SQLi, LFI, CMDi, and SSRF, and collects
    structured findings with payload and evidence.

    For authorised lab use only.
    """

    def __init__(
        self,
        base_url: str,
        session: requests.Session | None = None,
        config: WorkbenchConfig | None = None,
    ) -> None:
        """
        Initialise the Workbench.

        Args:
            base_url: Base URL of the target (e.g. http://localhost:8080).
            session: Optional requests.Session for connection reuse.
            config: Optional configuration; uses defaults if not provided.
        """
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self.config = config or WorkbenchConfig()
        self.endpoints: set[str] = set()
        self.findings: list[Finding] = []
        parsed = urlparse(self.base_url)
        self._base_netloc = parsed.netloc or ""

    def crawl(self) -> None:
        """
        Discover endpoints.

        Default implementation seeds the base URL. Override or extend
        for HTML form discovery, proxy import, OpenAPI, etc.
        """
        discovery.crawl(self)

    def _inject_query_param(self, url: str, name: str, value: str) -> str:
        """Safely inject or replace a query parameter in a URL."""
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        qs[name] = [value]
        new_query = urlencode(qs, doseq=True)
        return urlunparse(parsed._replace(query=new_query))

    def _extract_params(self, url: str) -> list[str]:
        """
        Extract testable query parameter names from a URL.

        Returns a list of param names. For URLs without params,
        returns a default list (e.g. ["q"]) for simple targets.
        """
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        if qs:
            return list(qs.keys())
        return ["q"]

    def _record(
        self,
        ftype: str,
        url: str,
        param: str,
        payload: str,
        detail: dict[str, Any] | None = None,
    ) -> None:
        """Record a finding."""
        self.findings.append(
            Finding(
                ftype=ftype,
                url=url,
                param=param,
                payload=payload,
                detail=detail or {},
            )
        )
        logger.info("Finding: %s url=%s param=%s", ftype, url, param)

    def run(self) -> list[Finding]:
        """
        Run all enabled tests on discovered endpoints.

        Returns:
            List of Finding objects.
        """
        self.findings = []
        self.crawl()

        in_scope = [ep for ep in self.endpoints if url_in_scope(ep, self._base_netloc)]
        if len(in_scope) < len(self.endpoints):
            logger.warning(
                "Skipped %d endpoints outside scope (host)",
                len(self.endpoints) - len(in_scope),
            )

        logger.info("Running workbench on %d endpoints", len(in_scope))

        for ep in in_scope:
            params = self._extract_params(ep)
            for param in params:
                test_xss(self, ep, param)
                test_traversal(self, ep, param)
                test_sqli_boolean(self, ep, param)
                test_cmd_injection(self, ep, param)
                test_ssrf_basic(self, ep, param)

        logger.info("Workbench complete: %d findings", len(self.findings))
        return self.findings
