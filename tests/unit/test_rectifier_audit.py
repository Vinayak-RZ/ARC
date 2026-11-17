"""Rectifier readout vs waveform mean (no rescaling); from first principles."""

from __future__ import annotations

import pytest

from electrical_engineer.engines.rectifier_waveforms import (
    _vo_closed_form,
    mean_waveform,
    sample_waveform,
    source_peak_v,
)
from electrical_engineer.engines.solvers.power_electronics import rectifier_1ph, rectifier_3ph

TOPOLOGIES = ("hw1", "semi1", "full1", "hw3", "semi3", "full3")
LOADS = ("R", "RL", "RLE")
ALPHAS = (0, 30, 60, 75, 90, 120, 150)


@pytest.mark.parametrize("topology", TOPOLOGIES)
@pytest.mark.parametrize("load", LOADS)
@pytest.mark.parametrize("alpha_deg", ALPHAS)
def test_rectifier_readout_mean_and_peak(topology: str, load: str, alpha_deg: float) -> None:
    v = 415.0 if topology.endswith("3") else 230.0
    problem = {
        "topology": topology,
        "load": load,
        "v_rms": v,
        "v_ll_rms": v,
        "alpha_deg": alpha_deg,
        "io_a": 0,
        "ls_h": 0,
        "r_ohm": 10,
    }
    vo = _vo_closed_form(problem, rectifier_1ph, rectifier_3ph)
    pts = sample_waveform(problem, n=7200)
    mean = mean_waveform(pts)
    peak = source_peak_v(problem)
    max_abs = max(abs(y) for _, y in pts)
    assert max_abs <= peak + 2.0, f"{topology} {load} α={alpha_deg}: max |v|={max_abs} > peak {peak}"
    if abs(vo) < 1.0:
        assert abs(mean) < 2.0
        return
    rel = abs(mean - vo) / abs(vo)
    assert rel < 0.005, f"{topology} {load} α={alpha_deg}: mean {mean} vs Vo {vo}"


def test_full1_r_alpha60_readout() -> None:
    vo = _vo_closed_form(
        {"topology": "full1", "load": "R", "v_rms": 230, "alpha_deg": 60, "io_a": 0, "ls_h": 0},
        rectifier_1ph,
        rectifier_3ph,
    )
    assert abs(vo - 155.3) < 0.25


def test_full3_r_alpha75_readout() -> None:
    vo = _vo_closed_form(
        {"topology": "full3", "load": "R", "v_rms": 415, "alpha_deg": 75, "io_a": 0, "ls_h": 0},
        rectifier_1ph,
        rectifier_3ph,
    )
    assert abs(vo - 164.1) < 0.35