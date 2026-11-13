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
  "explain-control": "Control",
  "explain-power": "Power",
};

export function subjectTag(run) {
  if (run?.subject) return run.subject;
  const recipe = String(run?.recipe_id || "").trim();
  if (recipe && SUBJECT_TAGS[recipe]) return SUBJECT_TAGS[recipe];
  if (recipe.includes("control")) return "Control";
  if (recipe.includes("power")) return "Power";
  if (recipe.includes("circuit")) return "Circuits";
  if (recipe.includes("signal")) return "Signals";
  if (String(run?.id || "").startsWith("cs-")) return "Control";
  return recipe ? recipe.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()) : "General";
}

export function displayTitle(run) {
  const title = String(run?.display_title || run?.title || "").trim();
  if (title && title !== run?.id) return title;
  const recipe = String(run?.recipe_id || "");
  if (recipe === "solve-circuit-problem") return "Voltage divider · Vout";
  if (String(run?.id || "").startsWith("cs-")) return "PID on DC motor";
  if (recipe === "unmatched-cosolver") return "Open question";
  if (recipe.startsWith("explain-")) {
    const subj = recipe.replace("explain-", "").replace(/-/g, " ");
    return `${subj.charAt(0).toUpperCase()}${subj.slice(1)} explanation`;
  }
  if (recipe) return recipe.replace(/-/g, " ");
  return "Untitled run";
}

export function runIdHint(run) {
  return String(run?.id || "");
}
