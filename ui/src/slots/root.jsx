import { useEffect, useState } from "react";
import { register, renderSlot } from "./registry.js";
import { useLayout } from "../store.js";
import { Canvas } from "./canvas/Canvas.jsx";
import { Inspector } from "./canvas/Inspector.jsx";

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
            title="The coding assistant will keep talking only to Arc. Arc will call MATLAB and return a short labeled result. A MATLAB Copilot scalar is not a check until Arc recomputes it. OSS simulators stay first-class."
          >
            MATLAB · coming next
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
  const setRun = useLayout((s) => s.setRun);
  useEffect(() => {
    const q = new URLSearchParams(window.location.search).get("run");
    if (q) setRun(q);
  }, [setRun]);
  useEffect(() => {
    fetch("/api/runs")
      .then((r) => r.json())
      .then((d) => setRuns(d.runs || []))
      .catch(() => setRuns([]));
  }, []);
  return (
    <>
      <button
        className="nav-toggle"
        type="button"
        aria-expanded={open}
        aria-controls="run-list"
        onClick={() => setOpen(!open)}
      >
        Runs
      </button>
      <nav id="run-list" className={open ? "sidebar is-open" : "sidebar"} aria-label="Runs">
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
      </nav>
    </>
  );
}

function Workspace() {
  const id = useLayout((s) => s.currentRunId);
  if (!id) {
    return <p className="empty">Select a run from the list.</p>;
  }
  return (
    <div className="lab">
      {renderSlot("run.result", { id })}
      <div className="lab-surface">
        {renderSlot("run.canvas", { id })}
        {renderSlot("run.inspector", { id })}
      </div>
      {renderSlot("run.argument", { id })}
      {renderSlot("run.more", { id })}
    </div>
  );
}

function useRun(id) {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  useEffect(() => {
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
  return (
    <div className="result-strip" aria-live="polite">
      <span className="asset-title">{title}</span>
      <span className={error ? "failed" : unchecked ? "number-display" : "number-display checked"}>
        {value}
      </span>
      {unchecked ? <span className="badge-pill">unchecked</span> : null}
      {evid.verifier ? <span className="hint">{evid.verifier}</span> : null}
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
  return (
    <div className="disclosures">
      <details>
        <summary>Evidentiary JSON</summary>
        <pre className="number-display">{data.evidentiary || ""}</pre>
      </details>
      <details>
        <summary>Plan</summary>
        {data.plan ? <pre className="number-display">{data.plan}</pre> : <p className="empty">No plan yet.</p>}
      </details>
      <details>
        <summary>Observation</summary>
        <pre className="number-display">{data.observation || ""}</pre>
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

