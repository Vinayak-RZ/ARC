import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { computeRectifier, meanWaveform } from "./rectifier.js";
import { loadInductanceH, rectifierRlFiniteL } from "./rectifier-rl.js";
import { rlReferenceSlice, rlVoMeanClosedForm } from "./rectifier-rl-steady.js";

const TOPOLOGIES = ["hw1", "semi1", "full1", "hw3", "semi3", "full3"];
const ALPHAS = [0, 15, 30, 45, 60, 75, 90];

describe("RL Vo readout equals waveform mean", () => {
  for (const topology of TOPOLOGIES) {
    for (const alpha_deg of ALPHAS) {
      if (topology === "full3" && alpha_deg > 90) continue;
      if (topology === "full1" && alpha_deg > 120) continue;
      it(`${topology} α=${alpha_deg}°`, () => {
        const p = {
          topology,
          load: "RL",
          v_rms: topology.endsWith("3") ? 415 : 230,
          alpha_deg,
          r_ohm: 10,
          l_h: 0.01,
          ls_h: 0,
          f_hz: 50,
        };
        const { points, Vo, waveformMean } = computeRectifier(p);
        assert.ok(points.length > 100);
        assert.ok(Math.abs(Vo - waveformMean) < 1e-6, `Vo ${Vo} vs mean ${waveformMean}`);
      });
    }
  }
});

describe("RL mean vs independent closed form (0.5%)", () => {
  for (const topology of TOPOLOGIES) {
    for (const alpha_deg of ALPHAS) {
      if (topology === "full3" && alpha_deg > 90) continue;
      if (topology === "full1" && alpha_deg > 120) continue;
      it(`${topology} α=${alpha_deg}°`, () => {
        const p = {
          topology,
          load: "RL",
          v_rms: topology.endsWith("3") ? 415 : 230,
          alpha_deg,
          r_ohm: 10,
          l_h: 0.01,
          ls_h: 0,
          f_hz: 50,
        };
        const ref = rlReferenceSlice(p);
        const expectVo = rlVoMeanClosedForm(ref);
        if (Math.abs(expectVo) < 1e-4) return;
        const { points, rlConduction } = computeRectifier(p);
        const mean = meanWaveform(points);
        assert.equal(rlConduction?.mode, ref.mode);
        const rel = Math.abs(mean - expectVo) / Math.abs(expectVo);
        assert.ok(rel < 0.005, `${topology} α=${alpha_deg}: ${(rel * 100).toFixed(2)}% mean ${mean} vs ${expectVo}`);
      });
    }
  }
});

describe("finite-L discontinuous", () => {
  it("full1 small L is discontinuous", () => {
    assert.ok(rectifierRlFiniteL({ load: "RL", l_h: 0.0005 }));
    assert.ok(loadInductanceH({ load: "RL", l_h: 0.0005 }) < 0.002);
    const { rlConduction } = computeRectifier({
      topology: "full1",
      load: "RL",
      v_rms: 230,
      alpha_deg: 30,
      r_ohm: 10,
      l_h: 0.0005,
      ls_h: 0,
    });
    assert.equal(rlConduction?.mode, "Discontinuous");
    assert.ok(rlConduction?.beta_deg != null);
  });
});