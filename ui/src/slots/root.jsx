import { useEffect, useMemo, useState } from "react";
import { register, renderSlot } from "./registry.js";
import { useLayout } from "../store.js";
import { Canvas } from "./canvas/Canvas.jsx";
import { Inspector } from "./canvas/Inspector.jsx";
import { Library } from "./library.jsx";
import { EngineArtifacts } from "./engine/EngineArtifacts.jsx";
import { VisualGallery } from "./gallery.jsx";
import { ControlStudio } from "./control_studio/ControlStudio.jsx";

const NAV = [
  { id: "home", label: "Home" },
  { id: "runs", label: "Runs" },
  { id: "library", label: "Books" },
  { id: "gallery", label: "Visuals" },
  { id: "control-studio", label: "Control" },
];

function recipeLabel(recipeId) {
  const id = String(recipeId || "").trim();
  if (!id) return "Other runs";
  return id.replace(/-/g, " ");
}

function formatRelative(modifiedAt) {
  const ts = Number(modifiedAt);
  if (!ts) return "";
  const delta = Date.now() / 1000 - ts;
  if (delta < 120) return "Just now";
  if (delta < 3600) return `${Math.floor(delta / 60)} min ago`;
  if (delta < 86400) return `${Math.floor(delta / 3600)} h ago`;
  if (delta < 86400 * 7) return `${Math.floor(delta / 86400)} d ago`;
  return new Date(ts * 1000).toLocaleDateString();
}

function groupRuns(runs) {
  const sorted = [...runs].sort((a, b) => Number(b.modified_at || 0) - Number(a.modified_at || 0));
  const groups = new Map();
  for (const run of sorted) {
    const key = recipeLabel(run.recipe_id);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(run);
  }
  return [...groups.entries()];
}

function Root() {
  return (
    <div className="shell">
      <a className="skip" href="#workspace">
        Skip to workspace
      </a>
      <header className="topbar">
        <img className="brand-mark" src="/arc-icon.png" width="32" height="32" alt="Arc" />
        <strong>Arc</strong>
        <span className="topbar-tagline">EE co-solver</span>
      </header>
      <div className="layout">
        {renderSlot("sidebar")}
        <main id="workspace" className="workspace">
          {renderSlot("workspace")}
        </main>
      </div>
    </div>
  );
}

