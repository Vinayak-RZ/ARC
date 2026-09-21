import { useEffect, useState } from "react";
import { register, renderSlot } from "./registry.js";
import { useLayout } from "../store.js";
import { Canvas } from "./canvas/Canvas.jsx";
import { Inspector } from "./canvas/Inspector.jsx";
import { Library } from "./library.jsx";
import { EngineArtifacts } from "./engine/EngineArtifacts.jsx";

function Root() {
  return (
    <div className="shell">
      <a className="skip" href="#workspace">
        Skip to workspace
      </a>
      <header className="topbar">
        <img className="brand-mark" src="/arc-icon.png" width="32" height="32" alt="Arc" />
        <strong>Arc</strong>
        <div className="engines" aria-label="Engines">
          <span className="chip">Numeric</span>
          <span className="chip">SPICE</span>
          <span
            className="chip"
            title="Optional. Arc calls MATLAB MCP when the binary is installed. The coding assistant does not attach MATLAB MCP. Missing MATLAB stays unchecked. OSS simulators stay first-class."
            aria-label="MATLAB optional via Arc"
          >
            MATLAB · via Arc
          </span>
          <span
            className="chip"
            title="Optional. Arc calls Simulink Agentic Toolkit tools inside the kernel when tools.json is installed. The coding assistant does not attach the toolkit. Missing Simulink stays unchecked (CD-SIMULINK-PLANT). OSS simulators stay first-class."
            aria-label="Simulink optional via Arc"
          >
            Simulink · via Arc
          </span>
        </div>
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
  const current = useLayout((s) => s.currentRunId);
  const view = useLayout((s) => s.view);
  const setRun = useLayout((s) => s.setRun);
  const setView = useLayout((s) => s.setView);
  useEffect(() => {
    const q = new URLSearchParams(window.location.search);
    const viewQ = q.get("view");
    if (viewQ === "library") setView("library");
    const run = q.get("run");
    if (run) setRun(run);
  }, [setRun, setView]);
  useEffect(() => {
    fetch("/api/runs")
      .then((r) => r.json())
      .then((d) => setRuns(d.runs || []))
      .catch(() => setRuns([]));
  }, []);
  function openRuns() {
    setView("runs");
    const url = new URL(window.location.href);
    url.searchParams.delete("view");
    window.history.replaceState({}, "", url);
    setOpen(false);
  }
  function openBooks() {
    setView("library");
    const url = new URL(window.location.href);
    url.searchParams.set("view", "library");
    url.searchParams.delete("run");
    window.history.replaceState({}, "", url);
    setOpen(false);
  }
  return (
    <>
      <button
        className="nav-toggle"
        type="button"
        aria-expanded={open}
        aria-controls="run-list"
        onClick={() => setOpen(!open)}
      >
        {view === "library" ? "Books" : "Runs"}
      </button>
      <nav id="run-list" className={open ? "sidebar is-open" : "sidebar"} aria-label="Workspace">
        <div className="sidebar-switch" role="group" aria-label="Workspace">
          <button type="button" className="sidebar-switch-btn" aria-current={view === "runs" ? "true" : undefined} onClick={openRuns}>
            Runs
          </button>
          <button type="button" className="sidebar-switch-btn" aria-current={view === "library" ? "true" : undefined} onClick={openBooks}>
            Books
          </button>
        </div>
        {view === "library" ? (
          <p className="hint">Ingest and tag books in the workspace. Files stay on this machine.</p>
        ) : (
          <>
            <h2>Runs</h2>
            {runs.length === 0 ? (
              <p className="hint">
                No saved runs yet. Ask the coding assistant, or type electrical-engineer run
                solve-circuit-problem.
              </p>
            ) : null}
            {runs.map((run) => {
              const id = run.id || run;
              const title = run.title || id;
              return (
                <button
                  key={id}
                  className="asset-row"
                  aria-current={current === id ? "true" : undefined}
                  onClick={() => {
                    setRun(id);
                    const url = new URL(window.location.href);
                    url.searchParams.set("run", id);
                    url.searchParams.delete("view");
                    window.history.replaceState({}, "", url);
                    setOpen(false);
                  }}
                >
                  <span className="asset-title">{title}</span>
                  {run.recipe_id ? <span className="hint">{run.recipe_id}</span> : null}
                  <span className="hint">{id}</span>
                  {run.unchecked ? <span className="badge-pill">unchecked</span> : null}
                </button>
              );
            })}
          </>
        )}
      </nav>
    </>
  );
}

function Workspace() {
  const view = useLayout((s) => s.view);
  const id = useLayout((s) => s.currentRunId);
  const { data } = useRun(id);
  if (view === "library") {
    return renderSlot("rag.inventory");
  }
  if (!id) {
    return <p className="empty">No run selected. Open one from the list, or type electrical-engineer run simulate-circuit.</p>;
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
      <div className="lab-surface lab-surface-primary">
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
  const live =
    state === "waiting-human"
      ? "Waiting for topology confirm"
      : state === "failed"
        ? "Run failed to load."
        : state === "Working"
          ? "Working"
          : "";
  const value = error ? "failed" : unchecked ? "unchecked" : evid.value == null ? "Working" : String(evid.value);
  const verifierRaw = evid.verifier ? String(evid.verifier) : "";
  let verifierHint = null;
  if (!unchecked && verifierRaw) {
    if (/label-unverified|label-unchecked| via /i.test(verifierRaw)) {
      verifierHint = "Checked simulation";
    } else {
      verifierHint = verifierRaw;
    }
  }
  return (
    <div className="result-strip" aria-live="polite">
      <span className="asset-title">{title}</span>
      <span className={error ? "failed" : unchecked ? "number-display" : "number-display checked"}>
        {value}
      </span>
      {unchecked ? <span className="badge-pill">unchecked</span> : null}
      {verifierHint ? <span className="hint">{verifierHint}</span> : null}
      {live ? <span className="hint">{live}</span> : null}
    </div>
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
    <div className="disclosures">
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

