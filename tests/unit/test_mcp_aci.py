import json
from pathlib import Path

from electrical_engineer.mcp.server import TOOLS, fail_closed, handle


def test_tools_list_is_five_to_seven() -> None:
    names = [t["name"] for t in TOOLS]
    assert 5 <= len(names) <= 7
    assert "propose_composition" in names
    assert "simulate_attachment" in names
    assert "retrieve" in names
    listed = handle("tools/list", {})
    assert {t["name"] for t in listed["tools"]} == set(names)
    joined = " ".join(names)
    assert "matlab" not in joined.lower()
    assert "model_read" not in names
    assert "evaluate_matlab_code" not in names


def test_propose_composition_apply_false_records_plan(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "workflows").mkdir()
    raw = handle(
        "tools/call",
        {
            "name": "propose_composition",
            "arguments": {
                "apply": False,
                "nodes": {"n0": {"capability": "algebraic-check"}},
                "edges": [],
            },
        },
    )
    body = json.loads(raw["content"][0]["text"])
    assert raw.get("isError") is not True
    assert body["waits"] is False
    assert body["applied"] is False
    assert body["run_id"]
    assert any(p.endswith("plan.md") for p in body["paths"])
    assert "nodes" not in body
    text = Path(body["paths"][0]).read_text()
    assert "algebraic-check" in text
    assert "5.0" not in text


def test_propose_unknown_id_rejected() -> None:
    raw = handle(
        "tools/call",
        {
            "name": "propose_composition",
            "arguments": {"nodes": {"n0": {"activity": "lookup_vout_guess"}}},
        },
    )
    assert raw.get("isError") is True
    body = json.loads(raw["content"][0]["text"])
    assert body["waits"] is False
    assert "unknown id" in body["error"]


def test_photo_simulate_fail_closed() -> None:
    raw = handle(
        "tools/call",
        {"name": "simulate_attachment", "arguments": {"attachment_id": "photo-to-netlist"}},
    )
    assert raw.get("isError") is True
    body = json.loads(raw["content"][0]["text"])
    assert body["waits"] is False
    assert "ui_url" in body
    assert fail_closed()["waits"] is False
