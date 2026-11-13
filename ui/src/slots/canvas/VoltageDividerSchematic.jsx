/** Textbook-style voltage divider (orthogonal, parts above wires). */

function pickNode(graph, id) {
  return (graph?.nodes || []).find((n) => n.id === id) || {};
}

function fmtResistor(refdes, value) {
  const v = Number(value);
  if (Number.isNaN(v)) return refdes;
  if (v >= 1000) return `${refdes}=${v / 1000} kΩ`;
  return `${refdes}=${v} Ω`;
}

function fmtVin(refdes, value) {
  return `${refdes}=${Number(value)} V`;
}

export function isVoltageDividerGraph(graph) {
  const nodes = graph?.nodes || [];
  if (nodes.length !== 4) return false;
  const kinds = new Map(nodes.map((n) => [n.id, n.type]));
  return (
    kinds.get("vin") === "source_v" &&
    kinds.get("r1") === "resistor" &&
    kinds.get("r2") === "resistor" &&
    kinds.get("gnd") === "ground"
  );
}

function VerticalSource({ x, y1, y2 }) {
  const cy = (y1 + y2) / 2;
  return (
    <g stroke="currentColor" fill="none" strokeWidth="2">
      <line x1={x - 12} y1={cy - 12} x2={x + 12} y2={cy - 12} strokeWidth="3" />
      <line x1={x - 8} y1={cy - 4} x2={x + 8} y2={cy - 4} />
    </g>
  );
}

function ResistorH({ x1, y, x2 }) {
  const w = x2 - x1;
  return (
    <path
      d={`M ${x1} ${y} h ${w * 0.15} l ${w * 0.05} -7 l ${w * 0.08} 14 l ${w * 0.08} -14 l ${w * 0.08} 14 l ${w * 0.08} -14 l ${w * 0.05} 7 h ${w * 0.15}`}
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
    />
  );
}

function ResistorV({ x, y1, y2 }) {
  const h = y2 - y1;
  return (
    <path
      d={`M ${x} ${y1} v ${h * 0.15} l -8 ${h * 0.08} l 16 ${h * 0.1} l -16 ${h * 0.1} l 16 ${h * 0.1} l -16 ${h * 0.1} l 8 ${h * 0.08} v ${h * 0.15}`}
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
    />
  );
}

function Ground({ x, y }) {
  return (
    <g stroke="currentColor" strokeWidth="2" fill="none">
      <line x1={x} y1={y - 10} x2={x} y2={y} />
      <line x1={x - 14} y1={y} x2={x + 14} y2={y} />
      <line x1={x - 9} y1={y + 6} x2={x + 9} y2={y + 6} />
      <line x1={x - 5} y1={y + 12} x2={x + 5} y2={y + 12} />
    </g>
  );
}

export function VoltageDividerSchematic({ graph }) {
  const vin = pickNode(graph, "vin");
  const r1 = pickNode(graph, "r1");
  const r2 = pickNode(graph, "r2");
  const xL = 80;
  const xJ = 320;
  const yTop = 72;
  const yBot = 200;

  return (
    <div className="static-diagram-wrap schematic-fit">
      <svg
        className="static-diagram voltage-divider-schematic"
        viewBox="0 0 440 240"
        width="100%"
        height="100%"
        preserveAspectRatio="xMidYMid meet"
        role="img"
        aria-label="Voltage divider schematic"
      >
        <g className="schematic-wires" stroke="var(--ee-color-ink)" strokeWidth="2" fill="none">
          <line x1={xL} y1={yTop} x2={xJ} y2={yTop} />
          <line x1={xL} y1={yTop} x2={xL} y2={yBot} />
          <line x1={xJ} y1={yTop} x2={xJ} y2={yBot} />
          <line x1={xL} y1={yBot} x2={xJ} y2={yBot} />
        </g>
        <g className="schematic-parts" style={{ color: "var(--ee-color-ink)" }}>
          <text x={xL - 16} y={(yTop + yBot) / 2} textAnchor="end" fontSize="12" fontWeight="500" dominantBaseline="middle">
            V<tspan baselineShift="sub" fontSize="9">
              in
            </tspan>
            {" = "}
            {Number(vin.value ?? 10)} V
          </text>
          <text x={(xL + xJ) / 2} y={50} textAnchor="middle" fontSize="12" fontWeight="500">
            R<tspan baselineShift="sub" fontSize="9">
              1
            </tspan>
            {" = "}
            {Number(r1.value ?? 1000) >= 1000 ? `${Number(r1.value ?? 1000) / 1000} kΩ` : `${r1.value ?? 1000} Ω`}
          </text>
          <text x={xJ + 20} y={(yTop + yBot) / 2} fontSize="12" fontWeight="500" dominantBaseline="middle">
            R<tspan baselineShift="sub" fontSize="9">
              2
            </tspan>
            {" = "}
            {Number(r2.value ?? 1000) >= 1000 ? `${Number(r2.value ?? 1000) / 1000} kΩ` : `${r2.value ?? 1000} Ω`}
          </text>
          <ResistorH x1={xL + 8} x2={xJ - 8} y={yTop} />
          <ResistorV x={xJ} y1={yTop + 6} y2={yBot - 6} />
          <VerticalSource x={xL} y1={yTop + 4} y2={yBot - 4} />
          <Ground x={xL} y={yBot + 14} />
        </g>
      </svg>
    </div>
  );
}
