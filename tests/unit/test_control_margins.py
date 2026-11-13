"""Control margin naming vs python-control wcg/wcp."""

from __future__ import annotations

import control

from electrical_engineer.engines.control_margins import loop_margins


def test_margin_40_third_order() -> None:
    sys = control.tf([40.0], [1.0, 12.0, 20.0, 0.0])
    m = loop_margins(sys)
    assert abs(m["gain_crossover_rad_s"] - 1.55868640406249) < 1e-5
    assert abs(m["phase_crossover_rad_s"] - 4.4721359682367465) < 1e-5
    assert abs(m["phase_margin_deg"] - 43.20984525381832) < 1e-4
    assert abs(m["gain_margin_dB"] - 15.563024919110225) < 1e-3


def test_control_runner_exports_margins(tmp_path) -> None:
    from electrical_engineer.engines.control_runner import run_control_plots

    out = run_control_plots(
        tmp_path,
        {"num": [40.0], "den": [1.0, 12.0, 20.0, 0.0]},
    )
    assert out["gain_crossover_rad_s"] == out["margins"]["gain_crossover_rad_s"]
    assert abs(out["gain_margin_dB"] - 15.563) < 0.01
