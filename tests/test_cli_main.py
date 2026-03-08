"""Tests for CLI."""

import json
import os
import tempfile
from unittest.mock import patch

import pytest

from rmlw.cli.main import _serialise_finding, main
from rmlw.workbench import Finding


def test_serialise_finding() -> None:
    """_serialise_finding produces valid dict."""
    f = Finding("xss", "http://t/", "q", "p", {"a": 1})
    d = _serialise_finding(f)
    assert d["ftype"] == "xss"
    json.dumps(d)


def test_cli_scan_baseline_requires_target() -> None:
    """Scan without --target exits with error."""
    with patch("sys.argv", ["rmlw", "scan"]), pytest.raises(SystemExit):
        main()


def test_cli_scan_rejects_invalid_url() -> None:
    """Scan with invalid URL exits with error."""
    with (
        patch("sys.argv", ["rmlw", "scan", "--target", "file:///etc/passwd"]),
        pytest.raises(SystemExit),
    ):
        main()


def test_cli_scan_baseline_output(capsys: pytest.CaptureFixture[str]) -> None:
    """Scan baseline with --format json produces JSON output."""
    with patch(
        "sys.argv",
        [
            "rmlw",
            "scan",
            "--target",
            "http://example.com",
            "--format",
            "json",
            "--no-wait",
        ],
    ):
        main()
    out, _ = capsys.readouterr()
    data = json.loads(out)
    assert isinstance(data, list)


def test_cli_scan_baseline_output_file() -> None:
    """Scan with --output writes to file."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        path = f.name
    try:
        with patch(
            "sys.argv",
            [
                "rmlw",
                "scan",
                "--target",
                "http://example.com",
                "--output",
                path,
                "--no-wait",
            ],
        ):
            main()
        with open(path) as f:
            data = json.load(f)
        assert isinstance(data, list)
    finally:
        os.unlink(path)


def test_cli_scan_human_format(capsys: pytest.CaptureFixture[str]) -> None:
    """Scan with --format human produces human-readable output."""
    with patch(
        "sys.argv",
        [
            "rmlw",
            "scan",
            "--target",
            "http://example.com",
            "--format",
            "human",
            "--no-wait",
        ],
    ):
        main()
    out, _ = capsys.readouterr()
    assert "param=" in out or "No findings" in out
    assert "[" in out or "No findings" in out


def test_cli_scan_human_format_exact_pattern(capsys: pytest.CaptureFixture[str]) -> None:
    """Human format lines match [ftype] url param=X payload='Y' pattern."""
    with patch(
        "sys.argv",
        [
            "rmlw",
            "scan",
            "--target",
            "http://example.com",
            "--format",
            "human",
            "--no-wait",
        ],
    ):
        main()
    out, _ = capsys.readouterr()
    for line in out.strip().splitlines():
        if line and line != "No findings.":
            assert line.startswith("["), "human line should start with [ftype]"
            assert " param=" in line, "human line should contain param="
            assert " payload=" in line, "human line should contain payload="


def test_cli_scan_learn_mode(capsys: pytest.CaptureFixture[str]) -> None:
    """Scan learn mode runs without error."""
    with patch(
        "sys.argv",
        [
            "rmlw",
            "scan",
            "--target",
            "http://example.com",
            "--mode",
            "learn",
            "--iterations",
            "2",
            "--format",
            "json",
            "--no-wait",
        ],
    ):
        main()
    out, err = capsys.readouterr()
    data = json.loads(out)
    assert isinstance(data, list)
