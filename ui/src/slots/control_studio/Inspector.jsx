import { useState } from "react";

function Field({ label, type = "text", value, onChange, error }) {
  return (
    <label className={`studio-field${error ? " has-error" : ""}`}>
      <span>{label}</span>
      <input type={type} value={value} onChange={(e) => onChange(e.target.value)} step={type === "number" ? "any" : undefined} />
      {error ? <span className="field-error">{error}</span> : null}
    </label>
  );
}

export function StudioInspector({ selected, blockIssues, onPatch, onComment, notes }) {
  const [comment, setComment] = useState("");
  if (!selected) {
    return (
      <aside className="studio-inspector">
        <h3>Inspector</h3>
        <p className="hint">Select a block for typed parameters and comments.</p>
      </aside>
    );
  }
  const t = selected.data?.blockType;
  const p = selected.data?.params || {};
  const issues = blockIssues[selected.id] || [];
  const blockNotes = (notes || []).filter((n) => n.block_id === selected.id);

  return (
    <aside className="studio-inspector">
      <h3>{selected.data?.label || t}</h3>
      <p className="hint">{t}</p>
      {t === "pid" ? (
        <>
          <Field
            label="Kp"
            type="number"
            value={p.kp ?? ""}
            onChange={(v) => onPatch({ kp: Number(v) })}
            error={issues.find((i) => i.code === "pid_kp")?.message}
          />
          <Field label="Ki" type="number" value={p.ki ?? ""} onChange={(v) => onPatch({ ki: Number(v) })} />
          <Field label="Kd" type="number" value={p.kd ?? ""} onChange={(v) => onPatch({ kd: Number(v) })} />
        </>
      ) : null}
      {t === "gain" || t === "plant_first_order" ? (
        <Field label="k" type="number" value={p.k ?? ""} onChange={(v) => onPatch({ k: Number(v) })} error={issues[0]?.message} />
      ) : null}
      {t === "transfer_function" ? (
        <Field label="Transfer function" value={p.tf ?? ""} onChange={(v) => onPatch({ tf: v })} error={issues[0]?.message} />
      ) : null}
      {t === "sum" ? (
        <Field label="Signs" value={p.signs ?? "+-"} onChange={(v) => onPatch({ signs: v })} error={issues[0]?.message} />
      ) : null}
      <div className="studio-comments">
        <h4>Pin comment</h4>
        {blockNotes.map((n) => (
          <p key={n.id} className="studio-comment">
            <span className={`studio-author-badge is-${n.author}`}>{n.author}</span> {n.text}
          </p>
        ))}
        <textarea rows={2} value={comment} onChange={(e) => setComment(e.target.value)} placeholder="Ask or explain at this block" />
        <button type="button" className="button-secondary" onClick={() => { onComment(comment); setComment(""); }}>
          Pin
        </button>
      </div>
    </aside>
  );
}
