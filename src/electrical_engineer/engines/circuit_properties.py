"""Property-style invariants reused by tests and the circuit benchmark."""

from __future__ import annotations

from electrical_engineer.engines.circuit_derive import derive


def _close(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol


def superposition_voltage_divider() -> None:
    base = derive({"kind": "dc_divider", "vin": 10, "r1": 1000, "r2": 1000})
    a = derive({"kind": "dc_divider", "vin": 4, "r1": 1000, "r2": 1000})
    b = derive({"kind": "dc_divider", "vin": 6, "r1": 1000, "r2": 1000})
    assert _close(float(a["value"]) + float(b["value"]), float(base["value"]))


def reciprocity_symmetric_divider() -> None:
    forward = derive({"kind": "dc_divider", "vin": 12, "r1": 2000, "r2": 1000})
    swap = derive({"kind": "dc_divider", "vin": 12, "r1": 1000, "r2": 2000})
    assert _close(float(forward["value"]) + float(swap["value"]), 12.0)


def power_balance_dc_divider() -> None:
    vin, r1, r2 = 12.0, 1500.0, 500.0
    out = derive({"kind": "dc_divider", "vin": vin, "r1": r1, "r2": r2})
    vout = float(out["value"])
    i = vin / (r1 + r2)
    p_in = vin * i
    p_r1 = (vin - vout) ** 2 / r1
    p_r2 = vout**2 / r2
    assert _close(p_in, p_r1 + p_r2, tol=1e-9)


def run_property_suite() -> dict[str, object]:
    checks = [
        ("superposition", superposition_voltage_divider),
        ("reciprocity", reciprocity_symmetric_divider),
        ("power_balance", power_balance_dc_divider),
    ]
    rows: list[dict[str, object]] = []
    for name, fn in checks:
        try:
            fn()
            rows.append({"name": name, "ok": True})
        except AssertionError as exc:
            rows.append({"name": name, "ok": False, "error": str(exc)})
    passed = sum(1 for r in rows if r["ok"])
    return {"total": len(rows), "passed": passed, "items": rows, "ok": passed == len(rows)}
