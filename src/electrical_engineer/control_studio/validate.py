"""Diagram validation and Arc trap checks."""

from __future__ import annotations

from typing import Any

from electrical_engineer.control_studio.schema import parse_diagram


def validate(diagram: dict[str, Any]) -> dict[str, Any]:
    d = parse_diagram(diagram)
    issues: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    for b in d["blocks"]:
        bid = b["id"]
        btype = b["type"]
        if btype in ("step", "ramp", "sine"):
            if not any(w["from"].startswith(f"{bid}:") for w in d["wires"]):
                issues.append({"code": "unconnected_source", "block_id": bid, "message": "source has no output wire"})
        elif btype == "scope":
            if not any(w["to"].startswith(f"{bid}:") for w in d["wires"]):
                issues.append({"code": "unconnected_scope", "block_id": bid, "message": "scope has no input wire"})
        elif btype == "sum":
            ins = [w for w in d["wires"] if w["to"].startswith(f"{bid}:")]
            if len(ins) < 2:
                issues.append({"code": "sum_inputs", "block_id": bid, "message": "sum needs reference and feedback wires"})
            signs = str((b.get("params") or {}).get("signs") or "+-")
            if signs not in ("+-", "++", "-+", "trap_plus_plus"):
                warnings.append({"code": "sum_signs", "block_id": bid, "message": "unusual sum signs"})
            if signs == "++":
                issues.append(
                    {
                        "code": "arc_trap_positive_feedback",
                        "block_id": bid,
                        "message": "Arc trap: both sum inputs positive (likely unstable positive feedback)",
                    }
                )
        elif btype == "gain":
            p = b.get("params") or {}
            unit = str(p.get("unit") or "")
            if unit and unit not in ("1", "V/V", "A/V", "rad/(N*m)", "unitless"):
                warnings.append({"code": "gain_units", "block_id": bid, "message": f"gain unit {unit} not verified"})
            if float(p.get("k") or p.get("gain") or 1.0) < 0:
                warnings.append({"code": "negative_gain", "block_id": bid, "message": "negative gain (check sensor polarity)"})

    has_dynamic = any(
        b["type"] in ("transfer_function", "plant_first_order", "plant_dc_motor", "integrator", "pid", "delay", "state_space")
        for b in d["blocks"]
    )
    if has_dynamic and _has_algebraic_loop(d):
        issues.append({"code": "algebraic_loop", "block_id": "", "message": "algebraic loop detected (add delay or break path)"})

    scopes = [b for b in d["blocks"] if b["type"] == "scope"]
    sources = [b for b in d["blocks"] if b["type"] in ("step", "ramp", "sine")]
    if sources and not scopes:
        issues.append({"code": "no_scope", "block_id": "", "message": "diagram has sources but no scope"})

    ok = not issues
    return {"ok": ok, "issues": issues, "warnings": warnings}


def _has_algebraic_loop(d: dict[str, Any]) -> bool:
    """Cycle detection; delay/saturation edges do not break loops (conservative)."""
    adj: dict[str, list[str]] = {b["id"]: [] for b in d["blocks"]}
    delay_blocks = {b["id"] for b in d["blocks"] if b["type"] == "delay"}
    by_id = {b["id"]: b for b in d["blocks"]}
    for w in d["wires"]:
        fb = w["from"].split(":", 1)[0]
        tb, tp = w["to"].split(":", 1)
        if fb in delay_blocks or tb in delay_blocks:
            continue
        if by_id.get(tb, {}).get("type") == "sum" and tp in ("feedback", "in2"):
            continue
        adj.setdefault(fb, []).append(tb)

    visited: set[str] = set()
    stack: set[str] = set()

    def dfs(n: str) -> bool:
        visited.add(n)
        stack.add(n)
        for m in adj.get(n, []):
            if m not in visited:
                if dfs(m):
                    return True
            elif m in stack:
                return True
        stack.remove(n)
        return False

    for node in list(adj):
        if node not in visited and dfs(node):
            return True
    return False
