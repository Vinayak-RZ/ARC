import { Handle, Position } from "@xyflow/react";

function Glyph({ kind }) {
  if (kind === "capacitor") {
    return (
      <svg width="26" height="14" aria-hidden="true">
        <path d="M1 7 H10 M16 7 H25 M10 1 V13 M16 1 V13" fill="none" stroke="currentColor" strokeWidth="1.6" />
      </svg>
    );
  }
  if (kind === "inductor") {
    return (
      <svg width="26" height="14" aria-hidden="true">
        <path d="M1 7 H5 a3.5 3.5 0 0 1 7 0 a3.5 3.5 0 0 1 7 0 H25" fill="none" stroke="currentColor" strokeWidth="1.6" />
      </svg>
    );
  }
  if (kind === "source_v") {
    return (
      <svg width="24" height="20" aria-hidden="true">
        <circle cx="12" cy="10" r="8" fill="none" stroke="currentColor" strokeWidth="1.6" />
        <text x="7.5" y="11" textAnchor="middle" fontSize="10" fontWeight="600" fill="currentColor">
          +
        </text>
        <text x="16.5" y="11" textAnchor="middle" fontSize="10" fontWeight="600" fill="currentColor">
          −
        </text>
      </svg>
    );
  }
  if (kind === "source_i") {
    return (
      <svg width="20" height="20" aria-hidden="true">
        <circle cx="10" cy="10" r="8" fill="none" stroke="currentColor" strokeWidth="1.6" />
        <path d="M10 4 V15 M7 12 L10 15 L13 12" fill="none" stroke="currentColor" strokeWidth="1.6" />
      </svg>
    );
  }
  if (kind === "ground") {
    return (
      <svg width="20" height="14" aria-hidden="true">
        <path d="M10 1 V6 M3 6 H17 M5 9 H15 M7 12 H13" fill="none" stroke="currentColor" strokeWidth="1.6" />
      </svg>
    );
  }
  return (
    <svg width="28" height="12" aria-hidden="true">
      <path d="M1 6 H5 L8 1 L14 11 L17 1 L20 11 L23 6 H27" fill="none" stroke="currentColor" strokeWidth="1.6" />
    </svg>
  );
}

function formatPartValue(kind, value, unit) {
  if (value == null || kind === "ground") return "";
  const v = Number(value);
  if (Number.isNaN(v)) return "";
  if (kind === "resistor") {
    if (v >= 1_000_000) return `${(v / 1_000_000).toFixed(1)} MΩ`;
    if (v >= 1000) return `${(v / 1000).toFixed(v % 1000 === 0 ? 0 : 1)} kΩ`;
    return `${v} Ω`;
  }
  if (kind === "capacitor") {
    if (v < 1e-6) return `${(v * 1e9).toFixed(0)} nF`;
    if (v < 1e-3) return `${(v * 1e6).toFixed(v * 1e6 >= 10 ? 0 : 1)} µF`;
    if (v < 1) return `${(v * 1e3).toFixed(1)} mF`;
    return `${v} F`;
  }
  if (kind === "inductor") {
    if (v <= 1e-3) return `${(v * 1e3).toFixed(1)} mH`;
    return `${v} H`;
  }
  if (kind === "source_v") return `${v} V`;
  if (kind === "source_i") return `${v} A`;
  return unit ? `${v} ${unit}` : String(v);
}

export function JunctionNode({ selected }) {
  const ports = [
    ["n", Position.Top],
    ["e", Position.Right],
    ["s", Position.Bottom],
    ["w", Position.Left],
  ];
  return (
    <div className={selected ? "junction-node is-selected" : "junction-node"}>
      {ports.map(([id, pos]) => (
        <Handle key={id} type="source" position={pos} id={id} className="circuit-port" />
      ))}
    </div>
  );
}

export function PartNode({ data, selected }) {
  const kind = data?.kind;
  if (kind === "junction") return <JunctionNode selected={selected} />;
  const rot = Number(data?.rot) === 90 ? 90 : 0;
  const twoPort = kind !== "ground";
  const vertical = rot === 90;
  const n1Pos = vertical ? Position.Top : Position.Left;
  const n2Pos = vertical ? Position.Bottom : Position.Right;
  const valueLabel = formatPartValue(kind, data?.value, data?.unit);
  return (
    <div className={["part-node", selected ? "is-selected" : "", vertical ? "is-vertical" : ""].filter(Boolean).join(" ")}>
      {twoPort ? <Handle type="source" position={n1Pos} id="n1" className="circuit-port" /> : <Handle type="source" position={Position.Top} id="n1" className="circuit-port" />}
      <Glyph kind={kind} />
      <span className="part-ref">{data?.refdes}</span>
      {valueLabel ? <span className="part-value">{valueLabel}</span> : null}
      {data?.diffChip ? <span className="lab-changes-chip part-diff-chip">{data.diffChip}</span> : null}
      {data?.ghost ? <span className="part-diff-ghost-tag">−</span> : null}
      {twoPort ? <Handle type="source" position={n2Pos} id="n2" className="circuit-port" /> : null}
    </div>
  );
}

export const nodeTypes = { part: PartNode };
