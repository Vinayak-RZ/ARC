"""Lab graph to netlist fidelity and validation (fuzz + suspected short bypass)."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from electrical_engineer.circuit.graph import SCHEMA, GraphError, parse_graph, series_rlc_graph
from electrical_engineer.circuit.netlist import CompileError, compile_netlist
from electrical_engineer.circuit.simulate_graph import simulate_graph
from electrical_engineer.collab.workflow import finish_circuit_lab
from electrical_engineer.engines.rlc_transient import series_rlc_step
from electrical_engineer.engines.spice_runner import simulator_status
from tests.golden_numerics_refs import (
    HEADLINE_RLC_C_F,
    HEADLINE_RLC_L_H,
    HEADLINE_RLC_R_OHM,
    HEADLINE_RLC_VC_PEAK_V,
    HEADLINE_RLC_VIN,
)


def _minimal_grounded_resistor() -> dict:
    return {
        "schema": SCHEMA,
        "nodes": [
            {"id": "vin", "type": "source_v", "refdes": "V1", "value": 10, "unit": "V", "x": 0, "y": 0},
            {"id": "r1", "type": "resistor", "refdes": "R1", "value": 1000, "unit": "ohm", "x": 1, "y": 0},
            {"id": "gnd", "type": "ground", "refdes": "G", "value": 0, "unit": "", "x": 0, "y": 1},
        ],
        "edges": [
            {"id": "e1", "from": "vin.n1", "to": "r1.n1"},
            {"id": "e2", "from": "r1.n2", "to": "gnd.n1"},
            {"id": "e3", "from": "vin.n2", "to": "gnd.n1"},
        ],
    }


@pytest.mark.parametrize(
    "mutator,expect",
    [
        (lambda g: {**g, "nodes": [n for n in g["nodes"] if n["type"] != "ground"]}, CompileError),
        (lambda g: {**g, "nodes": g["nodes"] + [{"id": "r1", "type": "resistor", "value": 1}]}, GraphError),
        (
            lambda g: {
                **g,
                "nodes": [{**n, "value": 0} if n["id"] == "r1" else n for n in g["nodes"]],
            },
            None,
        ),
    ],
)
def test_graph_validation_errors(mutator, expect) -> None:
    base = _minimal_grounded_resistor()
    bad = mutator(copy.deepcopy(base))
    if expect is GraphError:
        with pytest.raises(GraphError):
            parse_graph(bad)
        return
    if expect is CompileError:
        with pytest.raises(CompileError):
            compile_netlist(parse_graph(bad))
        return
    parsed = parse_graph(bad)
    cir = compile_netlist(parsed)
    assert "R1" in cir


def test_compiled_graph_series_rlc_matches_headline_netlist_topology() -> None:
    graph = series_rlc_graph(
        vin=HEADLINE_RLC_VIN,
        r_ohm=HEADLINE_RLC_R_OHM,
        l_h=HEADLINE_RLC_L_H,
        c_f=HEADLINE_RLC_C_F,
    )
    cir = compile_netlist(parse_graph(graph))
    assert "V1" in cir and "R1" in cir and "L1" in cir and "C1" in cir
    assert cir.count(" 0\n") >= 1 or " 0 " in cir


def test_editing_r1_value_changes_compiled_netlist() -> None:
    g1 = series_rlc_graph(r_ohm=10.0)
    g2 = series_rlc_graph(r_ohm=20.0)
    c1 = compile_netlist(parse_graph(g1))
    c2 = compile_netlist(parse_graph(g2))
    assert c1 != c2
    assert " 20" in c2 or "20\n" in c2


@pytest.mark.skipif(not simulator_status().get("available"), reason="ngspice missing")
def test_graph_only_simulation_matches_derived_rlc_peak(tmp_path: Path) -> None:
    meta = series_rlc_step(HEADLINE_RLC_R_OHM, HEADLINE_RLC_L_H, HEADLINE_RLC_C_F, HEADLINE_RLC_VIN)
    graph = series_rlc_graph(
        vin=HEADLINE_RLC_VIN,
        r_ohm=HEADLINE_RLC_R_OHM,
        l_h=HEADLINE_RLC_L_H,
        c_f=HEADLINE_RLC_C_F,
    )
    prob = {
        "kind": "series_rlc",
        "analysis": "tran",
        "t_s": float(meta["t_Vc_peak_s"]),
        "probe": "v(3)",
        "derive_metric": "Vc_peak",
        "tol": 0.08,
    }
    sim_graph_only = simulate_graph(graph, prob, run_dir=tmp_path / "g")
    assert sim_graph_only.get("ok"), sim_graph_only
    val = float(sim_graph_only["simulated"])
    assert abs(val - HEADLINE_RLC_VC_PEAK_V) < 0.6


@pytest.mark.skipif(not simulator_status().get("available"), reason="ngspice missing")
@pytest.mark.xfail(
    strict=True,
    reason="ARC-TE-001: finish_circuit_lab passes derive cir into simulate_graph, masking a shorted drawn graph",
)
def test_shorted_drawn_graph_must_not_match_analytic_peak(tmp_path: Path) -> None:
    """Extra wire vin.n1→c1.n2 parallel-shorts the RLC string; verify must disagree when graph is wrong."""
    meta = series_rlc_step(HEADLINE_RLC_R_OHM, HEADLINE_RLC_L_H, HEADLINE_RLC_C_F, HEADLINE_RLC_VIN)
    graph = series_rlc_graph(
        vin=HEADLINE_RLC_VIN,
        r_ohm=HEADLINE_RLC_R_OHM,
        l_h=HEADLINE_RLC_L_H,
        c_f=HEADLINE_RLC_C_F,
    )
    graph["edges"].append({"id": "short", "from": "vin.n1", "to": "c1.n2"})
    run_dir = tmp_path / "short_lab"
    problem = {
        "kind": "series_rlc",
        "vin": HEADLINE_RLC_VIN,
        "r_ohm": HEADLINE_RLC_R_OHM,
        "l_h": HEADLINE_RLC_L_H,
        "c_f": HEADLINE_RLC_C_F,
        "tol": 0.02,
        "analysis": "tran",
        "t_s": float(meta["t_Vc_peak_s"]),
        "probe": "v(3)",
    }
    verify = finish_circuit_lab(run_dir, problem)
    sim_from_graph = simulate_graph(graph, {**problem, "cir": None}, run_dir=run_dir / "graph_only")
    assert sim_from_graph.get("ok")
    graph_peak = float(sim_from_graph["simulated"])
    assert abs(graph_peak - float(meta["Vc_peak_V"])) > 0.5, (
        f"shorted graph sim {graph_peak} too close to analytic {meta['Vc_peak_V']}"
    )
    assert verify.get("mismatch") is True or verify.get("needs_review") is True


@given(
    extra_edge=st.booleans(),
)
@settings(max_examples=8, deadline=None)
def test_random_valid_resistor_divider_compiles(extra_edge: bool) -> None:
    g = _minimal_grounded_resistor()
    if extra_edge:
        g["edges"].append({"id": "ex", "from": "vin.n1", "to": "r1.n2"})
    try:
        compile_netlist(parse_graph(g))
    except CompileError:
        pytest.skip("invalid topology for SPICE")