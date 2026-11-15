import { SYMBOLS } from "../symbols/index.jsx";
import { pinPosition, routeWire } from "../geometry/route.js";
import { DiagramDefs, Wire } from "./Wire.jsx";

function parseEndpoint(ep, byId, grid) {
  // "r1.a" or {id, pin}
  let id;
  let pin;
  if (typeof ep === "string") {
    const i = ep.lastIndexOf(".");
    id = ep.slice(0, i);
    pin = ep.slice(i + 1);
  } else {
    id = ep.id;
    pin = ep.pin;
  }
  const comp = byId[id];
  if (!comp) return null;
  return pinPosition(comp, pin, grid);
}

export function Schematic({ panel }) {
  const grid = panel.grid || 40;
  const components = panel.components || [];
  const byId = Object.fromEntries(components.map((c) => [c.id, c]));
  const wires = (panel.wires || [])
    .map((w, i) => {
      const a = parseEndpoint(w.from, byId, grid);
      const b = parseEndpoint(w.to, byId, grid);
      if (!a || !b) return null;
      return { key: i, d: routeWire(a, b) };
    })
    .filter(Boolean);

  let minX = Infinity;
  let minY = Infinity;
  let maxX = -Infinity;
  let maxY = -Infinity;
  for (const c of components) {
    const [ax, ay] = c.at || [0, 0];
    const span = SYMBOLS[c.type]?.span || [1, 1];
    const x = ax * grid;
    const y = ay * grid;
    minX = Math.min(minX, x - span[0] * grid);
    minY = Math.min(minY, y - span[1] * grid);
    maxX = Math.max(maxX, x + span[0] * grid);
    maxY = Math.max(maxY, y + span[1] * grid);
  }
  if (!Number.isFinite(minX)) {
    minX = 0;
    minY = 0;
    maxX = 160;
    maxY = 100;
  }
  const pad = grid;
  const vb = `${minX - pad} ${minY - pad} ${maxX - minX + 2 * pad} ${maxY - minY + 2 * pad}`;

  return (
    <svg className="se-schematic" viewBox={vb} role="img" aria-label={panel.title || "Schematic"}>
      <DiagramDefs />
      <g className="se-wires" style={{ color: "var(--ee-color-ink)" }}>
        {wires.map((w) => (
          <Wire key={w.key} d={w.d} />
        ))}
      </g>
      {components.map((c) => {
        const sym = SYMBOLS[c.type];
        if (!sym) return null;
        const [ax, ay] = c.at || [0, 0];
        const x = ax * grid;
        const y = ay * grid;
        const Draw = sym.Draw;
        return (
          <g key={c.id} transform={`translate(${x} ${y}) rotate(${c.rot || 0})`} style={{ color: "var(--ee-color-ink)" }}>
            <Draw />
            {c.label ? (
              <text y={-18} textAnchor="middle" fontSize="13" fill="var(--ee-color-body)">
                {c.label}
              </text>
            ) : null}
            {c.value ? (
              <text y={22} textAnchor="middle" fontSize="13" fontWeight="600" fill="var(--ee-color-ink)">
                {c.value}
              </text>
            ) : null}
          </g>
        );
      })}
      {(panel.probes || []).map((p, i) => {
        const pos = parseEndpoint(p.at, byId, grid);
        if (!pos) return null;
        return (
          <g key={i} style={{ color: "var(--ee-color-primary)" }}>
            <circle cx={pos.x} cy={pos.y} r={4} fill="currentColor" />
            <text x={pos.x + 8} y={pos.y - 8} fontSize="13" fill="currentColor">
              {p.label}
            </text>
          </g>
        );
      })}
    </svg>
  );
}
