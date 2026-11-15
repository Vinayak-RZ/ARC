export function DiagramDefs() {
  return (
    <defs>
      <marker id="se-arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L7,3 L0,6 Z" fill="currentColor" />
      </marker>
    </defs>
  );
}

export function Wire({ d, dashed = false, marker = false }) {
  return (
    <path
      d={d}
      fill="none"
      stroke="currentColor"
      strokeWidth="1.75"
      strokeDasharray={dashed ? "6 4" : undefined}
      markerEnd={marker ? "url(#se-arrow)" : undefined}
      vectorEffect="non-scaling-stroke"
    />
  );
}
