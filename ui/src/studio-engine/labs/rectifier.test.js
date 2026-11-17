import { describe, it } from "node:test";
import assert from "node:assert/strict";
import {
  computeRectifier,
  meanWaveform,
  phasePeakFromLineVll,
  sampleWaveform,
  voClosedForm,
} from "./rectifier.js";

const SQRT2 = Math.SQRT2;
const SOURCE_PEAK_230 = SQRT2 * 230;
const SOURCE_PEAK_415 = SQRT2 * 415;
const VM_415 = phasePeakFromLineVll(415);

describe("rectifier closed form", () => {
  it("full1 continuous alpha 30 (RL)", () => {
    const Vo = voClosedForm({ topology: "full1", load: "RL", v_rms: 230, alpha_deg: 30, io_a: 0, ls_h: 0 });
    assert.ok(Math.abs(Vo - 179.33) < 0.5, String(Vo));
  });
  it("full3 alpha 45", () => {
    const Vo = voClosedForm({ topology: "full3", load: "RL", v_rms: 415, alpha_deg: 45, io_a: 0, ls_h: 0 });
    assert.ok(Math.abs(Vo - 396.3) < 0.5, String(Vo));
  });

  it("full1 R alpha 60 discontinuous readout", () => {
    const Vo = voClosedForm({ topology: "full1", load: "R", v_rms: 230, alpha_deg: 60, io_a: 0, ls_h: 0 });
    assert.ok(Math.abs(Vo - 155.3) < 0.25, String(Vo));
  });

  it("full3 R alpha 75 discontinuous readout", () => {
    const Vo = voClosedForm({ topology: "full3", load: "R", v_rms: 415, alpha_deg: 75, io_a: 0, ls_h: 0 });
    assert.ok(Math.abs(Vo - 164.1) < 0.35, String(Vo));
  });

  it("full1 R alpha 60 waveform not rescaled above Vm", () => {
    const pts = sampleWaveform({ topology: "full1", load: "R", v_rms: 230, alpha_deg: 60, io_a: 0, ls_h: 0 }, 3600);
    const maxY = Math.max(...pts.map(([, y]) => y));
    assert.ok(maxY <= SOURCE_PEAK_230 + 2, String(maxY));
    assert.ok(maxY > 200, String(maxY));
  });
  it("full3 with overlap", () => {
    const Vo = voClosedForm({
      topology: "full3",
      v_rms: 415,
      alpha_deg: 45,
      io_a: 20,
      ls_h: 0.002,
      f_hz: 50,
    });
    assert.ok(Math.abs(Vo - 384.3) < 1.0, String(Vo));
  });

  it("hw3 default discontinuous R load", () => {
    const p = {
      topology: "hw3",
      load: "R",
      v_rms: 415,
      alpha_deg: 45,
      r_ohm: 10,
      io_a: 0,
      ls_h: 0,
    };
    const { Vo, Io } = computeRectifier(p);
    assert.ok(Number.isFinite(Vo), String(Vo));
    assert.ok(Math.abs(Vo - 203.7) < 0.5, String(Vo));
    assert.ok(Math.abs(Io - 20.4) < 0.2, String(Io));
  });

  it("hw3 inductive at alpha 45", () => {
    const Vo = voClosedForm({
      topology: "hw3",
      load: "RL",
      v_rms: 415,
      alpha_deg: 45,
      io_a: 0,
      ls_h: 0.01,
    });
    assert.ok(Math.abs(Vo - 198.1) < 1.0, String(Vo));
  });

  it("hw3 formulas meet at alpha 30", () => {
    const disc = voClosedForm({ topology: "hw3", load: "R", v_rms: 415, alpha_deg: 30, io_a: 0, ls_h: 0 });
    const Vm = VM_415;
    const a = (30 * Math.PI) / 180;
    const continuous = ((3 * Math.sqrt(3)) / (2 * Math.PI)) * Vm * Math.cos(a);
    const discontinuous = (3 / (2 * Math.PI)) * Vm * (1 + Math.cos(a + Math.PI / 6));
    assert.ok(Math.abs(disc - continuous) < 0.5, `${disc} vs ${continuous}`);
    assert.ok(Math.abs(disc - discontinuous) < 0.5, `${disc} vs ${discontinuous}`);
  });
});

