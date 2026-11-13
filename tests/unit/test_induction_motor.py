"""P8 sheet equivalent circuit."""

from __future__ import annotations

from electrical_engineer.engines.induction_motor import solve_induction_motor


def test_p8_sheet_numbers() -> None:
    r = solve_induction_motor(
        {
            "kind": "im_ec",
            "f_hz": 50,
            "poles": 4,
            "v_line_v": 415,
            "r1_ohm": 0.5,
            "x1_ohm": 1.2,
            "r2p_ohm": 0.4,
            "x2p_ohm": 1.2,
            "xm_ohm": 30,
            "slip": 0.04,
        }
    )
    assert abs(r["rotor_speed_rpm"] - 1440.0) < 0.1
    assert abs(r["stator_current_A"] - 23.456116655053975) < 1e-3
    assert abs(r["developed_torque_Nm"] - 88.10049292522137) < 0.05
    assert abs(r["slip_at_max_torque"] - 0.16702205904356413) < 1e-3


def test_torque_missing_factor_of_three_fails_trap() -> None:
    r = solve_induction_motor(
        {
            "f_hz": 50,
            "poles": 4,
            "v_line_v": 415,
            "r1_ohm": 0.5,
            "x1_ohm": 1.2,
            "r2p_ohm": 0.4,
            "x2p_ohm": 1.2,
            "xm_ohm": 30,
            "slip": 0.04,
        }
    )
    wrong = r["developed_torque_Nm"] / 2.0
    assert abs(wrong - 44.05) < 0.1
    assert abs(r["developed_torque_Nm"] - 88.1) < 0.2
