/** Provenance bar above shared lab canvas (section 6a). */

import { ArcMascot } from "../mascot/index.js";

export function LabProvenanceBar({
  runTitle,
  problemId,
  stepLabel,
  revision,
  humanEdits,
  viewMode,
  onViewMode,
  onBackToProblem,
  onRestore,
  restoreDisabled,
}) {
  if (!problemId && !runTitle) return null;
  // Never show the raw run id as a title while the run detail is still loading.
  const titleLabel = runTitle || "this problem";
  const modes = [
    ["yours", "Yours"],
    ["agent", "Agent's"],
    ["changes", "Changes"],
  ];
  return (
    <div className="lab-provenance-bar" role="region" aria-label="Lab provenance">
      <div className="lab-provenance-left">
        <ArcMascot mode="ambient" size={20} label="Agent" />
        <span>
          Built by <strong>Agent</strong> for{" "}
          {problemId ? (
            <button type="button" className="text-link" onClick={onBackToProblem}>
              {titleLabel}
            </button>
          ) : (
            runTitle
          )}
        </span>
        {stepLabel ? <span className="lab-provenance-step">· {stepLabel}</span> : null}
        {revision != null ? (
          <span className="lab-provenance-rev">· r{revision}</span>
        ) : null}
        {humanEdits > 0 ? (
          <span className="lab-provenance-edited-pill">
            Edited by you · {humanEdits} change{humanEdits === 1 ? "" : "s"} since the agent&apos;s version
          </span>
        ) : null}
      </div>
      <div className="lab-provenance-right">
        <div className="lab-provenance-segment" role="tablist" aria-label="Artifact view">
          {modes.map(([id, label]) => (
            <button
              key={id}
              type="button"
              role="tab"
              aria-selected={viewMode === id}
              className={viewMode === id ? "is-active" : undefined}
              onClick={() => onViewMode?.(id)}
            >
              {label}
            </button>
          ))}
        </div>
        <button type="button" className="button-secondary" disabled={restoreDisabled} onClick={onRestore}>
          Restore agent version
        </button>
      </div>
    </div>
  );
}