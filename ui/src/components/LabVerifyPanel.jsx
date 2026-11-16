/** Derived vs lab simulation agreement (Problem + lab results strip). */

import { formatDiffPct, formatLabValue } from "./labFormat.js";

function badgeClass(status) {
  switch (status) {
    case "agrees":
      return "lab-verify-badge is-agrees";
    case "differs":
      return "lab-verify-badge is-differs";
    case "mismatch":
      return "lab-verify-badge is-mismatch";
    case "out_of_date":
      return "lab-verify-badge is-muted";
    default:
      return "lab-verify-badge is-muted";
  }
}

function loopStaleCopy() {
  return "Re-simulate the loop to refresh this check.";
}

export function LabVerifyPanel({ labVerify, labMeta, compact = false, onAskAgent, onReRun }) {
  if (!labVerify || (labVerify.derived == null && labVerify.simulated == null && !labVerify.metrics?.length)) {
    return null;
  }
  const needRederive = labVerify.derivation_matches_graph === false;
  const skipped = Boolean(labVerify.sim_skipped);
  const metrics = labVerify.metrics?.length
    ? labVerify.metrics
    : [
        {
          id: "primary",
          label: "Probe",
          derived: labVerify.derived,
          simulated: labVerify.simulated,
          unit: labVerify.unit || "V",
          rel_err_pct: labVerify.rel_err_pct,
          rel_tol_pct: labVerify.rel_tol_pct ?? 2,
          status: skipped ? "not_simulated" : labVerify.status || (labVerify.mismatch ? "differs" : "agrees"),
          status_label:
            labVerify.status_label ||
            (skipped
              ? "Not simulated"
              : labVerify.mismatch
                ? `Differs by ${formatDiffPct(labVerify.rel_err_pct)} (limit 2%)`
                : "Agrees (limit 2%)"),
        },
      ];
  const engine = labVerify.sim_engine || (skipped ? "ngspice not available" : "ngspice");
  const allRowsStale = Boolean(labVerify.all_rows_out_of_date);

  const globalStaleBanner = allRowsStale ? (
    <div className="lab-verify-stale-banner" role="status">
      <p>
        {labVerify.stale_reason ||
          (labVerify.lab_kind === "control" ? loopStaleCopy() : "Re-run simulation for every metric.")}
      </p>
      {onReRun ? (
        <button type="button" className="text-button" onClick={onReRun}>
          Re-run
        </button>
      ) : null}
    </div>
  ) : null;

  const rederiveBanner = needRederive ? (
    <div className="lab-verify-stale-banner is-rederive" role="status">
      <p>
        {labVerify.re_derive_reason ||
          labVerify.human_edit_notes?.[0] ||
          "The agent's derivation no longer matches the lab circuit."}
      </p>
      <div className="lab-verify-cta-row">
        {onAskAgent ? (
          <button type="button" className="text-button" onClick={onAskAgent}>
            Ask agent to re-derive
          </button>
        ) : null}
        {onReRun ? (
          <button type="button" className="text-button" onClick={onReRun}>
            Re-run
          </button>
        ) : null}
      </div>
    </div>
  ) : null;

  function renderDerivedCell(row) {
    if (row.derived_out_of_date) {
      return (
        <span className="lab-verify-ood-derived" title={row.derived_note}>
          <span className="lab-verify-ood-label">{formatLabValue(row.derived, row.unit)}</span>
          <span className="lab-verify-badge is-muted">Out of date</span>
          <span className="lab-verify-ood-note">{row.derived_note}</span>
        </span>
      );
    }
    return formatLabValue(row.derived, row.unit);
  }

  if (compact) {
    return (
      <section className="lab-verify-panel card-surface is-compact" aria-labelledby="lab-verify-heading">
        <header className="lab-verify-head">
          <h2 id="lab-verify-heading">Simulated vs derived</h2>
          {labVerify.needs_review ? <span className="lab-needs-review">Needs review</span> : null}
        </header>
        {globalStaleBanner}
        {rederiveBanner}
        <p className="lab-verify-engine-line">
          Simulated with {engine}
          {labVerify.graph_revision != null ? (
            <span className="lab-verify-rev-tag"> · verified at r{labVerify.graph_revision}</span>
          ) : null}
        </p>
        <ul className="lab-verify-stack">
          {metrics.map((row) => (
            <li key={row.id} className="lab-verify-stack-row">
              <div className="lab-verify-stack-metric">{row.label}</div>
              <div className="lab-verify-stack-values tabular-nums">
                <span title="Derived (agent)">{renderDerivedCell(row)}</span>
                <span className="lab-verify-stack-sep">vs</span>
                <span title="Simulated (lab)">
                  {row.status === "not_simulated" || row.simulated == null
                    ? "—"
                    : formatLabValue(row.simulated, row.unit)}
                </span>
                <span className="lab-verify-stack-sep">·</span>
                <span className="lab-verify-stack-diff">
                  {row.rel_err_pct == null ? "—" : formatDiffPct(row.rel_err_pct)}
                </span>
              </div>
              <span className={badgeClass(row.status)}>{row.status_label}</span>
            </li>
          ))}
        </ul>
        {labMeta?.op_log?.length ? (
          <p className="hint">{labMeta.op_log.length} lab edit(s) recorded (see Activity).</p>
        ) : null}
      </section>
    );
  }

  return (
    <section className="lab-verify-panel card-surface" aria-labelledby="lab-verify-heading">
      <header className="lab-verify-head">
        <h2 id="lab-verify-heading">Simulated vs derived</h2>
        {labVerify.needs_review ? <span className="lab-needs-review">Needs review</span> : null}
      </header>
      {globalStaleBanner}
      {rederiveBanner}
      <table className="lab-verify-table">
        <thead>
          <tr>
            <th scope="col">Metric</th>
            <th scope="col">Derived (agent, by hand)</th>
            <th scope="col">
              Simulated (lab)
              <span className="lab-verify-engine">{engine}</span>
            </th>
            <th scope="col">Difference</th>
            <th scope="col">Status</th>
          </tr>
        </thead>
        <tbody>
          {metrics.map((row) => (
            <tr key={row.id}>
              <th scope="row">{row.label}</th>
              <td className="tabular-nums">{renderDerivedCell(row)}</td>
              <td className="tabular-nums">
                {row.status === "not_simulated" || row.simulated == null
                  ? "Not simulated"
                  : formatLabValue(row.simulated, row.unit)}
              </td>
              <td className="tabular-nums">{row.rel_err_pct == null ? "—" : formatDiffPct(row.rel_err_pct)}</td>
              <td>
                <span className={badgeClass(row.status)}>{row.status_label}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {labMeta?.op_log?.length ? (
        <p className="hint">{labMeta.op_log.length} lab edit(s) recorded (see Activity).</p>
      ) : null}
    </section>
  );
}