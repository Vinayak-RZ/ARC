#!/usr/bin/env python3
"""Materialize circuit gold items under eval/gold/circuits/ from independent derive()."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "eval" / "gold" / "circuits"

CASES: list[dict] = [
    {"id": "dc-div-02", "kind": "dc_divider", "vin": 12, "r1": 3000, "r2": 1000, "tol": 1e-6, "source": "KVL divider, independent product rule"},
    {"id": "dc-div-03", "kind": "dc_divider", "vin": 5, "r1": 2000, "r2": 3000, "tol": 1e-6, "source": "Nodal at mid node, fraction r2/(r1+r2)"},
    {"id": "dc-div-04", "kind": "dc_divider", "vin": 24, "r1": 1200, "r2": 600, "tol": 1e-6, "source": "Sedra 1.3 style divider"},
    {"id": "dc-ser-01", "kind": "dc_series", "vin": 9, "resistors": [100, 200, 300], "tol": 1e-5, "source": "Series Ohm, I=V/sum(R)"},
    {"id": "dc-ser-02", "kind": "dc_series", "vin": 15, "resistors": [470, 330], "tol": 1e-5, "source": "Series current from KVL"},
    {"id": "dc-par-01", "kind": "dc_parallel", "vin": 10, "resistors": [1000, 2000], "tol": 1e-5, "source": "Parallel conductance sum"},
    {"id": "dc-par-02", "kind": "dc_parallel", "vin": 6, "resistors": [300, 600, 1200], "tol": 1e-5, "source": "Millman equivalent conductance"},
    {"id": "dc-cdiv-01", "kind": "dc_current_divider", "i_src": 0.01, "r1": 4000, "r2": 2000, "r_load": 1e9, "tol": 1e-5, "source": "Current divider I2=Is*R1/(R1+R2)"},
    {"id": "thev-r-01", "kind": "thevenin", "v_src": 12, "r1": 6000, "r2": 3000, "metric": "rth", "tol": 1e-4, "source": "Rth with port open, series parallel combo"},
    {"id": "thev-v-01", "kind": "thevenin", "v_src": 20, "r1": 5000, "r2": 5000, "metric": "vth", "tol": 1e-4, "source": "Vth open-circuit at port"},
    {"id": "ac-rc-01", "kind": "ac_rc_magnitude", "vin_rms": 10, "r": 1000, "c": 1e-6, "f_hz": 159.15, "tol": 1e-3, "source": "Capacitive divider magnitude at 1k||1u"},
    {"id": "ac-rc-02", "kind": "ac_rc_magnitude", "vin_rms": 5, "r": 470, "c": 2.2e-6, "f_hz": 100, "tol": 1e-3, "source": "XR impedance magnitude"},
    {"id": "ac-rl-01", "kind": "ac_rl_angle", "r": 1000, "l": 0.01, "f_hz": 50, "tol": 0.1, "source": "theta=atan(wL/R) degrees"},
    {"id": "ac-rl-02", "kind": "ac_rl_angle", "r": 220, "l": 0.05, "f_hz": 60, "tol": 0.1, "source": "Phasor angle line-frequency"},
    {"id": "tr-rc-02", "kind": "transient_rc", "v": 10, "r": 10000, "c": 10e-6, "t": 0.05, "tol": 1e-4, "source": "vc(t)=V(1-exp(-t/tau)), tau=RC"},
    {"id": "tr-rc-03", "kind": "transient_rc", "v": 5, "r": 2200, "c": 100e-6, "t": 0.2, "tol": 1e-4, "source": "First-order RC step response"},
    {"id": "tr-rl-01", "kind": "transient_rl", "v": 12, "r": 100, "l": 0.2, "t": 0.01, "tol": 1e-4, "source": "i(t)=(V/R)(1-exp(-Rt/L))"},
    {"id": "tr-rl-02", "kind": "transient_rl", "v": 24, "r": 47, "l": 0.05, "t": 0.005, "tol": 1e-4, "source": "RL energy branch L/R time constant"},
    {"id": "tr-rlc-01", "kind": "transient_rlc", "r": 50, "l": 1e-3, "c": 1e-6, "vc0": 10, "i0": 0, "t": 2e-5, "tol": 1e-3, "source": "Series RLC underdamped vc(t) closed form"},
    {"id": "tr-rlc-02", "kind": "transient_rlc", "r": 200, "l": 5e-3, "c": 0.5e-6, "vc0": 0, "i0": 0.1, "t": 1e-4, "tol": 1e-3, "source": "Natural response with initial inductor current"},
    {"id": "op-inv-01", "kind": "opamp_inverting", "vin": 0.1, "rf": 10000, "rin": 2000, "tol": 1e-6, "source": "Ideal opamp Av=-Rf/Rin"},
    {"id": "op-inv-02", "kind": "opamp_inverting", "vin": -0.25, "rf": 22000, "rin": 2200, "tol": 1e-6, "source": "Inverting gain block"},
    {"id": "op-ninv-01", "kind": "opamp_noninverting", "vin": 0.5, "rf": 9000, "rg": 1000, "tol": 1e-6, "source": "Noninverting Av=1+Rf/Rg"},
    {"id": "op-ninv-02", "kind": "opamp_noninverting", "vin": 1.0, "rf": 12000, "rg": 3000, "tol": 1e-6, "source": "Buffer gain from feedback ratio"},
    {"id": "dio-rd-01", "kind": "diode_small_signal", "id_a": 0.01, "n": 1.0, "vt_v": 0.02585, "tol": 1e-2, "source": "Small-signal rd=nVt/Id"},
    {"id": "dio-rd-02", "kind": "diode_small_signal", "id_a": 0.001, "n": 1.5, "vt_v": 0.026, "tol": 1e-2, "source": "Shockley linearization at Q-point"},
    {"id": "bjt-av-01", "kind": "bjt_ce_gain", "gm_s": 0.05, "rc_ohm": 2200, "vin": 1e-3, "tol": 1e-3, "source": "CE Av=-gm*Rc small-signal"},
    {"id": "bjt-av-02", "kind": "bjt_ce_gain", "gm_s": 0.02, "rc_ohm": 4700, "vin": 2e-3, "tol": 1e-3, "source": "Hybrid-pi voltage gain"},
    {"id": "z11-01", "kind": "two_port_z11", "r1": 100, "r2": 300, "r3": 600, "i1": 1.0, "tol": 1e-3, "source": "Pi network Z11 with port 2 open"},
    {"id": "z11-02", "kind": "two_port_z11", "r1": 50, "r2": 150, "r3": 150, "i1": 0.5, "tol": 1e-3, "source": "Two-port open-circuit input impedance"},
]


def main() -> int:
    from electrical_engineer.engines.circuit_derive import derive

    created = 0
    for case in CASES:
        cid = case["id"]
        item = PACK / cid
        item.mkdir(parents=True, exist_ok=True)
        meta = {k: v for k, v in case.items() if k not in {"id", "source", "tol"}}
        out = derive(meta)
        value = float(out["value"])
        tol = float(case.get("tol", 1e-4))
        expect = {
            "schema": "arc.eval.expect.v2",
            "engine": "circuit_unit",
            "value": value,
            "tol": tol,
            "kind": case["kind"],
        }
        fixtures = {**meta, "value": value, "expected": value, "tol": tol}
        (item / "expect.json").write_text(json.dumps(expect, indent=2) + "\n")
        (item / "fixtures" / "problem.json").parent.mkdir(parents=True, exist_ok=True)
        (item / "fixtures" / "problem.json").write_text(json.dumps(fixtures, indent=2) + "\n")
        (item / "source.md").write_text(f"# Source\n\n{case['source']}\n")
        (item / "task.md").write_text(f"Circuit unit {cid}: {case['kind']}\n")
        created += 1
    print(f"seeded {created} circuit gold items under {PACK}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