describe("rectifier waveforms", () => {
  it("hw3 has three pulses and max below Vm", () => {
    const p = { topology: "hw3", load: "R", v_rms: 415, alpha_deg: 45 };
    const pts = sampleWaveform(p, 3600);
    let peaks = 0;
    for (let i = 1; i < pts.length - 1; i += 1) {
      const y = pts[i][1];
      if (y > 50 && y >= pts[i - 1][1] && y >= pts[i + 1][1]) peaks += 1;
    }
    const maxY = Math.max(...pts.map(([, y]) => y));
    const mean = meanWaveform(pts);
    const Vo = voClosedForm({ ...p, io_a: 0, ls_h: 0 });
    assert.equal(peaks, 3, `peak count ${peaks}`);
    assert.ok(maxY <= VM_415 + 0.5, String(maxY));
    assert.ok(Math.abs(mean - Vo) / Vo < 0.005, `${mean} vs ${Vo}`);
  });

  it("full3 has six pulses", () => {
    const p = { topology: "full3", v_rms: 415, alpha_deg: 45 };
    const pts = sampleWaveform(p, 3600);
    let peaks = 0;
    for (let i = 1; i < pts.length - 1; i += 1) {
      const y = pts[i][1];
      if (y > 50 && y >= pts[i - 1][1] && y >= pts[i + 1][1]) peaks += 1;
    }
    assert.ok(peaks >= 5 && peaks <= 7, String(peaks));
    const Vo = voClosedForm({ ...p, io_a: 0, ls_h: 0 });
    const mean = meanWaveform(pts);
    assert.ok(Math.abs(mean - Vo) / Vo < 0.01, `${mean} vs ${Vo}`);
  });
});

describe("rectifier waveform mean vs Vo readout", () => {
  const topologies = ["hw1", "semi1", "full1", "hw3", "semi3", "full3"];
  const loads = ["R", "RL", "RLE"];
  const alphas = [0, 30, 60, 75, 90, 120, 150];
  for (const topology of topologies) {
    for (const load of loads) {
      for (const alpha_deg of alphas) {
        it(`${topology} ${load} α=${alpha_deg}`, () => {
          const p = {
            topology,
            load,
            v_rms: topology.endsWith("3") ? 415 : 230,
            alpha_deg,
            r_ohm: 10,
            io_a: 0,
            ls_h: 0,
          };
          const Vo = voClosedForm(p);
          const pts = sampleWaveform(p, 3600);
          const mean = meanWaveform(pts);
          assert.ok(Number.isFinite(Vo), String(Vo));
          if (Math.abs(Vo) < 1e-6) {
            return;
          }
          if (Math.abs(Vo) < 5) {
            assert.ok(Math.abs(mean) < 5, `mean ${mean} vs Vo ${Vo}`);
          } else {
            const rel = Math.abs(mean - Vo) / Math.abs(Vo);
            assert.ok(rel < 0.0051, `mean ${mean} vs Vo ${Vo} (${(rel * 100).toFixed(2)}%)`);
          }
          const peak = topology.endsWith("3") ? SOURCE_PEAK_415 : SOURCE_PEAK_230;
          const maxAbs = Math.max(...pts.map(([, y]) => Math.abs(y)));
          assert.ok(maxAbs <= peak + 2, `max |v| ${maxAbs} > source peak ${peak}`);
        });
      }
    }
  }
});

describe("rectifier finiteness sweep", () => {
  const topologies = ["hw1", "semi1", "full1", "hw3", "semi3", "full3"];
  const loads = ["R", "RL", "RLE", "CC"];
  const alphas = [0, 15, 30, 45, 60, 90, 120, 150, 180];
  for (const topology of topologies) {
    for (const load of loads) {
      for (const alpha_deg of alphas) {
        it(`${topology} ${load} α=${alpha_deg}`, () => {
          const { Vo, Io, VoFinite } = computeRectifier({
            topology,
            load,
            v_rms: topology.endsWith("3") ? 415 : 230,
            alpha_deg,
            r_ohm: 10,
            io_a: 15,
            ls_h: 0.002,
          });
          assert.ok(VoFinite && Number.isFinite(Vo), String(Vo));
          assert.ok(Number.isFinite(Io), String(Io));
        });
      }
    }
  }
});