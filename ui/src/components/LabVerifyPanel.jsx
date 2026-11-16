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

export function LabVerifyPanel({ labVerify, labMeta, compact = false }) {
  if (!labVerify || (labVerify.derived == null && labVerify.simulated == null && !labVerify.metrics?.length)) {
    return null;
  }
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
                ? `Differs by ${formatDiffPct(labVerify.rel_err_pct)} (limit ${formatDiffPct(labVerify.rel_tol_pct ?? 2)})`
                : `Agrees within ${formatDiffPct(labVerify.rel_tol_pct ?? 2)}`),
        },
      ];
  const engine = labVerify.sim_engine || (skipped ? "ngspice not available" : "ngspice");
  return (
    <section
      className={`lab-verify-panel card-surface${compact ? " is-compact" : ""}`}
      aria-labelledby="lab-verify-heading"
    >
      <header className="lab-verify-head">
        <h2 id="lab-verify-heading">Simulated vs derived</h2>
        {labVerify.needs_review ? <span className="lab-needs-review">Needs review</span> : null}
      </header>
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
              <td className="tabular-nums">{formatLabValue(row.derived, row.unit)}</td>
              <td className="tabular-nums">
                {row.status === "not_simulated" || row.simulated == null
                  ? "Not simulated"
                  : formatLabValue(row.simulated, row.unit)}
              </td>
              <td className="tabular-nums">
                {row.rel_err_pct == null ? "—" : formatDiffPct(row.rel_err_pct)}
              </td>
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