function Sidebar() {
  const [runs, setRuns] = useState([]);
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [runsLoading, setRunsLoading] = useState(true);
  const current = useLayout((s) => s.currentRunId);
  const view = useLayout((s) => s.view);
  const setRun = useLayout((s) => s.setRun);
  const setView = useLayout((s) => s.setView);
  useEffect(() => {
    const q = new URLSearchParams(window.location.search);
    const viewQ = q.get("view");
    if (viewQ === "library") setView("library");
    else if (viewQ === "gallery") setView("gallery");
    else if (viewQ === "control-studio") setView("control-studio");
    else if (viewQ === "home") setView("home");
    if (window.location.pathname === "/gallery") setView("gallery");
    const run = q.get("run");
    if (run) {
      setRun(run);
      setView("runs");
    }
  }, [setRun, setView]);
  useEffect(() => {
    setRunsLoading(true);
    fetch("/api/runs")
      .then((r) => r.json())
      .then((d) => setRuns(d.runs || []))
      .catch(() => setRuns([]))
      .finally(() => setRunsLoading(false));
  }, []);
  function navigate(nextView) {
    setView(nextView);
    const url = new URL(window.location.href);
    if (nextView === "home") {
      url.searchParams.set("view", "home");
      url.searchParams.delete("run");
    } else if (nextView === "runs") {
      url.searchParams.delete("view");
    } else {
      url.searchParams.set("view", nextView);
      url.searchParams.delete("run");
    }
    window.history.replaceState({}, "", url);
    setOpen(false);
  }
  function openRun(id) {
    setRun(id);
    setView("runs");
    const url = new URL(window.location.href);
    url.searchParams.set("run", id);
    url.searchParams.delete("view");
    window.history.replaceState({}, "", url);
    setOpen(false);
  }
  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return runs;
    return runs.filter((run) => {
      const id = String(run.id || "");
      const title = String(run.title || "");
      const recipe = String(run.recipe_id || "");
      return title.toLowerCase().includes(q) || id.toLowerCase().includes(q) || recipe.toLowerCase().includes(q);
    });
  }, [runs, query]);
  const groups = useMemo(() => groupRuns(filtered), [filtered]);
  const navCurrent = view === "runs" && !current ? "runs" : view;
  return (
    <>
      <button
        className="nav-toggle"
        type="button"
        aria-expanded={open}
        aria-controls="run-list"
        onClick={() => setOpen(!open)}
      >
        Menu
      </button>
      <nav id="run-list" className={open ? "sidebar is-open" : "sidebar"} aria-label="Workspace">
        <div className="app-nav" role="group" aria-label="Sections">
          {NAV.map((item) => (
            <button
              key={item.id}
              type="button"
              className="app-nav-btn"
              aria-current={navCurrent === item.id ? "true" : undefined}
              onClick={() => navigate(item.id)}
            >
              {item.label}
            </button>
          ))}
        </div>
        {view === "library" ? (
          <p className="hint">Ingest and tag books in the workspace. Files stay on this machine.</p>
        ) : view === "gallery" || view === "control-studio" || view === "home" ? (
          <p className="hint">Pick a section above. Saved runs appear here when you open Runs.</p>
        ) : (
          <>
            <h2>Runs</h2>
            <input
              className="run-search"
              type="search"
              placeholder="Search runs"
              aria-label="Search runs"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            {runsLoading ? <p className="hint">Loading runs…</p> : null}
            {!runsLoading && runs.length === 0 ? (
              <p className="hint">No saved runs yet. Start from Home or ask your coding agent to run a recipe.</p>
            ) : null}
            {!runsLoading && runs.length > 0 && filtered.length === 0 ? (
              <p className="hint">No runs match your search.</p>
            ) : null}
            <div className="run-list-scroll">
              {groups.map(([group, items]) => (
                <div key={group}>
                  <p className="run-group-title">{group}</p>
                  {items.map((run) => {
                    const id = run.id || run;
                    const title = run.title || id;
                    return (
                      <button
                        key={id}
                        type="button"
                        className="asset-row"
                        aria-current={current === id ? "true" : undefined}
                        onClick={() => openRun(id)}
                      >
                        <span className="asset-title">{title}</span>
                        <div className="asset-row-meta">
                          {run.unchecked ? (
                            <span className="status-badge unchecked">Unchecked</span>
                          ) : (
                            <span className="status-badge checked">Checked</span>
                          )}
                          {run.modified_at ? <span className="hint">{formatRelative(run.modified_at)}</span> : null}
                        </div>
                      </button>
                    );
                  })}
                </div>
              ))}
            </div>
          </>
        )}
      </nav>
    </>
  );
}

function Home({ runs }) {
  const recent = [...(runs || [])]
    .sort((a, b) => Number(b.modified_at || 0) - Number(a.modified_at || 0))
    .slice(0, 4);
  const setView = useLayout((s) => s.setView);
  const setRun = useLayout((s) => s.setRun);
  function openRun(id) {
    setRun(id);
    setView("runs");
    const url = new URL(window.location.href);
    url.searchParams.set("run", id);
    url.searchParams.delete("view");
    window.history.replaceState({}, "", url);
  }
  return (
    <section className="home-page" aria-label="Arc home">
      <h1>Co-solve EE problems with your agent</h1>
      <p className="home-lede">
        Arc runs verified engines on circuits, control, and power coursework. You and your coding agent share the same
        live run: answer, plots, and reasoning trail on this machine.
      </p>
      <ol className="home-steps">
        <li>Ask your agent to run an Arc recipe, or use the CLI below.</li>
        <li>Open the run here to inspect verification, plots, and the explanation.</li>
        <li>Edit parameters or the diagram, then re-run to explore what changes.</li>
      </ol>
      <div className="card">
        <h2>Try a problem</h2>
        <p className="hint">Runs are stored under ./runs on this machine.</p>
        <code className="home-cli">electrical-engineer run simulate-circuit</code>
        <button
          type="button"
          className="button-primary"
          style={{ marginTop: 16, alignSelf: "flex-start" }}
          onClick={() => setView("runs")}
        >
          Open runs
        </button>
      </div>
      {recent.length > 0 ? (
        <div className="card">
          <h2>Recent runs</h2>
          {recent.map((run) => {
            const id = run.id || run;
            return (
              <button key={id} type="button" className="asset-row" onClick={() => openRun(id)}>
                <span className="asset-title">{run.title || id}</span>
                <div className="asset-row-meta">
                  {run.unchecked ? (
                    <span className="status-badge unchecked">Unchecked</span>
                  ) : (
                    <span className="status-badge checked">Checked</span>
                  )}
                  {run.recipe_id ? <span className="hint">{run.recipe_id}</span> : null}
                </div>
              </button>
            );
          })}
        </div>
      ) : null}
    </section>
  );
}

