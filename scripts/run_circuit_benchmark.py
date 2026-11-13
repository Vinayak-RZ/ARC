#!/usr/bin/env python3
"""CIRCUIT subset runner: engine golds, property tests, multimodal smoke."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "frontier" / "circuit_benchmark.json"
CONTRACT = ROOT / "artifacts" / "frontier" / "b4_contract.json"


def _engine_items() -> list[Path]:
    pack = ROOT / "eval" / "gold" / "circuits"
    items: list[Path] = []
    for item in sorted(pack.iterdir()):
        if not item.is_dir() or item.name.startswith("."):
            continue
        expect_path = item / "expect.json"
        if not expect_path.is_file():
            continue
        expect = json.loads(expect_path.read_text())
        if expect.get("engine") in {"circuit_unit", "circuit_verify"}:
            items.append(item)
    return items


def _run_engine_golds() -> dict[str, object]:
    from electrical_engineer.eval_runner.circuit_score import run_circuit_item

    rows = []
    spice_agree = 0
    spice_ran = 0
    for item in _engine_items():
        expect = json.loads((item / "expect.json").read_text())
        row = run_circuit_item(item, expect, run_root=ROOT / "runs" / "_circuit_bench")
        sim = row.get("summary", {}).get("simulated")
        mismatch = row.get("summary", {}).get("mismatch")
        if sim is not None:
            spice_ran += 1
            if not mismatch:
                spice_agree += 1
        rows.append(
            {
                "id": item.name,
                "ok": bool(row.get("ok")),
                "mismatch": mismatch,
                "spice_skipped": row.get("summary", {}).get("spice_skipped"),
            }
        )
    passed = sum(1 for r in rows if r["ok"])
    total = len(rows)
    return {
        "engine_items": rows,
        "engine_passed": passed,
        "engine_total": total,
        "circuit_unit_pass_rate": (passed / total) if total else 0.0,
        "derive_spice_agreement_rate": (spice_agree / spice_ran) if spice_ran else 0.0,
        "spice_items_ran": spice_ran,
    }


def _property_tests() -> dict[str, object]:
    from electrical_engineer.engines.circuit_properties import run_property_suite

    return run_property_suite()


def _multimodal_smoke() -> dict[str, object]:
    from electrical_engineer.engines.circuit_multimodal import (
        confirm_and_write,
        propose_netlist_from_component,
    )
    from electrical_engineer.engines.circuit_verify import verify_after_derive
    from electrical_engineer.engines.spice_runner import simulator_status

    ok = True
    trace: list[dict[str, object]] = []
    run_dir = ROOT / "runs" / "_mm_smoke"
    for comp in ("schematic.divider", "schematic.rlc_series"):
        prop = propose_netlist_from_component(comp)
        step = {"component": comp, "proposed": bool(prop.get("ok"))}
        if not prop.get("ok"):
            ok = False
            trace.append(step)
            continue
        confirm_and_write(run_dir / comp.replace(".", "_"), cir=str(prop["cir"]), graph=prop.get("graph"))
        step["confirm"] = True
        if comp == "schematic.divider":
            problem = {
                "cir": "* mm\nV1 1 0 DC 10\nR1 1 2 1k\nR2 2 0 1k\n.end\n",
                "analysis": "dc",
                "probe": "v(2)",
                "value": 5.0,
                "tol": 1e-3,
            }
            v = verify_after_derive(problem, run_dir=run_dir / comp.replace(".", "_"))
            step["derive_ok"] = bool(v.get("gold_ok"))
            ok = ok and step["derive_ok"]
        else:
            cir = str(prop.get("cir") or "").upper()
            step["netlist_ok"] = "R1" in cir and "L1" in cir and "C1" in cir
            ok = ok and step["netlist_ok"]
        step["simulator"] = simulator_status()
        trace.append(step)
    return {"multimodal_path_smoke": ok, "steps": trace}


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    report: dict[str, object] = {"subset": "circuits", "version": "0.2"}
    report.update(_run_engine_golds())
    report["properties"] = _property_tests()
    report.update(_multimodal_smoke())
    contract = {
        "circuit_unit_pass_rate": report["circuit_unit_pass_rate"],
        "derive_spice_agreement_rate": report.get("derive_spice_agreement_rate", 0.0),
        "multimodal_path_smoke": report["multimodal_path_smoke"],
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    CONTRACT.write_text(json.dumps(contract, indent=2) + "\n")
    print(json.dumps(contract))
    rate = float(report["circuit_unit_pass_rate"])
    if rate < 0.55:
        print(f"WARN: circuit_unit_pass_rate {rate:.3f} below target 0.55", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
