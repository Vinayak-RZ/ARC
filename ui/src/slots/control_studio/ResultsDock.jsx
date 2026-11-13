import { useEffect, useState } from "react";
import { marginLine } from "../../control-studio/marginFormat.js";
import { StepChart } from "./StepChart.jsx";

const TABS = [
  { id: "step", label: "Step" },
  { id: "bode", label: "Bode" },
  { id: "rlocus", label: "Root locus" },
];

function isTextualKpi(value) {
  const s = String(value);
  return s === "Infinite" || s.includes("No crossover") || s === "Not defined";
}

function MarginTable({ margins, stale }) {
  if (!margins) {
    return (
      <p className="cs-margins-hint">Run Simulate to see the step response and margins.</p>
    );
  }
  if (margins.ok === false && margins.error === "python-control missing") {
    return (
      <p className="cs-margins-hint">
        Install the <strong>control</strong> extra to analyze margins.
      </p>
    );
  }
  const m = marginLine(margins);
  const tips = margins.margin_tooltips || {};
  const rows = [
    ["Gain margin (dB)", m.gm, tips.gm_db],
    ["Phase margin (°)", m.pm, tips.pm_deg],
    ["Gain crossover (rad/s)", m.wcg, tips.wcg],
    ["Phase crossover (rad/s)", m.wcp, tips.wcp],
  ];
  return (
    <table className="studio-margin-table studio-margin-grid-2x2">
      <thead>
        <tr>
          {rows.map(([label]) => (
            <th key={label}>{label}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        <tr>
          {rows.map(([label, value, tip]) => (
            <td key={label} className={stale ? "is-muted" : undefined} title={tip || undefined}>
              <span className={`studio-kpi tabular-nums${isTextualKpi(value) ? " is-textual" : ""}`}>{value}</span>
              {tip && (value === "Infinite" || String(value).includes("No crossover") || value === "Not defined") ? (
                <span className="studio-margin-meta">{tip}</span>
              ) : null}
            </td>
          ))}
        </tr>
      </tbody>
    </table>
  );
}

function useUiTheme() {
  const [theme, setTheme] = useState(() => document.documentElement.getAttribute("data-theme") || "light");
  useEffect(() => {
    const obs = new MutationObserver(() => {
      setTheme(document.documentElement.getAttribute("data-theme") || "light");
    });
    obs.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
    return () => obs.disconnect();
  }, []);
  return theme;
}

export function ResultsDock({ results, stepData, margins, stale, sessionId, onResimulate }) {
  const [tab, setTab] = useState("step");
  const [windowS, setWindowS] = useState(10);
  const uiTheme = useUiTheme();
  const ts = results?.ts || Date.now();
  const src = results ? results[tab] : null;

  function pickWindow(choice) {
    setWindowS(choice);
    if (!sessionId) return;
    const body =
      choice === "auto"
        ? { t_final: "auto" }
        : { t_final: Number(choice) };
    fetch(`/api/control-studio/sessions/${sessionId}/simulate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    })
      .then((r) => r.json())
      .then((sim) => onResimulate?.(sim))
      .catch(() => {});
  }

  return (
    <footer className={`studio-results${stale ? " is-stale" : ""}${results ? "" : " is-empty"}`} aria-label="Results">
      <div className="studio-results-layout">
        <div className="studio-results-margins-col">
          <MarginTable margins={margins} stale={stale} />
          {results ? (
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
          ) : null}
        </div>
        <div className="studio-results-stage">
          {!results ? null : tab === "step" && stepData ? (
            <StepChart
              data={stepData}
              margins={margins}
              windowS={windowS}
              onWindowChange={pickWindow}
            />
          ) : src ? (
            <img src={`${src}?t=${ts}&theme=${encodeURIComponent(uiTheme)}`} alt={`${tab} plot`} loading="eager" />
          ) : (
            <p className="cs-margins-hint">No plot.</p>
          )}
        </div>
      </div>
    </footer>
  );
}
