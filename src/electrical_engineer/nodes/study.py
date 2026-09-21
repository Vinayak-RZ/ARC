"""Coursework study nodes (block diagrams, protection, drives, digital control)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from electrical_engineer.nodes.registry import register
from electrical_engineer.nodes.sim import _missing, _problem
from electrical_engineer.unchecked import UNCHECKED


@register("compose-control-blocks")
def compose_control_blocks(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.block_diagram import plant_problem_dict
    from electrical_engineer.engines.control_runner import control_available

    problem = _problem(spec)
    if not control_available():
        return _missing("python-control", spec, inputs)
    try:
        plant = plant_problem_dict(problem)
    except (ValueError, ImportError) as exc:
        return {
            "ok": False,
            "error": str(exc),
            "unchecked": True,
            "token": UNCHECKED,
        }
    return {
        "ok": True,
        "unchecked": False,
        "plant": plant,
        "num": plant["num"],
        "den": plant["den"],
        "compose_meta": plant.get("compose_meta"),
    }


@register("run-digital-control")
def run_digital_control(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.digital_control import run_digital_plots

    run_dir_s = spec.get("run_dir")
    if not run_dir_s:
        return _missing("python-control", spec, inputs)
    return run_digital_plots(Path(run_dir_s), _problem(spec))


@register("run-protection-study")
def run_protection_study(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.protection_study import run_protection_study as _run

    run_dir_s = spec.get("run_dir")
    if not run_dir_s:
        return {"ok": False, "error": "no run_dir", "unchecked": True, "token": UNCHECKED}
    return _run(Path(run_dir_s), _problem(spec))


@register("run-drives-study")
def run_drives_study(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.drives_study import run_drives_study as _run

    run_dir_s = spec.get("run_dir")
    if not run_dir_s:
        return {"ok": False, "error": "no run_dir", "unchecked": True, "token": UNCHECKED}
    return _run(Path(run_dir_s), _problem(spec))
