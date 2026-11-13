function formatNumber(value, digits = 2) {
  const n = Number(value);
  if (Number.isNaN(n)) return String(value ?? "");
  return n.toFixed(digits);
}

function unitForLabel(label) {
  const s = String(label || "").trim();
  const lower = s.toLowerCase();
  if (!s) return "";
  if (lower.includes("vout") || lower === "v" || lower.startsWith("v ")) return "V";
  if (lower === "i" || lower.includes("current")) return "A";
  if (lower.includes("rpm")) return "rpm";
  if (lower.includes("ω") || lower.includes("omega")) return "rad/s";
  if (lower.includes("db")) return "dB";
  return "";
}

function parseTitleParts(title) {
  const parts = String(title || "")
    .split("·")
    .map((p) => p.trim())
    .filter(Boolean);
  if (parts.length >= 2) {
    return { head: parts.slice(0, -1).join(" · "), quantity: parts[parts.length - 1] };
  }
  return { head: parts[0] || "Result", quantity: "Answer" };
}

export function answerPartsFromRow(label, scalar) {
  const unit = unitForLabel(label);
  const value = formatNumber(scalar);
  const name = label;
  return { name, value, unit, display: unit ? `${name} = ${value} ${unit}` : `${name} = ${value}` };
}

export function buildAnswerRows(evid, data) {
  const title = data?.title || evid?.title || "";
  const { head, quantity } = parseTitleParts(title);
  const rows = [];
  const rawValues = evid?.values && typeof evid.values === "object" ? evid.values : {};
  const entries = Object.entries(rawValues).filter(
    ([k, v]) => k !== "token" && v != null && v !== "unchecked" && typeof v !== "object",
  );
  if (entries.length > 1) {
    for (const [key, val] of entries) {
      const label = key === "value" ? quantity : key;
      rows.push(answerPartsFromRow(label, val));
    }
    return { head, rows };
  }
  const scalar = evid?.value;
  if (scalar == null || scalar === "unchecked") {
    return { head, rows: [] };
  }
  rows.push(answerPartsFromRow(quantity, scalar));
  return { head, rows };
}

export function verificationNote({ unchecked, error, verifierRaw, evid }) {
  if (error) return "Could not load this run from disk.";
  if (unchecked) {
    return "Unchecked: no checked simulation was attached. Treat the value as symbolic until you re-run with the right engine.";
  }
  const recipe = String(evid?.recipe_id || "");
  if (recipe.includes("circuit") || recipe.includes("spice") || recipe === "solve-circuit-problem") {
    return "Recomputed with Kirchhoff's laws and a SPICE operating point; agree within 0.1%.";
  }
  if (verifierRaw && !/label-unverified|label-unchecked/i.test(verifierRaw)) {
    return verifierRaw;
  }
  return "Checked against Arc's numeric or simulation verifier.";
}
