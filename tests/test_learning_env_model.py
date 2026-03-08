"""Tests for EnvironmentModel."""

from rmlw.learning.env_model import EnvironmentModel
from rmlw.workbench import Finding


def test_env_model_initial_state() -> None:
    """EnvironmentModel starts with default values."""
    env = EnvironmentModel()
    assert env.waf_detected is False
    assert env.framework is None
    assert env.input_filtering == {}
    assert env.successful_payloads == {}
    assert env.failed_payloads == {}


def test_env_model_update_from_finding() -> None:
    """update_from_finding adds payload to successful_payloads."""
    env = EnvironmentModel()
    f = Finding("xss_reflection", "http://t/", "q", "<script>", {})
    env.update_from_finding(f)
    assert "xss_reflection" in env.successful_payloads
    assert "<script>" in env.successful_payloads["xss_reflection"]


def test_env_model_state_tuple() -> None:
    """state_tuple returns hashable tuple."""
    env = EnvironmentModel()
    t = env.state_tuple()
    assert isinstance(t, tuple)
    assert len(t) == 3
    assert t[0] is False
    assert t[1] is False
    assert t[2] == 0


def test_env_model_update_from_result_success() -> None:
    """update_from_result records success when payload in response."""
    env = EnvironmentModel()
    env.update_from_result(
        "xss_reflection",
        "q",
        "<script>",
        status_code=200,
        headers={},
        payload_in_response=True,
    )
    assert "xss_reflection" in env.successful_payloads
    assert "<script>" in env.successful_payloads["xss_reflection"]


def test_env_model_update_from_result_waf_detection() -> None:
    """update_from_result sets waf_detected when ModSecurity in headers."""
    env = EnvironmentModel()
    env.update_from_result(
        "xss",
        "q",
        "p",
        status_code=403,
        headers={"X-ModSecurity": "1"},
        payload_in_response=False,
    )
    assert env.waf_detected is True
    assert env.input_filtering["q"] == "blocked"


def test_env_model_copy() -> None:
    """copy() produces independent copy."""
    env = EnvironmentModel()
    env.waf_detected = True
    env.successful_payloads["xss"] = ["p1"]
    copy = env.copy()
    assert copy.waf_detected is True
    assert copy.successful_payloads["xss"] == ["p1"]
    copy.successful_payloads["xss"].append("p2")
    assert len(env.successful_payloads["xss"]) == 1
