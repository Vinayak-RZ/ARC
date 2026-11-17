/** Closed-form rectifier Vo and waveforms (EEC-303 style). V rms is line-to-line for 3φ. */

import { firingAnglesDeg, linePeakFromLineVll, phasePeakFromLineVll, voFull3Analytic } from "./rectifier-analytic.js";
import { gateSampleWaveform } from "./rectifier-gate.js";
import { rectifierRlConduction } from "./rectifier-rl.js";

export { phasePeakFromLineVll, firingAnglesDeg };

const PI = Math.PI;
const SQRT2 = Math.SQRT2;

function deg(rad) {
  return (rad * 180) / PI;
}

function rad(degVal) {
  return (degVal * PI) / 180;
}

/** R-load discontinuous-mode boundaries (EEC-303); RL/CC use continuous bridge formulas. */
function isContinuousConduction(load, topology, alphaDeg) {
  if (load !== "R") return true;
  if (topology === "full1") return false;
  if (topology === "full3") return alphaDeg <= 60;
  if (topology === "hw3" || topology === "half3") return alphaDeg <= 30;
  return alphaDeg <= 0;
}

function sourcePeakV(p) {
  const { topology, v_rms } = p;
  if (topology?.endsWith("3")) return linePeakFromLineVll(v_rms);
  return SQRT2 * v_rms;
}

function normTopoEarly(t) {
  const m = { half1: "hw1", half3: "hw3", half: "hw3", full: "full3", semi: "semi3" };
  return m[t] || t || "full3";
}

/** Valid firing-angle range per topology/load (degrees, inclusive). */
export function alphaLimitDeg(p) {
  const topo = normTopoEarly(p.topology);
  const load = p.load || "R";
  if (topo === "full3" && load === "R") return 120;
  if (topo === "hw3" && load === "R") return 150;
  if ((topo === "hw3" || topo === "half3") && load !== "R") return 90;
  return 180;
}

export function clampRectifierAlpha(p) {
  const lim = alphaLimitDeg(p);
  const raw = Number(p.alpha_deg);
  const alpha = Number.isFinite(raw) ? raw : 0;
  const past = alpha > lim || alpha < 0;
  return { alpha_deg: past ? Math.min(Math.max(alpha, 0), lim) : alpha, past_limit: past, limit_deg: lim };
}

export function voClosedForm(p) {
  const clamp = clampRectifierAlpha({ topology: p.topology, load: p.load, alpha_deg: p.alpha_deg });
  if (clamp.past_limit && (p.load || "R") === "R" && (p.ls_h ?? 0) <= 0) return 0;
  const { topology, load = "R", v_rms, alpha_deg, io_a = 0, ls_h = 0, f_hz = 50 } = p;
  const alpha = rad(alpha_deg);
  const w = 2 * PI * f_hz;
  const cosA = Math.cos(alpha);
  const cc = isContinuousConduction(load, topology, alpha_deg);

  if (topology === "hw1" || topology === "half1") {
    const Vm = SQRT2 * v_rms;
    return (Vm / (2 * PI)) * (1 + cosA);
  }
  if (topology === "semi1") {
    const Vm = SQRT2 * v_rms;
    return (Vm / PI) * (1 + cosA) - (w * ls_h * io_a) / PI;
  }
  if (topology === "full1") {
    const Vm = SQRT2 * v_rms;
    if (ls_h <= 0 && load === "R") {
      if (alpha_deg >= 180) return 0;
      return (Vm / PI) * (1 + cosA);
    }
    if (alpha_deg >= 90 && !(p.e_v > 0)) return 0;
    if (alpha_deg > 90 && !(p.e_v > 0)) return 0;
    return (2 * Vm * cosA) / PI - (2 * w * ls_h * io_a) / PI;
  }

  const Vm = phasePeakFromLineVll(v_rms);
  const VllPk = linePeakFromLineVll(v_rms);

  if (topology === "hw3" || topology === "half3") {
    if (load !== "R" && alpha_deg > 90 && !(p.e_v > 0)) return 0;
    let Vo;
    if (cc) {
      Vo = ((3 * Math.sqrt(3) * Vm) / (2 * PI)) * cosA - (3 * w * ls_h * io_a) / (2 * PI);
    } else {
      Vo = (3 / (2 * PI)) * Vm * (1 + Math.cos(alpha + PI / 6));
    }
    return Vo;
  }
  if (topology === "semi3") {
    return ((3 * VllPk) / (2 * PI)) * (1 + cosA) - (3 * w * ls_h * io_a) / (2 * PI);
  }
  if (load === "R" && ls_h <= 0) {
    if (alpha_deg > 120) return 0;
    if (alpha_deg > 60) return ((3 * VllPk) / PI) * (1 + Math.cos(alpha + PI / 3));
    return ((3 * VllPk) / PI) * cosA;
  }
  if (load !== "R" && alpha_deg > 90 && !(p.e_v > 0)) {
    return 0;
  }
  return ((3 * VllPk) / PI) * cosA - (3 * w * ls_h * io_a) / PI;
}

