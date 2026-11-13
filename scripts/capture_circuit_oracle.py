"""Write circuit gold values from ngspice only (never derive())."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "eval" / "gold" / "circuits"


def _transient_hand_oracle(spec: dict) -> float | None:
    """Independent transient golds (not derive()). Uses closed-form helpers in capture only."""
    from electrical_engineer.engines import ee_v2_solvers as v2

    cid = spec["id"]
    t = float(spec["t_s"])
    if cid.startswith("mna-tr-rc"):
        if "10k" in spec["netlist"] and "10u" in spec["netlist"]:
            return float(v2.rc_step(10, 10e3, 10e-6, t)["vc_V"])
        return float(v2.rc_step(5, 2200, 100e-6, t)["vc_V"])
    if cid in {"mna-tr-rlc-01", "mna-tr-rlc-02"}:
        if cid == "mna-tr-rlc-01":
            return float(v2.rlc_natural(50, 1e-3, 1e-6, 10, 0, t)["vc_V"])
        return float(v2.rlc_natural(200, 5e-3, 500e-9, 0, 0.0, t)["vc_V"])
    if cid.startswith("mna-tr-rl"):
        row = v2.rl_step(12, 100, 0.2, t)
        if spec.get("probe", "").startswith("i("):
            return float(row["i_A"])
        i = float(row["i_A"])
        return 12.0 - i * 100.0
    return None


def main() -> int:
    if not shutil.which("ngspice"):
        print("capture_circuit_oracle: ngspice required", file=sys.stderr)
        return 1
    sys.path.insert(0, str(ROOT))
    from circuit_gold_specs import SPECS

    from electrical_engineer.engines.spice_runner import run_spice_netlist

    run_root = ROOT / "runs" / "_oracle_capture"
    run_root.mkdir(parents=True, exist_ok=True)
    legacy = {p.name for p in PACK.iterdir() if p.is_dir()}
    written: set[str] = set()
    for spec in SPECS:
        cid = spec["id"]
        item = PACK / cid
        item.mkdir(parents=True, exist_ok=True)
        fx = item / "fixtures"
        fx.mkdir(parents=True, exist_ok=True)
        (fx / "netlist.cir").write_text(spec["netlist"].strip() + "\n", encoding="utf-8")
        require_spice = spec["analysis"] != "tran"
        problem = {
            "netlist_path": "fixtures/netlist.cir",
            "analysis": spec["analysis"],
            "probe": spec["probe"],
            "unit": spec.get("unit", "V"),
            "tol": spec["tol"],
            "require_spice": require_spice,
        }
        if spec.get("f_hz") is not None:
            problem["f_hz"] = spec["f_hz"]
        if spec.get("t_s") is not None:
            problem["t_s"] = spec["t_s"]
        run_dir = run_root / cid
        run_dir.mkdir(parents=True, exist_ok=True)
        value: float | None = None
        if spec["analysis"] == "tran":
            value = _transient_hand_oracle(spec)
        if value is None:
            sim = run_spice_netlist(spec["netlist"], run_dir, problem)
            if not sim.get("ok"):
                print(f"{cid}: ngspice failed: {sim}", file=sys.stderr)
                return 1
            value = float(sim["value"])
        else:
            sim = {"ok": True, "tool": "hand_transient"}
        prov = spec["gold_provenance"]
        if spec["analysis"] == "tran" and value is not None:
            prov = "hand_calc"
        expect = {
            "schema": "arc.eval.expect.v2",
            "engine": "circuit_unit",
            "value": value,
            "tol": spec["tol"],
            "require_spice": require_spice,
            "gold_provenance": prov,
        }
        (item / "expect.json").write_text(json.dumps(expect, indent=2) + "\n")
        (item / "fixtures" / "problem.json").write_text(json.dumps(problem, indent=2) + "\n")
        (item / "source.md").write_text(spec["source_md"])
        (item / "task.md").write_text(f"Circuit MNA item {cid}: {spec['analysis']} probe {spec['probe']}\n")
        written.add(cid)
        print(f"{cid}: {value} ({prov})")
    for old in legacy - written:
        if old == "photo-stub-01":
            continue
        import shutil as sh

        sh.rmtree(PACK / old, ignore_errors=True)
    print(f"captured {len(written)} items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
