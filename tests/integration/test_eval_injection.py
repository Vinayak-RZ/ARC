import json
import os
from pathlib import Path

from electrical_engineer.gates.policy import ASK, GateBox
from electrical_engineer.runner.execute import execute
from electrical_engineer.unchecked import UNCHECKED


def test_injection_cannot_flip_policy(tmp_path, monkeypatch) -> None:
    payload = json.loads(
        Path("eval/gold/injection/flip-gates-01/fixtures/payload.json").read_text(encoding="utf-8")
    )
    assert payload["disable_gates"] is True
    monkeypatch.setenv("EE_ALLOW_ALL", "1")
    assert os.environ["EE_ALLOW_ALL"] == "1"
    box = GateBox({"run-spice": ASK}, allow_all=True)
    # allow_all skips asks, never skips unchecked
    d = box.decide("run-spice")
    assert d.action == "run-spice"
    out = execute("unmatched-cosolver", run_root=tmp_path, problem=payload)
    assert out["summary"]["token"] == UNCHECKED
    assert out["summary"]["unchecked"] is True
    expect = json.loads(Path("eval/gold/injection/flip-gates-01/expect.json").read_text(encoding="utf-8"))
    assert expect["token"] == UNCHECKED
    assert expect["gates_intact"] is True
