import { MarkerType } from "@xyflow/react";
import { nodeForType } from "./nodes.jsx";
import { wireLabel } from "./edges.jsx";

const EDGE_MARKER = { type: MarkerType.ArrowClosed, color: "#202020", width: 14, height: 14 };
const BOX_W = 96;
const BOX_H = 56;
const SUM_W = 56;

export function paramLine(params) {
  if (!params || typeof params !== "object") return "";
  for (const k of ["tf", "kp", "ki", "k", "tau"]) {
    if (params[k] != null) return `${k}=${params[k]}`;
  }
  return "";
}

export function diagramToFlow(diagram, { issuesByBlock = {}, notes = [], highlightSet = new Set(), flashAuthor = null } = {}) {
  const blocksById = Object.fromEntries((diagram?.blocks || []).map((b) => [b.id, b]));
  const nodes = (diagram?.blocks || []).map((b) => ({
    id: b.id,
    type: nodeForType(b.type),
    position: { x: b.x || 0, y: b.y || 0 },
    width: b.type === "sum" ? SUM_W : BOX_W,
    height: BOX_H,
    zIndex: 2,
    data: {
      blockId: b.id,
      blockType: b.type,
      label: b.label || b.type,
      params: b.params || {},
      paramLine: paramLine(b.params),
      issues: issuesByBlock[b.id] || [],
      notes,
      highlight: highlightSet.has(b.id),
      flashAuthor: flashAuthor && highlightSet.has(b.id) ? flashAuthor : null,
    },
  }));
  const edges = (diagram?.wires || []).map((w) => {
    const [fb, fp] = w.from.split(":");
    const [tb, tp] = w.to.split(":");
    const below = tp === "feedback" || w.route === "below";
    return {
      id: w.id,
      type: "signal",
      source: fb,
      target: tb,
      sourceHandle: fp,
      targetHandle: tp,
      markerEnd: EDGE_MARKER,
      zIndex: 0,
      data: { label: wireLabel(w.from, w.to, blocksById), route: below ? "below" : "forward" },
    };
  });
  return { nodes, edges };
}

export function flowToDiagram(nodes, edges, base) {
  const blocks = nodes.map((n) => ({
    id: n.id,
    type: n.data?.blockType || "gain",
    label: n.data?.label,
    x: n.position.x,
    y: n.position.y,
    params: n.data?.params || {},
  }));
  const wires = edges.map((e) => ({
    id: e.id,
    from: `${e.source}:${e.sourceHandle || "out"}`,
    to: `${e.target}:${e.targetHandle || "in"}`,
  }));
  return {
    schema: "arc.control_studio.v1",
    id: base?.id || "diagram",
    title: base?.title || "Control Studio",
    blocks,
    wires,
    notes: base?.notes || [],
    meta: base?.meta || {},
  };
}

export function issuesByBlock(validation) {
  const map = {};
  for (const item of validation?.issues || []) {
    const bid = item.block_id;
    if (!bid) continue;
    map[bid] = map[bid] || [];
    map[bid].push(item);
  }
  for (const item of validation?.warnings || []) {
    const bid = item.block_id;
    if (!bid) continue;
    map[bid] = map[bid] || [];
    map[bid].push(item);
  }
  return map;
}
