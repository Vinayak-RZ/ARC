"""Plot mean vs RL reference Vo or R closed form (0.5%, no skips)."""

from __future__ import annotations

import pytest

from electrical_engineer.engines.rectifier_rl_steady import (
    rl_reference_slice,
    rl_vo_mean_closed_form,
)
from electrical_engineer.engines.rectifier_waveforms import (
    _vo_closed_form,
    mean_waveform,
    sample_waveform,
)
from electrical_engineer.engines.solvers.power_electronics import rectifier_1ph, rectifier_3ph

_TOPO_1PH = ("hw1", "semi1", "full1")
_TOPO_3PH = ("hw3", "semi3", "full3")
_ALPHAS = (0, 30, 45, 60, 75, 90)


@pytest.mark.parametrize("alpha_deg", _ALPHAS)
@pytest.mark.parametrize("load", ("R", "RL"))
@pytest.mark.parametrize("topology", _TOPO_1PH)
def test_rectifier_1ph_mean_matches_vo(topology: str, load: str, alpha_deg: float) -> None:
    problem = {
        "topology": topology,
        "load": load,
        "v_rms": 230,
        "alpha_deg": alpha_deg,
        "r_ohm": 10,
        "io_a": 0,
        "ls_h": 0,
        "l_h": 0.01 if load == "RL" else 0,
        "f_hz": 50,
    }
    if load == "RL":
        vo = rl_vo_mean_closed_form(rl_reference_slice(problem))
    else:
        vo = _vo_closed_form(problem, rectifier_1ph, rectifier_3ph)
    pts = sample_waveform(problem, n=3600)
    mean = mean_waveform(pts)
    if abs(vo) < 1e-6:
        return
    assert abs(mean - vo) / abs(vo) < 0.005


@pytest.mark.parametrize("alpha_deg", _ALPHAS)
@pytest.mark.parametrize("load", ("R", "RL"))
@pytest.mark.parametrize("topology", _TOPO_3PH)
def test_rectifier_3ph_mean_matches_vo(topology: str, load: str, alpha_deg: float) -> None:
    problem = {
        "topology": topology,
        "load": load,
        "v_ll_rms": 415,
        "v_rms": 415,
        "alpha_deg": alpha_deg,
        "r_ohm": 10,
        "io_a": 0,
        "ls_h": 0,
        "l_h": 0.01 if load == "RL" else 0,
        "f_hz": 50,
    }
    if load == "RL":
        vo = rl_vo_mean_closed_form(rl_reference_slice(problem))
    else:
        vo = _vo_closed_form(problem, rectifier_1ph, rectifier_3ph)
    pts = sample_waveform(problem, n=3600)
    mean = mean_waveform(pts)
    if abs(vo) < 1e-6:
        return
    assert abs(mean - vo) / abs(vo) < 0.005