function Workspace() {
  const view = useLayout((s) => s.view);
  const id = useLayout((s) => s.currentRunId);
  const { data } = useRun(id);
  const [runs, setRuns] = useState([]);
  useEffect(() => {
    fetch("/api/runs")
      .then((r) => r.json())
      .then((d) => setRuns(d.runs || []))
      .catch(() => setRuns([]));
  }, [id, view]);
  if (view === "home") {
    return <Home runs={runs} />;
  }
  if (view === "gallery") {
    return renderSlot("visual.gallery");
  }
  if (view === "control-studio") {
    return renderSlot("control.studio");
  }
  if (view === "library") {
    return renderSlot("rag.inventory");
  }
  if (!id) {
    return (
      <section className="home-page">
        <h1>Runs</h1>
        <p className="empty">Select a run from the sidebar, or go to Home to start with the CLI.</p>
        <button type="button" className="button-secondary" onClick={() => useLayout.getState().setView("home")}>
          Back to Home
        </button>
      </section>
    );
  }
  let recipeId = "";
  let hasStudyDiagram = false;
  try {
    const evid = JSON.parse(data?.summary || "{}");
    recipeId = evid.recipe_id || "";
  } catch {
    recipeId = "";
  }
  const cd = data?.control_diagram;
  hasStudyDiagram = Boolean(cd && Array.isArray(cd.nodes) && cd.nodes.length > 0);
  return (
    <div className="lab">
      {renderSlot("run.result", { id })}
      <div
        className={
          hasStudyDiagram ? "lab-surface lab-surface-primary lab-surface-study" : "lab-surface lab-surface-primary lab-surface-circuit"
        }
      >
        {renderSlot("run.canvas", { id })}
        {hasStudyDiagram ? null : renderSlot("run.inspector", { id })}
      </div>
      <EngineArtifacts id={id} recipeId={recipeId} />
      {renderSlot("run.argument", { id })}
      {renderSlot("run.more", { id })}
    </div>
  );
}

function useRun(id) {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  useEffect(() => {
    if (!id) {
      setData(null);
      setError("");
      return;
    }
    fetch(`/api/runs/${id}`)
      .then((r) => {
        if (!r.ok) throw new Error("failed");
        return r.json();
      })
      .then((d) => {
        setData(d);
        setError("");
      })
      .catch(() => {
        setData(null);
        setError("failed");
      });
  }, [id]);
  return { data, error };
}

function parseEvid(summary) {
  try {
    const obj = JSON.parse(summary);
    return obj && typeof obj === "object" ? obj : {};
  } catch {
    return {};
  }
}

function Result({ id }) {
  const { data, error } = useRun(id);
  const evid = parseEvid(data?.summary || "");
  const unchecked = evid.unchecked === true || evid.token === "unchecked";
  const title = data?.title || evid.title || id;
  const state = error ? "failed" : data?.state || "Working";
  const loading = !data && !error;
  const live =
    state === "waiting-human"
      ? "Waiting for topology confirm"
      : state === "failed"
        ? "Run failed to load."
        : state === "Working"
          ? "Working"
          : "";
  const value = error ? "unavailable" : unchecked ? "Pending verification" : evid.value == null ? "Working…" : String(evid.value);
  const verifierRaw = evid.verifier ? String(evid.verifier) : "";
  let verifierHint = "This answer passed a checked simulation step.";
  if (unchecked) {
    verifierHint =
      "Unchecked means Arc could not attach a checked simulation for this result. Treat numbers as symbolic until you re-run with the right engine.";
  } else if (verifierRaw && !/label-unverified|label-unchecked| via /i.test(verifierRaw)) {
    verifierHint = verifierRaw;
  }
  if (loading) {
    return <p className="loading-block" aria-live="polite">Loading run…</p>;
  }
  return (
    <article className="answer-card" aria-live="polite">
      <h1>{title}</h1>
      <p className={error ? "answer-value" : unchecked ? "answer-value" : "answer-value is-checked"}>{value}</p>
      {error ? (
        <span className="status-badge failed">Failed</span>
      ) : unchecked ? (
        <span className="status-badge unchecked">Unchecked</span>
      ) : (
        <span className="status-badge checked">Checked</span>
      )}
      <p className="status-hint">{error ? "Could not load this run from disk. Check the run id or create a new run." : verifierHint}</p>
      {live ? <p className="hint">{live}</p> : null}
    </article>
  );
}

