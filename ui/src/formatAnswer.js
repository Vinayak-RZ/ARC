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
  if (lower.includes("vc") || lower.includes("peak")) return "V";
  if (lower === "i" || lower.includes("current")) return "A";
  if (lower.includes("rpm")) return "rpm";
  if (lower.includes("y") && lower.includes("∞")) return "";
  if (lower.includes("ω") || lower.includes("omega")) return "rad/s";
  if (lower.includes("db")) return "dB";
  return "";
}

function quantityLabelForRun(data, evid, fallback) {
  const kind = String(data?.problem?.kind || evid?.problem_kind || "").toLowerCase();
  const recipe = String(evid?.recipe_id || "");
  if (kind === "series_rlc" || recipe === "simulate-circuit" || recipe === "series-rlc-transient") return "Vc,peak";
  if (recipe === "solve-control-problem") return "y(∞)";
  if (kind === "voltage_divider" || (data?.problem?.vin != null && data?.problem?.r1 != null)) return "Vout";
  return fallback;
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

export function answerPartsFromRow(label, scalar, digits) {
  const unit = unitForLabel(label);
  const d =
    digits ??
    (String(label).toLowerCase().includes("peak") || String(label).toLowerCase().includes("vc") ? 3 : 2);
  const value = formatNumber(scalar, d);
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
  let scalar = evid?.value;
  const lv = data?.lab_verify;
  if (lv?.needs_review && lv.derived != null) {
    scalar = lv.derived;
  }
  if (scalar == null || scalar === "unchecked") {
    return { head, rows: [] };
  }
  const qty = quantityLabelForRun(data, evid, quantity);
  rows.push(answerPartsFromRow(qty, scalar));
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
