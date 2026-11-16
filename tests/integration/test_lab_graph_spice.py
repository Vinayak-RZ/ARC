"""Lab graph netlist is what ngspice simulates."""

from __future__ import annotations

import copy
import json

import pytest

from electrical_engineer.circuit.graph import (
    default_graph_for,
    graph_port_errors,
    parse_graph,
    series_rlc_graph,
    series_rlc_netlist_signature,
)
from electrical_engineer.circuit.netlist import compile_netlist
from electrical_engineer.circuit.simulate_graph import simulate_graph
from electrical_engineer.collab.workflow import finish_circuit_lab
from electrical_engineer.engines.rlc_transient import series_rlc_step
from electrical_engineer.runner.runs import new_run_id


@pytest.fixture
def run_root(tmp_path):
    rd = tmp_path / "runs" / new_run_id()
    rd.mkdir(parents=True)
    return rd


def test_agent_series_rlc_graph_is_intended_topology() -> None:
    graph = series_rlc_graph(vin=10, r_ohm=10, l_h=0.01, c_f=100e-6)
    parsed = parse_graph(graph)
    assert graph_port_errors(parsed) == []
    cir = compile_netlist(parsed)
    sig = series_rlc_netlist_signature(cir)
    assert "V1:" in "".join(sig)
    assert "R1:" in "".join(sig)
    assert "L1:" in "".join(sig)
    assert "C1:" in "".join(sig)


def test_graph_json_matches_saved_netlist(run_root) -> None:
    meta = series_rlc_step(10, 0.01, 100e-6, 10.0)
    gold = float(meta["Vc_peak_V"])
    problem = {
        "kind": "series_rlc",
        "vin": 10,
        "r_ohm": 10,
        "l_h": 0.01,
        "c_f": 100e-6,
        "analysis": "tran",
        "t_s": float(meta["t_Vc_peak_s"]),
        "tol": 0.02,
        "value": gold,
    }
    derived = {
        "value": gold,
        "analysis": "tran",
        "t_s": problem["t_s"],
        "derive_metric": "Vc_peak",
    }
    finish_circuit_lab(run_root, problem, derived=derived)
    graph = json.loads((run_root / "graph.json").read_text(encoding="utf-8"))
    on_disk = (run_root / "netlist.cir").read_text(encoding="utf-8")
    live = compile_netlist(parse_graph(graph))
    assert series_rlc_netlist_signature(on_disk) == series_rlc_netlist_signature(live)


@pytest.mark.skipif(
    not __import__("shutil").which("ngspice"),
    reason="ngspice required",
)
def test_changing_r1_in_graph_changes_spice_peak(run_root) -> None:
    meta = series_rlc_step(10, 0.01, 100e-6, 10.0)
    problem = {
        "kind": "series_rlc",
        "vin": 10,
        "r_ohm": 10,
        "l_h": 0.01,
        "c_f": 100e-6,
        "analysis": "tran",
        "t_s": float(meta["t_Vc_peak_s"]),
        "derive_metric": "Vc_peak",
        "tol": 0.02,
    }
    graph = default_graph_for(problem)
    assert graph is not None
    (run_root / "a").mkdir(parents=True, exist_ok=True)
    (run_root / "b").mkdir(parents=True, exist_ok=True)
    base = simulate_graph(graph, problem, run_dir=run_root / "a")
    assert base.get("simulated") is not None
    bumped = copy.deepcopy(graph)
    for node in bumped["nodes"]:
        if node.get("id") == "r1":
            node["value"] = 15
    other = simulate_graph(bumped, {**problem, "r_ohm": 15}, run_dir=run_root / "b")
    assert other.get("simulated") is not None
    assert abs(float(other["simulated"]) - float(base["simulated"])) > 0.05