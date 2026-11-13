import { useMemo, useState } from "react";
import { ArrowUpRight, Copy, RotateCw } from "lucide-react";
import { displayTitle, subjectTag } from "../runDisplay.js";
import { relativeTime } from "../units/format.js";

const STATUS_CHIPS = [
  { id: "all", label: "All" },
  { id: "checked", label: "Checked" },
  { id: "unchecked", label: "Unchecked" },
];

function timeGroup(ts) {
  const delta = Date.now() / 1000 - Number(ts || 0);
  if (delta < 86400) return "Today";
  if (delta < 86400 * 7) return "This week";
  return "Earlier";
}

function titleCaseSubject(s) {
  if (!s) return "Unknown";
  return String(s)
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

export function ProblemsPage({ runs, loading, error, onOpenProblem, onTryExample, onReload }) {
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("all");
  const [subjectFilter, setSubjectFilter] = useState("all");
  const [madeByFilter, setMadeByFilter] = useState("all");
  const counts = useMemo(
    () => ({
      all: runs.length,
      checked: runs.filter((r) => !r.unchecked).length,
      unchecked: runs.filter((r) => r.unchecked).length,
    }),
    [runs],
  );
  const subjects = useMemo(() => {
    const set = new Set(runs.map((r) => r.subject || subjectTag(r)).filter(Boolean));
    return ["all", ...[...set].sort()];
  }, [runs]);
  const madeByOptions = useMemo(() => {
    const set = new Set(runs.map((r) => r.made_by || "Agent").filter(Boolean));
    return ["all", ...[...set].sort()];
  }, [runs]);
  const filtered = useMemo(() => {
    return runs.filter((run) => {
      const title = displayTitle(run).toLowerCase();
      const q = query.toLowerCase();
      if (q && !title.includes(q) && !String(run.id).includes(q)) return false;
      if (status === "checked" && run.unchecked) return false;
      if (status === "unchecked" && !run.unchecked) return false;
      const subj = run.subject || subjectTag(run);
      if (subjectFilter !== "all" && subj !== subjectFilter) return false;
      const made = run.made_by || "Agent";
      if (madeByFilter !== "all" && made !== madeByFilter) return false;
      return true;
    });
  }, [runs, query, status, subjectFilter, madeByFilter]);
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
        <div className="problems-skeleton" aria-hidden="true">
          {Array.from({ length: 8 }, (_, i) => (
            <div key={i} className="problems-skeleton-row" />
          ))}
        </div>
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
          {STATUS_CHIPS.map(({ id, label }) => (
            <button
              key={id}
              type="button"
              className="gallery-filter-chip"
              aria-pressed={status === id ? "true" : "false"}
              onClick={() => setStatus(id)}
            >
              {label} ({counts[id]})
            </button>
          ))}
        </div>
        <label className="problems-select-label">
          <span className="hint">Subject</span>
          <select
            className="problems-select"
            value={subjectFilter}
            onChange={(e) => setSubjectFilter(e.target.value)}
            aria-label="Filter by subject"
          >
            {subjects.map((s) => (
              <option key={s} value={s}>
                {s === "all" ? "All subjects" : titleCaseSubject(s)}
              </option>
            ))}
          </select>
        </label>
        <label className="problems-select-label">
          <span className="hint">Made by</span>
          <select
            className="problems-select"
            value={madeByFilter}
            onChange={(e) => setMadeByFilter(e.target.value)}
            aria-label="Filter by author"
          >
            {madeByOptions.map((s) => (
              <option key={s} value={s}>
                {s === "all" ? "Anyone" : s}
              </option>
            ))}
          </select>
        </label>
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
                    <span className="subject-tag">{titleCaseSubject(run.subject || subjectTag(run))}</span>
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
                      className="row-action-quiet"
                      aria-label="Open problem"
                      onClick={(e) => {
                        e.stopPropagation();
                        onOpenProblem(run.id);
                      }}
                    >
                      <ArrowUpRight size={16} strokeWidth={1.5} />
                    </button>
                    <button
                      type="button"
                      className="row-action-quiet"
                      aria-label="Refresh list"
                      onClick={(e) => {
                        e.stopPropagation();
                        onReload();
                      }}
                    >
                      <RotateCw size={16} strokeWidth={1.5} />
                    </button>
                    <button
                      type="button"
                      className="row-action-quiet"
                      aria-label="Copy problem id"
                      onClick={(e) => {
                        e.stopPropagation();
                        void navigator.clipboard?.writeText(run.id);
                      }}
                    >
                      <Copy size={16} strokeWidth={1.5} />
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