function CanvasStub({ id }) {
  return <Canvas id={id} />;
}

function InspectorSlot() {
  return <Inspector />;
}

function Argument({ id }) {
  const { data, error } = useRun(id);
  const text = data?.argument || "";
  return (
    <section className="argument">
      <h2>Explanation</h2>
      {error ? <p className="failed">unavailable</p> : null}
      {!error && !text ? <p className="empty">No explanation yet.</p> : null}
      {text ? <div className="prose">{text}</div> : null}
    </section>
  );
}

function More({ id }) {
  const { data, error } = useRun(id);
  if (error || !data) return null;
  const excerpt = data.observation_excerpt || {};
  const spans = Array.isArray(data.trace_excerpt) ? data.trace_excerpt : [];
  return (
    <div className="disclosures diagnostics-panel">
      <details>
        <summary>Observation</summary>
        <dl className="obs-excerpt">
          <div>
            <dt>unchecked</dt>
            <dd>
              <code>{excerpt.unchecked ? String(excerpt.token || "unchecked") : "false"}</code>
            </dd>
          </div>
          {excerpt.unchecked_reason ? (
            <div>
              <dt>unchecked_reason</dt>
              <dd>
                <code>{excerpt.unchecked_reason}</code>
              </dd>
            </div>
          ) : null}
          <div>
            <dt>capabilities</dt>
            <dd>{(excerpt.capabilities || []).join(", ") || "—"}</dd>
          </div>
          <div>
            <dt>providers</dt>
            <dd>{(excerpt.providers || []).join(", ") || "—"}</dd>
          </div>
          <div>
            <dt>retrieve.empty</dt>
            <dd>{excerpt.retrieve_empty ? "true" : "false"}</dd>
          </div>
        </dl>
        <details>
          <summary>Raw observation JSON</summary>
          <pre className="number-display">{data.observation || ""}</pre>
        </details>
      </details>
      <details>
        <summary>Trace</summary>
        {spans.length === 0 ? (
          <p className="empty">No trace.jsonl for this run.</p>
        ) : (
          <ol className="trace-list">
            {spans.map((span, idx) => (
              <li key={`${span.name}-${idx}`}>
                <code>{span.name}</code>
                {span.node_id ? <span className="hint"> {span.node_id}</span> : null}
                {span.duration_ms != null ? (
                  <span className="hint"> {Number(span.duration_ms).toFixed(1)}ms</span>
                ) : null}
                {span.unchecked ? <span className="badge-pill">unchecked</span> : null}
              </li>
            ))}
          </ol>
        )}
      </details>
      <details>
        <summary>Evidentiary JSON</summary>
        <pre className="number-display">{data.evidentiary || ""}</pre>
      </details>
      <details>
        <summary>Plan</summary>
        {data.plan ? <pre className="number-display">{data.plan}</pre> : <p className="empty">No plan yet.</p>}
      </details>
      <details>
        <summary>Raw graph</summary>
        <pre className="number-display">{JSON.stringify(data.graph || {}, null, 2)}</pre>
      </details>
      <details>
        <summary>Artifacts</summary>
        <p className="hint">Library SVG/PNG from this run only.</p>
        <img className="plot" alt={`Run ${id} artifact`} src={`/api/runs/${id}/artifact.svg`} width="200" height="80" />
      </details>
    </div>
  );
}

register("root", Root);
register("sidebar", Sidebar);
register("workspace", Workspace);
register("run.result", Result);
register("run.canvas", CanvasStub);
register("run.inspector", InspectorSlot);
register("run.argument", Argument);
register("run.more", More);
register("photo.confirm", function PhotoConfirm() {
  return null;
});
register("rag.inventory", Library);
register("visual.gallery", VisualGallery);
register("control.studio", ControlStudio);

