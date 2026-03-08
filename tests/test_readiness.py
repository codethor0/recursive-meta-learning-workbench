"""Tests for readiness module."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from rmlw.readiness import ReadinessTimeoutError, wait_for_http_ready


def test_wait_for_http_ready_succeeds_immediately() -> None:
    """Target returns 200 on first attempt."""
    with patch("rmlw.readiness.requests") as mock_requests:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_requests.get.return_value = mock_resp

        wait_for_http_ready("http://test:80", max_wait=10, interval=1)

        mock_requests.get.assert_called_once_with("http://test:80", timeout=5.0)


def test_wait_for_http_ready_succeeds_after_retries() -> None:
    """Target returns 200 on third attempt."""
    with patch("rmlw.readiness.requests") as mock_requests:
        mock_fail = MagicMock()
        mock_fail.status_code = 503
        mock_ok = MagicMock()
        mock_ok.status_code = 200
        mock_requests.get.side_effect = [mock_fail, mock_fail, mock_ok]

        wait_for_http_ready("http://test:80", max_wait=10, interval=0.01)

        assert mock_requests.get.call_count == 3


def test_wait_for_http_ready_timeout() -> None:
    """Raises ReadinessTimeoutError when target never returns 200."""
    with patch("rmlw.readiness.requests") as mock_requests:
        mock_resp = MagicMock()
        mock_resp.status_code = 503
        mock_requests.get.return_value = mock_resp

        with pytest.raises(ReadinessTimeoutError) as exc_info:
            wait_for_http_ready("http://test:80", max_wait=0.05, interval=0.01)

        assert "did not return HTTP 200" in str(exc_info.value)
        assert "http://test:80" in str(exc_info.value)


def test_wait_for_http_ready_request_exception_then_success() -> None:
    """Target raises RequestException then returns 200."""
    with patch("rmlw.readiness.requests") as mock_requests:
        mock_ok = MagicMock()
        mock_ok.status_code = 200
        mock_requests.get.side_effect = [
            requests.RequestException("connection refused"),
            mock_ok,
        ]

        wait_for_http_ready("http://test:80", max_wait=10, interval=0.01)

        assert mock_requests.get.call_count == 2
