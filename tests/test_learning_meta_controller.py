"""Tests for MetaController."""

from unittest.mock import MagicMock

from rmlw.learning.meta_controller import MECHANISMS, MetaController
from rmlw.workbench import WebAttackWorkbench


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
