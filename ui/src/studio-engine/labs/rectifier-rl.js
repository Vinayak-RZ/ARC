/** RL/RLE conduction mode: continuous (large L) vs finite-L ODE in gate model. */

const PI = Math.PI;

export const FINITE_L_THRESHOLD_H = 0.002;

export function loadInductanceH(p) {
  const load = p.load || "R";
  if (load !== "RL" && load !== "RLE") return 0;
  if (p.l_h != null && p.l_h > 0) return Number(p.l_h);
  if (load === "RL") return 0.01;
  return Number(p.l_h || 0.01);
}

/** Whether load uses explicit small L (always gate ODE). */
export function rectifierRlFiniteL(p) {
  const lh = loadInductanceH(p);
  return lh > 0 && lh < FINITE_L_THRESHOLD_H;
}

/** 1φ full bridge, stiff load current: v_o = V_m sin(ωt) from α to π+α. */
export function voFull1RlContinuous(wt, vm, alphaDeg) {
  const a = (alphaDeg * PI) / 180;
  const beta = PI + a;
  const w = ((wt % (2 * PI)) + 2 * PI) % (2 * PI);
  if (w >= a && w < beta) return vm * Math.sin(wt);
  return 0;
}

/** 1φ semi with freewheel: terminal follows source sine while thyristor+firediode conduct (α .. π+α). */
export function voSemi1RlContinuous(wt, vm, alphaDeg) {
  const a = (alphaDeg * PI) / 180;
  const cycle = ((wt % PI) + PI) % PI;
  if (cycle < a) return 0;
  const beta = PI + a;
  const w = ((wt % (2 * PI)) + 2 * PI) % (2 * PI);
  if (w >= a && w < beta) return vm * Math.sin(wt);
  return 0;
}