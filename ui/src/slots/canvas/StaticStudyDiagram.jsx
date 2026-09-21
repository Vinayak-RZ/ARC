/** Read-only diagram (control blocks or one-line study) as SVG. Avoids React Flow mount issues. */

function captionFor(diagram) {
  const nodes = diagram?.nodes || [];
  if (nodes.some((n) => n.type === "equip")) {
    return "One-line study diagram from this run (read-only).";
  }
  return "Closed-loop block diagram from this run (read-only).";
}

function nodeCenter(n) {
  const x = Number(n.x) || 0;
  const y = Number(n.y) || 0;
  const w = n.type === "sum" ? 52 : n.type === "equip" ? 96 : 80;
  const h = n.type === "sum" ? 52 : 56;
  return { x: x + w / 2, y: y + h / 2, w, h };
}

export function StaticStudyDiagram({ diagram }) {
  const nodes = diagram?.nodes || [];
  const edges = diagram?.edges || [];
  const byId = Object.fromEntries(nodes.map((n) => [n.id, n]));
  const extra = [];
  if (!byId.r && !nodes.some((n) => n.type === "equip")) {
    extra.push({ id: "r", type: "ref", label: "r", x: 8, y: 128 });
  }
  if (!byId.y && !nodes.some((n) => n.type === "equip")) {
    extra.push({ id: "y", type: "tap", label: "y", x: 520, y: 128 });
  }
  const all = [...nodes, ...extra];
  const width = 720;
  const height = 320;

  return (
    <div className="static-diagram-wrap">
      <p className="hint">{captionFor(diagram)}</p>
      <svg
        className="static-diagram"
        viewBox={`0 0 ${width} ${height}`}
        width="100%"
        height="340"
        role="img"
        aria-label={captionFor(diagram)}
      >
        {edges.map((e) => {
          const from = byId[e.from] || extra.find((n) => n.id === e.from);
          const to = byId[e.to] || extra.find((n) => n.id === e.to);
          if (!from || !to) return null;
          const a = nodeCenter(from);
          const b = nodeCenter(to);
          return (
            <line
              key={e.id}
              x1={a.x + a.w / 2 - 8}
              y1={a.y}
              x2={b.x - b.w / 2 + 8}
              y2={b.y}
              stroke="var(--ee-color-ink)"
              strokeWidth="1.5"
              markerEnd="url(#arrow)"
            />
          );
        })}
        <defs>
          <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
            <path d="M0,0 L6,3 L0,6 Z" fill="var(--ee-color-ink)" />
          </marker>
        </defs>
        {all.map((n) => {
          const x = Number(n.x) || 0;
          const y = Number(n.y) || 0;
          if (n.type === "sum") {
            return (
              <g key={n.id}>
                <circle cx={x + 26} cy={y + 26} r="24" fill="var(--ee-color-surface-soft)" stroke="var(--ee-color-ink)" />
                <text x={x + 26} y={y + 31} textAnchor="middle" fontSize="16">Σ</text>
              </g>
            );
          }
          const w = n.type === "equip" ? 96 : n.type === "tap" || n.type === "ref" ? 44 : 80;
          const h = 56;
          return (
            <g key={n.id}>
              <rect
                x={x}
                y={y}
                width={w}
                height={h}
                rx="6"
                fill="var(--ee-color-canvas)"
                stroke="var(--ee-color-ink)"
                strokeWidth={n.type === "equip" ? 2 : 1}
              />
              <text x={x + w / 2} y={y + 22} textAnchor="middle" fontSize="13" fontWeight="500">
                {n.label || n.id}
              </text>
              {n.tf ? (
                <text x={x + w / 2} y={y + 40} textAnchor="middle" fontSize="11" fill="var(--ee-color-muted)">
                  {n.tf}
                </text>
              ) : null}
            </g>
          );
        })}
      </svg>
    </div>
  );
}
