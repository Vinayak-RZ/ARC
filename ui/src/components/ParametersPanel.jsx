import { useEffect, useMemo, useState } from "react";

const FIELDS = {
  voltage_divider: [
    { key: "vin", label: "Vin", unit: "V", scale: 1 },
    { key: "r1", label: "R1", unit: "Ω", scale: 1 },
    { key: "r2", label: "R2", unit: "Ω", scale: 1 },
  ],
  ohms_law: [
    { key: "v", label: "V", unit: "V", scale: 1 },
    { key: "r", label: "R", unit: "Ω", scale: 1 },
  ],
};

function inferKind(problem) {
  if (!problem) return "";
  if (problem.kind) return problem.kind;
  if ("vin" in problem && "r1" in problem) return "voltage_divider";
  if ("v" in problem && "r" in problem) return "ohms_law";
  return "";
}

function displayValue(key, raw, scale) {
  const n = Number(raw);
  if (Number.isNaN(n)) return raw ?? "";
  if (key.startsWith("r") && n >= 1000) return (n / 1000).toFixed(3);
  return String(n);
}

function parseInput(key, text, scale) {
  const n = Number(text);
  if (Number.isNaN(n)) return null;
  if (key.startsWith("r") && n < 1000) return n * 1000;
  return n;
}

export function ParametersPanel({ problem, stale, onChange, onRunAgain }) {
  const kind = inferKind(problem);
  const schema = FIELDS[kind] || [];
  const [draft, setDraft] = useState(() => ({ ...(problem || {}) }));

  useEffect(() => {
    setDraft({ ...(problem || {}) });
  }, [problem]);

  const rows = useMemo(() => schema, [schema]);

  if (!rows.length) {
    return <p className="empty">No editable parameters for this problem type.</p>;
  }

  function update(key, text) {
    const next = parseInput(key, text, 1);
    if (next == null) return;
    const merged = { ...draft, [key]: next, kind: kind || draft.kind };
    setDraft(merged);
    onChange?.(merged);
  }

  return (
    <div className="parameters-panel">
      {stale ? (
        <div className="stale-banner" role="status">
          Answer is stale after your edit.
          <button type="button" className="button-primary button-compact" onClick={onRunAgain}>
            Run again
          </button>
        </div>
      ) : null}
      <ul className="param-fields">
        {rows.map((f) => (
          <li key={f.key} className="param-field">
            <label htmlFor={`param-${f.key}`}>{f.label}</label>
            <div className="param-input-wrap">
              <input
                id={`param-${f.key}`}
                type="text"
                inputMode="decimal"
                value={displayValue(f.key, draft[f.key], f.scale)}
                onChange={(e) => update(f.key, e.target.value)}
              />
              <span className="param-unit">{f.unit}</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
