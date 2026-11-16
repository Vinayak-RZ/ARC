/** Activity timeline — agent vs human ops with restore affordances. */

import { useMemo, useState } from "react";
import { ArcMascot } from "../mascot/index.js";

function relTime(tsMs) {
  if (!tsMs) return "";
  const delta = Math.max(0, Date.now() - Number(tsMs)) / 1000;
  if (delta < 60) return "just now";
  if (delta < 3600) return `${Math.floor(delta / 60)}m ago`;
  return `${Math.floor(delta / 3600)}h ago`;
}

function sentenceFor(entry) {
  const who = entry.actor_label || (entry.author === "human" ? "You" : "Agent");
  const target = entry.target ? ` ${entry.target}` : "";
  switch (entry.op) {
    case "seed_from_problem":
      return entry.author === "agent" ? "Agent built the circuit" : `${who} built the circuit`;
    case "add_part":
      return `${who} added${target}`;
    case "connect":
      return `${who} wired${target}`;
    case "layout_save":
      return `${who} moved parts (layout only)`;
    case "re_derive":
      return entry.author === "agent"
        ? `Agent re-derived (${entry.detail?.value != null ? `${entry.detail.value} V` : "updated derivation"})`
        : `${who} requested a re-derive`;
    case "ui_save":
      return `${who} saved the circuit`;
    case "set":
      if (entry.before != null && entry.after != null) {
        return `${who} changed ${entry.target || "a value"} to ${entry.after}`;
      }
      return `${who} updated ${entry.target || "a part"}`;
    case "simulate":
      return `${who} re-ran the simulation`;
    case "restore":
      return `${who} restored ${entry.target || (entry.detail?.rev ? `r${entry.detail.rev}` : "agent version")}`;
    default:
      return `${who} ${entry.op || "edited"}${target}`;
  }
}

function Avatar({ author }) {
  if (author === "human") {
    return <span className="lab-activity-avatar is-human" aria-hidden>You</span>;
  }
  return <ArcMascot mode="ambient" size={20} label="Agent" />;
}

export function LabActivity({ labMeta, onRestore, onPreview }) {
  const [filter, setFilter] = useState("all");
  const log = labMeta?.op_log || [];
  const rows = useMemo(() => {
    if (filter === "all") return log;
    return log.filter((e) => e.author === filter);
  }, [filter, log]);
  if (!log.length) {
    return <p className="hint">No lab edits yet. Agent and human changes appear here.</p>;
  }
  const currentRev = labMeta?.revision;
  return (
    <div className="lab-activity-wrap">
      <div className="lab-activity-filters" role="toolbar" aria-label="Filter activity">
        {[
          ["all", "All"],
          ["agent", "Agent"],
          ["human", "You"],
        ].map(([id, label]) => (
          <button
            key={id}
            type="button"
            className={filter === id ? "is-active" : undefined}
            onClick={() => setFilter(id)}
          >
            {label}
          </button>
        ))}
      </div>
      <ol className="lab-activity-timeline">
        {rows.map((entry) => {
          const isNow = entry.rev === currentRev;
          return (
            <li key={entry.id} className={`lab-activity-item is-${entry.author || "agent"}`}>
              <Avatar author={entry.author} />
              <div className="lab-activity-body">
                <p className="lab-activity-sentence">
                  {sentenceFor(entry)}
                  {entry.rev != null ? ` · rev ${entry.rev}` : ""}
                  {` · ${relTime(entry.ts_ms) || "just now"}`}
                </p>
                <div className="lab-activity-meta" hidden>
                  <span className="lab-activity-rev">r{entry.rev ?? "—"}</span>
                </div>
                {!isNow ? (
                  <div className="lab-activity-actions">
                    <button type="button" className="text-link" onClick={() => onPreview?.(entry)}>
                      Preview
                    </button>
                    <button type="button" className="text-link" onClick={() => onRestore?.(entry)}>
                      Restore to here
                    </button>
                  </div>
                ) : null}
              </div>
            </li>
          );
        })}
      </ol>
    </div>
  );
}