"""Tests for URL validation and normalization."""

import pytest

from rmlw.url_utils import (
    URLValidationError,
    normalize_url,
    url_in_scope,
    validate_target_url,
)


def test_validate_target_url_accepts_http() -> None:
    """validate_target_url accepts http URLs."""
    result = validate_target_url("http://example.com")
    assert result.startswith("http://")
    assert "example.com" in result


def test_validate_target_url_accepts_https() -> None:
    """validate_target_url accepts https URLs."""
    result = validate_target_url("https://example.com/path")
    assert result.startswith("https://")


def test_validate_target_url_adds_http_if_no_scheme() -> None:
    """validate_target_url adds http when scheme missing."""
    result = validate_target_url("example.com")
    assert result.startswith("http://")


def test_validate_target_url_rejects_file_scheme() -> None:
    """validate_target_url rejects file: scheme."""
    with pytest.raises(URLValidationError, match="not allowed"):
        validate_target_url("file:///etc/passwd")


def test_validate_target_url_rejects_javascript_scheme() -> None:
    """validate_target_url rejects javascript: scheme."""
    with pytest.raises(URLValidationError, match="not allowed"):
        validate_target_url("javascript:alert(1)")


def test_validate_target_url_rejects_ftp_scheme() -> None:
    """validate_target_url rejects ftp: scheme."""
    with pytest.raises(URLValidationError, match="not allowed"):
        validate_target_url("ftp://example.com")


def test_validate_target_url_rejects_empty() -> None:
    """validate_target_url rejects empty string."""
    with pytest.raises(URLValidationError, match="empty"):
        validate_target_url("")


def test_url_in_scope_same_host() -> None:
    """url_in_scope returns True for same host."""
    assert url_in_scope("http://example.com/path", "example.com") is True


def test_url_in_scope_different_host() -> None:
    """url_in_scope returns False for different host."""
    assert url_in_scope("http://evil.com/path", "example.com") is False


def test_url_in_scope_case_insensitive() -> None:
    """url_in_scope is case-insensitive for netloc."""
    assert url_in_scope("http://Example.COM/path", "example.com") is True


def test_normalize_url_strips_trailing_slash() -> None:
    """normalize_url strips trailing slash from path (except root)."""
    result = normalize_url("http://example.com/path/")
    assert result == "http://example.com/path"
