import { useEffect, useState } from "react";
import { marginLine } from "../../control-studio/marginFormat.js";
import { StepChart } from "./StepChart.jsx";

const TABS = [
  { id: "step", label: "Step" },
  { id: "bode", label: "Bode" },
  { id: "rlocus", label: "Root locus" },
];

function splitValue(raw) {
  const s = String(raw ?? "—");
  if (s === "Infinite" || s.includes("No crossover") || s === "Not defined") {
    return { num: s, unit: "", textual: true };
  }
  const m = s.match(/^([\d.]+)\s*(.*)$/);
  if (m) return { num: m[1], unit: m[2] || "", textual: false };
  return { num: s, unit: "", textual: false };
}

function MarginsStrip({ margins, stale }) {
  if (!margins) {
    return <p className="cs-margins-hint">Run Simulate to see the step response and margins.</p>;
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
    { label: "Gain margin", value: m.gm, tip: tips.gm_db },
    { label: "Phase margin", value: m.pm, tip: tips.pm_deg },
    { label: "Gain crossover", value: m.wcg, tip: tips.wcg },
    { label: "Phase crossover", value: m.wcp, tip: tips.wcp },
  ];
  return (
    <dl className="studio-margins">
      {rows.map(({ label, value, tip }) => {
        const { num, unit, textual } = splitValue(value);
        return (
          <div className="studio-margin" key={label}>
            <dt>{label}</dt>
            <dd className={stale ? "is-muted" : undefined}>
              {textual ? (
                <span className="is-textual">{num}</span>
              ) : (
                <>
                  <span className="num tabular-nums">{num}</span>
                  {unit ? <span className="unit">{unit}</span> : null}
                </>
              )}
            </dd>
            {tip ? (
              <p className="studio-margin-meta" title={tip}>
                {tip}
              </p>
            ) : null}
          </div>
        );
      })}
    </dl>
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
  const [windowS, setWindowS] = useState("auto");
  const uiTheme = useUiTheme();
  const ts = results?.ts || Date.now();
  const src = results ? results[tab] : null;

  function pickWindow(choice) {
    setWindowS(choice);
    if (!sessionId) return;
    const body = choice === "auto" ? { t_final: "auto" } : { t_final: Number(choice) };
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
        {results || margins ? <MarginsStrip margins={margins} stale={stale} /> : null}
        <div className="studio-results-chart-col">
          <div className="studio-results-stage">
            {!results ? (
              <p className="studio-results-placeholder cs-margins-hint">Run Simulate to see the step response and margins.</p>
            ) : tab === "step" && stepData ? (
              <StepChart
                data={stepData}
                margins={margins}
                windowS={windowS}
                onWindowChange={pickWindow}
                tabBar={
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
                }
              />
            ) : results ? (
              <>
                <div className="studio-results-chart-head">
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
                {src ? (
                  <div className="studio-export-plot-frame">
                    <img src={`${src}?t=${ts}&theme=${encodeURIComponent(uiTheme)}`} alt={`${tab} plot`} loading="eager" />
                  </div>
                ) : (
                  <p className="cs-margins-hint">No plot.</p>
                )}
              </>
            ) : null}
          </div>
        </div>
      </div>
    </footer>
  );
}
