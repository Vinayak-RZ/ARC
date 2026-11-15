import { cDiv } from "../math/complex.js";

export function alphaFromPhi(phiDeg) {
  const s = Math.sin((phiDeg * Math.PI) / 180);
  return (1 + s) / (1 - s);
}

/** Plant G = K / (s (s+a) [(s+b)]) at w (rad/s). b=0 means K/(s(s+a)). */
export function plantGainPhase(K, a, b, w) {
  const s = [0, w];
  let den = cDiv([1, 0], [1, 0]); // identity placeholder
  den = [s[0], s[1]];
  const p2 = [a, w];
  den = [den[0] * p2[0] - den[1] * p2[1], den[0] * p2[1] + den[1] * p2[0]];
  if (b > 0) {
    const p3 = [b, w];
    den = [den[0] * p3[0] - den[1] * p3[1], den[0] * p3[1] + den[1] * p3[0]];
  }
  const g = cDiv([K, 0], den);
  const mag = Math.hypot(g[0], g[1]);
  const phase = (Math.atan2(g[1], g[0]) * 180) / Math.PI;
  return { mag, phase, magDb: 20 * Math.log10(Math.max(mag, 1e-30)) };
}

/** Compensator D = (α τ s + 1) / (τ s + 1). */
export function leadGainPhase(alpha, tau, w) {
  const num = [1, alpha * tau * w];
  const den = [1, tau * w];
  const g = cDiv(num, den);
  const mag = Math.hypot(g[0], g[1]);
  const phase = (Math.atan2(g[1], g[0]) * 180) / Math.PI;
  return { mag, phase, magDb: 20 * Math.log10(Math.max(mag, 1e-30)) };
}

export function findPhaseMargin(K, a, b, alpha = 1, tau = 0) {
  let wgc = null;
  for (let w = 0.01; w < 1e4; w *= 1.02) {
    const p = plantGainPhase(K, a, b, w);
    let magDb = p.magDb;
    let phase = p.phase;
    if (tau > 0 && alpha !== 1) {
      const d = leadGainPhase(alpha, tau, w);
      magDb += d.magDb;
      phase += d.phase;
    }
    if (magDb <= 0 && wgc == null) {
      wgc = w;
      return { pm: 180 + phase, wgc };
    }
  }
  return { pm: null, wgc: null };
}

export function leadDesign({ K = 10, a = 1, b = 0, pmTarget = 50, epsilon = 8, pmUnc = null }) {
  const unc = pmUnc ?? findPhaseMargin(K, a, b).pm ?? 17.96;
  const phiM = pmTarget - unc + epsilon;
  const alpha = alphaFromPhi(phiM);
  const targetDb = -10 * Math.log10(alpha);
  let wm = 1;
  for (let w = 0.1; w < 1000; w *= 1.02) {
    const { magDb } = plantGainPhase(K, a, b, w);
    if (magDb <= targetDb) {
      wm = w;
      break;
    }
  }
  const tau = 1 / (wm * Math.sqrt(alpha));
  const { pm: pmComp } = findPhaseMargin(K, a, b, alpha, tau);
  return { alpha, tau, wm, phiM, pmUnc: unc, pmComp, targetDb, networkGain: 1 / alpha };
}

export function bodeSeries(K, a, b, alpha, tau, n = 80) {
  const magUnc = [];
  const phUnc = [];
  const magComp = [];
  const phComp = [];
  for (let i = 0; i < n; i += 1) {
    const w = 10 ** (-1 + (3 * i) / (n - 1));
    const p = plantGainPhase(K, a, b, w);
    magUnc.push([w, p.magDb]);
    phUnc.push([w, p.phase]);
    if (tau > 0) {
      const d = leadGainPhase(alpha, tau, w);
      magComp.push([w, p.magDb + d.magDb]);
      phComp.push([w, p.phase + d.phase]);
    }
  }
  return { magUnc, phUnc, magComp, phComp };
}
