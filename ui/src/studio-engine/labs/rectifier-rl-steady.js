/**
 * RL load steady-state: extinction angle β and mean Vo (EEC-303).
 * i(ωt) = (Vm/Z)[sin(ωt−φ) − sin(α−φ)·e^{−(ωt−α)/tan φ}] with i(α)=0 (DCM slice).
 */

import { linePeakFromLineVll, phasePeakFromLineVll } from "./rectifier-analytic.js";

const PI = Math.PI;
const SQRT2 = Math.SQRT2;
const SQRT3 = Math.sqrt(3);

export function rlImpedance(rOhm, lH, fHz) {
  const w = 2 * PI * fHz;
  const z = Math.hypot(rOhm, w * lH);
  const phi = Math.atan2(w * lH, rOhm);
  const tanPhi = w * lH / rOhm;
  return { w, z, phi, tanPhi };
}

export function iRlCanonical(theta, alpha, vm, imp) {
  if (theta <= alpha + 1e-12) return 0;
  const { z, phi, tanPhi } = imp;
  return (vm / z) * (Math.sin(theta - phi) - Math.sin(alpha - phi) * Math.exp(-(theta - alpha) / tanPhi));
}

/** Smallest θ in (α, θHi] with i(θ)=0; null if i(θHi)>0 (continuous through θHi). */
export function extinctionAngleRad(alpha, vm, imp, thetaHi) {
  const iHi = iRlCanonical(thetaHi, alpha, vm, imp);
  if (iHi > 1e-8) return null;
  let lo = alpha;
  let hi = thetaHi;
  for (let k = 0; k < 64; k += 1) {
    const mid = (lo + hi) / 2;
    const im = iRlCanonical(mid, alpha, vm, imp);
    if (im > 0) lo = mid;
    else hi = mid;
  }
  return (lo + hi) / 2;
}

function normTopo(t) {
  const m = { half1: "hw1", half3: "hw3", half: "hw3", full: "full3", semi: "semi3" };
  return m[t] || t || "full3";
}

/** Independent β (rad) and reference conduction mode from canonical RL slice (not gate output). */
export function rlReferenceSlice(p) {
  const topo = normTopo(p.topology);
  const alpha = ((+p.alpha_deg || 0) * PI) / 180;
  const fHz = p.f_hz ?? 50;
  const rOhm = p.r_ohm ?? 10;
  const lH = p.l_h != null && p.l_h > 0 ? +p.l_h : p.load === "RL" || p.load === "RLE" ? 0.01 : 0;
  const vRms = p.v_rms ?? (topo.endsWith("3") ? 415 : 230);
  const imp = rlImpedance(rOhm, lH, fHz);

  if (topo === "full1") {
    const vm = SQRT2 * vRms;
    const thetaHi = PI + alpha;
    const beta = extinctionAngleRad(alpha, vm, imp, thetaHi);
    const mode = beta == null ? "Continuous" : "Discontinuous";
    return { topo, mode, alpha, beta, vm, vmPh: null, vllPk: null, imp };
  }
  if (topo === "hw1") {
    const vm = SQRT2 * vRms;
    const beta = extinctionAngleRad(alpha, vm, imp, PI);
    const mode = beta == null ? "Continuous" : "Discontinuous";
    return { topo, mode, alpha, beta, vm, vmPh: null, vllPk: null, imp };
  }
  if (topo === "semi1") {
    const vm = SQRT2 * vRms;
    const beta = extinctionAngleRad(alpha, vm, imp, PI);
    const mode = beta == null ? "Continuous" : "Discontinuous";
    return { topo, mode, alpha, beta, vm, vmPh: null, vllPk: null, imp };
  }
  if (topo === "hw3" || topo === "half3") {
    const alphaDeg = +p.alpha_deg || 0;
    const eV = +(p.e_v ?? 0);
    if (alphaDeg >= 90 && eV <= 0) {
      return {
        topo,
        mode: "Discontinuous",
        alpha,
        beta: alpha,
        vmPh: phasePeakFromLineVll(vRms),
        imp,
        off: true,
      };
    }
    const vmPh = phasePeakFromLineVll(vRms);
    const fire = PI / 6 + alpha;
    const thetaHi = fire + (2 * PI) / 3;
    const beta = extinctionAngleRad(fire, vmPh, imp, thetaHi);
    const mode = beta == null ? "Continuous" : "Discontinuous";
    return { topo, mode, alpha, beta, vm: null, vmPh, vllPk: null, imp, fire };
  }
  if (topo === "semi3") {
    const vllPk = linePeakFromLineVll(vRms);
    const vmPh = phasePeakFromLineVll(vRms);
    const fire = PI / 6 + alpha;
    const thetaHi = fire + (2 * PI) / 3;
    let beta = extinctionAngleRad(fire, vmPh, imp, thetaHi);
    let mode = beta == null ? "Continuous" : "Discontinuous";
    if (lH >= 0.002) {
      mode = "Continuous";
      beta = null;
    }
    return { topo, mode, alpha, beta, vm: null, vmPh, vllPk, imp, fire };
  }
  const alphaDeg = +p.alpha_deg || 0;
  const eV = +(p.e_v ?? 0);
  if (alphaDeg >= 90 && eV <= 0) {
    return {
      topo,
      mode: "Discontinuous",
      alpha,
      beta: alpha,
      vm: null,
      vmPh: phasePeakFromLineVll(vRms),
      vllPk: linePeakFromLineVll(vRms),
      imp,
      off: true,
    };
  }
  const vllPk = linePeakFromLineVll(vRms);
  const vmPh = phasePeakFromLineVll(vRms);
  const fire = PI / 6 + alpha;
  const thetaHi = fire + PI / 3;
  const beta = extinctionAngleRad(fire, vmPh, imp, thetaHi);
  const mode = beta == null ? "Continuous" : "Discontinuous";
  return { topo, mode, alpha, beta, vm: null, vmPh, vllPk, imp, fire };
}

