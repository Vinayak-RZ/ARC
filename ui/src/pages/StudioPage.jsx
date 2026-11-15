import { useEffect, useState } from "react";
import { useLayout } from "../store.js";
import { renderSlot } from "../slots/registry.js";
import { DiagramView } from "../studio-engine/DiagramView.jsx";
import { CircuitSandbox } from "../studio-engine/CircuitSandbox.jsx";
import { STUDIO_WORKSPACES } from "../studio-engine/catalog.js";
import { LAB_REGISTRY } from "../studio-engine/labs/registry.js";
import "../studio-engine/labs/RectifierLab.jsx";
import "../studio-engine/labs/ConverterLab.jsx";
import "../studio-engine/labs/IdmtLab.jsx";
import "../studio-engine/labs/LeadLab.jsx";

export function StudioPage({ onNavigate }) {
  const tab = useLayout((s) => s.studioTab) || "home";
  const lab = useLayout((s) => s.studioLab);
  const setStudio = useLayout((s) => s.setStudio);
  const [runs, setRuns] = useState([]);
  const [selected, setSelected] = useState("");
  const [diagram, setDiagram] = useState(null);

  useEffect(() => {
    if (tab !== "diagrams") return undefined;
    let cancelled = false;
    fetch("/api/runs")
      .then((r) => r.json())
      .then(async (d) => {
        const list = (d.runs || []).slice(0, 20);
        const withDiagram = [];
        for (const r of list) {
          try {
            const body = await fetch(`/api/runs/${r.id}`).then((x) => x.json());
            if (body?.diagram?.panels?.length) withDiagram.push({ id: r.id, title: r.title || r.id, diagram: body.diagram });
          } catch {
            /* skip */
          }
        }
        if (!cancelled) {
          setRuns(withDiagram);
          if (withDiagram.length && !selected) {
            setSelected(withDiagram[0].id);
            setDiagram(withDiagram[0].diagram);
          }
        }
      })
      .catch(() => {
        if (!cancelled) setRuns([]);
      });
    return () => {
      cancelled = true;
    };
  }, [tab, selected]);

  function goHome() {
    onNavigate?.({ view: "studio", tab: "home", lab: null });
  }

  function openWorkspace(workspaceTab) {
    setStudio({ tab: workspaceTab, lab: null });
    onNavigate?.({ view: "studio", tab: workspaceTab, lab: null });
  }

  function openSimLab(labId) {
    setStudio({ tab: "labs", lab: labId });
    onNavigate?.({ view: "studio", tab: "labs", lab: labId });
  }

  function selectRun(id) {
    setSelected(id);
    const hit = runs.find((r) => r.id === id);
    setDiagram(hit?.diagram || null);
  }

  function exportSvg() {
    const svg = document.querySelector(".se-diagram-view svg");
    if (!svg) return;
    const clone = svg.cloneNode(true);
    const style = getComputedStyle(document.documentElement);
    const colors = ["--ee-color-ink", "--ee-color-body", "--ee-color-primary", "--ee-color-muted", "--ee-color-surface-card", "--ee-color-hairline", "--ee-color-copper", "--ee-semantic-up", "--ee-semantic-down", "--ee-color-primary-tint", "--ee-color-primary-ink"];
    let css = ":root{";
    for (const c of colors) css += `${c}:${style.getPropertyValue(c)};`;
    css += "}";
    const styleEl = document.createElementNS("http://www.w3.org/2000/svg", "style");
    styleEl.textContent = css;
    clone.insertBefore(styleEl, clone.firstChild);
    const blob = new Blob([new XMLSerializer().serializeToString(clone)], { type: "image/svg+xml" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "arc-diagram.svg";
    a.click();
    URL.revokeObjectURL(url);
  }

  const SimLab = lab ? LAB_REGISTRY.find((l) => l.id === lab)?.Component : null;
  const inWorkspace = tab !== "home";

  return (
    <div className={`studio-page page-column${inWorkspace ? " studio-page-workspace" : " studio-home"}`}>
      {inWorkspace ? (
        <button type="button" className="text-link studio-back" onClick={goHome}>
          ← All laboratories
        </button>
      ) : (
        <header className="page-header">
          <h1>Studio</h1>
          <p className="home-lede">Run simulations, sketch block and circuit diagrams, and open teaching labs.</p>
        </header>
      )}

      {tab === "home" ? (
        <>
          <section className="home-section">
            <h2>Workspaces</h2>
            <div className="learn-lab-grid studio-pick-grid">
              {STUDIO_WORKSPACES.map((w) => (
                <button key={w.id} type="button" className="learn-lab-card" onClick={() => openWorkspace(w.tab)}>
                  <strong>{w.title}</strong>
                  <span className="hint">{w.blurb}</span>
                </button>
              ))}
            </div>
          </section>
          <section className="home-section">
            <h2>Simulation laboratories</h2>
            <div className="learn-lab-grid studio-pick-grid">
              {LAB_REGISTRY.map((l) => (
                <button key={l.id} type="button" className="learn-lab-card" onClick={() => openSimLab(l.id)}>
                  <strong>{l.title}</strong>
                  <span className="hint">{l.pack}</span>
                </button>
              ))}
            </div>
          </section>
        </>
      ) : null}

      {tab === "control" ? (
        <div className="studio-workspace-pane">
          {renderSlot("control.studio", { autoBoot: true })}
        </div>
      ) : null}

      {tab === "circuits" ? (
        <div className="studio-workspace-pane">
          <CircuitSandbox />
        </div>
      ) : null}

      {tab === "diagrams" ? (
        <div className="studio-workspace-pane studio-diagrams">
          {!runs.length ? (
            <p className="hint">Solve a problem to see its diagram here.</p>
          ) : (
            <>
              <div className="studio-diagrams-toolbar">
                <label>
                  Run{" "}
                  <select value={selected} onChange={(e) => selectRun(e.target.value)}>
                    {runs.map((r) => (
                      <option key={r.id} value={r.id}>
                        {r.title}
                      </option>
                    ))}
                  </select>
                </label>
                <button type="button" className="button-secondary" onClick={exportSvg}>
                  Export SVG
                </button>
              </div>
              {diagram ? <DiagramView diagram={diagram} /> : null}
            </>
          )}
        </div>
      ) : null}

      {tab === "labs" ? (
        <div className="studio-workspace-pane studio-labs">
          {SimLab ? <SimLab /> : <p className="hint">Unknown lab.</p>}
        </div>
      ) : null}
    </div>
  );
}