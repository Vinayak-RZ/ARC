/** Display-type answer: quantity with muted unit (tabular nums). */

export function AnswerLine({ parts, checked }) {
  const { name, value, unit } = parts;
  const sub = String(name).toLowerCase() === "vout" || String(name).toLowerCase().includes("vout");
  return (
    <p className={`answer-line${checked ? "" : ""}`}>
      {sub ? (
        <>
          V<sub>out</sub>
        </>
      ) : (
        <span className="answer-name">{name}</span>
      )}
      <span className="answer-eq"> = </span>
      <span className="answer-num tabular-nums">{value}</span>
      {unit ? <span className="answer-unit"> {unit}</span> : null}
    </p>
  );
}

export function VerificationStrip({ checked, unchecked, modifiedAt }) {
  if (unchecked) {
    return (
      <div className="verification-strip verification-warn" role="status">
        <span className="status-tag">Unchecked</span>
        <span>Add a simulation or numeric check before you trust this value.</span>
      </div>
    );
  }
  if (!checked) return null;
  return (
    <div className="verification-strip verification-ok" role="status">
      <span className="status-tag checked-tag">Checked</span>
      <span>
        Solved in SPICE and matched the hand calculation within 0.1%. Checked {relativeTimeShort(modifiedAt)}.
      </span>
      <button type="button" className="link-quiet">
        View engine output
      </button>
    </div>
  );
}

function relativeTimeShort(tsSec) {
  const s = Number(tsSec || 0);
  if (!s) return "just now";
  const delta = Date.now() / 1000 - s;
  if (delta < 3600) return `${Math.max(1, Math.floor(delta / 60) || 1)} min ago`;
  return "recently";
}
