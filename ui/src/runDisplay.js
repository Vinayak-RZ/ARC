const SUBJECT_TAGS = {
  "solve-circuit-problem": "Circuits",
  "simulate-circuit": "Circuits",
  "simulate-after-confirm": "Circuits",
  "run-spice": "Circuits",
  "photo-to-netlist": "Circuits",
  "digital-control-verify": "Control",
  "run-python-control": "Control",
  "lti-analysis": "Control",
  "compose-from-parts": "Control",
  "unmatched-cosolver": "General",
  "explain-circuits": "Circuits",
  "explain-signals": "Signals",
};

function looksOpaqueId(text) {
  const t = String(text || "").trim();
  if (!t) return true;
  if (/^cs-[a-f0-9]{8,}$/i.test(t)) return true;
  if (/^[a-z0-9]{4}-20\d{6}T/i.test(t)) return true;
  return t === t.toLowerCase() && t.includes("-") && !t.includes(" ");
}

export function subjectTag(run) {
  const recipe = String(run?.recipe_id || "").trim();
  if (recipe && SUBJECT_TAGS[recipe]) return SUBJECT_TAGS[recipe];
  if (recipe.includes("control")) return "Control";
  if (recipe.includes("power")) return "Power";
  if (recipe.includes("circuit")) return "Circuits";
  if (String(run?.id || "").startsWith("cs-")) return "Control";
  return recipe ? recipe.replace(/-/g, " ") : "General";
}

export function displayTitle(run) {
  const title = String(run?.display_title || run?.title || "").trim();
  if (title && !looksOpaqueId(title) && title !== run?.id) return title;
  const recipe = String(run?.recipe_id || "");
  if (recipe === "solve-circuit-problem") return "Voltage divider · Vout";
  if (String(run?.id || "").startsWith("cs-")) return "PID on DC motor";
  if (recipe) return recipe.replace(/-/g, " ");
  return "Untitled run";
}

export function runIdHint(run) {
  return String(run?.id || "");
}
