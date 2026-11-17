/** Derived vs lab simulation agreement (Problem + lab results strip). */

import { formatDiffPct, formatLabValue } from "./labFormat.js";
import { openRunLab } from "../studio-engine/labs/openExample.js";

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

function labEditCount(n) {
  const c = Number(n) || 0;
  if (!c) return "";
  return `${c} lab edit${c === 1 ? "" : "s"}`;
}

export function LabVerifyPanel({
  runId,
  runData,
  labVerify,
  labMeta,
  compact = false,
  onAskAgent,
  onReRun,
  onAcceptSimulated,
}) {
  if (!labVerify || (labVerify.derived == null && labVerify.simulated == null && !labVerify.metrics?.length)) {
    return null;
  }
  const derivedStale = labVerify.derivation_matches_graph === false;
  const sameRevMismatch = Boolean(labVerify.needs_review) && !derivedStale;
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

  const globalStaleBanner =
    allRowsStale && !derivedStale ? (
      <div className="lab-verify-stale-banner" role="status">
        <p>
          {labVerify.stale_reason ||
            (labVerify.lab_kind === "control" ? loopStaleCopy() : "Re-run simulation for every metric.")}
        </p>
      </div>
    ) : null;

  const contextBanner = derivedStale ? (
    <div className="lab-verify-stale-banner is-rederive" role="status">
      <p>
        {labVerify.re_derive_reason ||
          labVerify.human_edit_notes?.[0] ||
          "The agent's derivation no longer matches the lab circuit."}
      </p>
    </div>
  ) : null;

  const showActions = derivedStale || sameRevMismatch;
  const actionCta = showActions ? (
    <div className="lab-verify-stale-banner is-review" role="group" aria-label="Review actions">
      <div className="lab-verify-cta-row">
        {onReRun ? (
          <button
            type="button"
            className={derivedStale ? "button-primary" : "text-button"}
            onClick={onReRun}
          >
            {derivedStale ? "Re-simulate in lab" : "Re-run"}
          </button>
        ) : null}
        {(derivedStale || sameRevMismatch) && onAskAgent ? (
          <button type="button" className="text-button" onClick={onAskAgent}>
            Ask agent to re-derive
          </button>
        ) : null}
        {sameRevMismatch && onAcceptSimulated ? (
          <button type="button" className="text-button" onClick={onAcceptSimulated}>
            Accept simulated value
          </button>
        ) : null}
      </div>
    </div>
  ) : null;

  function rowStatus(row) {
    if (row.derived_out_of_date) {
      return { status: "out_of_date", label: "Out of date" };
    }
    return { status: row.status, label: row.status_label };
  }

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
        </header>
        {globalStaleBanner}
        {contextBanner}
        {actionCta}
        <p className="lab-verify-engine-line">
          Simulated with {engine}
          {labVerify.graph_revision != null ? (
            <span className="lab-verify-rev-tag"> · simulated at r{labVerify.graph_revision}</span>
          ) : null}
        </p>
        <ul className="lab-verify-stack">
          {metrics.map((row) => {
            const badge = rowStatus(row);
            return (
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
                  {!row.derived_out_of_date ? (
                    <>
                      <span className="lab-verify-stack-sep">·</span>
                      <span className="lab-verify-stack-diff">
                        {row.rel_err_pct == null ? "—" : formatDiffPct(row.rel_err_pct)}
                      </span>
                    </>
                  ) : null}
                </div>
                <span className={badgeClass(badge.status)}>{badge.label}</span>
              </li>
            );
          })}
        </ul>
        {labMeta?.op_log?.length ? (
          <p className="hint">{labEditCount(labMeta.op_log.length)} recorded (see Activity).</p>
        ) : null}
      </section>
    );
  }

  const labRev = labVerify?.graph_revision ?? labMeta?.revision ?? runData?.lab?.revision;
  const labOpenAside =
    runId && runData?.lab ? (
      <a
        className="lab-verify-lab-aside"
        href={runData.lab?.ui_url || "#"}
        onClick={(e) => {
          e.preventDefault();
          openRunLab(runData);
        }}
      >
        <img
          className="lab-verify-lab-thumb"
          src={`/api/runs/${runId}/artifact.svg`}
          alt=""
          width={160}
          height={72}
        />
        <span className="lab-verify-lab-caption">
          Agent&apos;s circuit · r{labRev ?? "—"} · {engine} · Open in lab →
        </span>
      </a>
    ) : null;

  return (
    <section className="lab-verify-panel card-surface" aria-labelledby="lab-verify-heading">
      <header className="lab-verify-head">
        <h2 id="lab-verify-heading">Simulated vs derived</h2>
      </header>
      {globalStaleBanner}
      {contextBanner}
      {actionCta}
      <div className="lab-verify-body-grid">
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
          {metrics.map((row) => {
            const badge = rowStatus(row);
            return (
              <tr key={row.id}>
                <th scope="row">{row.label}</th>
                <td className="tabular-nums">{renderDerivedCell(row)}</td>
                <td className="tabular-nums">
                  {row.status === "not_simulated" || row.simulated == null
                    ? "Not simulated"
                    : formatLabValue(row.simulated, row.unit)}
                </td>
                <td className="tabular-nums">
                  {row.derived_out_of_date ? "—" : row.rel_err_pct == null ? "—" : formatDiffPct(row.rel_err_pct)}
                </td>
                <td>
                  <span className={badgeClass(badge.status)}>{badge.label}</span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
      {labOpenAside}
      </div>
      {labMeta?.op_log?.length ? (
        <p className="hint">{labEditCount(labMeta.op_log.length)} recorded (see Activity).</p>
      ) : null}
    </section>
  );
}