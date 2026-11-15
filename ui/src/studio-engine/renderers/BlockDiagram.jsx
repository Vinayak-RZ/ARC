import { orthoPath } from "../geometry/route.js";
import { DiagramDefs, Wire } from "./Wire.jsx";

const GRID = 80;

export function BlockDiagram({ panel }) {
  const nodes = panel.nodes || [];
  const edges = panel.edges || [];
  const byId = Object.fromEntries(nodes.map((n) => [n.id, n]));
  let minX = 0;
  let minY = 0;
  let maxX = 200;
  let maxY = 120;
  for (const n of nodes) {
    const [ax, ay] = n.at || [0, 0];
    const x = ax * GRID;
    const y = ay * GRID;
    minX = Math.min(minX, x - 60);
    minY = Math.min(minY, y - 40);
    maxX = Math.max(maxX, x + 60);
    maxY = Math.max(maxY, y + 40);
  }
  const pad = 40;
  const vb = `${minX - pad} ${minY - pad} ${maxX - minX + 2 * pad} ${maxY - minY + 2 * pad}`;

  return (
    <svg className="se-block" viewBox={vb} role="img" aria-label={panel.title || "Block diagram"}>
      <DiagramDefs />
      <g style={{ color: "var(--ee-color-ink)" }}>
        {edges.map((e, i) => {
          const a = byId[e.from];
          const b = byId[e.to];
          if (!a || !b) return null;
          const x1 = (a.at?.[0] || 0) * GRID + 40;
          const y1 = (a.at?.[1] || 0) * GRID;
          const x2 = (b.at?.[0] || 0) * GRID - 40;
          const y2 = (b.at?.[1] || 0) * GRID;
          return <Wire key={i} d={orthoPath(x1, y1, x2, y2)} marker />;
        })}
        {nodes.map((n) => {
          const x = (n.at?.[0] || 0) * GRID;
          const y = (n.at?.[1] || 0) * GRID;
          if (n.type === "sum") {
            return (
              <g key={n.id} transform={`translate(${x} ${y})`}>
                <circle r={14} fill="var(--ee-color-surface-card)" stroke="currentColor" strokeWidth={1.75} />
                <text textAnchor="middle" dominantBaseline="central" fontSize="12">
                  Σ
                </text>
              </g>
            );
          }
          if (n.type === "input" || n.type === "output" || n.type === "takeoff") {
            return (
              <g key={n.id} transform={`translate(${x} ${y})`}>
                <text textAnchor="middle" fontSize="13" fill="var(--ee-color-body)">
                  {n.label || n.id}
                </text>
              </g>
            );
          }
          return (
            <g key={n.id} transform={`translate(${x} ${y})`}>
              <rect x={-40} y={-22} width={80} height={44} rx={4} fill="var(--ee-color-surface-card)" stroke="currentColor" strokeWidth={1.75} />
              <text y={-4} textAnchor="middle" fontSize="12" fill="var(--ee-color-body)">
                {n.label || n.id}
              </text>
              {n.tf ? (
                <text y={12} textAnchor="middle" fontSize="11" fontWeight="600" fill="var(--ee-color-ink)">
                  {n.tf}
                </text>
              ) : null}
            </g>
          );
        })}
      </g>
    </svg>
  );
}