/** 3φ half-wave: phase-k voltage Vm·sin(wt − k·120°), gated from firing to commutation. */
function voThreePhaseHalf(wt, Vm, alphaRad, continuous) {
  let vo = 0;
  const w = ((wt % (2 * PI)) + 2 * PI) % (2 * PI);
  for (let k = 0; k < 3; k += 1) {
    const fire = PI / 6 + alphaRad + k * ((2 * PI) / 3);
    const vf = ((fire % (2 * PI)) + 2 * PI) % (2 * PI);
    const phaseShift = k * ((2 * PI) / 3);
    let end = ((phaseShift + PI) % (2 * PI) + (2 * PI)) % (2 * PI);
    if (continuous) {
      const nextFire = PI / 6 + alphaRad + ((k + 1) % 3) * ((2 * PI) / 3);
      end = ((nextFire % (2 * PI)) + 2 * PI) % (2 * PI);
    }
    let inConduction;
    if (vf <= end) inConduction = w >= vf && w < end;
    else inConduction = w >= vf || w < end;
    if (!inConduction) continue;
    const v = Vm * Math.sin(w - phaseShift);
    if (continuous || v > 0) vo = continuous ? Math.max(vo, v) : Math.max(vo, Math.max(0, v));
  }
  return continuous ? vo : Math.max(0, vo);
}

function voSemiFreewheel1(wt, Vm, alphaRad) {
  const cycle = ((wt % PI) + PI) % PI;
  if (cycle < alphaRad) return 0;
  return Math.abs(Vm * Math.sin(wt));
}

function voFull1RWave(wt, Vm, alphaDeg) {
  if (alphaDeg >= 180) return 0;
  const alphaRad = rad(alphaDeg);
  const cycle = ((wt % PI) + PI) % PI;
  if (cycle < alphaRad) return 0;
  if (alphaDeg < 60) return Math.abs(Vm * Math.sin(wt));
  return Math.max(0, Vm * Math.sin(wt));
}

function voSinglePhaseHalf(wt, Vm, alphaRad, fullWave, continuous = false) {
  if (fullWave) {
    const cycle = ((wt % PI) + PI) % PI;
    if (cycle < alphaRad) return 0;
    const v = Vm * Math.sin(wt);
    const mag = Math.abs(v);
    if (!continuous) return mag;
    return v < 0 ? v : mag;
  }
  const cycle = ((wt % (2 * PI)) + 2 * PI) % (2 * PI);
  if (cycle >= alphaRad && cycle < PI) return Math.max(0, Vm * Math.sin(wt));
  return 0;
}

export function sampleWaveform(p, N = 720) {
  const gp = { ...p };
  if (gp.load === "RL" && gp.l_h == null) gp.l_h = 0.01;
  if (gp.load === "R" || gp.load === "CC") gp.l_h = 0;
  return gateSampleWaveform(gp, N);
}

export function meanWaveform(points) {
  if (!points.length) return NaN;
  const sum = points.reduce((a, [, y]) => a + y, 0);
  return sum / points.length;
}

function rmsFromPoints(points) {
  if (!points.length) return 0;
  let sum = 0;
  for (const [, y] of points) sum += y * y;
  return Math.sqrt(sum / points.length);
}

function normTopo(t) {
  const m = { half1: "hw1", half3: "hw3", half: "hw3", full: "full3", semi: "semi3" };
  return m[t] || t || "full3";
}

const SQRT3 = Math.sqrt(3);

/** R load: PF = P/S with IL,rms from topology (3φ full: Io,rms·√(2/3)). */
export function powerFactorFromWaveform(p, points, Vo) {
  if (p.load !== "R") {
    return p.topology === "full3" ? (3 / PI) * Math.cos(rad(p.alpha_deg)) : null;
  }
  if (!points.length || !Number.isFinite(Vo) || Math.abs(Vo) < 1e-6) return 0;
  const vrmsO = rmsFromPoints(points);
  if (vrmsO < 1e-9) return 0;
  const r = Math.max(p.r_ohm || 1, 1e-9);
  const pW = (vrmsO * vrmsO) / r;
  const ioRms = vrmsO / r;
  const topo = normTopo(p.topology);
  const vLine = p.v_rms ?? (topo.endsWith("3") ? 415 : 230);
  let sVa;
  if (topo === "hw3") {
    return vrmsO / (SQRT3 * vLine);
  }
  if (topo === "full3" || topo === "semi3") {
    const ilRms = ioRms * Math.sqrt(2 / 3);
    sVa = SQRT3 * vLine * ilRms;
  } else if (topo === "hw1") {
    sVa = SQRT2 * vLine * ioRms;
  } else {
    sVa = vLine * ioRms;
  }
  if (sVa < 1e-12) return 0;
  const pf = pW / sVa;
  return Number.isFinite(pf) ? pf : 0;
}

export function computeRectifier(p) {
  const clamp = clampRectifierAlpha(p);
  const work = clamp.past_limit ? { ...p, alpha_deg: clamp.limit_deg, _past_alpha_limit: true } : p;
  let VoRaw = voClosedForm(work);
  if (clamp.past_limit) VoRaw = 0;
  const Vo = Number.isFinite(VoRaw) ? VoRaw : NaN;
  const Io = p.load === "CC" ? p.io_a : Vo / Math.max(p.r_ohm || 1, 1e-9);
  const sampleP =
    work.load === "RL" || work.load === "RLE"
      ? { ...work, io_a: Number.isFinite(Io) ? Io : work.io_a }
      : work;
  const points = !clamp.past_limit && Number.isFinite(Vo) ? sampleWaveform(sampleP) : [];
  const mean = meanWaveform(points);
  const PF = powerFactorFromWaveform(work, points, Vo);
  const rlConduction = rectifierRlConduction(p);
  return {
    Vo,
    Io: Number.isFinite(Io) ? Io : NaN,
    points,
    waveformMean: mean,
    PF,
    alpha_past_limit: clamp.past_limit,
    alpha_limit_deg: clamp.limit_deg,
    rlConduction,
    phasePeakVm: p.topology.endsWith("3") ? phasePeakFromLineVll(p.v_rms) : SQRT2 * p.v_rms,
    VoFinite: Number.isFinite(Vo),
  };
}