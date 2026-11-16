"""Lab verify flags, layout-only revision, RLC params from graph."""

from __future__ import annotations

import copy
import json

import pytest

from electrical_engineer.circuit.graph import (
    format_series_rlc_param_strip,
    series_rlc_params_from_graph,
)
from electrical_engineer.circuit.run_session import apply_graph, load_graph
from electrical_engineer.collab.lab_meta import ensure_lab_meta, load_lab_meta
from electrical_engineer.collab.lab_verify import derivation_matches_graph
from electrical_engineer.collab.workflow import default_graph_for, finish_circuit_lab
from electrical_engineer.engines.circuit_derive import derive
from electrical_engineer.engines.rlc_transient import series_rlc_step


def test_param_strip_from_graph() -> None:
    problem = {"kind": "series_rlc", "vin": 10, "r_ohm": 10, "l_h": 0.01, "c_f": 100e-6}
    graph = default_graph_for(problem)
    assert graph is not None
    assert format_series_rlc_param_strip(graph) == "V 10 V · R 10 Ω · L 10.0 mH · C 100 µF"


def test_settling_2pct_r20_ms() -> None:
    meta = series_rlc_step(20, 0.01, 100e-6, 10.0)
    t_ms = float(meta["settling_2pct_entry_s"] or 0) * 1000
    assert t_ms == pytest.approx(5.83, abs=0.05)


def test_series_rlc_params_from_graph() -> None:
    problem = {"kind": "series_rlc", "vin": 10, "r_ohm": 10, "l_h": 0.01, "c_f": 100e-6}
    graph = default_graph_for(problem)
    assert graph is not None
    params = series_rlc_params_from_graph(graph)
    assert params is not None
    assert params["r_ohm"] == 10
    assert params["l_h"] == 0.01
    assert params["c_f"] == 100e-6
    assert params["v_step"] == 10


def test_layout_only_save_does_not_bump_revision(tmp_path) -> None:
    problem = {"kind": "series_rlc", "vin": 10, "r_ohm": 10, "l_h": 0.01, "c_f": 100e-6}
    run_dir = tmp_path / "run-layout"
    run_dir.mkdir()
    ensure_lab_meta(run_dir, kind="circuit")
    graph = default_graph_for(problem)
    assert graph is not None
    apply_graph(run_dir, graph, author="agent", op="seed_from_problem")
    rev0 = int(load_lab_meta(run_dir)["revision"])
    moved = copy.deepcopy(graph)
    moved["nodes"][0]["x"] = float(moved["nodes"][0].get("x") or 0) + 32
    apply_graph(run_dir, moved, author="human", op="ui_save")
    rev1 = int(load_lab_meta(run_dir)["revision"])
    assert rev1 == rev0
    last = (load_lab_meta(run_dir).get("op_log") or [])[-1]
    assert last.get("op") == "layout_save"
    assert last.get("electrical") is False


def test_derive_bug_forward_euler_mismatches_spice_gold() -> None:
    meta = series_rlc_step(10, 0.01, 100e-6, 10.0)
    gold = float(meta["Vc_peak_V"])
    assert abs(gold - 11.630) < 0.02
    assert abs(float(meta["t_Vc_peak_s"]) - 0.003628) < 1e-5
    derived = derive(
        {
            "kind": "series_rlc",
            "vin": 10,
            "r_ohm": 10,
            "l_h": 0.01,
            "c_f": 100e-6,
            "derive_bug": "forward_euler",
            "allow_template_fallback": True,
        }
    )
    assert derived.get("engine") == "forward_euler_bug"
    assert abs(float(derived["value"]) - 11.963) < 0.05
    assert abs(float(derived["value"]) - gold) / gold > 0.02

    with_cir = derive(
        {
            **derived,
            "cir": "* netlist present\nV1 1 0 DC 10\n.end\n",
            "derive_bug": "forward_euler",
            "vin": 10,
            "r_ohm": 10,
            "l_h": 0.01,
            "c_f": 100e-6,
            "kind": "series_rlc",
        }
    )
    assert with_cir.get("engine") == "forward_euler_bug"
    assert with_cir.get("derived_via") == "derive_bug"


def test_human_resistor_edit_flags_derivation_mismatch(tmp_path) -> None:
    problem = {"kind": "series_rlc", "vin": 10, "r_ohm": 10, "l_h": 0.01, "c_f": 100e-6, "tol": 0.15}
    run_dir = tmp_path / "run-edit"
    run_dir.mkdir(parents=True)
    (run_dir / "problem.json").write_text(json.dumps(problem), encoding="utf-8")
    finish_circuit_lab(run_dir, problem)
    graph = load_graph(run_dir)
    edited = copy.deepcopy(graph)
    for node in edited["nodes"]:
        if node.get("id") == "r1":
            node["value"] = 20
    apply_graph(run_dir, edited, author="human", op="set", target="r1")
    meta = load_lab_meta(run_dir)
    assert not derivation_matches_graph(meta, load_graph(run_dir))
    from electrical_engineer.collab.lab_verify import reverify_circuit_lab

    verify = reverify_circuit_lab(run_dir)
    assert verify.get("verdict_current") is True
    assert verify.get("derivation_matches_graph") is False