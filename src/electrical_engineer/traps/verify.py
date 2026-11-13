"""Run trap detectors and split outcome vs process scores."""

from __future__ import annotations

from typing import Any

from electrical_engineer.traps.detectors import DETECTORS, infer_trap_ids
from electrical_engineer.traps.index import automated_trap_ids
from electrical_engineer.traps.schema import GradeScores, ProcessStatus, SolutionTrace, TrapCheck


def trace_has_substance(trace: SolutionTrace) -> bool:
    if trace.steps:
        return True
    if trace.givens:
        return True
    final = trace.final or {}
    skip = {"text", "expected", "golden", "outcome_tolerance", "outcome_pass", "givens"}
    return any(k not in skip for k in final)


def _outcome_from_trace(trace: SolutionTrace) -> bool:
    final = trace.final
    if not final:
        return True
    tol = float(final.get("outcome_tolerance") or 0.05)
    targets = final.get("expected") or final.get("golden") or {}
    if not isinstance(targets, dict) or not targets:
        if final.get("outcome_pass") is not None:
            return bool(final.get("outcome_pass"))
        return True
    for key, target in targets.items():
        got = final.get(key)
        if got is None:
            continue
        if isinstance(target, (int, float)) and isinstance(got, (int, float)):
            if abs(float(got) - float(target)) > tol * max(1.0, abs(float(target))):
                return False
        elif got != target:
            return False
    return True


def run_detectors(trace: SolutionTrace, trap_ids: tuple[str, ...] | None = None) -> list[TrapCheck]:
    if not trace_has_substance(trace):
        return []
    ids = trap_ids or infer_trap_ids(trace)
    checks: list[TrapCheck] = []
    for tid in ids:
        fn = DETECTORS.get(tid)
        if fn is None:
            continue
        checks.append(fn(trace))
    return checks


def _process_status(checks: list[TrapCheck], *, substantive: bool) -> ProcessStatus:
    if not substantive or not checks:
        return "unchecked"
    if any(c.status == "fail" for c in checks):
        return "fail"
    if all(c.status == "pass" for c in checks):
        return "pass"
    if all(c.status == "unchecked" for c in checks):
        return "unchecked"
    if any(c.status == "pass" for c in checks) and not any(c.status == "fail" for c in checks):
        return "unchecked"
    return "unchecked"


def grade_trace(trace: SolutionTrace, *, trap_ids: tuple[str, ...] | None = None) -> GradeScores:
    substantive = trace_has_substance(trace)
    checks = run_detectors(trace, trap_ids)
    status = _process_status(checks, substantive=substantive)
    process_pass = status == "pass"
    outcome_pass = _outcome_from_trace(trace)
    if not checks:
        process_score = 0.0
    else:
        process_score = sum(1.0 for c in checks if c.status == "pass") / len(checks)
    advisories = tuple(c.advisory for c in checks if c.advisory)
    return GradeScores(
        outcome_pass=outcome_pass,
        process_pass=process_pass,
        process_status=status,
        outcome_score=1.0 if outcome_pass else 0.0,
        process_score=round(process_score, 4),
        checks=tuple(checks),
        advisories=advisories,
    )


def grade_with_verifier(trace: SolutionTrace, **kwargs: Any) -> GradeScores:
    return grade_trace(trace, **kwargs)


def grade_outcome_only(trace: SolutionTrace) -> GradeScores:
    outcome = _outcome_from_trace(trace)
    return GradeScores(
        outcome_pass=outcome,
        process_pass=True,
        process_status="pass",
        outcome_score=1.0 if outcome else 0.0,
        process_score=1.0,
        checks=(),
    )


def verify_trace_payload(trace: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
    parsed = SolutionTrace.from_mapping(trace)
    grades = grade_with_verifier(parsed, **kwargs)
    ok = grades.outcome_pass and grades.process_status != "fail"
    return {
        "tool": "trap-verify",
        "automated_traps": automated_trap_ids(),
        "trap_ids": list(parsed.trap_ids or infer_trap_ids(parsed)),
        "outcome_pass": grades.outcome_pass,
        "process_pass": grades.process_pass,
        "process_status": grades.process_status,
        "outcome_score": grades.outcome_score,
        "process_score": grades.process_score,
        "ok": ok,
        "advisories": list(grades.advisories),
        "checks": [
            {
                "trap_id": c.trap_id,
                "status": c.status,
                "passed": c.passed,
                "offending_step": c.offending_step,
                "message": c.message,
                "advisory": c.advisory,
            }
            for c in grades.checks
        ],
    }


def trace_from_inputs(inputs: dict[str, Any], spec: dict[str, Any]) -> SolutionTrace:
    from electrical_engineer.nodes.sim import _problem
    from electrical_engineer.traps.schema import TraceStep

    problem = _problem(spec)
    host_trace = problem.get("solution_trace")
    if isinstance(host_trace, dict):
        base = SolutionTrace.from_mapping({**host_trace, "givens": {**(problem.get("givens") or {}), **(host_trace.get("givens") or {})}})
    else:
        base = SolutionTrace(
            topic=str(problem.get("topic") or problem.get("kind") or ""),
            givens=dict(problem.get("givens") or {}),
        )
    step_rows: list[TraceStep] = list(base.steps)
    values: dict[str, Any] = {}
    texts: list[str] = []
    for v in inputs.values():
        if not isinstance(v, dict):
            continue
        tool = str(v.get("tool") or v.get("activity") or "")
        if v.get("text"):
            texts.append(str(v["text"]))
        if v.get("value") is not None:
            values["value"] = v["value"]
        for key in (
            "delta_cr_deg",
            "t_to_dcr_s",
            "cct_s",
            "delta_f1_hz",
            "delta_p12_mw",
            "P2_mw",
            "lam",
            "lambda",
            "recomputed",
            "solver_used",
        ):
            if v.get(key) is not None:
                values[key] = v[key]
        if tool:
            step_rows.append(
                TraceStep(
                    id=tool,
                    text=str(v.get("text") or tool),
                    values={k: val for k, val in v.items() if k not in ("text",)},
                )
            )
    final = dict(base.final)
    final.update(values)
    if texts and "text" not in final:
        final["text"] = "\n".join(texts[:3])
    return SolutionTrace(
        trap_ids=base.trap_ids,
        givens=base.givens,
        steps=tuple(step_rows),
        final=final,
        topic=base.topic,
    )
