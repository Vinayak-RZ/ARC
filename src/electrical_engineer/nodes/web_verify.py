"""web-verify activity: external context + similar-problem search."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from electrical_engineer.nodes.registry import register
from electrical_engineer.nodes.sim import _problem
from electrical_engineer.unchecked import UNCHECKED
from electrical_engineer.web_verify.engine import run_web_verify


def _solver_outputs(inputs: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for v in inputs.values():
        if not isinstance(v, dict):
            continue
        if v.get("value") is not None:
            out.setdefault("primary", v.get("value"))
        for k, val in v.items():
            if k.endswith("_value") or k in ("recomputed", "I_phase_pu", "V_touch"):
                out[k] = val
    return out


def _primary_value(inputs: dict[str, Any]) -> Any:
    for v in inputs.values():
        if isinstance(v, dict) and v.get("value") is not None and not v.get("skipped"):
            return v.get("value")
    return None


@register("web-verify")
def web_verify(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    problem = _problem(spec)
    run_dir_s = spec.get("run_dir")
    run_dir = Path(run_dir_s) if run_dir_s else None
    result = run_web_verify(
        problem=problem,
        solver_outputs=_solver_outputs(inputs),
        summary_lines=list(problem.get("summary_lines") or []),
        run_dir=run_dir,
        arc_primary_result=_primary_value(inputs),
    )
    status = str(result.get("status") or "")
    needs_review = bool(result.get("needs_review"))
    offline_unverified = bool(result.get("offline_unverified"))
    ok = status in ("pass", "offline_pass") and not needs_review
    paths: list[str] = []
    if run_dir:
        for name in ("evidence/web_sources.json", "evidence/similar_problems.json", "evidence/answer_cited.md"):
            p = run_dir / name
            if p.is_file():
                paths.append(str(p))
    verified_values = {}
    for c in (result.get("web_sources") or {}).get("claims") or []:
        if c.get("claim_id"):
            verified_values[c["claim_id"]] = {
                "web_value": c.get("web_value"),
                "unit": c.get("unit"),
                "status": c.get("status"),
                "citation_ids": [s.get("citation_id") for s in c.get("sources") or []],
            }
    disagreement = None
    for c in (result.get("web_sources") or {}).get("claims") or []:
        if c.get("disagreement"):
            disagreement = c["disagreement"]
            break
    for m in (result.get("similar_problems") or {}).get("matches") or []:
        if m.get("agrees_after_adjustment") is False:
            disagreement = disagreement or {"similar_problem": m.get("url")}
    payload: dict[str, Any] = {
        "ok": ok,
        "tool": "web-verify",
        "web_verify_status": status,
        "needs_review": needs_review,
        "offline_unverified": offline_unverified,
        "provider": result.get("provider"),
        "paths": paths,
        "citations": result.get("citations") or [],
        "answer_markdown": result.get("answer_markdown"),
        "verified_values": verified_values,
        "similar_problems": result.get("similar_problems"),
        "web_sources": result.get("web_sources"),
        "disagreement_banner": disagreement,
        "value": _primary_value(inputs),
        "inputs": inputs,
    }
    if needs_review or status in ("pending_host", "unsupported", "mismatch_library"):
        payload["unchecked"] = True
        payload["token"] = UNCHECKED
        payload["ok"] = False
    elif offline_unverified:
        payload["unchecked"] = False
        payload["label_message"] = "checked (offline, unverified context)"
    elif ok:
        payload["unchecked"] = False
    else:
        payload["unchecked"] = True
        payload["token"] = UNCHECKED
    return payload
