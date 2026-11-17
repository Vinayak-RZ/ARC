// Axis bounds for the Waveform renderer. Pure, so node --test can cover it.

function expandBounds(xMin, xMax, yMin, yMax, logX, logY) {
  if (logX && xMin > 0 && xMax > 0) {
    const lo = Math.log10(xMin);
    const hi = Math.log10(xMax);
    const d = hi - lo || 1;
    xMin = 10 ** (lo - d * 0.06);
    xMax = 10 ** (hi + d * 0.04);
  } else {
    const xPad = (xMax - xMin) * 0.04 || 0.1;
    xMin -= xPad;
    xMax += xPad;
  }
  if (logY && yMin > 0 && yMax > 0) {
    const lo = Math.log10(yMin);
    const hi = Math.log10(yMax);
    const d = hi - lo || 1;
    yMin = 10 ** (lo - d * 0.1);
    yMax = 10 ** (hi + d * 0.12);
  } else {
    const yPad = (yMax - yMin) * 0.1 || 0.1;
    yMin -= yPad;
    yMax += yPad;
  }
  return { xMin, xMax, yMin, yMax };
}

/**
 * Data bounds with padding. When the panel's y axis carries finite `min` and
 * `max` (min < max), the y range is held exactly there instead of autoscaling.
 */
export function waveformBounds(series, panel = {}) {
  let xMin = Infinity;
  let xMax = -Infinity;
  let yMin = Infinity;
  let yMax = -Infinity;
  for (const s of series || []) {
    for (const [x, y] of s.points || []) {
      xMin = Math.min(xMin, x);
      xMax = Math.max(xMax, x);
      yMin = Math.min(yMin, y);
      yMax = Math.max(yMax, y);
    }
  }
  if (!Number.isFinite(xMin)) return { xMin: 0, xMax: 1, yMin: 0, yMax: 1 };
  if (yMin === yMax) {
    yMin -= 1;
    yMax += 1;
  }
  const logX = panel.x?.scale === "log";
  const logY = panel.y?.scale === "log";
  const out = expandBounds(xMin, xMax, yMin, yMax, logX, logY);
  const fixMin = panel.y?.min;
  const fixMax = panel.y?.max;
  if (Number.isFinite(fixMin) && Number.isFinite(fixMax) && fixMin < fixMax) {
    out.yMin = fixMin;
    out.yMax = fixMax;
  }
  return out;
}
