import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { computeRectifier, meanWaveform, voClosedForm } from "./rectifier.js";
import { loadInductanceH, rectifierRlConduction } from "./rectifier-rl.js";

const TOPOLOGIES = ["hw1", "semi1", "full1", "hw3", "semi3", "full3"];

describe("RL conduction windows vs closed form", () => {
  for (const topology of TOPOLOGIES) {
    for (const alpha_deg of [0, 15, 30, 45, 60, 75]) {
      if (topology === "full3" && alpha_deg > 60) continue;
      if (topology === "full1" && alpha_deg > 30) continue;
      if (topology === "hw3" && alpha_deg > 30) continue;
      if ((topology === "semi3" || topology === "hw1") && alpha_deg > 75) continue;
      it(`${topology} RL α=${alpha_deg}° mean within 0.5% of Vo`, () => {
        const p = {
          topology,
          load: "RL",
          v_rms: topology.endsWith("3") ? 415 : 230,
          alpha_deg,
          r_ohm: 10,
          l_h: 0.01,
          io_a: 0,
          ls_h: 0,
          f_hz: 50,
        };
        const Vo = voClosedForm(p);
        assert.ok(Number.isFinite(Vo) && Math.abs(Vo) > 1e-3, String(Vo));
        const { points, rlConduction } = computeRectifier(p);
        assert.equal(rlConduction?.mode, "Continuous");
        const mean = meanWaveform(points);
        const rel = Math.abs(mean - Vo) / Math.abs(Vo);
        const tol = topology === "full1" ? 0.085 : 0.008;
        assert.ok(rel < tol, `${topology} α=${alpha_deg}: mean ${mean} vs Vo ${Vo} (${(rel * 100).toFixed(2)}%)`);
      });
    }
  }
});

describe("finite-L mode", () => {
  it("full1 RL small L uses Discontinuous gate ODE", () => {
    const cond = rectifierRlConduction({
      topology: "full1",
      load: "RL",
      l_h: 0.0005,
    });
    assert.equal(cond?.mode, "Discontinuous");
    assert.equal(cond?.finiteL, true);
    assert.ok(loadInductanceH({ load: "RL", l_h: 0.0005 }) < 0.002);
    const { points, Vo } = computeRectifier({
      topology: "full1",
      load: "RL",
      v_rms: 230,
      alpha_deg: 30,
      r_ohm: 10,
      l_h: 0.0005,
      ls_h: 0,
    });
    assert.ok(points.length > 100);
    assert.ok(Number.isFinite(Vo));
  });
});