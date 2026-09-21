/** Manhattan paths between anchor points {x,y} with optional arrow at end. */

export function orthoPath(x1, y1, x2, y2) {
  if (Math.abs(y1 - y2) < 1) {
    return `M ${x1} ${y1} H ${x2}`;
  }
  if (Math.abs(x1 - x2) < 1) {
    return `M ${x1} ${y1} V ${y2}`;
  }
  const midX = (x1 + x2) / 2;
  return `M ${x1} ${y1} H ${midX} V ${y2} H ${x2}`;
}

export function DiagramDefs() {
  return (
    <defs>
      <marker id="ee-arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L7,3 L0,6 Z" fill="currentColor" />
      </marker>
      <marker id="ee-arrow-start" markerWidth="8" markerHeight="8" refX="0" refY="3" orient="auto" markerUnits="strokeWidth">
        <path d="M7,0 L0,3 L7,6 Z" fill="currentColor" />
      </marker>
    </defs>
  );
}

export function Wire({ d, dashed = false, marker = true }) {
  return (
    <path
      d={d}
      fill="none"
      stroke="currentColor"
      strokeWidth="1.75"
      strokeDasharray={dashed ? "6 4" : undefined}
      markerEnd={marker ? "url(#ee-arrow)" : undefined}
    />
  );
}
