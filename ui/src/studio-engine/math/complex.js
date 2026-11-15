/** Minimal complex helpers for Bode labs. */

export function cAdd(a, b) {
  return [a[0] + b[0], a[1] + b[1]];
}

export function cMul(a, b) {
  return [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]];
}

export function cDiv(a, b) {
  const d = b[0] * b[0] + b[1] * b[1];
  return [(a[0] * b[0] + a[1] * b[1]) / d, (a[1] * b[0] - a[0] * b[1]) / d];
}

/** Evaluate polynomial coeffs (highest first) at complex s. */
export function polyval(coeffs, s) {
  let acc = [0, 0];
  for (const c of coeffs) {
    acc = cAdd(cMul(acc, s), [c, 0]);
  }
  return acc;
}
