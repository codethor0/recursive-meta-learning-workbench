"""Tests for Finding data structure and shape."""

import json

from rmlw.workbench import Finding


def test_finding_has_required_fields() -> None:
    """Finding dataclass has ftype, url, param, payload, detail."""
    f = Finding(
        ftype="xss_reflection",
        url="http://test/",
        param="q",
        payload="<script>",
        detail={"status_code": 200, "length": 100},
    )
    assert f.ftype == "xss_reflection"
    assert f.url == "http://test/"
    assert f.param == "q"
    assert f.payload == "<script>"
    assert f.detail["status_code"] == 200
    assert f.detail["length"] == 100


def test_finding_to_dict_json_serialisable() -> None:
    """Finding.to_dict produces valid JSON."""
    f = Finding("sqli_boolean", "http://x/", "id", "1' OR '1'='1", {"code": 200})
    d = f.to_dict()
    json_str = json.dumps(d)
    loaded = json.loads(json_str)
    assert loaded["ftype"] == "sqli_boolean"
    assert loaded["param"] == "id"


def test_finding_detail_can_hold_evidence() -> None:
    """Finding.detail holds status codes, lengths, timing."""
    f = Finding(
        "cmd_time",
        "http://x/",
        "ip",
        "test; sleep 5",
        {"elapsed": 5.2},
    )
    assert "elapsed" in f.detail
    assert f.detail["elapsed"] == 5.2
