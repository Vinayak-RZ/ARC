"""Run trap detectors and split outcome vs process scores."""

from __future__ import annotations

from typing import Any

from electrical_engineer.traps.detectors import DETECTORS, infer_trap_ids
from electrical_engineer.traps.index import automated_trap_ids
from electrical_engineer.traps.schema import GradeScores, SolutionTrace, TrapCheck


def _outcome_from_trace(trace: SolutionTrace) -> bool:
    """Outcome grader: final numeric keys within tolerance when present."""
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
    ids = trap_ids or infer_trap_ids(trace)
    checks: list[TrapCheck] = []
    for tid in ids:
        fn = DETECTORS.get(tid)
        if fn is None:
            continue
        result = fn(trace)
        if result is not None:
            checks.append(result)
    return checks


def grade_trace(trace: SolutionTrace, *, trap_ids: tuple[str, ...] | None = None) -> GradeScores:
    checks = run_detectors(trace, trap_ids)
    process_pass = all(c.passed for c in checks) if checks else True
    outcome_pass = _outcome_from_trace(trace)
    process_score = 1.0 if process_pass else 0.0
    if not checks:
        process_score = 1.0
    else:
        process_score = sum(1.0 for c in checks if c.passed) / len(checks)
    outcome_score = 1.0 if outcome_pass else 0.0
    return GradeScores(
        outcome_pass=outcome_pass,
        process_pass=process_pass,
        outcome_score=outcome_score,
        process_score=process_score,
        checks=tuple(checks),
    )


def grade_with_verifier(trace: SolutionTrace, **kwargs: Any) -> GradeScores:
    return grade_trace(trace, **kwargs)


def grade_outcome_only(trace: SolutionTrace) -> GradeScores:
    outcome = _outcome_from_trace(trace)
    return GradeScores(
        outcome_pass=outcome,
        process_pass=True,
        outcome_score=1.0 if outcome else 0.0,
        process_score=1.0,
        checks=(),
    )


def verify_trace_payload(trace: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
    parsed = SolutionTrace.from_mapping(trace)
    grades = grade_with_verifier(parsed, **kwargs)
    return {
        "tool": "trap-verify",
        "automated_traps": automated_trap_ids(),
        "trap_ids": list(parsed.trap_ids or infer_trap_ids(parsed)),
        "outcome_pass": grades.outcome_pass,
        "process_pass": grades.process_pass,
        "outcome_score": grades.outcome_score,
        "process_score": round(grades.process_score, 4),
        "ok": grades.outcome_pass and grades.process_pass,
        "checks": [
            {
                "trap_id": c.trap_id,
                "passed": c.passed,
                "offending_step": c.offending_step,
                "message": c.message,
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
        base = SolutionTrace.from_mapping(host_trace)
    else:
        base = SolutionTrace(topic=str(problem.get("topic") or problem.get("kind") or ""))
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
    return SolutionTrace(trap_ids=base.trap_ids, steps=tuple(step_rows), final=final, topic=base.topic)
