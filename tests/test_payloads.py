"""Tests for payload libraries."""

from rmlw.workbench.payloads import IP_ALIASES, TRAVERSAL_PROBES, XSS_PROBES


def test_xss_probes_non_empty() -> None:
    """XSS_PROBES contains expected payloads."""
    assert len(XSS_PROBES) >= 1
    assert any("<script>" in p for p in XSS_PROBES)


def test_traversal_probes_contain_passwd() -> None:
    """TRAVERSAL_PROBES target /etc/passwd."""
    assert any("passwd" in p for p in TRAVERSAL_PROBES)
    assert any(".." in p for p in TRAVERSAL_PROBES)


def test_ip_aliases_contain_loopback() -> None:
    """IP_ALIASES contains loopback variants."""
    assert "127.0.0.1" in IP_ALIASES
    assert "localhost" in IP_ALIASES
