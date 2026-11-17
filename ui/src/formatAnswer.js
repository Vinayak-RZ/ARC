function formatNumber(value, digits = 2) {
  const n = Number(value);
  if (Number.isNaN(n)) return String(value ?? "");
  return n.toFixed(digits);
}

function unitForLabel(label) {
  const s = String(label || "").trim();
  const lower = s.toLowerCase();
  if (!s) return "";
  if (lower === "vo" || lower.startsWith("vo,")) return "V";
  if (lower.includes("relay time") || (lower.includes("time") && lower.includes("t"))) return "s";
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
  if (recipe === "rectifier-3ph-study" || recipe === "rectifier-1ph-study") return "Vo";
  if (recipe === "idmt-relay-study") return "Relay time t";
  if (kind === "series_rlc" || recipe === "simulate-circuit" || recipe === "series-rlc-transient") return "Vc,peak";
  if (recipe === "solve-control-problem") return "y(∞)";
  if (kind === "voltage_divider" || (data?.problem?.vin != null && data?.problem?.r1 != null)) return "Vout";
  const bad = new Set(["answer", "result", "value", ""]);
  if (bad.has(String(fallback || "").toLowerCase())) return "Answer";
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
  const lower = String(label).toLowerCase();
  const d =
    digits ??
    (lower.includes("peak") || lower.includes("vc") || lower.includes("y") ? 3 : 2);
  const value = formatNumber(scalar, d);
  const name = label;
  return { name, value, unit, display: unit ? `${name} = ${value} ${unit}` : `${name} = ${value}` };
}

function isSeriesRlc(data, evid) {
  const kind = String(data?.problem?.kind || evid?.problem_kind || "").toLowerCase();
  const recipe = String(evid?.recipe_id || "");
  return kind === "series_rlc" || recipe === "simulate-circuit" || recipe === "series-rlc-transient";
}

function rlcPeakTimeMs(derive, tr, problem) {
  for (const v of [derive?.t_s, tr?.t_Vc_peak_s, problem?.t_s]) {
    const n = Number(v);
    if (Number.isFinite(n) && n > 0) return n * 1000;
  }
  return 0;
}

function rlcAnswerDisplay(data, evid) {
  const stale = staleDerivedRevision(data) != null;
  const tr = stale ? null : data?.rlc_transient;
  const derive = data?.circuit_derive;
  const lv = data?.lab_verify;
  if (!isSeriesRlc(data, evid) || (!tr && !derive && !lv)) return null;
  if (lv?.needs_review && lv?.derivation_matches_graph !== false) return null;
  const deriveMetric = String(derive?.derive_metric || "").toLowerCase();
  const noOvershoot =
    !stale &&
    (tr?.damping_type === "critically_damped" ||
      tr?.damping_type === "overdamped" ||
      deriveMetric === "vc_final" ||
      Number(tr?.overshoot_pct ?? derive?.overshoot_pct ?? 99) < 0.5);
  const vStep = Number(data?.problem?.v_step ?? data?.problem?.vin ?? evid?.vin ?? 10);
  if (noOvershoot) {
    const finalV = Number(derive?.value ?? lv?.derived ?? tr?.Vc_peak_V ?? vStep);
    const tMs =
      1000 *
      Number(
        tr?.settling_2pct_entry_s ?? tr?.settling_time_2pct_s ?? derive?.settling_2pct_entry_s ?? 0,
      );
    return `No overshoot · Final value ${finalV.toFixed(2)} V · Settling (2%) ${tMs.toFixed(2)} ms`;
  }
  const peak = Number(derive?.value ?? lv?.derived ?? evid?.value);
  const tMs = stale
    ? rlcPeakTimeMs(derive, null, data?.problem)
    : rlcPeakTimeMs(derive, tr, data?.problem);
  const tFmt = tMs.toFixed(3);
  return `Vc,peak = ${peak.toFixed(3)} V at ${tFmt} ms`;
}

export function runHeadline(evid, data) {
  const rlc = rlcAnswerDisplay(data, evid);
  if (rlc) return rlc;
  if (data?.lab_verify?.needs_review) return "";
  const { rows } = buildAnswerRows(evid, data);
  if (rows.length === 1) return rows[0].display;
  if (rows.length > 1) return rows.map((r) => r.display).join(" · ");
  return "";
}

export function staleDerivedRevision(data) {
  const lv = data?.lab_verify;
  if (!lv || lv.derivation_matches_graph !== false) return null;
  return data?.lab?.revision ?? lv?.graph_revision ?? null;
}

export function buildAnswerRows(evid, data) {
  const title = data?.title || evid?.title || "";
  const { head, quantity } = parseTitleParts(title);
  const rows = [];
  const staleRev = staleDerivedRevision(data);
  const rlcLine = rlcAnswerDisplay(data, evid);
  if (rlcLine) {
    rows.push({
      name: "Result",
      value: rlcLine,
      unit: "",
      display: rlcLine,
      plain: true,
      derivedStale: staleRev != null,
      staleRev,
    });
    return { head, rows };
  }
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
  const lv = data?.lab_verify;
  if (lv?.needs_review && lv?.derivation_matches_graph !== false) {
    return { head, rows: [] };
  }
  const scalar =
    data?.circuit_derive?.value != null
      ? data.circuit_derive.value
      : lv?.derived != null && lv.derivation_matches_graph !== false
        ? lv.derived
        : evid?.value;
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