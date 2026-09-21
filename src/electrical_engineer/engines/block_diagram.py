"""Compose SISO transfer functions from UG block-diagram specs (OSS, no Simulink)."""

from __future__ import annotations

import re
from typing import Any


def _parse_tf(block: dict[str, Any]):
    import control

    if "num" in block and "den" in block:
        return control.tf(block["num"], block["den"])
    raw = str(block.get("tf") or block.get("transfer_function") or "1").strip()
    if raw in ("1", "1.0"):
        return control.tf([1.0], [1.0])
    m = re.match(
        r"^([0-9.+-]+)\s*/\s*\(\s*s\s*([+-])\s*([0-9.]+)\s*\)$",
        raw.replace(" ", ""),
    )
    if m:
        k = float(m.group(1))
        tau = float(m.group(3)) if m.group(2) == "+" else -float(m.group(3))
        return control.tf([k], [1.0, tau])
    if "/" in raw:
        num_s, den_s = raw.split("/", 1)
        num_s = num_s.strip().strip("()")
        den_s = den_s.strip().strip("()")
        try:
            num = [float(num_s)]
        except ValueError:
            raise ValueError(f"unsupported numerator {num_s}") from None
        if den_s in ("1", "1.0"):
            return control.tf(num, [1.0])
        raise ValueError(f"unsupported denominator {den_s}; use num/den arrays")
    try:
        return control.tf([float(raw)], [1.0])
    except ValueError:
        raise ValueError(f"unsupported tf {raw}") from None


def compose_plant(problem: dict[str, Any]):
    """Return (control.StateSpace or tf, summary dict)."""
    import control

    blocks = problem.get("blocks") or []
    if not blocks:
        raise ValueError("blocks[] required for control block diagram")
    by_id = {str(b.get("id") or f"b{i}"): b for i, b in enumerate(blocks)}

    if problem.get("unity_feedback"):
        uf = problem["unity_feedback"]
        if not isinstance(uf, dict):
            raise ValueError("unity_feedback must be an object")
        fwd_id = str(uf.get("forward") or blocks[0].get("id"))
        fb_id = str(uf.get("feedback") or "")
        g = _parse_tf(by_id[fwd_id])
        h = _parse_tf(by_id[fb_id]) if fb_id and fb_id in by_id else control.tf([1.0], [1.0])
        sys = control.feedback(g, h, sign=-1 if uf.get("negative", True) else 1)
        return sys, {"structure": "unity_feedback", "forward": fwd_id, "feedback": fb_id}

    structure = str(problem.get("structure") or "series").lower()
    systems = [_parse_tf(b) for b in blocks]
    if structure == "series":
        sys = control.series(*systems)
    elif structure == "parallel":
        sys = control.parallel(*systems)
    elif structure == "feedback":
        if len(systems) < 2:
            raise ValueError("feedback needs at least two blocks")
        sys = control.feedback(systems[0], systems[1])
    else:
        raise ValueError(f"unsupported structure {structure}")
    return sys, {"structure": structure, "block_count": len(systems)}


def plant_problem_dict(problem: dict[str, Any]) -> dict[str, Any]:
    sys, meta = compose_plant(problem)
    num, den = sys.num, sys.den
    num_list = [float(x) for x in num[0][0].tolist()]
    den_list = [float(x) for x in den[0][0].tolist()]
    return {
        "num": num_list,
        "den": den_list,
        "compose_meta": meta,
    }
