"""Lab verify freshness: verdict vs derivation, human-edit re-sim, agent re-derive."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from electrical_engineer.circuit.graph import (
    graph_resistor_values,
    graphs_electrically_equal,
    series_rlc_params_from_graph,
)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def human_edit_notes(
    baseline_graph: dict[str, Any] | None,
    current_graph: dict[str, Any],
) -> list[str]:
    if not baseline_graph:
        return []
    base = graph_resistor_values(baseline_graph)
    cur = graph_resistor_values(current_graph)
    notes: list[str] = []
    for key in sorted(set(base) | set(cur)):
        if key not in base or key not in cur:
            continue
        b, c = base[key], cur[key]
        if abs(b - c) <= 1e-9 * max(abs(b), abs(c), 1.0):
            continue
        notes.append(f"Your edit changed {key} from {b:g} to {c:g} Ω")
    return notes


def _baseline_derived_rev(meta: dict[str, Any]) -> int:
    return int(meta.get("agent_baseline_rev") or meta.get("revision") or 1)


def derived_for_label(meta: dict[str, Any], *, target: str = "r1") -> str:
    base = meta.get("agent_baseline_graph")
    if not isinstance(base, dict):
        return f"Derived for r{_baseline_derived_rev(meta)}"
    vals = graph_resistor_values(base)
    ref = next((k for k in vals if k.upper() == "R1"), None) or next(iter(vals.keys()), "R1")
    rev = _baseline_derived_rev(meta)
    if ref in vals:
        return f"Derived for r{rev} ({ref} = {vals[ref]:g} Ω)"
    return f"Derived for r{rev}"


def _decorate_metric_rows(verify: dict[str, Any], meta: dict[str, Any], graph: dict[str, Any]) -> None:
    matches = derivation_matches_graph(meta, graph or {})
    deriv_rev = _baseline_derived_rev(meta)
    sim_rev = int(verify.get("computed_at_revision") or verify.get("graph_revision") or 0)
    verdict_current = bool(verify.get("verdict_current", True))
    derived_label = derived_for_label(meta)
    for row in verify.get("metrics") or []:
        if not isinstance(row, dict):
            continue
        row["derived_revision"] = deriv_rev
        row["simulated_revision"] = sim_rev if verdict_current else None
        row["derived_out_of_date"] = not matches
        row["simulated_out_of_date"] = not verdict_current
        if row.get("derived_out_of_date"):
            row["derived_note"] = derived_label
            row["derived_status"] = "out_of_date"
            row["derived_status_label"] = "Out of date"
            row["rel_err_pct"] = None
            row["status"] = "out_of_date"
            row["status_label"] = "Out of date"
            if row.get("simulated_out_of_date"):
                row["status"] = "out_of_date"
                row["status_label"] = "Out of date"
        if row.get("simulated_out_of_date"):
            row["simulated_status"] = "out_of_date"
            row["simulated_status_label"] = "Out of date"


def derivation_matches_graph(meta: dict[str, Any], graph: dict[str, Any]) -> bool:
    baseline = meta.get("agent_baseline_graph")
    if not isinstance(baseline, dict) or not baseline.get("nodes"):
        return True
    return graphs_electrically_equal(baseline, graph)


def rlc_compare_metric_label(
    meta: dict[str, Any],
    graph: dict[str, Any],
    *,
    no_overshoot: bool,
) -> str:
    if no_overshoot:
        return "Final value"
    return "Capacitor peak"


def apply_verify_semantics(
    verify: dict[str, Any] | None,
    meta: dict[str, Any],
    graph: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    if not verify:
        return verify
    out = dict(verify)
    kind = str(out.get("lab_kind") or meta.get("kind") or "circuit")
    rev = int(meta.get("revision") or 0)
    vrev = int(out.get("computed_at_revision") or out.get("graph_revision") or 0)
    if kind == "control":
        out["verdict_current"] = vrev > 0 and rev <= vrev
        out["derivation_matches_graph"] = True
        out["stale"] = not out["verdict_current"]
        if out["stale"]:
            out["status"] = "out_of_date"
            out["stale_reason"] = "Re-simulate the loop to refresh this check."
    else:
        out["derivation_matches_graph"] = derivation_matches_graph(meta, graph or {})
        out["verdict_current"] = vrev > 0 and rev <= vrev
        out["stale"] = not out["verdict_current"]
        if not out["verdict_current"]:
            if out.get("status") == "agrees" and not out.get("mismatch"):
                out["status"] = "out_of_date"
            out["stale_reason"] = out.get("stale_reason") or (
                "Simulation is behind the current lab revision — run Simulate again."
            )
        if not out["derivation_matches_graph"]:
            notes = human_edit_notes(meta.get("agent_baseline_graph"), graph or {})
            if notes:
                out["human_edit_notes"] = notes
            out["re_derive_reason"] = (
                (notes[0] + "; the agent's derivation no longer applies.")
                if notes
                else "The agent derived for a different circuit than the lab shows now."
            )
        if not out["derivation_matches_graph"]:
            out["needs_review"] = False
            out["mismatch"] = False
            out.pop("disagreement_banner", None)
        elif out.get("mismatch") and out.get("verdict_current"):
            out["needs_review"] = True
        else:
            out["needs_review"] = False
    if graph is not None:
        _decorate_metric_rows(out, meta, graph)
        rows = [r for r in (out.get("metrics") or []) if isinstance(r, dict)]
        out["all_rows_out_of_date"] = bool(
            rows
            and all(bool(r.get("derived_out_of_date")) and bool(r.get("simulated_out_of_date")) for r in rows)
        )
    return out


def attach_verify_freshness(
    verify: dict[str, Any] | None,
    meta: dict[str, Any],
    *,
    run_dir: Path | None = None,
    graph: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    if not verify:
        return verify
    if graph is None and run_dir is not None:
        from electrical_engineer.circuit.run_session import load_graph

        graph = load_graph(run_dir)
    return apply_verify_semantics(verify, meta, graph or {})


def agent_rederive_circuit_lab(run_dir: Path) -> dict[str, Any]:
    """Re-run derive on agent baseline params (or updated problem) and refresh verify."""
    from electrical_engineer.circuit.run_session import load_graph
    from electrical_engineer.collab import lab_meta
    from electrical_engineer.collab.workflow import refresh_circuit_lab_verify
    from electrical_engineer.engines.circuit_derive import derive

    meta = lab_meta.load_lab_meta(run_dir)
    problem = dict(_read_json(run_dir / "problem.json"))
    graph = load_graph(run_dir)
    params = series_rlc_params_from_graph(graph)
    if params:
        problem.update(params)
        problem.setdefault("kind", "series_rlc")
        problem.setdefault("analysis", "tran")
        problem.setdefault("allow_template_fallback", True)
        problem.pop("cir", None)
    derived = derive(problem)
    (run_dir / "circuit_derive.json").write_text(json.dumps(derived, indent=2), encoding="utf-8")
    if params:
        (run_dir / "problem.json").write_text(json.dumps(problem, indent=2), encoding="utf-8")
    params = series_rlc_params_from_graph(graph) or problem
    if str(problem.get("kind") or "") == "series_rlc" or params.get("r_ohm") is not None:
        from electrical_engineer.engines.rlc_transient import series_rlc_step

        rlc = series_rlc_step(
            float(params.get("r_ohm") or 10),
            float(params.get("l_h") or 0.01),
            float(params.get("c_f") or 100e-6),
            float(params.get("v_step") or params.get("vin") or 10),
        )
        (run_dir / "rlc_transient.json").write_text(json.dumps(rlc, indent=2), encoding="utf-8")
        for name in ("evidentiary.json", "summary.json"):
            path = run_dir / name
            if not path.is_file():
                continue
            evid = _read_json(path)
            if not evid.get("unchecked"):
                evid["value"] = float(derived.get("value") if derived.get("value") is not None else rlc["Vc_peak_V"])
                path.write_text(json.dumps(evid, indent=2), encoding="utf-8")
    # The derivation now belongs to this graph: move the baseline before judging
    # freshness, or every row is stamped "Out of date" against the old baseline.
    meta = lab_meta.load_lab_meta(run_dir)
    meta["agent_baseline_graph"] = graph
    meta["agent_baseline_rev"] = int(meta.get("revision") or 1)
    lab_meta.save_lab_meta(run_dir, meta)
    verify = refresh_circuit_lab_verify(run_dir, problem, derived=derived, graph=graph)
    meta = lab_meta.load_lab_meta(run_dir)
    verify = apply_verify_semantics(verify, meta, graph) or verify
    (run_dir / "lab_verify.json").write_text(json.dumps(verify, indent=2), encoding="utf-8")
    meta["lab_verify"] = {
        "mismatch": verify.get("mismatch"),
        "derived": verify.get("derived"),
        "simulated": verify.get("simulated"),
    }
    lab_meta.save_lab_meta(run_dir, meta)
    from electrical_engineer.circuit.run_session import append_lab_op

    # After the save, so the op is appended to the updated meta rather than overwritten.
    append_lab_op(
        run_dir,
        author="agent",
        op="re_derive",
        detail={"engine": derived.get("engine"), "value": derived.get("value")},
        electrical=False,
    )
    return verify


def restore_agent_circuit_lab(run_dir: Path) -> dict[str, Any]:
    """Restore the original agent seed graph+derivation as a new lab revision and re-verify."""
    from electrical_engineer.circuit.run_session import apply_graph, load_graph
    from electrical_engineer.collab import lab_meta
    from electrical_engineer.collab.workflow import refresh_circuit_lab_verify

    meta = lab_meta.load_lab_meta(run_dir)
    graph = meta.get("agent_seed_graph") or meta.get("agent_baseline_graph")
    if not isinstance(graph, dict) or not graph.get("nodes"):
        raise ValueError("no agent seed graph to restore")
    seed_derive = meta.get("agent_seed_derive")
    problem0 = _read_json(run_dir / "problem.json")
    if not isinstance(seed_derive, dict):
        params_seed = series_rlc_params_from_graph(graph) or {}
        if str(problem0.get("kind") or "") == "series_rlc" and params_seed:
            from electrical_engineer.engines.circuit_derive import derive

            seed_derive = derive(
                {
                    **problem0,
                    **params_seed,
                    "allow_template_fallback": True,
                }
            )
    if isinstance(seed_derive, dict):
        (run_dir / "circuit_derive.json").write_text(json.dumps(seed_derive, indent=2), encoding="utf-8")
        params = series_rlc_params_from_graph(graph) or {}
        if str(_read_json(run_dir / "problem.json").get("kind") or "") == "series_rlc" and params:
            from electrical_engineer.engines.rlc_transient import series_rlc_step

            rlc = series_rlc_step(
                float(params.get("r_ohm") or 10),
                float(params.get("l_h") or 0.01),
                float(params.get("c_f") or 100e-6),
                float(params.get("v_step") or params.get("vin") or 10),
            )
            (run_dir / "rlc_transient.json").write_text(json.dumps(rlc, indent=2), encoding="utf-8")
            for name in ("evidentiary.json", "summary.json"):
                path = run_dir / name
                if path.is_file():
                    evid = _read_json(path)
                    evid["value"] = float(seed_derive.get("value") if seed_derive.get("value") is not None else rlc["Vc_peak_V"])
                    path.write_text(json.dumps(evid, indent=2), encoding="utf-8")
    apply_graph(
        run_dir,
        graph,
        author="human",
        op="restore",
        target="circuit",
        detail={"source": "agent_seed", "seed_rev": meta.get("agent_seed_rev")},
    )
    graph_live = load_graph(run_dir)
    params_restore = series_rlc_params_from_graph(graph_live) or {}
    if params_restore:
        problem0 = {**problem0, **params_restore}
        problem0.setdefault("prompt", "Series RLC step")
        (run_dir / "problem.json").write_text(json.dumps(problem0, indent=2), encoding="utf-8")
    meta = lab_meta.load_lab_meta(run_dir)
    meta["agent_baseline_graph"] = load_graph(run_dir)
    meta["agent_baseline_rev"] = int(meta.get("revision") or 1)
    lab_meta.save_lab_meta(run_dir, meta)
    problem = _read_json(run_dir / "problem.json")
    derived = _read_json(run_dir / "circuit_derive.json")
    graph_live = load_graph(run_dir)
    params = series_rlc_params_from_graph(graph_live)
    if params:
        problem = {**problem, **params}
    verify = refresh_circuit_lab_verify(run_dir, problem, derived=derived or None, graph=graph_live)
    verify = apply_verify_semantics(verify, meta, graph_live) or verify
    verify["graph_revision"] = int(meta.get("revision") or 0)
    verify["computed_at_revision"] = verify["graph_revision"]
    (run_dir / "lab_verify.json").write_text(json.dumps(verify, indent=2), encoding="utf-8")
    meta["lab_verify"] = {
        "mismatch": verify.get("mismatch"),
        "derived": verify.get("derived"),
        "simulated": verify.get("simulated"),
    }
    lab_meta.save_lab_meta(run_dir, meta)
    return verify


def reverify_circuit_lab(run_dir: Path) -> dict[str, Any]:
    """Re-simulate current graph; keep agent derivation snapshot."""
    from electrical_engineer.circuit.run_session import load_graph
    from electrical_engineer.collab import lab_meta
    from electrical_engineer.collab.workflow import refresh_circuit_lab_verify

    meta = lab_meta.load_lab_meta(run_dir)
    problem = _read_json(run_dir / "problem.json")
    if not problem:
        raise ValueError("missing problem.json")
    derived = _read_json(run_dir / "circuit_derive.json")
    if not derived:
        old = _read_json(run_dir / "lab_verify.json")
        if isinstance(old.get("derive"), dict):
            derived = old["derive"]
    graph = load_graph(run_dir)
    params = series_rlc_params_from_graph(graph)
    if params:
        problem = {**problem, **params}
    verify = refresh_circuit_lab_verify(run_dir, problem, derived=derived or None, graph=graph)
    verify = apply_verify_semantics(verify, meta, graph) or verify
    verify["graph_revision"] = int(meta.get("revision") or verify.get("graph_revision") or 0)
    verify["computed_at_revision"] = verify["graph_revision"]
    (run_dir / "lab_verify.json").write_text(json.dumps(verify, indent=2), encoding="utf-8")
    meta = lab_meta.load_lab_meta(run_dir)
    meta["lab_verify"] = {
        "mismatch": verify.get("mismatch"),
        "derived": verify.get("derived"),
        "simulated": verify.get("simulated"),
    }
    lab_meta.save_lab_meta(run_dir, meta)
    return verify


def accept_simulated_lab(run_dir: Path) -> dict[str, Any]:
    """Human accepts the lab simulation as the trusted headline value."""
    from electrical_engineer.circuit.run_session import append_lab_op
    from electrical_engineer.collab import lab_meta
    from electrical_engineer.collab.verify_policy import status_label

    verify = _read_json(run_dir / "lab_verify.json")
    if not verify:
        raise ValueError("missing lab_verify.json")
    simulated = verify.get("simulated")
    if simulated is None:
        for row in verify.get("metrics") or []:
            if isinstance(row, dict) and row.get("simulated") is not None:
                simulated = row["simulated"]
                break
    if simulated is None:
        raise ValueError("no simulated value to accept")

    old_value = None
    for name in ("evidentiary.json", "summary.json"):
        path = run_dir / name
        if not path.is_file():
            continue
        evid = _read_json(path)
        old_value = evid.get("value")
        evid["value"] = simulated
        if isinstance(evid.get("values"), dict):
            evid["values"]["value"] = simulated
        path.write_text(json.dumps(evid, indent=2), encoding="utf-8")

    derived_was = verify.get("derived")
    verify["derived"] = simulated
    verify["mismatch"] = False
    verify["needs_review"] = False
    verify["ok"] = True
    verify["status"] = "agrees"
    verify["rel_err_pct"] = 0.0
    verify["status_label"] = status_label(agrees=True, rel_err_pct=0.0)
    verify.pop("disagreement_banner", None)
    for row in verify.get("metrics") or []:
        if not isinstance(row, dict):
            continue
        row["rel_err_pct"] = 0.0
        row["status"] = "agrees"
        row["status_label"] = verify["status_label"]
    (run_dir / "lab_verify.json").write_text(json.dumps(verify, indent=2), encoding="utf-8")

    meta = lab_meta.load_lab_meta(run_dir)
    meta["lab_verify"] = {
        "mismatch": False,
        "derived": simulated,
        "simulated": simulated,
    }
    append_lab_op(
        run_dir,
        author="human",
        op="accept_simulated",
        target="value",
        before=old_value if old_value is not None else derived_was,
        after=simulated,
        electrical=False,
    )
    lab_meta.save_lab_meta(run_dir, meta)
    return verify