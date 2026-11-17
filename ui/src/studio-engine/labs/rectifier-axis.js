/**
 * Parse an optional fixed y axis from a query string: ?ymax=600 (ymin defaults to 0).
 * Returns { min, max } or null when absent or invalid, so the plot keeps autoscaling.
 */
export function fixedYAxisFromSearch(search) {
  const q = new URLSearchParams(search || "");
  if (!q.has("ymax")) return null;
  const max = Number(q.get("ymax"));
  const min = q.has("ymin") ? Number(q.get("ymin")) : 0;
  if (!Number.isFinite(max) || !Number.isFinite(min) || !(min < max)) return null;
  return { min, max };
}
