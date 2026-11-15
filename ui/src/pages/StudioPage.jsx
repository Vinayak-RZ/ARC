import { useEffect, useState } from "react";
import { useLayout } from "../store.js";
import { renderSlot } from "../slots/registry.js";
import { DiagramView } from "../studio-engine/DiagramView.jsx";
import { LAB_REGISTRY } from "../studio-engine/labs/registry.js";
import "../studio-engine/labs/RectifierLab.jsx";

const TABS = [
  { id: "control", label: "Control" },
  { id: "diagrams", label: "Diagrams" },
  { id: "labs", label: "Labs" },
];

export function StudioPage({ onNavigate }) {
  const tab = useLayout((s) => s.studioTab) || "control";
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

  const Lab = lab ? LAB_REGISTRY.find((l) => l.id === lab)?.Component : null;

  return (
    <div className="studio-page">
      <div className="se-tabs" role="tablist" aria-label="Studio">
        {TABS.map((t) => (
          <button
            key={t.id}
            type="button"
            role="tab"
            aria-selected={tab === t.id}
            className={tab === t.id ? "tab is-active" : "tab"}
            onClick={() => {
              setStudio({ tab: t.id, lab: t.id === "labs" ? lab : null });
              onNavigate?.({ view: "studio", tab: t.id, lab: t.id === "labs" ? lab : null });
            }}
          >
            {t.label}
          </button>
        ))}
      </div>
      {tab === "control" ? renderSlot("control.studio") : null}
      {tab === "diagrams" ? (
        <div className="studio-diagrams">
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
        <div className="studio-labs">
          {Lab ? (
            <>
              <button type="button" className="text-link" onClick={() => setStudio({ tab: "labs", lab: null })}>
                ← All labs
              </button>
              <Lab />
            </>
          ) : (
            <div className="learn-lab-grid">
              {LAB_REGISTRY.map((l) => (
                <button
                  key={l.id}
                  type="button"
                  className="learn-lab-card"
                  onClick={() => {
                    setStudio({ tab: "labs", lab: l.id });
                    onNavigate?.({ view: "studio", tab: "labs", lab: l.id });
                  }}
                >
                  <strong>{l.title}</strong>
                  <span className="hint">{l.pack}</span>
                </button>
              ))}
            </div>
          )}
        </div>
      ) : null}
    </div>
  );
}
