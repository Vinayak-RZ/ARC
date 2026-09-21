/** IIT-style series R–L–C sheet schematic (orthogonal, symbol glyphs). */

function pickNode(graph, id) {
  return (graph?.nodes || []).find((n) => n.id === id) || {};
}

function sheetLabel(kind, refdes, value) {
  const v = Number(value);
  if (Number.isNaN(v)) return refdes;
  if (kind === "source_v") return `${refdes}=${v} V`;
  if (kind === "resistor") {
    if (v >= 1000) return `${refdes}=${v / 1000} kΩ`;
    return `${refdes}=${v} Ω`;
  }
  if (kind === "inductor") {
    if (v <= 1e-3) return `${refdes}=${(v * 1e3).toFixed(0)} mH`;
    return `${refdes}=${v} H`;
  }
  if (kind === "capacitor") {
    if (v <= 1e-6) return `${refdes}=${(v * 1e6).toFixed(0)} µF`;
    return `${refdes}=${v} F`;
  }
  return refdes;
}

function Battery({ x, y }) {
  return (
    <g transform={`translate(${x},${y})`}>
      <line x1="0" y1="0" x2="0" y2="28" stroke="currentColor" strokeWidth="2" />
      <line x1="-10" y1="0" x2="10" y2="0" stroke="currentColor" strokeWidth="3" />
      <line x1="-6" y1="8" x2="6" y2="8" stroke="currentColor" strokeWidth="1.5" />
    </g>
  );
}

function ResistorZigzag({ x, y }) {
  return (
    <path
      d={`M ${x} ${y + 14} h 8 l 6 -10 l 6 20 l 6 -20 l 6 20 l 6 -10 h 8`}
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
    />
  );
}

function InductorCoil({ x, y }) {
  const cy = y + 14;
  return (
    <path
      d={`M ${x} ${cy} h 5 q 7 -10 14 0 q 7 10 14 0 q 7 -10 14 0 h 5`}
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
    />
  );
}

function CapacitorPlates({ x, y }) {
  return (
    <g stroke="currentColor" strokeWidth="2">
      <line x1={x + 18} y1={y + 4} x2={x + 18} y2={y + 24} />
      <line x1={x + 30} y1={y + 4} x2={x + 30} y2={y + 24} />
      <line x1={x} y1={y + 14} x2={x + 18} y2={y + 14} />
      <line x1={x + 30} y1={y + 14} x2={x + 48} y2={y + 14} />
    </g>
  );
}

function GroundSymbol({ x, y }) {
  return (
    <g stroke="currentColor" strokeWidth="2" fill="none">
      <line x1={x} y1={y} x2={x} y2={y + 10} />
      <line x1={x - 14} y1={y + 10} x2={x + 14} y2={y + 10} />
      <line x1={x - 9} y1={y + 16} x2={x + 9} y2={y + 16} />
      <line x1={x - 5} y1={y + 22} x2={x + 5} y2={y + 22} />
    </g>
  );
}

export function isSeriesRlcSheetGraph(graph) {
  const nodes = graph?.nodes || [];
  if (nodes.length !== 5) return false;
  const ids = new Set(nodes.map((n) => n.id));
  return ids.has("vin") && ids.has("r1") && ids.has("l1") && ids.has("c1") && ids.has("gnd");
}

export function SeriesRlcSchematic({ graph }) {
  const vin = pickNode(graph, "vin");
  const r1 = pickNode(graph, "r1");
  const l1 = pickNode(graph, "l1");
  const c1 = pickNode(graph, "c1");
  const yTop = 72;
  const yBot = 168;
  const xV = 48;
  const xR = 168;
  const xL = 288;
  const xC = 408;
  const xEnd = 528;

  const labels = [
    { x: xV, text: sheetLabel("source_v", vin.refdes || "V1", vin.value) },
    { x: xR, text: sheetLabel("resistor", r1.refdes || "R1", r1.value) },
    { x: xL, text: sheetLabel("inductor", l1.refdes || "L1", l1.value) },
    { x: xC, text: sheetLabel("capacitor", c1.refdes || "C1", c1.value) },
  ];

  return (
    <div className="static-diagram-wrap">
      <p className="hint">Series R–L–C (tutorial sheet style, read-only seed).</p>
      <svg
        className="static-diagram series-rlc-schematic"
        viewBox="0 0 600 220"
        width="100%"
        height="280"
        role="img"
        aria-label="Series RLC schematic"
      >
        <g className="schematic-ink" style={{ color: "var(--ee-color-ink)" }}>
          {labels.map((lb) => (
            <text key={lb.text} x={lb.x} y={36} textAnchor="middle" fontSize="12" fontWeight="500">
              {lb.text}
            </text>
          ))}
          <line x1={xV} y1={yTop} x2={xEnd} y2={yTop} stroke="currentColor" strokeWidth="2" />
          <line x1={xV} y1={yTop} x2={xV} y2={yBot} stroke="currentColor" strokeWidth="2" />
          <line x1={xV} y1={yBot} x2={xC + 24} y2={yBot} stroke="currentColor" strokeWidth="2" />
          <line x1={xC + 24} y1={yTop} x2={xC + 24} y2={yBot} stroke="currentColor" strokeWidth="2" />
          <Battery x={xV} y={yTop} />
          <ResistorZigzag x={xR} y={yTop} />
          <InductorCoil x={xL} y={yTop} />
          <CapacitorPlates x={xC} y={yTop} />
          <GroundSymbol x={xV} y={yBot} />
        </g>
      </svg>
    </div>
  );
}
