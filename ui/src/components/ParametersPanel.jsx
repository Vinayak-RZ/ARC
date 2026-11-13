import { useEffect, useMemo, useState } from "react";
import { formatResistanceOhms, formatVoltage, parseResistanceInput } from "../units/format.js";

const FIELDS = {
  voltage_divider: [
    { key: "vin", label: "Vin", kind: "voltage" },
    { key: "r1", label: "R1", kind: "resistance" },
    { key: "r2", label: "R2", kind: "resistance" },
  ],
  ohms_law: [
    { key: "v", label: "V", kind: "voltage" },
    { key: "r", label: "R", kind: "resistance" },
  ],
};

function inferKind(problem) {
  if (!problem) return "";
  if (problem.kind) return problem.kind;
  if ("vin" in problem && "r1" in problem) return "voltage_divider";
  if ("v" in problem && "r" in problem) return "ohms_law";
  return "";
}

function displayField(kind, raw) {
  if (kind === "voltage") return formatVoltage(raw);
  return formatResistanceOhms(raw);
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

  function update(key, fieldKind, text, unit) {
    let next;
    if (fieldKind === "resistance") {
      next = parseResistanceInput(text, unit);
    } else {
      next = Number(text);
    }
    if (next == null || Number.isNaN(next)) return;
    const merged = { ...draft, [key]: next, kind: kind || draft.kind };
    setDraft(merged);
    onChange?.(merged);
  }

  return (
    <div className="parameters-panel">
      {stale ? (
        <div className="stale-banner" role="status">
          Answer is stale after your edit.{" "}
          <button type="button" className="text-link" onClick={onRunAgain}>
            Run again
          </button>
        </div>
      ) : null}
      <ul className="param-fields">
        {rows.map((f) => {
          const fmt = displayField(f.kind, draft[f.key]);
          return (
            <li key={f.key} className="param-field">
              <label htmlFor={`param-${f.key}`}>{f.label}</label>
              <div className="param-input-suffix">
                <input
                  id={`param-${f.key}`}
                  type="text"
                  inputMode="decimal"
                  value={fmt.value}
                  onChange={(e) => update(f.key, f.kind, e.target.value, fmt.unit)}
                />
                <span className="param-suffix">{fmt.unit}</span>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export function inputsForWork(problem) {
  const kind = inferKind(problem);
  if (kind !== "voltage_divider") return [];
  return FIELDS.voltage_divider.map((f) => {
    const fmt = displayField(f.kind, problem[f.key]);
    return { label: f.label, display: fmt.text };
  });
}
