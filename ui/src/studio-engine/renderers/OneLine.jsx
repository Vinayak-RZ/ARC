import { DiagramDefs, Wire } from "./Wire.jsx";
import { orthoPath } from "../geometry/route.js";

const GRID = 80;

export function OneLine({ panel }) {
  const buses = panel.buses || [];
  const elements = panel.elements || [];
  const byBus = Object.fromEntries(buses.map((b) => [b.id, b]));
  let minX = 0;
  let minY = 0;
  let maxX = 240;
  let maxY = 160;
  for (const b of buses) {
    const x = (b.at?.[0] || 0) * GRID;
    const y = (b.at?.[1] || 0) * GRID;
    minX = Math.min(minX, x - 40);
    minY = Math.min(minY, y - 40);
    maxX = Math.max(maxX, x + 40);
    maxY = Math.max(maxY, y + 40);
  }
  const pad = 40;
  const vb = `${minX - pad} ${minY - pad} ${maxX - minX + 2 * pad} ${maxY - minY + 2 * pad}`;

  return (
    <svg className="se-oneline" viewBox={vb} role="img" aria-label={panel.title || "One-line diagram"}>
      <DiagramDefs />
      <g style={{ color: "var(--ee-color-ink)" }}>
        {buses.map((b) => {
          const x = (b.at?.[0] || 0) * GRID;
          const y = (b.at?.[1] || 0) * GRID;
          return (
            <g key={b.id}>
              <line x1={x - 28} y1={y} x2={x + 28} y2={y} stroke="currentColor" strokeWidth={4} />
              <text x={x} y={y - 12} textAnchor="middle" fontSize="12" fill="var(--ee-color-body)">
                {b.label || b.id}
                {b.kv != null ? ` ${b.kv} kV` : ""}
              </text>
            </g>
          );
        })}
        {elements.map((el) => {
          if (el.type === "line" || el.type === "xfmr") {
            const a = byBus[el.from];
            const b = byBus[el.to];
            if (!a || !b) return null;
            const x1 = (a.at?.[0] || 0) * GRID;
            const y1 = (a.at?.[1] || 0) * GRID;
            const x2 = (b.at?.[0] || 0) * GRID;
            const y2 = (b.at?.[1] || 0) * GRID;
            return <Wire key={el.id} d={orthoPath(x1, y1, x2, y2)} />;
          }
          const bus = byBus[el.bus];
          if (!bus) return null;
          const x = (bus.at?.[0] || 0) * GRID;
          const y = (bus.at?.[1] || 0) * GRID;
          if (el.type === "gen") {
            return (
              <g key={el.id} transform={`translate(${x} ${y + 36})`}>
                <circle r={12} fill="none" stroke="currentColor" strokeWidth={1.75} />
                <text textAnchor="middle" dominantBaseline="central" fontSize="11">
                  ~
                </text>
                <text y={22} textAnchor="middle" fontSize="11" fill="var(--ee-color-body)">
                  {el.label}
                </text>
              </g>
            );
          }
          if (el.type === "load") {
            return (
              <g key={el.id} transform={`translate(${x} ${y + 28})`}>
                <path d="M 0 0 V 16 M -6 16 L 0 24 L 6 16" fill="none" stroke="currentColor" strokeWidth={1.75} />
                <text y={36} textAnchor="middle" fontSize="11" fill="var(--ee-color-body)">
                  {el.label}
                </text>
              </g>
            );
          }
          if (el.type === "breaker") {
            return (
              <rect key={el.id} x={x - 6} y={y - 6} width={12} height={12} fill="var(--ee-color-surface-card)" stroke="currentColor" strokeWidth={1.75} />
            );
          }
          if (el.type === "relay") {
            return (
              <g key={el.id} transform={`translate(${x + 24} ${y - 24})`}>
                <circle r={10} fill="var(--ee-color-primary-tint)" stroke="var(--ee-color-primary)" strokeWidth={1.5} />
                <text textAnchor="middle" dominantBaseline="central" fontSize="10" fill="var(--ee-color-primary-ink)">
                  {el.label || "51"}
                </text>
              </g>
            );
          }
          if (el.type === "fault") {
            return (
              <g key={el.id} transform={`translate(${x} ${y - 28})`} style={{ color: "var(--ee-semantic-down)" }}>
                <path d="M 0 -10 L 4 0 L -2 0 L 2 12" fill="currentColor" />
                <text y={20} textAnchor="middle" fontSize="11" fill="currentColor">
                  {el.label || "F"}
                </text>
              </g>
            );
          }
          return null;
        })}
      </g>
    </svg>
  );
}
