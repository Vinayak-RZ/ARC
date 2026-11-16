"""Focused tests to kill mutants in verify, netlist, and solver paths (mutation testing)."""

from __future__ import annotations

import math

import pytest

from electrical_engineer.circuit.netlist import CompileError, compile_netlist
from electrical_engineer.circuit.simulate_graph import compare_derived
from electrical_engineer.engines.rlc_transient import series_rlc_step
from electrical_engineer.engines.solvers.power import idmt_relay_time
from electrical_engineer.circuit.graph import parse_graph, series_rlc_graph
from tests.golden_numerics_refs import HEADLINE_IDMT_T_S, HEADLINE_RLC_VC_PEAK_V


def test_compare_derived_match_margin_uses_max_of_rel_and_abs() -> None:
    chk = compare_derived(10.0, 10.09, rel_tol=0.01, abs_tol=0.05)
    assert chk["match"] is True
    chk2 = compare_derived(10.0, 10.2, rel_tol=0.01, abs_tol=0.05)
    assert chk2["mismatch"] is True


def test_compare_derived_rel_err_pct_divisor() -> None:
    chk = compare_derived(0.0, 0.001, rel_tol=1.0)
    assert chk["rel_err_pct"] > 0


def test_compile_netlist_ground_node_zero() -> None:
    g = series_rlc_graph()
    cir = compile_netlist(parse_graph(g))
    assert " 0" in cir or " 0\n" in cir


def test_compile_netlist_rejects_no_ground() -> None:
    with pytest.raises(CompileError):
        compile_netlist(parse_graph({"nodes": [{"id": "r1", "type": "resistor", "value": 1}], "edges": []}))


def test_idmt_standard_curve_k_factor() -> None:
    out = idmt_relay_time(1000, 100, 1.0, "standard", plug_setting=1.0)
    assert abs(out["t_op_s"] - HEADLINE_IDMT_T_S) < 0.01
    with pytest.raises(ValueError):
        idmt_relay_time(50, 100, 1.0, "standard", plug_setting=1.0)


def test_rlc_peak_underdamped_headline() -> None:
    r = series_rlc_step(10, 0.01, 100e-6, 10)
    assert abs(r["Vc_peak_V"] - HEADLINE_RLC_VC_PEAK_V) < 0.02
    assert math.isfinite(r["zeta"])