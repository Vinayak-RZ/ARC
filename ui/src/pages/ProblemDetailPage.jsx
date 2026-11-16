import { useCallback, useEffect, useState } from "react";
import { useLayout } from "../store.js";
import { renderSlot } from "../slots/registry.js";
import { EngineArtifacts } from "../slots/engine/EngineArtifacts.jsx";
import { StepTimeline, TraceDiagnostics } from "../components/StepTimeline.jsx";
import { ParametersPanel } from "../components/ParametersPanel.jsx";
import { ProblemHeader } from "../components/ProblemHeader.jsx";
import { LabVerifyPanel } from "../components/LabVerifyPanel.jsx";
import { LabActivityPanel } from "../components/LabActivityPanel.jsx";
import { labForRecipe, openLab, openRunLab } from "../studio-engine/labs/openExample.js";

const TABS = [
  { id: "work", label: "Work" },
  { id: "figures", label: "Figures" },
  { id: "diagram", label: "Diagram" },
  { id: "activity", label: "Activity" },
];

export function ProblemDetailPage({ id, data: initialData, runMeta }) {
  const [data, setData] = useState(initialData);
  useEffect(() => {
    setData(initialData);
  }, [initialData, id]);

  const refreshRun = useCallback(async () => {
    if (!id) return;
    try {
      const r = await fetch(`/api/runs/${id}`);
      if (r.ok) setData(await r.json());
    } catch {
      /* keep prior */
    }
  }, [id]);

  const labPost = useCallback(
    async (path) => {
      if (!id) return;
      await fetch(`/api/runs/${id}/lab/${path}`, { method: "POST" });
      await refreshRun();
    },
    [id, refreshRun],
  );

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

  return (
    <div className="page-column problem-detail">
      <ProblemHeader runMeta={runMeta} data={data} />
      {data?.lab ? (
        <button type="button" className="button-primary" onClick={() => openRunLab(data)}>
          Open in lab
        </button>
      ) : null}
      {!data?.lab && labForRecipe(recipeId) ? (
        <button type="button" className="button-secondary" onClick={() => openLab(labForRecipe(recipeId))}>
          Open simulation lab
        </button>
      ) : null}
      {renderSlot("run.result", { id, runMeta })}
      <LabVerifyPanel
        labVerify={data?.lab_verify}
        labMeta={data?.lab}
        onAskAgent={() => labPost("re-derive")}
        onReRun={() => labPost("verify")}
        onAcceptSimulated={() => labPost("accept-simulated")}
      />
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
              <LabActivityPanel labMeta={data?.lab} />
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