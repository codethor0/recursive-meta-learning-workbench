"""Tests for Web Attack Workbench core."""

import json
from unittest.mock import MagicMock

import requests

from rmlw.workbench import Finding, WebAttackWorkbench


def test_finding_to_dict() -> None:
    """Finding.to_dict returns serialisable dict."""
    f = Finding(
        ftype="xss_reflection",
        url="http://test/",
        param="q",
        payload="<script>alert(1)</script>",
        detail={"status_code": 200},
    )
    d = f.to_dict()
    assert d["ftype"] == "xss_reflection"
    assert d["url"] == "http://test/"
    assert d["param"] == "q"
    assert d["payload"] == "<script>alert(1)</script>"
    assert d["detail"]["status_code"] == 200
    json.dumps(d)


def test_workbench_inject_query_param() -> None:
    """_inject_query_param correctly modifies URL."""
    w = WebAttackWorkbench("http://example.com")
    url = w._inject_query_param("http://example.com/page", "q", "test")
    assert "q=test" in url


def test_workbench_inject_query_param_preserves_existing() -> None:
    """_inject_query_param replaces existing param."""
    w = WebAttackWorkbench("http://example.com")
    url = w._inject_query_param("http://example.com/?q=old", "q", "new")
    assert "q=new" in url
    assert "q=old" not in url


def test_workbench_extract_params() -> None:
    """_extract_params returns param names from URL."""
    w = WebAttackWorkbench("http://example.com")
    params = w._extract_params("http://example.com/?a=1&b=2")
    assert set(params) == {"a", "b"}


def test_workbench_extract_params_empty_returns_default() -> None:
    """_extract_params returns ['q'] when no params."""
    w = WebAttackWorkbench("http://example.com")
    params = w._extract_params("http://example.com/")
    assert params == ["q"]


def test_workbench_crawl_seeds_base_url() -> None:
    """crawl() adds base URL to endpoints."""
    w = WebAttackWorkbench("http://example.com")
    w.crawl()
    assert "http://example.com" in w.endpoints


def test_workbench_run_calls_crawl() -> None:
    """run() calls crawl() first."""
    w = WebAttackWorkbench("http://example.com")
    original_crawl = w.crawl
    call_count = 0

    def counting_crawl() -> None:
        nonlocal call_count
        call_count += 1
        original_crawl()

    w.crawl = counting_crawl
    w.run()
    assert call_count == 1


def test_workbench_record_appends_finding() -> None:
    """_record appends to findings."""
    w = WebAttackWorkbench("http://example.com")
    w._record("xss_reflection", "http://test/", "q", "<script>", {"code": 200})
    assert len(w.findings) == 1
    assert w.findings[0].ftype == "xss_reflection"


def test_workbench_run_returns_findings() -> None:
    """run() returns list of Finding."""
    w = WebAttackWorkbench("http://invalid-target-for-test")
    w.endpoints.add("http://invalid-target-for-test/?q=1")
    findings = w.run()
    assert isinstance(findings, list)
    for f in findings:
        assert isinstance(f, Finding)


def test_workbench_skips_out_of_scope_endpoints() -> None:
    """run() skips endpoints from different host than base_url."""
    w = WebAttackWorkbench("http://example.com")
    w.endpoints.add("http://example.com/?q=1")
    w.endpoints.add("http://evil.com/?q=1")
    findings = w.run()
    for f in findings:
        assert "evil.com" not in f.url


def test_workbench_handles_network_errors_gracefully() -> None:
    """run() completes without crashing when requests fail (timeout, etc)."""
    mock_session = MagicMock()
    mock_session.get.side_effect = requests.Timeout("Connection timed out")
    w = WebAttackWorkbench("http://example.com", session=mock_session)
    w.endpoints.add("http://example.com/?q=1")
    findings = w.run()
    assert isinstance(findings, list)
    assert len(findings) == 0
