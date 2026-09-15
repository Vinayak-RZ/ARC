import { useEffect, useState } from "react";
import { useLayout } from "../../store.js";

function Field({ label, value, onCommit }) {
  const [text, setText] = useState(String(value ?? ""));
  useEffect(() => {
    setText(String(value ?? ""));
  }, [value]);
  return (
    <label className="field">
      {label}
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        onBlur={() => onCommit(text)}
      />
    </label>
  );
}

export function Inspector() {
  const selectedId = useLayout((s) => s.selectedNodeId);
  const flowNodes = useLayout((s) => s.flowNodes);
  const applyPartPatch = useLayout((s) => s.applyPartPatch);
  const node = flowNodes.find((n) => n.id === selectedId);
  if (!node) {
    return (
      <aside className="inspector" aria-label="Inspector">
        <p className="hint">Select a part to edit refdes and value.</p>
      </aside>
    );
  }
  const data = node.data || {};
  const grounded = data.kind === "ground";
  return (
    <aside className="inspector" aria-label="Inspector">
      <h2>Inspector</h2>
      <Field label="Refdes" value={data.refdes || ""} onCommit={(v) => applyPartPatch(node.id, { refdes: v })} />
      {grounded ? null : (
        <>
          <Field
            label="Value"
            value={data.value ?? ""}
            onCommit={(v) => {
              const n = Number(v);
              applyPartPatch(node.id, { value: Number.isFinite(n) ? n : v });
            }}
          />
          <Field label="Unit" value={data.unit || ""} onCommit={(v) => applyPartPatch(node.id, { unit: v })} />
          <button
            type="button"
            className="button-secondary"
            onClick={() => applyPartPatch(node.id, { rot: Number(data.rot) === 90 ? 0 : 90 })}
          >
            {Number(data.rot) === 90 ? "Make horizontal" : "Make vertical"}
          </button>
        </>
      )}
    </aside>
  );
}
