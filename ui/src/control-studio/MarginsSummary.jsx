import { marginLine } from "./marginFormat.js";

export function MarginsSummary({ margins, stale }) {
  if (!margins) {
    return (
      <div className="cs-margins cs-margins--empty" role="status">
        <p className="cs-margins-hint">Run Simulate to see gain and phase margins for this loop.</p>
      </div>
    );
  }
  const m = marginLine(margins);
  return (
    <div className={`cs-margins${stale ? " is-stale" : ""}`} role="status" aria-live="polite">
      {stale ? <p className="cs-stale-banner">Diagram changed since last run. Simulate again for fresh margins.</p> : null}
      <dl className="cs-margin-grid">
        <div>
          <dt>Gain margin</dt>
          <dd>{m.gm}</dd>
        </div>
        <div>
          <dt>Phase margin</dt>
          <dd>{m.pm}</dd>
        </div>
        <div>
          <dt>ω gain cross</dt>
          <dd>{m.wcg}</dd>
        </div>
        <div>
          <dt>ω phase cross</dt>
          <dd>{m.wcp}</dd>
        </div>
      </dl>
    </div>
  );
}
