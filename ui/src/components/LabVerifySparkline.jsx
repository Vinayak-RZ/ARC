/** Inline SVG sparkline for verify aside. */

function xScale(points, width) {
  const xs = points.map((p) => p[0]);
  const xmin = Math.min(...xs);
  const xmax = Math.max(...xs);
  const span = xmax - xmin || 1;
  return (x) => ((x - xmin) / span) * width;
}

function yScale(points, height, hline, pad = 4) {
  const ys = points.map((p) => p[1]);
  let ymin = Math.min(...ys);
  let ymax = Math.max(...ys);
  if (hline != null) {
    ymin = Math.min(ymin, hline);
    ymax = Math.max(ymax, hline);
  }
  const span = ymax - ymin || 1;
  return (y) => height - pad - ((y - ymin) / span) * (height - 2 * pad);
}

export function LabVerifySparkline({ spec, width = 160, height = 48 }) {
  if (!spec?.points?.length) return null;
  const { points, hline, marker } = spec;
  const sx = xScale(points, width);
  const sy = yScale(points, height, hline, 4);
  const d = points
    .map((p, i) => `${i === 0 ? "M" : "L"}${sx(p[0]).toFixed(2)},${sy(p[1]).toFixed(2)}`)
    .join(" ");
  const markerEl =
    marker && Number.isFinite(marker.x) ? (
      <circle
        cx={sx(marker.x)}
        cy={sy(points.find((p) => Math.abs(p[0] - marker.x) < 1e-6)?.[1] ?? points[0][1])}
        r="3"
        className="lab-verify-spark-marker"
      />
    ) : null;
  const hlineY = hline != null ? sy(hline) : null;
  return (
    <svg
      className="lab-verify-sparkline"
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      role="img"
      aria-hidden
    >
      {hlineY != null ? (
        <line x1={0} y1={hlineY} x2={width} y2={hlineY} className="lab-verify-spark-hline" strokeDasharray="3 2" />
      ) : null}
      <path d={d} className="lab-verify-spark-path" fill="none" />
      {markerEl}
    </svg>
  );
}