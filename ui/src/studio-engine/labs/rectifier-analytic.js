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