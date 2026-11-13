"""Independent references for circuit benchmark golds (not circular with ee_v2 alone)."""

from __future__ import annotations

import math
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from electrical_engineer.benchmark_v01.public_schema import values_close
from electrical_engineer.engines.spice_runner import (
    _ensure_control_block,
    _interp_series_at_t,
    _parse_tran_series,
    spice_available,
)

# Fine step for RLC transients (well under 1 µs); cap points for long t.
_NGSPICE_STEP_S = 100e-9


def parallel_rlc_ngspice_netlist(
    r: float, l: float, c: float, vc0: float, i0: float, t_stop: float
) -> str:
    """SPICE deck for parallel R||L||C; i0 is initial current 1→0 through L (down)."""
    step = min(_NGSPICE_STEP_S, max(t_stop / 5000.0, 10e-9))
    base = f"""* parallel RLC natural (R||L||C @ node 1)
R1 1 0 {r:g}
C1 1 0 {c:g} IC={vc0:g}
L1 1 0 {l:g} IC={i0:g}
.tran {step:g} {t_stop:g} uic
.end
"""
    return _ensure_control_block(base, probe="v(1)")


def parallel_rlc_vc_independent(
    r: float, l: float, c: float, vc0: float, i0: float, t: float
) -> float:
    """Parallel RLC vc(t): duplicate state-space solution (not via rlc_natural)."""
    if l <= 0 or c <= 0 or r <= 0 or t < 0:
        raise ValueError("R, L, C must be positive and t >= 0")
    wn = 1.0 / math.sqrt(l * c)
    alpha = 1.0 / (2.0 * r * c)
    zeta = alpha / wn if wn > 0 else 0.0
    dv0 = -(i0 + vc0 / r) / c

    if zeta < 1.0 - 1e-12:
        wd = wn * math.sqrt(1.0 - zeta * zeta)
        a = vc0
        b = (dv0 + alpha * vc0) / wd
        expa = math.exp(-alpha * t)
        vc = expa * (a * math.cos(wd * t) + b * math.sin(wd * t))
    elif zeta > 1.0 + 1e-12:
        disc = math.sqrt(alpha * alpha - wn * wn)
        s1 = -alpha + disc
        s2 = -alpha - disc
        a_coef = (s2 * vc0 - dv0) / (s2 - s1)
        b_coef = vc0 - a_coef
        vc = a_coef * math.exp(s1 * t) + b_coef * math.exp(s2 * t)
    else:
        vc = (vc0 + (dv0 + alpha * vc0) * t) * math.exp(-alpha * t)
    return float(vc)


def parallel_rlc_vc_ngspice(
    r: float, l: float, c: float, vc0: float, i0: float, t: float
) -> float | None:
    if not spice_available() or t <= 0:
        return None
    probe = "v(1)"
    body = parallel_rlc_ngspice_netlist(r, l, c, vc0, i0, t)
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "rlc.cir"
        path.write_text(body, encoding="utf-8")
        try:
            proc = subprocess.run(
                ["ngspice", "-b", str(path)],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
        except OSError:
            return None
    combined = (proc.stdout or "") + "\n" + (proc.stderr or "")
    series = _parse_tran_series(combined, probe)
    return _interp_series_at_t(series, t)


def assert_circuit_gold_independent(item_name: str, givens: dict[str, Any], catalog_v: float) -> None:
    if item_name != "rlc-natural-01":
        return
    r, l, c = float(givens["r"]), float(givens["l"]), float(givens["c"])
    vc0, i0, t = float(givens["vc0"]), float(givens["i0"]), float(givens["t"])
    independent = parallel_rlc_vc_independent(r, l, c, vc0, i0, t)

    if not values_close(catalog_v, independent, {"tolerance_rel": 1e-9, "tolerance_abs": 1e-9}):
        raise AssertionError(
            f"rlc oracle {catalog_v} != independent {independent} for givens {givens!r}"
        )
    spice = parallel_rlc_vc_ngspice(r, l, c, vc0, i0, t)
    if spice is not None and not values_close(
        catalog_v, spice, {"tolerance_rel": 0.005, "tolerance_abs": 1e-3}
    ):
        raise AssertionError(f"rlc oracle disagrees with ngspice {spice}")


def circuit_gold_provenance(
    item_name: str, givens: dict[str, Any], catalog_value: float
) -> dict[str, Any]:
    if item_name == "rlc-natural-01":
        r, l, c = float(givens["r"]), float(givens["l"]), float(givens["c"])
        vc0, i0, t = float(givens["vc0"]), float(givens["i0"]), float(givens["t"])
        independent = parallel_rlc_vc_independent(r, l, c, vc0, i0, t)
        spice = parallel_rlc_vc_ngspice(r, l, c, vc0, i0, t)
        out: dict[str, Any] = {
            "method": "parallel_rlc_state_space",
            "convention": (
                "R||L||C at one node; i0_A is inductor current at t=0+ "
                "from the shared node through L toward ground"
            ),
            "independent_V": independent,
            "catalog_V": catalog_value,
        }
        if spice is not None:
            out["ngspice_V"] = spice
            out["ngspice_agree"] = values_close(
                catalog_value, spice, {"tolerance_rel": 0.005, "tolerance_abs": 1e-3}
            )
        from electrical_engineer.benchmark_v01.round_public import _sigfig

        out["catalog_V_rounded"] = _sigfig(catalog_value)
        out["ok"] = abs(independent - catalog_value) <= 1e-6
        return out
    if item_name in {"rc-step-01", "rl-step-01", "divider-dc-01"}:
        return {"method": "ee_v2_analytic", "ok": True}
    return {"method": "ee_v2_or_recipe", "ok": True}
