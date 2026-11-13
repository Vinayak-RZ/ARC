import { useLayout } from "../store.js";
import { renderSlot } from "../slots/registry.js";
import { EngineArtifacts } from "../slots/engine/EngineArtifacts.jsx";
import { StepTimeline, TraceDiagnostics } from "../components/StepTimeline.jsx";
import { ParametersPanel } from "../components/ParametersPanel.jsx";
import { ProblemHeader } from "../components/ProblemHeader.jsx";

const TABS = [
  { id: "work", label: "Work" },
  { id: "figures", label: "Figures" },
  { id: "diagram", label: "Diagram" },
  { id: "activity", label: "Activity" },
];

export function ProblemDetailPage({ id, data, runMeta }) {
  const tab = useLayout((s) => s.problemTab);
  const setTab = useLayout((s) => s.setProblemTab);
  const drawer = useLayout((s) => s.parametersOpen);
  const stale = useLayout((s) => s.parametersStale);
  const setStale = useLayout((s) => s.setParametersStale);
  let recipeId = "";
  try {
    const evid = JSON.parse(data?.summary || "{}");
    recipeId = evid.recipe_id || "";
  } catch {
    recipeId = "";
  }
  const hasStudy = Boolean(data?.control_diagram?.nodes?.length);

  return (
    <div className="page-column problem-detail">
      <ProblemHeader runMeta={runMeta} data={data} />
      {renderSlot("run.result", { id, runMeta })}
      <div className="problem-tabs tabs-underline" role="tablist">
        {TABS.map((t) => (
          <button
            key={t.id}
            type="button"
            role="tab"
            aria-selected={tab === t.id}
            className="tab-underline"
            onClick={() => setTab(t.id)}
          >
            {t.label}
          </button>
        ))}
      </div>
      <div className={`problem-detail-body${drawer ? " is-drawer-open" : ""}`}>
        <div className="problem-tab-panel">
          {tab === "work" ? <StepTimeline data={data} /> : null}
          {tab === "figures" ? <EngineArtifacts id={id} recipeId={recipeId} /> : null}
          {tab === "diagram" ? (
            <div className="diagram-shell">
              {renderSlot("run.canvas", { id })}
            </div>
          ) : null}
          {tab === "activity" ? (
            <>
              {renderSlot("run.more", { id })}
              <TraceDiagnostics trace={data?.trace_excerpt} />
            </>
          ) : null}
        </div>
        {drawer ? (
          <aside className="parameters-drawer" aria-label="Parameters">
            <h2>Parameters</h2>
            <ParametersPanel
              problem={data?.problem}
              stale={stale}
              onChange={() => setStale(true)}
              onRunAgain={() => setStale(false)}
            />
          </aside>
        ) : null}
      </div>
    </div>
  );
}
