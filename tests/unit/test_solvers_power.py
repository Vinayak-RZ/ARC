from __future__ import annotations

import math

import pytest

from electrical_engineer.engines.ee_v2_runner import solve_ee_v2
from electrical_engineer.engines.solvers.power import _idmt_time, _idmt_psm


def _solve(sid: str, **kw):
    return solve_ee_v2({"solver": sid, **kw})


def test_idmt_relay_golden() -> None:
    out = _solve(
        "idmt_relay_time",
        i_fault_a=1000,
        ct_primary_a=100,
        tms=1,
        curve="standard",
    )
    assert out["value"] == pytest.approx(2.971, rel=1e-3)


def test_idmt_coordination_hand() -> None:
    i_fault = 1000.0
    psm1 = _idmt_psm(i_fault, 100, 1.0, 1.0)
    t1 = _idmt_time(psm1, 0.5, "standard")
    psm2 = _idmt_psm(i_fault, 100, 1.0, 1.5)
    t2_req = t1 + 0.3
    k, a = 0.14, 0.02
    r2_tms = t2_req * (psm2**a - 1.0) / k
    out = _solve(
        "idmt_coordination",
        i_fault_a=i_fault,
        r1_ct_primary_a=100,
        r1_plug_setting=1.0,
        r1_tms=0.5,
        r1_curve="standard",
        r2_ct_primary_a=100,
        r2_plug_setting=1.5,
        r2_curve="standard",
    )
    assert out["value"] == pytest.approx(r2_tms, rel=1e-6)


def test_differential_bias() -> None:
    out = _solve("differential_bias", i1_a=5, i2_a=4)
    assert out["value"] == pytest.approx(1.0, abs=1e-9)
    assert out["result"]["trip"] is False


def test_mho_reach() -> None:
    out = _solve(
        "mho_reach",
        z_line_ohm=10,
        line_angle_deg=75,
        ct_ratio=600,
        vt_ratio=1200,
    )
    assert out["value"] == pytest.approx(4.0, rel=1e-6)


def test_cb_rrrv() -> None:
    out = _solve("cb_rrrv", v_ll_kv=11, l_h=0.006, c_f=1e-8)
    assert out["value"] == pytest.approx(1.159e9, rel=1e-2)


def test_equal_area_critical() -> None:
    out = _solve(
        "equal_area_critical",
        pm_pu=1,
        pmax_pre_pu=2,
        pmax_post_pu=2,
        pmax_fault_pu=0,
        h_s=5,
    )
    assert out["value"] == pytest.approx(79.56, abs=0.05)


def test_lfc_single_area() -> None:
    out = _solve("lfc_single_area", delta_pd_pu=0.01, r_pu=0.05, d_pu=1, f_hz=50)
    assert out["value"] == pytest.approx(-0.02381, rel=1e-4)