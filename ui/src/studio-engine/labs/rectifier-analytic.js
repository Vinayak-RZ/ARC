/** Shared rectifier analytic helpers (full3 arcs). */

const PI = Math.PI;
const SQRT2 = Math.SQRT2;
const SQRT3 = Math.sqrt(3);

const FULL3_LINE_PAIRS = [
  [0, 1],
  [0, 2],
  [1, 2],
  [1, 0],
  [2, 0],
  [2, 1],
];

export function phasePeakFromLineVll(vLlRms) {
  return (SQRT2 * vLlRms) / SQRT3;
}

export function linePeakFromLineVll(vLlRms) {
  return SQRT2 * vLlRms;
}

function deg(rad) {
  return (rad * 180) / PI;
}

export function voFull3Analytic(wt, vllPk, alphaDeg) {
  const vm = vllPk / SQRT3;
  const fire0 = 30 + alphaDeg;
  const degWt = deg(wt);
  const rel = ((degWt - fire0) % 360 + 360) % 360;
  const k = Math.floor(rel / 60) % 6;
  const [ia, ib] = FULL3_LINE_PAIRS[k];
  const phase = (ph) => vm * Math.sin(wt - ph * ((2 * PI) / 3));
  return phase(ia) - phase(ib);
}

/** ωt commutation angles (phase-a frame; matches lab plot x-axis). */
/** 3φ half-wave RL continuous: pulse width (deg) so sampled mean matches (3√3 Vm)/(2π) cos α. */
export function hw3RlPulseWidthDeg(alphaDeg) {
  if (alphaDeg >= 90) return 0;
  if (alphaDeg <= 30) return 120;
  const knots = [
    [30, 119],
    [45, 90],
    [60, 60],
    [75, 30],
    [89, 4],
  ];
  if (alphaDeg >= knots[knots.length - 1][0]) return knots[knots.length - 1][1];
  for (let i = 0; i < knots.length - 1; i += 1) {
    const [a0, w0] = knots[i];
    const [a1, w1] = knots[i + 1];
    if (alphaDeg <= a1) {
      const t = (alphaDeg - a0) / (a1 - a0);
      return w0 + t * (w1 - w0);
    }
  }
  return 0;
}

export function voFull1RlWave(wt, vm, alphaDeg) {
  if (alphaDeg >= 90) return 0;
  const a = (alphaDeg * PI) / 180;
  const cycle = ((wt % PI) + PI) % PI;
  if (cycle >= a && cycle <= PI - a) return Math.abs(vm * Math.sin(wt));
  return 0;
}

export function voHw3RWave(wt, vmPh, alphaDeg) {
  const alpha = (alphaDeg * PI) / 180;
  const w = ((wt % (2 * PI)) + 2 * PI) % (2 * PI);
  let vo = 0;
  for (let k = 0; k < 3; k += 1) {
    const fire = PI / 6 + alpha + k * ((2 * PI) / 3);
    const vf = ((fire % (2 * PI)) + 2 * PI) % (2 * PI);
    const phaseShift = k * ((2 * PI) / 3);
    const end = ((phaseShift + PI) % (2 * PI) + (2 * PI)) % (2 * PI);
    let inCond;
    if (vf <= end) inCond = w >= vf && w < end;
    else inCond = w >= vf || w < end;
    if (!inCond) continue;
    const v = vmPh * Math.sin(w - phaseShift);
    vo = Math.max(vo, Math.max(0, v));
  }
  return Math.max(0, vo);
}

export function voHw3RlWave(wt, vmPh, alphaDeg) {
  const pulse = (hw3RlPulseWidthDeg(alphaDeg) * PI) / 180;
  if (pulse <= 0) return 0;
  const alpha = (alphaDeg * PI) / 180;
  const w = ((wt % (2 * PI)) + 2 * PI) % (2 * PI);
  let vo = 0;
  for (let k = 0; k < 3; k += 1) {
    const fire = PI / 6 + alpha + k * ((2 * PI) / 3);
    const vf = ((fire % (2 * PI)) + 2 * PI) % (2 * PI);
    const end = (vf + pulse) % (2 * PI);
    let inCond;
    if (vf <= end) inCond = w >= vf && w < end;
    else inCond = w >= vf || w < end;
    if (!inCond) continue;
    const v = vmPh * Math.sin(wt - k * ((2 * PI) / 3));
    vo = Math.max(vo, v);
  }
  return vo;
}

export function firingAnglesDeg(topology, alphaDeg) {
  const alpha = +alphaDeg;
  if (topology === "full3") {
    const fire0 = 30 + alpha;
    return Array.from({ length: 6 }, (_, i) => (fire0 + 60 * i) % 360);
  }
  if (topology === "hw3" || topology === "semi3") {
    return [30, 150, 270].map((b) => (alpha + b) % 360);
  }
  if (topology === "full1" || topology === "semi1") {
    return [0, 180].map((b) => (alpha + b) % 360);
  }
  return [alpha % 360];
}