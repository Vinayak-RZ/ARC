/** Provenance of human vs agent edits on the shared lab artifact. */

function relTime(tsMs) {
  if (!tsMs) return "";
  const delta = Math.max(0, Date.now() - Number(tsMs)) / 1000;
  if (delta < 60) return "just now";
  if (delta < 3600) return `${Math.floor(delta / 60)}m ago`;
  return `${Math.floor(delta / 3600)}h ago`;
}

export function LabActivity({ labMeta }) {
  const log = labMeta?.op_log || [];
  if (!log.length) return <p className="hint">No lab edits yet. Agent and human changes appear here.</p>;
  return (
    <ul className="lab-activity-list">
      {log.map((entry) => (
        <li key={entry.id} className={`lab-activity-item is-${entry.author || "agent"}`}>
          <span className={`lab-activity-author lab-author-${entry.author || "agent"}`}>{entry.author || "agent"}</span>
          <span className="lab-activity-op">{entry.op}</span>
          {entry.target ? <span className="lab-activity-target">{entry.target}</span> : null}
          <span className="lab-activity-time">{relTime(entry.ts_ms)}</span>
        </li>
      ))}
    </ul>
  );
}