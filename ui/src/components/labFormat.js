/** Shared number formatting for derived vs simulated rows. */

export function formatLabValue(n, unit = "") {
  if (n == null || Number.isNaN(Number(n))) return "—";
  const v = Number(n);
  let text;
  if (unit === "s" && Math.abs(v) > 0 && Math.abs(v) < 1) {
    return `${(v * 1000).toFixed(3)} ms`;
  }
  if (Math.abs(v) >= 1000 || (Math.abs(v) > 0 && Math.abs(v) < 0.001)) {
    text = v.toExponential(3);
  } else {
    text = v.toFixed(3);
  }
  return unit ? `${text} ${unit}` : text;
}

export function formatDiffPct(pct) {
  if (pct == null || Number.isNaN(Number(pct))) return "—";
  const v = Number(pct);
  if (v < 0.05) return "0.0%";
  return `${v.toFixed(1)}%`;
}