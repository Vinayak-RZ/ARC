"""LTI Bode and step plots via the ``control`` package."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def control_available() -> bool:
    try:
        import control  # noqa: F401
    except ImportError:
        return False
    return True


def _tf_from_problem(problem: dict[str, Any]):
    import control

    from electrical_engineer.engines.block_diagram import _parse_tf

    if "num" in problem and "den" in problem:
        return control.tf(problem["num"], problem["den"])
    if "tf" in problem:
        return _parse_tf({"tf": problem["tf"]})
    # default first-order for demos
    k = float(problem.get("k", 1.0))
    tau = float(problem.get("tau", 1.0))
    return control.tf([k], [tau, 1.0])


def run_control_plots(run_dir: Path, problem: dict[str, Any]) -> dict[str, Any]:
    if not control_available():
        return {"ok": False, "error": "python-control missing", "unchecked": True, "tool": "control"}
    import control
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sys = _tf_from_problem(problem)
    run_dir.mkdir(parents=True, exist_ok=True)
    bode_png = run_dir / "bode.png"
    step_png = run_dir / "step.png"
    artifact_png = run_dir / "artifact.png"
    artifact_svg = run_dir / "artifact.svg"

    plt.figure(figsize=(6, 4))
    control.bode_plot(sys, dB=True, Hz=False, omega_limits=(0.1, 100))
    plt.tight_layout()
    plt.savefig(bode_png, dpi=120)
    plt.close()

    plt.figure(figsize=(6, 4))
    t, y = control.step_response(sys)
    plt.plot(t, y, color="#0052ff")
    plt.xlabel("Time (s)")
    plt.ylabel("Output")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(step_png, dpi=120)
    plt.close()

    # UI primary artifact: step response
    artifact_png.write_bytes(step_png.read_bytes())
    artifact_svg.write_text(
        (
            "<svg xmlns='http://www.w3.org/2000/svg' width='320' height='120'>"
            "<text x='8' y='24' font-size='14'>Step response (control)</text>"
            f"<text x='8' y='56' font-size='12'>tf={problem.get('tf', 'num/den')}</text>"
            "</svg>"
        ),
        encoding="utf-8",
    )

    y_ss = float(y[-1]) if len(y) else None
    return {
        "ok": True,
        "tool": "python-control",
        "unchecked": False,
        "value": y_ss,
        "paths": [str(bode_png), str(step_png), str(artifact_png), str(artifact_svg)],
        "bode_png": str(bode_png),
        "step_png": str(step_png),
    }
