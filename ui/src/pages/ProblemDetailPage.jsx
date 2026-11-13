import { useLayout } from "../store.js";
import { renderSlot } from "../slots/registry.js";
import { EngineArtifacts } from "../slots/engine/EngineArtifacts.jsx";
import { Inspector } from "../slots/canvas/Inspector.jsx";

const TABS = [
  { id: "work", label: "Work" },
  { id: "figures", label: "Figures" },
  { id: "diagram", label: "Diagram" },
  { id: "activity", label: "Activity" },
];

export function ProblemDetailPage({ id, data }) {
  const tab = useLayout((s) => s.problemTab);
  const setTab = useLayout((s) => s.setProblemTab);
  const drawer = useLayout((s) => s.parametersOpen);
  const setDrawer = useLayout((s) => s.setParametersOpen);
  let recipeId = "";
  try {
    const evid = JSON.parse(data?.summary || "{}");
    recipeId = evid.recipe_id || "";
  } catch {
    recipeId = "";
  }
  const hasStudy = Boolean(data?.control_diagram?.nodes?.length);
  return (
    <div className="problem-detail">
      {renderSlot("run.result", { id })}
      <div className="problem-tabs" role="tablist">
        {TABS.map((t) => (
          <button
            key={t.id}
            type="button"
            role="tab"
            aria-selected={tab === t.id}
            className="problem-tab"
            onClick={() => setTab(t.id)}
          >
            {t.label}
          </button>
        ))}
        <button type="button" className="button-secondary problem-params-toggle" onClick={() => setDrawer(!drawer)}>
          Parameters
        </button>
      </div>
      <div className="problem-detail-body">
        <div className="problem-tab-panel">
          {tab === "work" ? renderSlot("run.argument", { id }) : null}
          {tab === "figures" ? <EngineArtifacts id={id} recipeId={recipeId} /> : null}
          {tab === "diagram" ? (
            <div className={hasStudy ? "lab-surface lab-surface-study" : "lab-surface lab-surface-circuit"}>
              {renderSlot("run.canvas", { id })}
            </div>
          ) : null}
          {tab === "activity" ? renderSlot("run.more", { id }) : null}
        </div>
        {drawer ? (
          <aside className="parameters-drawer" aria-label="Parameters">
            <h2>Parameters</h2>
            <p className="hint">Edits mark the answer stale. Re-run from your agent or Studio.</p>
            {!hasStudy ? <Inspector /> : <p className="empty">Use Studio for this diagram type.</p>}
          </aside>
        ) : null}
      </div>
    </div>
  );
}
