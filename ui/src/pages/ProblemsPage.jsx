import { useMemo, useState } from "react";
import { displayTitle, subjectTag } from "../runDisplay.js";
import { relativeTime } from "../units/format.js";

function timeGroup(ts) {
  const delta = Date.now() / 1000 - Number(ts || 0);
  if (delta < 86400) return "Today";
  if (delta < 86400 * 7) return "This week";
  return "Earlier";
}

export function ProblemsPage({ runs, loading, error, onOpenProblem, onTryExample, onReload }) {
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("all");
  const counts = useMemo(
    () => ({
      all: runs.length,
      checked: runs.filter((r) => !r.unchecked).length,
      unchecked: runs.filter((r) => r.unchecked).length,
    }),
    [runs],
  );
  const filtered = useMemo(() => {
    return runs.filter((run) => {
      const title = displayTitle(run).toLowerCase();
      const q = query.toLowerCase();
      if (q && !title.includes(q) && !String(run.id).includes(q)) return false;
      if (status === "checked" && run.unchecked) return false;
      if (status === "unchecked" && !run.unchecked) return false;
      return true;
    });
  }, [runs, query, status]);
  const groups = useMemo(() => {
    const m = new Map();
    for (const run of filtered) {
      const g = timeGroup(run.modified_at);
      if (!m.has(g)) m.set(g, []);
      m.get(g).push(run);
    }
    return [...m.entries()];
  }, [filtered]);

  if (loading) {
    return (
      <div className="problems-page problems-loading" aria-busy="true">
        <h1>Problems</h1>
        <p className="empty loading-shimmer">Loading problems…</p>
      </div>
    );
  }
  if (error) {
    return (
      <div className="problems-page problems-error">
        <h1>Problems</h1>
        <p className="empty">Could not load problems. Check that the Arc server is running.</p>
        <button type="button" className="button-primary" onClick={onReload}>
          Try again
        </button>
      </div>
    );
  }
  if (runs.length === 0) {
    return (
      <div className="problems-empty">
        <h1>Problems</h1>
        <p className="empty">No problems yet.</p>
        <button type="button" className="button-primary" onClick={onTryExample}>
          Try an example
        </button>
      </div>
    );
  }
  return (
    <div className="problems-page">
      <h1>Problems</h1>
      <div className="problems-toolbar">
        <input
          className="run-search"
          type="search"
          placeholder="Search problems"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          aria-keyshortcuts="/"
        />
        <span className="hint search-hint" aria-hidden="true">
          Press / to focus
        </span>
        <div className="gallery-filters" role="group" aria-label="Status">
          {["all", "checked", "unchecked"].map((s) => (
            <button
              key={s}
              type="button"
              className="gallery-filter-chip"
              aria-pressed={status === s ? "true" : "false"}
              onClick={() => setStatus(s)}
            >
              {s} ({counts[s]})
            </button>
          ))}
        </div>
      </div>
      {groups.map(([label, items]) => (
        <section key={label} className="problems-group">
          <h2 className="run-group-title">{label}</h2>
          <table className="problems-table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Subject</th>
                <th>Status</th>
                <th>Made by</th>
                <th>Updated</th>
                <th className="problems-actions-col">
                  <span className="visually-hidden">Actions</span>
                </th>
              </tr>
            </thead>
            <tbody>
              {items.map((run) => (
                <tr key={run.id} className="problems-row" onClick={() => onOpenProblem(run.id)} title={run.id}>
                  <td>{displayTitle(run)}</td>
                  <td>
                    <span className="subject-tag">{run.subject || subjectTag(run)}</span>
                  </td>
                  <td>
                    <span className={run.unchecked ? "status-badge unchecked" : "status-badge checked"}>
                      {run.unchecked ? "Unchecked" : "Checked"}
                    </span>
                  </td>
                  <td className="hint">{run.made_by || "Agent"}</td>
                  <td className="hint">{relativeTime(run.modified_at)}</td>
                  <td className="problems-row-actions">
                    <button
                      type="button"
                      className="button-secondary button-compact row-action"
                      onClick={(e) => {
                        e.stopPropagation();
                        onOpenProblem(run.id);
                      }}
                    >
                      Open
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      ))}
    </div>
  );
}
