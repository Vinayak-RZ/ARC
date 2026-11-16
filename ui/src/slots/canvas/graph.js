export const SCHEMA = "arc.circuit.v1";
export const MAX_NODES = 16;
export const MAX_EDGES = 24;

export const PARTS = [
  { type: "resistor", label: "Resistor", unit: "ohm", prefix: "R" },
  { type: "capacitor", label: "Capacitor", unit: "F", prefix: "C" },
  { type: "inductor", label: "Inductor", unit: "H", prefix: "L" },
  { type: "source_v", label: "Voltage", unit: "V", prefix: "V" },
  { type: "source_i", label: "Current", unit: "A", prefix: "I" },
  { type: "ground", label: "Ground", unit: "", prefix: "Gnd" },
];

const PREFIX = Object.fromEntries(PARTS.map((p) => [p.type, p.prefix.toLowerCase()]));

export function toFlow(graph) {
  const src = graph && typeof graph === "object" ? graph : {};
  const nodes = (src.nodes || []).map((n) => ({
    id: String(n.id),
    type: "part",
    position: { x: Number(n.x) || 0, y: Number(n.y) || 0 },
    data: {
        kind: n.type,
        refdes: n.refdes || n.id,
        value: n.value,
        unit: n.unit || "",
        rot: Number(n.rot) === 90 ? 90 : 0,
      },
  }));
  const edges = (src.edges || []).map((e) => {
    const [source, sourceHandle] = String(e.from).split(".");
    const [target, targetHandle] = String(e.to).split(".");
    return {
      id: String(e.id),
      source,
      target,
      sourceHandle: sourceHandle || "n1",
      targetHandle: targetHandle || "n1",
      type: "step",
    };
  });
  return { nodes, edges };
}

/** Read V/R/L/C from a series RLC flow graph (first of each kind). */
export function seriesRlcParamsFromFlow(nodes, edges) {
  const graph = fromFlow(nodes, edges);
  const byType = (t) => (graph.nodes || []).find((n) => n.type === t);
  const src = byType("source_v");
  const res = byType("resistor");
  const ind = byType("inductor");
  const cap = byType("capacitor");
  if (!src || !res || !ind || !cap) return null;
  const v = Number(src.value);
  const r = Number(res.value);
  const l = Number(ind.value);
  const c = Number(cap.value);
  if (![v, r, l, c].every((x) => Number.isFinite(x))) return null;
  return { v_step: v, vin: v, r_ohm: r, l_h: l, c_f: c };
}

export function fromFlow(nodes, edges) {
  return {
    schema: SCHEMA,
    nodes: (nodes || []).map((n) => ({
      id: n.id,
      type: n.data?.kind,
      refdes: n.data?.refdes || n.id,
      value: n.data?.value,
      unit: n.data?.unit || "",
      x: n.position?.x || 0,
      y: n.position?.y || 0,
      rot: Number(n.data?.rot) === 90 ? 90 : 0,
    })),
    edges: (edges || []).map((e) => ({
      id: e.id,
      from: `${e.source}.${e.sourceHandle || "n1"}`,
      to: `${e.target}.${e.targetHandle || "n1"}`,
    })),
  };
}

export function nextPartId(nodes, type) {
  const prefix = PREFIX[type] || "n";
  const used = new Set((nodes || []).map((n) => n.id));
  let i = 1;
  while (used.has(`${prefix}${i}`)) i += 1;
  return `${prefix}${i}`;
}

export function nextEdgeId(edges) {
  const used = new Set((edges || []).map((e) => e.id));
  let i = 1;
  while (used.has(`e${i}`)) i += 1;
  return `e${i}`;
}

export function nextJunctionId(nodes) {
  const used = new Set((nodes || []).map((n) => n.id));
  let i = 1;
  while (used.has(`j${i}`)) i += 1;
  return `j${i}`;
}

export function partCount(nodes) {
  return (nodes || []).filter((n) => (n.data?.kind || n.type) !== "junction").length;
}

/** Split one flow edge into two by inserting a junction at `point`. */
export function splitEdgeAt(nodes, edges, edgeId, point) {
  const edge = (edges || []).find((e) => e.id === edgeId);
  if (!edge) return null;
  const id = nextJunctionId(nodes);
  const junction = {
    id,
    type: "part",
    position: { x: Number(point?.x) || 0, y: Number(point?.y) || 0 },
    data: { kind: "junction", refdes: "", value: 0, unit: "", rot: 0 },
  };
  const rest = edges.filter((e) => e.id !== edgeId);
  const left = {
    id: nextEdgeId(rest),
    source: edge.source,
    target: id,
    sourceHandle: edge.sourceHandle || "n1",
    targetHandle: "w",
    type: "step",
  };
  const right = {
    id: nextEdgeId([...rest, left]),
    source: id,
    target: edge.target,
    sourceHandle: "e",
    targetHandle: edge.targetHandle || "n1",
    type: "step",
  };
  return { nodes: [...(nodes || []), junction], edges: [...rest, left, right] };
}

export function nextRefdes(nodes, type) {
  const spec = PARTS.find((p) => p.type === type);
  const prefix = spec?.prefix || "N";
  if (type === "ground") return "Gnd";
  const used = new Set((nodes || []).map((n) => n.data?.refdes));
  let i = 1;
  while (used.has(`${prefix}${i}`)) i += 1;
  return `${prefix}${i}`;
}
