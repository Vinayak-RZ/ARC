"""Property-style invariants reused by tests and the circuit benchmark."""

from __future__ import annotations

from electrical_engineer.engines.circuit_derive import derive


def _divider_cir(vin: float, r1: float, r2: float) -> str:
    return f"* div\nV1 1 0 DC {vin}\nR1 1 2 {r1}\nR2 2 0 {r2}\n.end\n"


def _close(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol


def superposition_voltage_divider() -> None:
    base = derive({"cir": _divider_cir(10, 1000, 1000), "analysis": "dc", "probe": "v(2)"})
    a = derive({"cir": _divider_cir(4, 1000, 1000), "analysis": "dc", "probe": "v(2)"})
    b = derive({"cir": _divider_cir(6, 1000, 1000), "analysis": "dc", "probe": "v(2)"})
    assert _close(float(a["value"]) + float(b["value"]), float(base["value"]))


def reciprocity_symmetric_divider() -> None:
    forward = derive({"cir": _divider_cir(12, 2000, 1000), "analysis": "dc", "probe": "v(2)"})
    swap = derive({"cir": _divider_cir(12, 1000, 2000), "analysis": "dc", "probe": "v(2)"})
    assert _close(float(forward["value"]) + float(swap["value"]), 12.0)


def power_balance_dc_divider() -> None:
    vin, r1, r2 = 12.0, 1500.0, 500.0
    out = derive({"cir": _divider_cir(vin, r1, r2), "analysis": "dc", "probe": "v(2)"})
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
