"""Seed graph.json, control_diagram.json, and missing figures for the localhost UI."""

from __future__ import annotations

import json
import logging
import math
from pathlib import Path
from typing import Any

_LOG = logging.getLogger(__name__)

from electrical_engineer.circuit.graph import default_graph_for, write_graph
from electrical_engineer.control.diagram import control_diagram_for_recipe, write_control_diagram
from electrical_engineer.visual_kit.diagram_spec import diagram_for_run, write_diagram_json


def seed_run_visuals(run_dir: Path, recipe_id: str, problem: dict[str, Any] | None) -> None:
    problem = problem or {}
    if not (run_dir / "graph.json").is_file():
        graph = default_graph_for(problem)
        if graph is None and recipe_id == "simulate-circuit":
            graph = default_graph_for({"kind": "series_rlc", **problem})
        if graph is not None:
            write_graph(run_dir, graph)
    diagram = control_diagram_for_recipe(recipe_id, problem)
    cd_path = run_dir / "control_diagram.json"
    if diagram is not None:
        write_control_diagram(run_dir, diagram)
    elif cd_path.is_file():
        cd_path.unlink()
    try:
        write_diagram_json(run_dir, diagram_for_run(run_dir, recipe_id, problem))
    except Exception as exc:  # noqa: BLE001
        _LOG.warning("diagram.json seed skipped for %s: %s", recipe_id, exc)
    try:
        _seed_figures(run_dir, recipe_id, problem)
    except Exception as exc:  # noqa: BLE001
        _LOG.warning("figure seed skipped for %s: %s", recipe_id, exc)


def _seed_figures(run_dir: Path, recipe_id: str, problem: dict[str, Any]) -> None:
    if recipe_id == "smib-swing-study":
        _copy_render(run_dir, "power.swing_equal_area.png", _render_swing)
    elif recipe_id == "ed-lambda-study":
        pd = float(problem.get("PD") or problem.get("pd_mw") or 500)
        _copy_render(run_dir, "power.dispatch_curve.png", lambda out: _render_dispatch(out, pd))
    elif recipe_id == "simulate-circuit" and str(problem.get("kind") or "") == "series_rlc":
        _rlc_step_png(run_dir, problem)
    elif recipe_id == "study-power-electronics-v2" and str(problem.get("solver") or "") == "ccm_buck":
        _buck_png(run_dir, problem)
    elif recipe_id == "solve-circuit-problem" and (
        str(problem.get("kind") or "") == "voltage_divider" or {"vin", "r1", "r2"} <= set(problem)
    ):
        _divider_svg(run_dir, problem)


def _copy_render(run_dir: Path, name: str, render) -> None:
    dest = run_dir / name
    if dest.is_file():
        return
    render(run_dir)


def _render_swing(run_dir: Path) -> None:
    from electrical_engineer.visual_kit.render_power import render_swing_equal_area

    render_swing_equal_area(run_dir)


def _render_dispatch(run_dir: Path, pd_mw: float) -> None:
    from electrical_engineer.visual_kit.render_power import render_dispatch_curve

    render_dispatch_curve(run_dir, pd_mw)


def _rlc_step_png(run_dir: Path, problem: dict[str, Any]) -> None:
    dest = run_dir / "step.png"
    if dest.is_file():
        return
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    r = float(problem.get("r_ohm") or problem.get("r") or 10)
    l_h = float(problem.get("l_h") or problem.get("l") or 0.01)
    c_f = float(problem.get("c_f") or problem.get("c") or 100e-6)
    v = float(problem.get("v_step") or problem.get("vin") or 10)
    i = 0.0
    vc = 0.0
    wn = 1.0 / math.sqrt(l_h * c_f)
    steps = 400
    dt = (8.0 / wn) / (steps - 1)
    ts: list[float] = []
    ys: list[float] = []
    for n in range(steps):
        ts.append(n * dt * 1e3)
        ys.append(vc)
        di = (v - vc - r * i) / l_h * dt
        dvc = (i / c_f) * dt
        i += di
        vc += dvc
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.plot(ts, ys, color="#2f6feb")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Vc (V)")
    ax.set_title("Series RLC capacitor voltage")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(dest, dpi=120)
    plt.close(fig)


def _buck_png(run_dir: Path, problem: dict[str, Any]) -> None:
    dest = run_dir / "buck.png"
    if dest.is_file():
        return
    result = _load(run_dir / "ee_v2_result.json").get("result") or {}
    duty = float(result.get("D") or (problem.get("vout", 5) / problem.get("vin", 12)))
    delta = float(result.get("delta_I_A") or 0.4)
    i_out = float(problem.get("i_out") or 1.0)
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # One switching period: inductor current rises for D, falls for 1-D.
    xs = [0.0, duty, 1.0]
    ys = [i_out - delta / 2, i_out + delta / 2, i_out - delta / 2]
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.plot(xs, ys, color="#2f6feb")
    ax.axhline(i_out, color="#8a8a86", linestyle="--", linewidth=1)
    ax.set_xlabel("Fraction of the switching period")
    ax.set_ylabel("Inductor current (A)")
    ax.set_title(f"Buck CCM, D = {duty:.3f}")
    ax.set_xlim(0, 1)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(dest, dpi=120)
    plt.close(fig)


def _divider_svg(run_dir: Path, problem: dict[str, Any]) -> None:
    dest = run_dir / "artifact.svg"
    if dest.is_file():
        return
    vin = float(problem.get("vin") or 0)
    r1 = float(problem.get("r1") or 0)
    r2 = float(problem.get("r2") or 0)
    vout = vin * r2 / (r1 + r2) if r1 + r2 else 0.0
    dest.write_text(
        (
            "<svg xmlns='http://www.w3.org/2000/svg' width='480' height='220' viewBox='0 0 480 220'>"
            "<rect width='480' height='220' fill='#fafaf9'/>"
            "<g fill='none' stroke='#202020' stroke-width='2'>"
            "<line x1='70' y1='48' x2='250' y2='48'/>"
            "<line x1='70' y1='48' x2='70' y2='170'/>"
            "<line x1='250' y1='48' x2='250' y2='170'/>"
            "<line x1='70' y1='170' x2='250' y2='170'/>"
            "<polyline points='90,48 110,48 118,40 134,56 150,40 166,56 182,40 190,48 230,48'/>"
            "<polyline points='250,70 242,86 258,102 242,118 258,134 250,150'/>"
            "</g>"
            f"<text x='150' y='32' text-anchor='middle' font-family='sans-serif' font-size='13' fill='#202020'>R1 = {r1:g} Ω</text>"
            f"<text x='268' y='112' font-family='sans-serif' font-size='13' fill='#202020'>R2 = {r2:g} Ω</text>"
            f"<text x='40' y='114' text-anchor='end' font-family='sans-serif' font-size='13' fill='#202020'>Vin {vin:g} V</text>"
            f"<text x='300' y='100' font-family='sans-serif' font-size='16' fill='#1d47a3'>Vout = {vout:.2f} V</text>"
            "</svg>"
        ),
        encoding="utf-8",
    )


def _load(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}
