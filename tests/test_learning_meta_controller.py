"""Tests for MetaController."""

from unittest.mock import MagicMock

from rmlw.learning.meta_controller import MECHANISMS, MetaController
from rmlw.workbench import Finding, WebAttackWorkbench


def test_meta_controller_reward_is_finding_count() -> None:
    """Reward equals number of findings returned by workbench."""
    mock_wb = MagicMock(spec=WebAttackWorkbench)
    mock_findings = [
        Finding("xss", "http://test/", "q", "p1", {}),
        Finding("ssrf_candidate", "http://test/", "q", "p2", {}),
    ]
    mock_wb.run.return_value = mock_findings
    mock_wb.base_url = "http://test"
    mock_wb.endpoints = {"http://test/"}
    mock_wb._base_netloc = "test"
    controller = MetaController(mock_wb)
    controller.workbench = mock_wb
    initial_reward = controller._ucb_rewards.copy()
    findings = controller.run_iteration()
    assert len(findings) == 2
    for m in MECHANISMS:
        if controller._ucb_counts[m] == 1:
            assert controller._ucb_rewards[m] == initial_reward[m] + 2.0
            break


def test_meta_controller_selects_valid_mechanism() -> None:
    """_select_mechanism returns one of the defined mechanisms."""
    mock_wb = MagicMock(spec=WebAttackWorkbench)
    mock_wb.run.return_value = []
    mock_wb.base_url = "http://test"
    mock_wb.endpoints = set()
    mock_wb._base_netloc = "test"
    controller = MetaController(mock_wb)
    for _ in range(20):
        m = controller._select_mechanism()
        assert m in MECHANISMS


def test_meta_controller_run_iteration_calls_workbench() -> None:
    """run_iteration calls workbench.run()."""
    mock_wb = MagicMock(spec=WebAttackWorkbench)
    mock_wb.run.return_value = []
    mock_wb.base_url = "http://test"
    mock_wb.endpoints = {"http://test/"}
    mock_wb._base_netloc = "test"
    controller = MetaController(mock_wb)
    controller.workbench = mock_wb
    findings = controller.run_iteration()
    mock_wb.run.assert_called()
    assert isinstance(findings, list)


def test_meta_controller_ucb_prefers_high_reward() -> None:
    """After high reward, mechanism is more likely to be selected again."""
    mock_wb = MagicMock(spec=WebAttackWorkbench)
    mock_wb.run.return_value = []
    mock_wb.base_url = "http://test"
    mock_wb.endpoints = {"http://test/"}
    mock_wb._base_netloc = "test"
    controller = MetaController(mock_wb)
    controller.workbench = mock_wb
    controller._ucb_counts["baseline"] = 5
    controller._ucb_rewards["baseline"] = 10.0
    controller._ucb_total_selections = 10
    m = controller._select_mechanism()
    assert m in MECHANISMS


def test_meta_controller_run_iterations_updates_mechanism_counts() -> None:
    """run_iterations updates _ucb_counts per mechanism."""
    mock_wb = MagicMock(spec=WebAttackWorkbench)
    mock_wb.run.return_value = []
    mock_wb.base_url = "http://test"
    mock_wb.endpoints = {"http://test/"}
    mock_wb._base_netloc = "test"
    controller = MetaController(mock_wb)
    controller.workbench = mock_wb
    controller.run_iterations(3)
    total = sum(controller._ucb_counts[m] for m in MECHANISMS)
    assert total == 3
