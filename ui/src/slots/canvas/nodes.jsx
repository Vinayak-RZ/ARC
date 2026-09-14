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

export function PartNode({ data, selected }) {
  const kind = data?.kind;
  const twoPort = kind !== "ground";
  return (
    <div className={selected ? "part-node is-selected" : "part-node"}>
      <Handle type="source" position={Position.Left} id="n1" />
      <Glyph kind={kind} />
      <span className="part-ref">{data?.refdes}</span>
      {twoPort ? <Handle type="source" position={Position.Right} id="n2" /> : null}
    </div>
  );
}

export const nodeTypes = { part: PartNode };
