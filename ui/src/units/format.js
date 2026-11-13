/** Consistent value + unit display for parameters and work trail. */

export function formatResistanceOhms(raw) {
  const v = Number(raw);
  if (Number.isNaN(v)) return { text: String(raw ?? ""), value: "", unit: "" };
  if (v >= 1000) {
    const k = v / 1000;
    const value = Number.isInteger(k) ? String(k) : k.toFixed(3).replace(/\.?0+$/, "");
    return { text: `${value} kΩ`, value, unit: "kΩ", ohms: v };
  }
  return { text: `${v} Ω`, value: String(v), unit: "Ω", ohms: v };
}

export function formatVoltage(raw) {
  const v = Number(raw);
  if (Number.isNaN(v)) return { text: String(raw ?? ""), value: "", unit: "V" };
  const value = Number.isInteger(v) ? String(v) : v.toFixed(2).replace(/\.?0+$/, "");
  return { text: `${value} V`, value, unit: "V" };
}

export function parseResistanceInput(text, unitHint) {
  const t = String(text).trim();
  const n = Number(t);
  if (Number.isNaN(n)) return null;
  if (unitHint === "kΩ" || (t.includes("k") && !t.includes("m"))) return n * 1000;
  return n;
}

export function relativeTime(tsSec) {
  const s = Number(tsSec || 0);
  if (!s) return "just now";
  const delta = Date.now() / 1000 - s;
  if (delta < 60) return "just now";
  if (delta < 3600) return `${Math.floor(delta / 60)} min ago`;
  if (delta < 86400) return `${Math.floor(delta / 3600)} hr ago`;
  return new Date(s * 1000).toLocaleDateString();
}
