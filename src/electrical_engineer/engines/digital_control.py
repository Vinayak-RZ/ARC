"""Discrete-time LTI step / pole checks via python-control."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def run_digital_plots(run_dir: Path, problem: dict[str, Any]) -> dict[str, Any]:
    try:
        import control
    except ImportError:
        return {"ok": False, "error": "python-control missing", "unchecked": True, "tool": "digital-control"}
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ts = float(problem.get("ts") or problem.get("sample_time") or 0.01)
    if "num" in problem and "den" in problem:
        sys = control.tf(problem["num"], problem["den"], ts)
    elif problem.get("continuous_num") and problem.get("continuous_den"):
        cont = control.tf(problem["continuous_num"], problem["continuous_den"])
        sys = control.sample_system(cont, ts, method=str(problem.get("method") or "zoh"))
    else:
        return {"ok": False, "error": "discrete num/den or continuous_* required", "unchecked": True}

    run_dir.mkdir(parents=True, exist_ok=True)
    step_png = run_dir / "step.png"
    pole_png = run_dir / "bode.png"
    artifact_svg = run_dir / "artifact.svg"

    t, y = control.step_response(sys)
    plt.figure(figsize=(6, 4))
    plt.step(t, y, where="post", color="#0052ff")
    plt.xlabel("Sample n")
    plt.ylabel("Output")
    plt.grid(True, alpha=0.3)
    plt.title(f"Discrete step (Ts={ts})")
    plt.tight_layout()
    plt.savefig(step_png, dpi=120)
    plt.close()

    poles = control.poles(sys)
    plt.figure(figsize=(5, 5))
    plt.scatter(poles.real, poles.imag, color="#0052ff")
    plt.axhline(0, color="#dee1e6")
    plt.axvline(0, color="#dee1e6")
    plt.xlabel("Real")
    plt.ylabel("Imag")
    plt.title("Discrete poles (z-plane)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(pole_png, dpi=120)
    plt.close()

    artifact_svg.write_text(
        (
            "<svg xmlns='http://www.w3.org/2000/svg' width='320' height='120'>"
            "<text x='8' y='24' font-size='14'>Digital control</text>"
            f"<text x='8' y='56' font-size='12'>Ts={ts} poles={len(poles)}</text>"
            "</svg>"
        ),
        encoding="utf-8",
    )

    max_pole = float(max(abs(p) for p in poles)) if len(poles) else None
    stable = max_pole is not None and max_pole < 1.0
    return {
        "ok": True,
        "tool": "digital-control",
        "unchecked": False,
        "value": max_pole,
        "stable": stable,
        "poles": [{"re": float(p.real), "im": float(p.imag)} for p in poles],
        "paths": [str(step_png), str(pole_png), str(artifact_svg)],
    }