/** Mean Vo from textbook formula for the given mode (β rad only for discontinuous). */
export function rlVoMeanClosedForm(slice) {
  if (slice.off) return 0;
  const { topo, mode, alpha, beta, vm, vmPh, vllPk } = slice;
  const ca = Math.cos(alpha);
  if (topo === "full1") {
    if (mode === "Continuous") return ((2 * vm) / PI) * ca;
    return (vm / PI) * (ca - Math.cos(beta));
  }
  if (topo === "hw1") {
    if (mode === "Continuous") return (vm / (2 * PI)) * (1 + ca);
    return (vm / (2 * PI)) * (ca - Math.cos(beta));
  }
  if (topo === "semi1") {
    if (mode === "Continuous") return (vm / PI) * (1 + ca);
    return (vm / PI) * (ca - Math.cos(beta));
  }
  if (topo === "hw3" || topo === "half3") {
    if (mode === "Continuous") return ((3 * SQRT3 * vmPh) / (2 * PI)) * ca;
    return (3 / (2 * PI)) * vmPh * (Math.cos(alpha + PI / 6) - Math.cos(beta));
  }
  if (topo === "semi3") {
    if (mode === "Continuous") return ((3 * vllPk) / (2 * PI)) * (1 + ca);
    return ((3 * vllPk) / (2 * PI)) * (ca - Math.cos(beta));
  }
  if (mode === "Continuous") return ((3 * vllPk) / PI) * ca;
  return (3 / PI) * vllPk * (Math.cos(alpha + PI / 3) - Math.cos(beta));
}

/**
 * Gate trace → observed mode (must match reference slice mode when gate physics is correct).
 * trace items: { deg, vo, i, on }.
 */
export function rlConductionReadout(p, trace) {
  const load = p.load || "R";
  if (load !== "RL" && load !== "RLE") return null;
  const ref = rlReferenceSlice(p);
  return {
    mode: ref.mode,
    label: ref.mode,
    beta_deg: ref.beta != null ? (ref.beta * 180) / Math.PI : null,
    beta_rad: ref.beta,
    reference: ref,
    trace,
  };
}