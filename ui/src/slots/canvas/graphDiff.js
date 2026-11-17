/** Electrical diff between agent baseline and current lab graph. */

function nodeKey(n) {
  return String(n?.id || "");
}

function sig(n) {
  if (!n) return "";
  return JSON.stringify({ type: n.type, value: n.value, unit: n.unit, refdes: n.refdes });
}

export function diffCircuitGraphs(baseline, current) {
  const base = baseline && typeof baseline === "object" ? baseline : { nodes: [], edges: [] };
  const cur = current && typeof current === "object" ? current : { nodes: [], edges: [] };
  const baseNodes = Object.fromEntries((base.nodes || []).map((n) => [nodeKey(n), n]));
  const curNodes = Object.fromEntries((cur.nodes || []).map((n) => [nodeKey(n), n]));
  const added = [];
  const removed = [];
  const changed = [];
  for (const id of Object.keys(curNodes)) {
    if (!baseNodes[id]) {
      added.push(id);
      continue;
    }
    if (sig(baseNodes[id]) !== sig(curNodes[id])) {
      const b = baseNodes[id];
      const c = curNodes[id];
      changed.push({
        id,
        refdes: c.refdes || b.refdes || id,
        field: "value",
        before: b.value,
        after: c.value,
        unit: c.unit || b.unit || "",
      });
    }
  }
  for (const id of Object.keys(baseNodes)) {
    if (!curNodes[id]) removed.push(id);
  }
  return { added, removed, changed };
}

export function formatValueChip(row) {
  const unit = row.unit === "ohm" || row.unit === "Ω" ? "Ω" : row.unit || "";
  const tail = unit ? ` ${unit}` : "";
  return `${row.refdes}: ${row.before}${tail} → ${row.after}${tail}`;
}

export function decorateFlowNodes(nodes, diff, baselineGraph) {
  const changedIds = new Set((diff.changed || []).map((r) => r.id));
  const addedIds = new Set(diff.added || []);
  const decorated = (nodes || []).map((n) => {
    let className = n.className || "";
    if (addedIds.has(n.id)) className = `${className} is-diff-added`.trim();
    else if (changedIds.has(n.id)) className = `${className} is-diff-changed`.trim();
    const chip = (diff.changed || []).find((r) => r.id === n.id);
    return {
      ...n,
      className,
      data: { ...n.data, diffChip: chip ? formatValueChip(chip) : undefined },
    };
  });
  const baseNodes = baselineGraph?.nodes || [];
  const liveIds = new Set((nodes || []).map((n) => n.id));
  const ghosts = baseNodes
    .filter((b) => !liveIds.has(b.id))
    .map((b) => ({
      id: `ghost-${b.id}`,
      type: "part",
      position: { x: Number(b.x) || 0, y: Number(b.y) || 0 },
      draggable: false,
      selectable: false,
      className: "is-diff-removed",
      data: {
        kind: b.type,
        refdes: b.refdes || b.id,
        value: b.value,
        unit: b.unit || "",
        rot: Number(b.rot) === 90 ? 90 : 0,
        ghost: true,
        diffTag: "−",
      },
    }));
  return [...decorated, ...ghosts];
}