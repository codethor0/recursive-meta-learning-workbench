"""Tests for PersistentArchive."""

from rmlw.learning.archive import PersistentArchive


def test_archive_add_success() -> None:
    """add_success appends entry."""
    arch = PersistentArchive()
    arch.add_success("xss", "<script>", {"code": 200})
    assert len(arch.items) == 1
    assert arch.items[0]["vuln_type"] == "xss"
    assert arch.items[0]["payload"] == "<script>"
    assert "timestamp" in arch.items[0]


def test_archive_recent() -> None:
    """recent returns last n entries."""
    arch = PersistentArchive()
    for i in range(5):
        arch.add_success("xss", f"p{i}", {})
    recent = arch.recent(2)
    assert len(recent) == 2
    assert recent[0]["payload"] == "p3"
    assert recent[1]["payload"] == "p4"


def test_archive_recent_more_than_exists() -> None:
    """recent(n) with n > len returns all."""
    arch = PersistentArchive()
    arch.add_success("xss", "p", {})
    assert len(arch.recent(10)) == 1
