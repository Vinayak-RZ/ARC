import { Handle, Position } from "@xyflow/react";

function Glyph({ kind }) {
  if (kind === "capacitor") {
    return (
      <svg width="36" height="20" aria-hidden="true">
        <path d="M2 10 H14 M22 10 H34 M14 2 V18 M22 2 V18" fill="none" stroke="currentColor" strokeWidth="2" />
      </svg>
    );
  }
  if (kind === "inductor") {
    return (
      <svg width="36" height="20" aria-hidden="true">
        <path d="M2 10 H8 a5 5 0 0 1 10 0 a5 5 0 0 1 10 0 H34" fill="none" stroke="currentColor" strokeWidth="2" />
      </svg>
    );
  }
  if (kind === "source_v") {
    return (
      <svg width="28" height="28" aria-hidden="true">
        <circle cx="14" cy="14" r="12" fill="none" stroke="currentColor" strokeWidth="2" />
        <text x="14" y="18" textAnchor="middle" fontSize="12" fill="currentColor">
          V
        </text>
      </svg>
    );
  }
  if (kind === "source_i") {
    return (
      <svg width="28" height="28" aria-hidden="true">
        <circle cx="14" cy="14" r="12" fill="none" stroke="currentColor" strokeWidth="2" />
        <path d="M14 6 V20 M10 16 L14 20 L18 16" fill="none" stroke="currentColor" strokeWidth="2" />
      </svg>
    );
  }
  if (kind === "ground") {
    return (
      <svg width="28" height="20" aria-hidden="true">
        <path d="M14 2 V8 M6 8 H22 M8 12 H20 M11 16 H17" fill="none" stroke="currentColor" strokeWidth="2" />
      </svg>
    );
  }
  return (
    <svg width="40" height="16" aria-hidden="true">
      <path d="M2 8 H8 L12 2 L20 14 L24 2 L28 14 L32 8 H38" fill="none" stroke="currentColor" strokeWidth="2" />
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
    if (v <= 1e-6) return `${(v * 1e6).toFixed(1)} µF`;
    if (v <= 1e-3) return `${(v * 1e3).toFixed(1)} mF`;
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

export function PartNode({ data, selected }) {
  const kind = data?.kind;
  const rot = Number(data?.rot) === 90 ? 90 : 0;
  const twoPort = kind !== "ground";
  const vertical = rot === 90;
  const n1Pos = vertical ? Position.Top : Position.Left;
  const n2Pos = vertical ? Position.Bottom : Position.Right;
  const valueLabel = formatPartValue(kind, data?.value, data?.unit);
  return (
    <div className={["part-node", selected ? "is-selected" : "", vertical ? "is-vertical" : ""].filter(Boolean).join(" ")}>
      {twoPort ? <Handle type="source" position={n1Pos} id="n1" /> : <Handle type="source" position={Position.Top} id="n1" />}
      <Glyph kind={kind} />
      <span className="part-ref">{data?.refdes}</span>
      {valueLabel ? <span className="part-value">{valueLabel}</span> : null}
      {twoPort ? <Handle type="source" position={n2Pos} id="n2" /> : null}
    </div>
  );
}

export const nodeTypes = { part: PartNode };
