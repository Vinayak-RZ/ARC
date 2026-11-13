"""Compare derived circuit values with SPICE (or skip with reason)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from electrical_engineer.engines.circuit_derive import DeriveError, derive
from electrical_engineer.engines.spice_runner import run_spice_netlist, simulator_status


def verify_after_derive(
    problem: dict[str, Any],
    *,
    item_root: Path | None = None,
    run_dir: Path | None = None,
    rel_tol: float = 1e-3,
    abs_tol: float = 1e-9,
) -> dict[str, Any]:
    """Derive analytically, simulate when a backend exists, flag mismatches."""
    try:
        derived = derive(problem, item_root=item_root)
    except DeriveError as exc:
        return {
            "ok": False,
            "unchecked": True,
            "error": str(exc),
            "mismatch": False,
            "engine": "circuit_verify",
        }
    dval = float(derived["value"])
    sim_status = simulator_status()
    spice_payload: dict[str, Any] = {
        "simulator": sim_status,
        "skipped": False,
        "reason": None,
    }
    simulated: float | None = None
    mismatch = False
    if not sim_status.get("available"):
        spice_payload["skipped"] = True
        spice_payload["reason"] = sim_status.get("reason") or "simulator missing"
    elif run_dir is None:
        spice_payload["skipped"] = True
        spice_payload["reason"] = "no run_dir for simulation"
    else:
        prob = {
            **problem,
            "cir": derived.get("cir"),
            "probe_node": derived.get("probe_node"),
            "analysis": derived.get("analysis"),
            "f_hz": derived.get("f_hz"),
            "t_s": derived.get("t_s"),
        }
        sim_out = run_spice_netlist(str(derived["cir"]), run_dir, prob)
        spice_payload.update(sim_out)
        if sim_out.get("ok") and sim_out.get("value") is not None:
            simulated = float(sim_out["value"])
            tol = max(abs_tol, rel_tol * max(abs(dval), 1.0))
            mismatch = abs(simulated - dval) > tol
        elif sim_out.get("unchecked"):
            spice_payload["skipped"] = True
            spice_payload["reason"] = sim_out.get("error") or "simulation failed"
    gold = problem.get("value") if problem.get("value") is not None else problem.get("expected")
    gold_ok = True
    if gold is not None:
        tol_gold = float(problem.get("tol", 1e-4))
        gold_ok = abs(dval - float(gold)) <= max(abs_tol, tol_gold * max(abs(float(gold)), 1.0))
    require_spice = bool(problem.get("require_spice") or problem.get("require_spice_match"))
    spice_skipped = bool(spice_payload.get("skipped"))
    ok = gold_ok
    if require_spice and spice_skipped:
        ok = False
    elif require_spice and simulated is not None and mismatch:
        ok = False
    unchecked = not gold_ok
    return {
        "ok": ok,
        "unchecked": unchecked,
        "value": dval,
        "derived": dval,
        "simulated": simulated,
        "mismatch": mismatch,
        "mismatch_delta": (simulated - dval) if simulated is not None else None,
        "gold_ok": gold_ok,
        "unit": derived.get("unit"),
        "cir": derived.get("cir"),
        "spice": spice_payload,
        "engine": "circuit_verify",
        "kind": derived.get("kind"),
    }
