import { useState } from "react";

const TABS = [
  { id: "step", label: "Step" },
  { id: "bode", label: "Bode" },
  { id: "rlocus", label: "Root locus" },
];

export function ResultsDock({ results, stale }) {
  const [tab, setTab] = useState("step");
  if (!results) {
    return (
      <footer className="studio-results empty">
        <div className="studio-results-head">
          <h3>Plots</h3>
        </div>
        <div className="studio-results-stage">
          <p className="cs-margins-hint">Plots appear here after Simulate completes.</p>
        </div>
      </footer>
    );
  }
  const ts = results.ts || Date.now();
  const src = results[tab];
  return (
    <footer className={`studio-results${stale ? " is-stale" : ""}`} aria-label="Simulation plots">
      <div className="studio-results-head">
        <h3>Plots</h3>
        {stale ? <span className="cs-stale-banner">Out of date with diagram</span> : null}
        <div className="studio-results-tabs" role="tablist">
          {TABS.map((t) => (
            <button
              key={t.id}
              type="button"
              role="tab"
              aria-selected={tab === t.id}
              className={tab === t.id ? "is-active" : ""}
              onClick={() => setTab(t.id)}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>
      <div className="studio-results-stage">
        {src ? <img src={`${src}?t=${ts}`} alt={`${tab} plot`} loading="eager" /> : <p className="cs-margins-hint">No plot.</p>}
      </div>
    </footer>
  );
}
