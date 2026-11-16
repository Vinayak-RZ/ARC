"""Agent path: build lab artifact, simulate, match hand-derived golds."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

from electrical_engineer.circuit import mcp_lab
from electrical_engineer.circuit.mcp_tools import handle_tool as circuit_mcp
from electrical_engineer.collab.workflow import finish_circuit_lab, finish_control_lab
from electrical_engineer.control_studio import simulate as cs_simulate
from electrical_engineer.control_studio.goldens import GOLDENS
from electrical_engineer.engines.rlc_transient import series_rlc_step
from electrical_engineer.runner.execute import execute
from electrical_engineer.runner.runs import new_run_id


@pytest.fixture
def run_root(tmp_path: Path) -> Path:
    rd = tmp_path / "runs" / new_run_id()
    rd.mkdir(parents=True)
    return rd


def test_voltage_divider_lab(run_root: Path, monkeypatch) -> None:
    monkeypatch.chdir(run_root.parent.parent)
    problem = {"kind": "voltage_divider", "vin": 10, "r1": 1000, "r2": 1000, "expected": 5.0, "tol": 1e-3}
    gold = 10 * 1000 / (1000 + 1000)
    verify = finish_circuit_lab(run_root, problem)
    assert abs(float(verify["derived"]) - gold) < 1e-9
    if verify.get("simulated") is not None:
        assert verify.get("mismatch") is False


def test_series_rlc_transient_lab(run_root: Path, monkeypatch) -> None:
    monkeypatch.chdir(run_root.parent.parent)
    r, l, c, vin = 50.0, 1e-3, 1e-6, 10.0
    meta = series_rlc_step(r, l, c, vin)
    gold = float(meta["Vc_peak_V"])
    t_stop = max(float(meta["t_Vc_peak_s"]) * 2, 1e-4)
    cir = (
        f"* rlc\nV1 1 0 DC {vin}\nR1 1 2 {r}\nL1 2 3 {l}\nC1 3 0 {c}\n"
        f".ic v(3)=0\n.tran 1u {t_stop:g} uic\n.end\n"
    )
    problem = {
        "kind": "series_rlc",
        "r": r,
        "l": l,
        "c": c,
        "vin": vin,
        "cir": cir,
        "analysis": "tran",
        "t_s": float(meta["t_Vc_peak_s"]),
        "probe": "v(3)",
        "tol": 0.05,
        "value": gold,
    }
    derived = {
        "value": gold,
        "cir": cir,
        "probe": "v(3)",
        "analysis": "tran",
        "t_s": problem["t_s"],
        "derive_metric": "Vc_peak",
    }
    verify = finish_circuit_lab(run_root, problem, derived=derived)
    assert abs(float(verify["derived"]) - gold) < 1e-6
    if verify.get("simulated") is not None:
        assert verify.get("mismatch") is False


def test_series_rlc_headline_verify_catches_bad_derive(run_root: Path, monkeypatch) -> None:
    monkeypatch.chdir(run_root.parent.parent)
    r, l, c, vin = 10.0, 0.01, 100e-6, 10.0
    meta = series_rlc_step(r, l, c, vin)
    gold = float(meta["Vc_peak_V"])
    assert abs(gold - 11.630) < 0.01
    euler_wrong = 11.963
    cir = (
        "* rlc headline\n"
        f"V1 1 0 DC {vin}\nR1 1 2 {r}\nL1 2 3 {l}\nC1 3 0 {c}\n"
        f".tran 1u {float(meta['t_Vc_peak_s']) * 2}\n.end\n"
    )
    problem = {
        "kind": "series_rlc",
        "r_ohm": r,
        "l_h": l,
        "c_f": c,
        "vin": vin,
        "cir": cir,
        "analysis": "tran",
        "t_s": float(meta["t_Vc_peak_s"]),
        "probe": "v(3)",
        "tol": 0.02,
        "value": euler_wrong,
    }
    derived = {
        "value": euler_wrong,
        "unit": "V",
        "cir": cir,
        "probe": "v(3)",
        "analysis": "tran",
        "t_s": problem["t_s"],
        "derive_metric": "Vc_peak",
        "engine": "forward_euler_bug",
    }
    verify = finish_circuit_lab(run_root, problem, derived=derived)
    assert abs(float(verify["derived"]) - euler_wrong) < 1e-6
    if verify.get("simulated") is not None and not verify.get("sim_skipped"):
        assert verify.get("needs_review") is True or verify.get("mismatch") is True
        sim = float(verify["simulated"])
        if abs(sim - gold) / gold < 0.02:
            assert verify.get("rel_err_pct", 0) > 2.0


def test_series_rlc_headline_lab_closed_form(run_root: Path, monkeypatch) -> None:
    monkeypatch.chdir(run_root.parent.parent)
    problem = {
        "kind": "series_rlc",
        "vin": 10,
        "r_ohm": 10,
        "l_h": 0.01,
        "c_f": 100e-6,
        "tol": 0.05,
    }
    verify = finish_circuit_lab(run_root, problem)
    assert abs(float(verify["derived"]) - 11.630) < 0.01
    if verify.get("simulated") is not None and not verify.get("sim_skipped"):
        sim = float(verify["simulated"])
        rel = abs(sim - float(verify["derived"])) / float(verify["derived"])
        if rel <= 0.05:
            assert verify.get("needs_review") is not True
        else:
            assert verify.get("needs_review") is True


def test_rc_lowpass_bode_lab(run_root: Path, monkeypatch) -> None:
    monkeypatch.chdir(run_root.parent.parent)
    vin, r_ohm, c_f = 5.0, 1000.0, 1e-6
    f_hz = 1.0 / (2.0 * math.pi * r_ohm * c_f)
    gold = vin / math.sqrt(1.0 + (2.0 * math.pi * f_hz * r_ohm * c_f) ** 2)
    cir = (
        f"* rc lowpass\nV1 1 0 AC {vin}\nR1 1 2 {r_ohm}\nC1 2 0 {c_f}\n"
        f".ac lin 1 {f_hz} {f_hz}\n.end\n"
    )
    problem = {
        "kind": "rc_lowpass",
        "vin": vin,
        "r_ohm": r_ohm,
        "c_f": c_f,
        "cir": cir,
        "analysis": "ac",
        "f_hz": f_hz,
        "probe": "mag(v(2))",
        "tol": 0.05,
        "value": gold,
    }
    derived = {
        "value": gold,
        "cir": cir,
        "probe": "mag(v(2))",
        "analysis": "ac",
        "f_hz": f_hz,
    }
    verify = finish_circuit_lab(run_root, problem, derived=derived)
    if verify.get("simulated") is not None and not verify.get("mismatch"):
        assert verify.get("mismatch") is False
    assert verify.get("derived") is not None


def test_unity_feedback_control_lab(run_root: Path, monkeypatch) -> None:
    monkeypatch.chdir(run_root.parent.parent)
    diagram = GOLDENS["unity_first_order"]()
    sim = cs_simulate.simulate(diagram, run_dir=run_root)
    assert sim.get("ok")
    assert sim.get("y_ss") is not None
    y_ss = float(sim["y_ss"])
    verify = finish_control_lab(run_root, {"kind": "unity_feedback", "golden": "unity_first_order"}, derived_value=y_ss)
    assert verify.get("mismatch") is False


def test_lead_compensator_control_lab(run_root: Path, monkeypatch) -> None:
    monkeypatch.chdir(run_root.parent.parent)
    verify = finish_control_lab(run_root, {"kind": "lead", "golden": "lead_compensator"})
    assert verify.get("simulate", {}).get("ok")


def test_series_rlc_transient_workflow_seeds_lab(tmp_path: Path) -> None:
    problem = {
        "kind": "series_rlc",
        "vin": 10,
        "r_ohm": 10,
        "l_h": 0.01,
        "c_f": 100e-6,
        "analysis": "tran",
        "t_s": 0.0005,
        "probe": "v(3)",
        "tol": 0.15,
    }
    out = execute("series-rlc-transient", run_root=tmp_path, problem=problem)
    run_dir = Path(out["run_dir"])
    assert (run_dir / "graph.json").is_file()
    assert (run_dir / "lab_meta.json").is_file()
    assert (run_dir / "lab_verify.json").is_file()


def test_solve_control_workflow_seeds_lab(tmp_path: Path) -> None:
    out = execute(
        "solve-control-problem",
        run_root=tmp_path,
        problem={"golden": "unity_first_order", "num": [10], "den": [1, 1]},
    )
    run_dir = Path(out["run_dir"])
    assert (run_dir / "lab_meta.json").is_file()
    meta = json.loads((run_dir / "lab_meta.json").read_text(encoding="utf-8"))
    assert meta.get("control_session_id")
    verify = json.loads((run_dir / "lab_verify.json").read_text(encoding="utf-8"))
    assert verify.get("metrics")
    y_row = next(m for m in verify["metrics"] if m["id"] == "y_ss")
    assert y_row["derived"] == pytest.approx(10 / 11, rel=0.02)
    assert y_row["simulated"] == pytest.approx(10 / 11, rel=0.02)
    assert verify.get("mismatch") is False


def test_derive_circuit_workflow_seeds_lab(tmp_path: Path) -> None:
    out = execute(
        "derive-circuit",
        run_root=tmp_path,
        problem={"kind": "voltage_divider", "vin": 10, "r1": 1000, "r2": 1000, "expected": 5.0},
    )
    run_dir = Path(out["run_dir"])
    assert (run_dir / "graph.json").is_file()
    assert (run_dir / "lab_meta.json").is_file()


def test_mcp_lab_surface() -> None:
    from electrical_engineer.collab.mcp_tools import TOOL_DEFS as COLLAB_TOOL_DEFS

    names = {t["name"] for t in mcp_lab.TOOL_DEFS}
    assert "arc_circuit_lab_finish_solve" in names
    assert any(t["name"] == "arc_lab_finish_control" for t in COLLAB_TOOL_DEFS)


def test_agent_mcp_build_divider(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "runs").mkdir(exist_ok=True)
    out = circuit_mcp(
        "arc_circuit_lab_finish_solve",
        {
            "problem": {"kind": "voltage_divider", "vin": 12, "r1": 3000, "r2": 1000, "tol": 1e-3},
        },
    )
    assert out.get("run_id")
    get = circuit_mcp("arc_circuit_lab_get", {"run_id": out["run_id"]})
    assert get["graph"]["nodes"]