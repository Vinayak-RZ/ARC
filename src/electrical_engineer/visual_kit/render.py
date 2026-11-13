"""Render Visual Kit components; numeric props must come from engines."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from electrical_engineer.engines.agc_two_area import TwoAreaAgcCase, simulate_two_area
from electrical_engineer.engines.ed_lambda import EdCase, solve_lambda_ed
from electrical_engineer.engines.smib_swing import SmibCase, eec301_reference


def _require_mpl():
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("matplotlib required for visual-kit render") from exc
    return plt


def render_swing_equal_area(out_dir: Path, case: SmibCase | None = None) -> dict[str, Any]:
    case = case or SmibCase()
    ref = eec301_reference(case)
    plt = _require_mpl()
    fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=120)
    deltas = [math.radians(x) for x in range(120)]
    pe = [case.pmax_post_pu * math.sin(d) for d in deltas]
    ax.plot([math.degrees(d) for d in deltas], pe, label="Pe post")
    ax.axhline(case.pm_pu, color="C2", linestyle="--", label="Pm")
    ax.axvline(ref["delta0_deg"], color="C3", linestyle=":", label=f"delta0={ref['delta0_deg']:.2f}")
    ax.axvline(ref["delta_cr_deg"], color="C4", linestyle=":", label=f"dcr={ref['delta_cr_deg']:.2f}")
    ax.set_xlabel("delta (deg)")
    ax.set_ylabel("power (pu)")
    ax.set_title("SMIB equal-area (engine-bound)")
    ax.legend(fontsize=7, loc="upper right")
    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / "power.swing_equal_area.png"
    fig.tight_layout()
    fig.savefig(png)
    plt.close(fig)
    meta = {"component_id": "power.swing_equal_area", "props_source": "smib_swing", **ref}
    return {"png": str(png), "meta": meta}


def render_agc_trace(out_dir: Path) -> dict[str, Any]:
    case = TwoAreaAgcCase.eec301_default().with_k(0.3)
    out = simulate_two_area(case, run="agc", t_end_s=20.0)
    trail = out.get("trail") or []
    plt = _require_mpl()
    fig, ax = plt.subplots(figsize=(6.4, 3.2), dpi=120)
    if trail:
        f0 = case.f0_hz
        t = [p[0] for p in trail]
        f1 = [p[1][0] * f0 for p in trail]
        ax.plot(t, f1, label="f1 (Hz)")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("frequency (Hz)")
    ax.set_title("Two-area AGC trace (engine-bound)")
    ax.legend(fontsize=8)
    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / "power.agc_trace.png"
    fig.tight_layout()
    fig.savefig(png)
    plt.close(fig)
    steady = out.get("steady") or {}
    return {
        "png": str(png),
        "meta": {"component_id": "power.agc_trace", "steady": steady, "props_source": "agc_two_area"},
    }


def render_dispatch_curve(out_dir: Path, pd_mw: float = 500.0) -> dict[str, Any]:
    case = EdCase.eec301_default()
    plt = _require_mpl()
    fig, ax = plt.subplots(figsize=(6.4, 3.2), dpi=120)
    for pd in (300.0, 450.0, 500.0):
        row = solve_lambda_ed(case, pd)
        p = row["P"]
        ax.plot(p, [row["lam"]] * len(p), "o", label=f"PD={pd:.0f}")
    ax.set_xlabel("generator P (MW)")
    ax.set_ylabel("lambda")
    ax.set_title("Lambda ED (engine-bound)")
    ax.legend(fontsize=7)
    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / "power.dispatch_curve.png"
    fig.tight_layout()
    fig.savefig(png)
    plt.close(fig)
    return {
        "png": str(png),
        "meta": {"component_id": "power.dispatch_curve", "props_source": "ed_lambda", "pd_mw": pd_mw},
    }


def render_component(component_id: str, out_dir: Path, props: dict[str, Any] | None = None) -> dict[str, Any]:
    props = props or {}
    if component_id == "power.swing_equal_area":
        case = SmibCase(**props) if props else SmibCase()
        return render_swing_equal_area(out_dir, case)
    if component_id == "power.agc_trace":
        return render_agc_trace(out_dir)
    if component_id == "power.dispatch_curve":
        return render_dispatch_curve(out_dir, float(props.get("PD", 500.0)))
    raise ValueError(f"unknown visual component: {component_id}")
