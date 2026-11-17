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
  if (v < 0.0005) return "0.000%";
  if (v < 0.05) return `${v.toFixed(3)}%`;
  if (v < 0.15) return `${v.toFixed(2)}%`;
  return `${v.toFixed(1)}%`;
}

export function formatRelTolPct(limitPct) {
  if (limitPct == null || Number.isNaN(Number(limitPct))) return "2%";
  const v = Number(limitPct);
  if (v < 0.15) return `${v.toFixed(2)}%`;
  if (v < 1) return `${v.toFixed(2)}%`;
  return `${v.toFixed(1)}%`;
}