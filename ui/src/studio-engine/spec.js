/** arc.diagram.v1 validation (pure JS). */

export const SCHEMA = "arc.diagram.v1";
export const MAX_POINTS = 4000;

export const COMPONENT_PINS = {
  resistor: ["a", "b"],
  inductor: ["a", "b"],
  capacitor: ["a", "b"],
  switch: ["a", "b"],
  vsource: ["p", "n"],
  isource: ["p", "n"],
  acsource: ["p", "n"],
  diode: ["a", "k"],
  scr: ["a", "k", "g"],
  igbt: ["c", "e", "g"],
  ground: ["a"],
  transformer: ["p1", "p2", "s1", "s2"],
  motor: ["a", "b"],
  opamp: ["inp", "inn", "out"],
  bjt: ["c", "b", "e"],
  junction: ["a"],
  terminal: ["a"],
};

const PANEL_KINDS = new Set(["schematic", "block", "oneline", "waveform"]);
const ROTS = new Set([0, 90, 180, 270]);
const WAVE_STYLES = new Set(["primary", "secondary", "positive", "muted-dashed"]);
const SCALES = new Set(["linear", "log"]);

export function validateDiagram(d) {
  const errors = [];
  if (!d || typeof d !== "object") return ["diagram must be object"];
  if (d.schema !== SCHEMA) errors.push(`schema must be ${SCHEMA}`);
  if (!Array.isArray(d.panels)) {
    errors.push("panels must be array");
    return errors;
  }
  d.panels.forEach((panel, i) => {
    const pfx = `panels[${i}]`;
    if (!PANEL_KINDS.has(panel?.kind)) errors.push(`${pfx}: unknown kind`);
    if (panel.kind === "schematic") {
      for (const c of panel.components || []) {
        if (!COMPONENT_PINS[c.type]) errors.push(`${pfx}: unknown component ${c.type}`);
        if (c.rot != null && !ROTS.has(c.rot)) errors.push(`${pfx}: bad rot`);
      }
    }
    if (panel.kind === "waveform") {
      for (const s of panel.series || []) {
        if (!WAVE_STYLES.has(s.style || "primary")) errors.push(`${pfx}: bad series style`);
        const n = (s.points || []).length;
        if (n > MAX_POINTS) errors.push(`${pfx}: series ${s.id} exceeds ${MAX_POINTS} points`);
      }
      if (panel.x?.scale && !SCALES.has(panel.x.scale)) errors.push(`${pfx}: bad x scale`);
      if (panel.y?.scale && !SCALES.has(panel.y.scale)) errors.push(`${pfx}: bad y scale`);
    }
  });
  return errors;
}
