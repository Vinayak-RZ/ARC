const EXAMPLE_ID = {
  rectifier: "rectifier-3ph",
  converter: "boost-ccm",
  idmt: "idmt-relay",
  lead: "lead-design",
};

const RECIPE_LAB = {
  "rectifier-3ph-study": "rectifier",
  "boost-converter-study": "converter",
  "idmt-relay-study": "idmt",
  "lead-compensator-design-study": "lead",
};

export function labForRecipe(recipeId) {
  return RECIPE_LAB[recipeId] || "";
}

export async function openMatchingProblem(labId) {
  const exampleId = EXAMPLE_ID[labId];
  if (!exampleId) return;
  const r = await fetch(`/api/examples/${exampleId}/run`, { method: "POST" });
  const body = await r.json();
  if (!r.ok || !body.run_id) return;
  const url = new URL(window.location.href);
  url.search = "";
  url.searchParams.set("problem", body.run_id);
  window.history.pushState({}, "", url);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

export function openLab(labId) {
  const url = new URL(window.location.href);
  url.searchParams.delete("problem");
  url.searchParams.delete("run");
  url.searchParams.set("view", "studio");
  url.searchParams.set("tab", "labs");
  url.searchParams.set("lab", labId);
  window.history.pushState({}, "", url);
  window.dispatchEvent(new PopStateEvent("popstate"));
}