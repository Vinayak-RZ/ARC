import json
import shutil
from pathlib import Path

import pytest

from electrical_engineer.circuit.graph import series_rlc_graph
from electrical_engineer.circuit.run_session import apply_graph, load_graph
from electrical_engineer.collab import lab_meta
from electrical_engineer.collab.lab_verify import agent_rederive_circuit_lab
from electrical_engineer.collab.workflow import finish_circuit_lab


@pytest.mark.skipif(not shutil.which("ngspice"), reason="ngspice required")
def test_rederive_after_human_edit_marks_rows_current(tmp_path: Path) -> None:
    run = tmp_path / "run"
    run.mkdir()
    problem = {"kind": "series_rlc", "vin": 10, "v_step": 10, "r_ohm": 10, "l_h": 0.01, "c_f": 1e-4, "tol": 0.02}
    (run / "problem.json").write_text(json.dumps(problem), encoding="utf-8")
    lab_meta.ensure_lab_meta(run, kind="circuit")
    apply_graph(run, series_rlc_graph(vin=10, r_ohm=10, l_h=0.01, c_f=1e-4), author="agent", op="open")
    finish_circuit_lab(run, problem)

    g = load_graph(run)
    for n in g["nodes"]:
        if n["id"] == "r1":
            n["value"] = 20
    apply_graph(run, g, author="human", op="ui_save")

    verify = agent_rederive_circuit_lab(run)
    statuses = [m.get("status") for m in verify.get("metrics") or []]
    assert statuses and all(s == "agrees" for s in statuses), statuses
    ops = [e.get("op") for e in lab_meta.load_lab_meta(run).get("op_log") or []]
    assert ops[-1] == "re_derive"
