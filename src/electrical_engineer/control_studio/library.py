"""Built-in plant and controller presets for the palette."""

from __future__ import annotations

from typing import Any

PALETTE_GROUPS: list[dict[str, Any]] = [
    {
        "id": "sources",
        "label": "Sources",
        "items": [
            {"type": "step", "label": "Step", "icon": "▸", "default_params": {"amplitude": 1.0, "unit": "1"}},
            {"type": "ramp", "label": "Ramp", "icon": "↗", "default_params": {"slope": 1.0, "unit": "1/s"}},
            {"type": "sine", "label": "Sine", "icon": "~", "default_params": {"amplitude": 1.0, "frequency_hz": 1.0}},
        ],
    },
    {
        "id": "linear",
        "label": "Linear",
        "items": [
            {"type": "gain", "label": "Gain", "icon": "△", "default_params": {"k": 1.0, "unit": "1"}},
            {"type": "sum", "label": "Sum", "icon": "⊕", "default_params": {"signs": "+-"}},
            {"type": "transfer_function", "label": "Transfer Fcn", "icon": "H", "default_params": {"tf": "1/(s+1)", "unit": "1"}},
            {"type": "pid", "label": "PID", "icon": "PID", "default_params": {"kp": 1.0, "ki": 0.0, "kd": 0.0}},
            {"type": "integrator", "label": "Integrator", "icon": "∫", "default_params": {}},
            {"type": "derivative", "label": "Derivative", "icon": "d/dt", "default_params": {}},
        ],
    },
    {
        "id": "nonlinear",
        "label": "Nonlinear",
        "items": [
            {"type": "saturation", "label": "Saturation", "icon": "⎍", "default_params": {"upper": 1.0, "lower": -1.0}},
            {"type": "delay", "label": "Delay (Pade)", "icon": "τ", "default_params": {"tau_s": 0.1, "order": 1}},
        ],
    },
    {
        "id": "sinks",
        "label": "Sinks",
        "items": [
            {"type": "scope", "label": "Scope", "icon": "◔", "default_params": {}},
        ],
    },
    {
        "id": "plants",
        "label": "Plants",
        "items": [
            {"type": "plant_dc_motor", "label": "DC motor", "icon": "⚙", "default_params": {"J": 0.01, "b": 0.1, "K": 0.01, "R": 1.0, "L": 0.5}},
            {"type": "plant_first_order", "label": "1st-order plant", "icon": "P", "default_params": {"k": 10.0, "tau": 1.0, "unit": "1"}},
            {"type": "plant_agc_area", "label": "AGC area", "icon": "A", "default_params": {"case": "eec301_default"}},
        ],
    },
]


PALETTE: list[dict[str, Any]] = [
    {"type": "step", "label": "Step", "default_params": {"amplitude": 1.0, "unit": "1"}},
    {"type": "ramp", "label": "Ramp", "default_params": {"slope": 1.0, "unit": "1/s"}},
    {"type": "sine", "label": "Sine", "default_params": {"amplitude": 1.0, "frequency_hz": 1.0}},
    {"type": "gain", "label": "Gain", "default_params": {"k": 1.0, "unit": "1"}},
    {"type": "sum", "label": "Sum", "default_params": {"signs": "+-"}},
    {"type": "transfer_function", "label": "Transfer Fcn", "default_params": {"tf": "1/(s+1)", "unit": "1"}},
    {"type": "pid", "label": "PID", "default_params": {"kp": 1.0, "ki": 0.0, "kd": 0.0}},
    {"type": "integrator", "label": "Integrator", "default_params": {}},
    {"type": "derivative", "label": "Derivative", "default_params": {}},
    {"type": "saturation", "label": "Saturation", "default_params": {"upper": 1.0, "lower": -1.0}},
    {"type": "delay", "label": "Delay (Pade)", "default_params": {"tau_s": 0.1, "order": 1}},
    {"type": "scope", "label": "Scope", "default_params": {}},
    {"type": "plant_dc_motor", "label": "DC motor", "default_params": {"J": 0.01, "b": 0.1, "K": 0.01, "R": 1.0, "L": 0.5}},
    {"type": "plant_first_order", "label": "1st-order plant", "default_params": {"k": 10.0, "tau": 1.0, "unit": "1"}},
    {"type": "plant_agc_area", "label": "AGC area", "default_params": {"case": "eec301_default"}},
]


def dc_motor_tf(params: dict[str, Any]):
    """J,b,K,R,L plant; output shaft velocity / torque input (UG simplification)."""
    import control

    J = float(params.get("J") or 0.01)
    b = float(params.get("b") or 0.1)
    K = float(params.get("K") or 0.01)
    R = float(params.get("R") or 1.0)
    L = float(params.get("L") or 0.5)
    # K/(R+sL) * K/(Js+b) roughly; standard second-order approx:
    num = [K]
    den = [L * J, L * b + R * J, R * b + K * K]
    return control.tf(num, den)


def first_order_tf(params: dict[str, Any]):
    import control

    k = float(params.get("k") or 1.0)
    tau = float(params.get("tau") or 1.0)
    return control.tf([k], [tau, 1.0])


def pid_tf(params: dict[str, Any]):
    import control

    kp = float(params.get("kp") or params.get("Kp") or 0.0)
    ki = float(params.get("ki") or params.get("Ki") or 0.0)
    kd = float(params.get("kd") or params.get("Kd") or 0.0)
    # Parallel PID as one rational TF: (kd*s^2 + kp*s + ki) / s
    return control.tf([kd, kp, ki], [1.0, 0.0])
