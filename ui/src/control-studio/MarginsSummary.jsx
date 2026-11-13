import { marginLine } from "./marginFormat.js";

function Cell({ label, value, tip, stale }) {
  return (
    <div title={tip || undefined}>
      <dt>{label}</dt>
      <dd className={stale ? "is-muted" : undefined}>{value}</dd>
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
  const note = margins.margin_note;
  return (
    <div className={`cs-margins${stale ? " is-stale" : ""}`} role="status" aria-live="polite">
      {stale ? <p className="cs-stale-banner">Diagram changed since last run. Simulate again for fresh margins.</p> : null}
      {note && !stale ? (
        <p className="cs-margins-footnote" title={note}>
          {note.length > 120 ? `${note.slice(0, 117)}…` : note}
        </p>
      ) : null}
      <dl className="cs-margin-grid">
        <Cell label="Gain margin" value={m.gm} tip={tips.gm_db || note} stale={stale} />
        <Cell label="Phase margin" value={m.pm} tip={tips.pm_deg || note} stale={stale} />
        <Cell label="ω gain cross" value={m.wcg} tip={tips.wcg} stale={stale} />
        <Cell label="ω phase cross" value={m.wcp} tip={tips.wcp} stale={stale} />
      </dl>
    </div>
  );
}
