import { marginLine } from "./marginFormat.js";

function Cell({ label, value, tip, stale }) {
  const showCaption = tip && (value === "Infinite" || value === "No crossover");
  return (
    <div>
      <dt>{label}</dt>
      <dd className={stale ? "is-muted" : undefined} title={!showCaption && tip ? tip : undefined}>
        {value}
      </dd>
      {showCaption ? <p className="cs-margin-caption">{tip}</p> : null}
    </div>
  );
}

export function MarginsSummary({ margins, stale }) {
  if (!margins) {
    return (
      <div className="cs-margins cs-margins--empty" role="status">
        <p className="cs-margins-hint">Run Simulate to see gain and phase margins for this loop.</p>
      </div>
    );
  }
  if (margins.ok === false && margins.error === "python-control missing") {
    return (
      <div className="cs-margins cs-margins--empty" role="status">
        <p className="cs-margins-hint">
          Install the <strong>control</strong> extra to analyze margins:{" "}
          <code>uv sync</code> or <code>pip install electrical-engineer[control]</code>.
        </p>
      </div>
    );
  }
  const m = marginLine(margins);
  const tips = margins.margin_tooltips || {};
  return (
    <div className={`cs-margins${stale ? " is-stale" : ""}`} role="status" aria-live="polite">
      {stale ? <p className="cs-stale-banner">Diagram changed since last run. Simulate again for fresh margins.</p> : null}
      <dl className="cs-margin-grid">
        <Cell label="Gain margin" value={m.gm} tip={tips.gm_db} stale={stale} />
        <Cell label="Phase margin" value={m.pm} tip={tips.pm_deg} stale={stale} />
        <Cell label="ω gain cross" value={m.wcg} tip={tips.wcg} stale={stale} />
        <Cell label="ω phase cross" value={m.wcp} tip={tips.wcp} stale={stale} />
      </dl>
    </div>
  );
}
