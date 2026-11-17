"""Netlist-first circuit derive (MNA); per-kind templates are fallback only."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from electrical_engineer.engines.circuit_mna import MnaError, mna_solve


class DeriveError(ValueError):
    pass


def _load_cir(problem: dict[str, Any], item_root: Path | None = None) -> str:
    if problem.get("cir"):
        return str(problem["cir"])
    if problem.get("netlist"):
        return str(problem["netlist"])
    rel = problem.get("netlist_path") or problem.get("cir_file") or "fixtures/netlist.cir"
    if item_root is not None:
        p = item_root / str(rel)
        if p.is_file():
            return p.read_text()
    p = Path(str(rel))
    if p.is_file():
        return p.read_text()
    raise DeriveError("missing netlist (cir, netlist_path, or fixtures/netlist.cir)")


def derive(problem: dict[str, Any], *, item_root: Path | None = None) -> dict[str, Any]:
    """Return derived scalar from MNA on the item netlist (templates only as fallback)."""
    allow = bool(problem.get("allow_template_fallback"))
    kind = str(problem.get("kind") or problem.get("circuit_kind") or "").lower()
    try:
        cir = _load_cir(problem, item_root)
    except DeriveError:
        if allow and kind and kind in _KINDS:
            out = _KINDS[kind](problem)
            out["kind"] = kind
            out.setdefault("engine", "circuit_derive")
            out["derived_via"] = "template_fallback"
            return out
        raise
    analysis = str(problem.get("analysis") or "dc").lower()
    probe = str(problem.get("probe") or problem.get("probe_expr") or "v(2)")
    f_hz = problem.get("f_hz")
    t_s = problem.get("t_s")
    try:
        raw = mna_solve(
            cir,
            analysis=analysis,
            f_hz=float(f_hz) if f_hz is not None else None,
            t_s=float(t_s) if t_s is not None else None,
            dt=float(problem["dt"]) if problem.get("dt") is not None else None,
            probe=probe,
        )
    except MnaError as exc:
        if allow and kind and kind in _KINDS:
            out = _KINDS[kind](problem)
            out["kind"] = kind
            out.setdefault("engine", "circuit_derive")
            out["derived_via"] = "template_fallback"
            return out
        raise DeriveError(str(exc)) from exc
    unit = str(problem.get("unit") or _default_unit(probe, analysis))
    out = {
        "value": float(raw["value"]),
        "unit": unit,
        "cir": cir,
        "probe": probe,
        "analysis": analysis,
        "engine": "circuit_derive",
        "derived_via": "mna",
    }
    if problem.get("probe_node"):
        out["probe_node"] = str(problem["probe_node"])
    if f_hz is not None:
        out["f_hz"] = float(f_hz)
    if t_s is not None:
        out["t_s"] = float(t_s)
    if kind:
        out["kind"] = kind
    return out


def _default_unit(probe: str, analysis: str) -> str:
    p = probe.lower()
    if p.startswith("ph("):
        return "deg"
    if p.startswith("i("):
        return "A"
    if analysis == "ac" and p.startswith("mag("):
        return "V"
    return "V"


# --- template fallback (deprecated for golds; tests may set allow_template_fallback) ---


def netlist_dc_divider(vin: float, r1: float, r2: float) -> tuple[str, str]:
    cir = (
        "* arc dc divider\n"
        f"V1 1 0 DC {vin}\n"
        f"R1 1 2 {r1}\n"
        f"R2 2 0 {r2}\n"
        ".end\n"
    )
    return cir, "v(2)"


def _dc_divider(problem: dict[str, Any]) -> dict[str, Any]:
    vin = float(problem["vin"])
    r1, r2 = float(problem["r1"]), float(problem["r2"])
    if r1 + r2 == 0:
        raise DeriveError("r1+r2 is zero")
    vout = vin * r2 / (r1 + r2)
    cir, probe = netlist_dc_divider(vin, r1, r2)
    return {"value": vout, "unit": "V", "cir": cir, "probe_node": "2", "probe": probe}


def _series_rlc(problem: dict[str, Any]) -> dict[str, Any]:
    from electrical_engineer.engines.rlc_transient import series_rlc_step

    vin = float(problem.get("vin") or problem.get("v_step") or 10)
    r_ohm = float(problem.get("r_ohm") or problem.get("r") or 10)
    l_h = float(problem.get("l_h") or problem.get("l") or 1e-3)
    c_f = float(problem.get("c_f") or problem.get("c") or 1e-6)
    step_v = float(problem.get("v_step") or vin)
    meta = series_rlc_step(r_ohm, l_h, c_f, step_v)
    t_peak_s = float(meta["t_Vc_peak_s"])
    t_settle = meta.get("settling_2pct_entry_s") or meta.get("settling_time_2pct_s")
    t_stop = float(problem.get("t_s") or max(t_peak_s * 1.2, 1e-4))
    probe = str(problem.get("probe") or problem.get("probe_expr") or "v(3)")
    bug = str(problem.get("derive_bug") or "").lower()
    if bug in ("forward_euler", "euler"):
        from electrical_engineer.engines.rlc_transient import forward_euler_vc_peak

        value, t_peak_s = forward_euler_vc_peak(r_ohm, l_h, c_f, step_v)
        engine = "forward_euler_bug"
    else:
        overshoot = float(meta.get("overshoot_pct") or 0.0) < 0.5
        value = float(step_v if overshoot else meta["Vc_peak_V"])
        engine = "circuit_derive"
    cir = (
        "* arc series rlc\n"
        f"V1 1 0 DC {step_v}\n"
        f"R1 1 2 {r_ohm}\nL1 2 3 {l_h}\nC1 3 0 {c_f}\n"
        f".ic v(3)=0\n"
        f".tran {max(t_stop / 500, 1e-7):g} {t_stop:g} uic\n.end\n"
    )
    return {
        "value": value,
        "unit": "V",
        "cir": cir,
        "probe": probe,
        "probe_node": str(problem.get("probe_node") or "3"),
        "analysis": "tran",
        "t_s": t_peak_s,
        "t_stop": t_stop,
        "derive_metric": "Vc_final" if float(meta.get("overshoot_pct") or 0.0) < 0.5 else "Vc_peak",
        "settling_2pct_entry_s": t_settle,
        "settling_time_2pct_s": meta.get("settling_time_2pct_s"),
        "engine": engine,
    }


_KINDS = {
    "dc_divider": _dc_divider,
    "voltage_divider": _dc_divider,
    "series_rlc": _series_rlc,
    "rlc": _series_rlc,
}
