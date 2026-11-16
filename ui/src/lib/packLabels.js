/** Human labels for curriculum / lab pack ids. */
const PACK_LABELS = {
  power_electronics: "Power electronics",
  power: "Power systems",
  control: "Control",
  circuits: "Circuits",
  signals: "Signals",
  course_content: "Course content",
  earthing_safety: "Earthing & safety",
  low_voltage_protection: "Low-voltage protection",
};

export function packLabel(id) {
  if (!id) return "";
  const key = String(id);
  if (PACK_LABELS[key]) return PACK_LABELS[key];
  return key
    .split("_")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase())
    .join(" ");
}