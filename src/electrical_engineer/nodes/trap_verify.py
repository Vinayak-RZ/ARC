"""trap-verify activity: deterministic process PRM before final label."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from electrical_engineer.nodes.registry import register
from electrical_engineer.traps.verify import trace_from_inputs, verify_trace_payload


@register("trap-verify")
def trap_verify(spec: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    trace = trace_from_inputs(inputs, spec)
    payload = verify_trace_payload(
        {
            "trap_ids": list(trace.trap_ids),
            "steps": [{"id": s.id, "text": s.text, **s.values} for s in trace.steps],
            "final": trace.final,
            "topic": trace.topic,
        }
    )
    run_dir_s = spec.get("run_dir")
    if run_dir_s:
        rd = Path(run_dir_s)
        rd.mkdir(parents=True, exist_ok=True)
        evidence = rd / "evidence" / "trap_prm.json"
        evidence.parent.mkdir(parents=True, exist_ok=True)
        import json

        evidence.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        payload["paths"] = [str(evidence)]
    if not payload.get("ok"):
        from electrical_engineer.unchecked import UNCHECKED

        payload["unchecked"] = True
        payload["token"] = UNCHECKED
    else:
        payload["unchecked"] = False
    payload["inputs"] = inputs
    return payload
