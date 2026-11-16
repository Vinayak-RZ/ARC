/** Derived vs lab simulation on a shared run artifact. */

function fmt(n, digits = 4) {
  if (n == null || Number.isNaN(Number(n))) return "—";
  const v = Number(n);
  if (Math.abs(v) >= 1000 || (Math.abs(v) > 0 && Math.abs(v) < 0.001)) return v.toExponential(3);
  return v.toFixed(digits);
}

export function LabVerifyPanel({ labVerify, labMeta }) {
  if (!labVerify || (labVerify.derived == null && labVerify.simulated == null)) return null;
  const mismatch = Boolean(labVerify.mismatch);
  const skipped = Boolean(labVerify.sim_skipped);
  return (
    <section className="lab-verify-panel card-surface" aria-labelledby="lab-verify-heading">
      <h2 id="lab-verify-heading">Lab check</h2>
      <dl className="lab-verify-grid">
        <div>
          <dt>Derived</dt>
          <dd>{fmt(labVerify.derived)}</dd>
        </div>
        <div>
          <dt>Simulated</dt>
          <dd>{skipped ? "skipped (no ngspice)" : fmt(labVerify.simulated)}</dd>
        </div>
      </dl>
      {mismatch ? (
        <p className="lab-verify-mismatch" role="alert">
          Derive and simulation disagree within tolerance.
        </p>
      ) : (
        <p className="hint">{skipped ? "Graph saved; run ngspice locally to compare." : "Derived and simulation agree."}</p>
      )}
      {labMeta?.op_log?.length ? (
        <p className="hint">{labMeta.op_log.length} lab edit(s) recorded (see Activity).</p>
      ) : null}
    </section>
  );
}