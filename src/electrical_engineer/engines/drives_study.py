"""UG intro electric drives — OSS steady-state torque/speed (no Simulink plant)."""

from __future__ import annotations

import json
from math import pi
from pathlib import Path
from typing import Any


def _dc_drive(problem: dict[str, Any]) -> dict[str, float]:
    ra = float(problem.get("ra_ohm") or problem.get("armature_r") or 1.0)
    k = float(problem.get("k_torque") or problem.get("ke") or 0.5)
    v = float(problem.get("v_dc") or problem.get("voltage") or 120.0)
    t_load = float(problem.get("t_load_nm") or problem.get("load_torque") or 5.0)
    if k <= 0:
        raise ValueError("k_torque must be positive")
    ia = t_load / k
    omega = (v - ra * ia) / k
    return {
        "ia_a": ia,
        "omega_rad_s": omega,
        "rpm": omega * 60.0 / (2.0 * pi),
        "t_elect_nm": t_load,
    }


def _im_slip_torque(problem: dict[str, Any]) -> dict[str, float]:
    f_hz = float(problem.get("f_hz") or 50.0)
    poles = int(problem.get("poles") or 4)
    n_sync = 120.0 * f_hz / poles
    t_rated = float(problem.get("t_rated_nm") or 20.0)
    slip_rated = float(problem.get("slip_rated") or 0.04)
    k = t_rated / slip_rated if slip_rated > 0 else 0.0
    t_load = float(problem.get("t_load_nm") or t_rated)
    slip = t_load / k if k > 0 else 0.0
    rpm = n_sync * (1.0 - slip)
    return {
        "n_sync_rpm": n_sync,
        "slip": slip,
        "rpm": rpm,
        "t_load_nm": t_load,
    }


def run_drives_study(run_dir: Path, problem: dict[str, Any]) -> dict[str, Any]:
    run_dir.mkdir(parents=True, exist_ok=True)
    kind = str(problem.get("kind") or problem.get("machine") or "dc").lower()
    try:
        if kind in {"dc", "dc_motor", "separately_excited"}:
            result = _dc_drive(problem)
        elif kind in {"im", "induction", "im_slip"}:
            result = _im_slip_torque(problem)
        else:
            return {"ok": False, "error": f"unsupported drive kind {kind}", "unchecked": True}
    except ValueError as exc:
        return {"ok": False, "error": str(exc), "unchecked": True}
    path = run_dir / "drives_result.json"
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    rpm = float(result["rpm"])
    svg = run_dir / "artifact.svg"
    svg.write_text(
        (
            "<svg xmlns='http://www.w3.org/2000/svg' width='320' height='120'>"
            f"<text x='8' y='24' font-size='14'>{kind.upper()} drive</text>"
            f"<text x='8' y='56' font-size='13'>Speed {rpm:.2f} rpm</text>"
            "</svg>"
        ),
        encoding="utf-8",
    )
    return {
        "ok": True,
        "tool": "drives-study",
        "unchecked": False,
        "value": rpm,
        "result": result,
        "paths": [str(path), str(svg)],
    }
