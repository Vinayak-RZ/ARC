import { useEffect, useState } from "react";
import { register, renderSlot } from "./registry.js";
import { useLayout } from "../store.js";

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
    return (
      <p className="empty">
        No saved runs yet. Ask the coding assistant, or type electrical-engineer run
        solve-circuit-problem.
      </p>
    );
  }
  return (
    <div>
      {renderSlot("run.detail", { id })}
      {renderSlot("run.evidentiary", { id })}
      {renderSlot("run.argument", { id })}
      {renderSlot("run.plan", { id })}
      {renderSlot("run.observation", { id })}
      {renderSlot("run.artifacts", { id })}
      {renderSlot("photo.confirm", { id })}
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

function RunDetail({ id }) {
  const { data, error } = useRun(id);
  const summary = data?.summary || "";
  const unchecked = (() => {
    try {
      const obj = JSON.parse(summary);
      return obj.unchecked === true || obj.token === "unchecked";
    } catch {
      return false;
    }
  })();
  const state = error ? "failed" : data?.state || "running";
  return (
    <section className="card" aria-live="polite">
      <div className="row-title">
        <h1>{id}</h1>
        {unchecked ? <span className="badge-pill">unchecked</span> : null}
      </div>
      <p className="hint">
        state {state}
        {state === "waiting-human" ? " — confirm in the photo slot" : ""}
      </p>
      {error ? <p className="failed">Run failed to load.</p> : null}
    </section>
  );
}

function Band({ id, title, field }) {
  const { data, error } = useRun(id);
  let body = data?.[field] || "";
  if (error) body = "";
  return (
    <section className="card">
      <h2>{title}</h2>
      {error ? <p className="failed">unavailable</p> : null}
      {!error && !body ? <p className="empty">No {title.toLowerCase()} yet.</p> : null}
      {body ? <pre className="number-display">{body}</pre> : null}
    </section>
  );
}

function Evidentiary({ id }) {
  return <Band id={id} title="Evidentiary" field="evidentiary" />;
}

function Argument({ id }) {
  return <Band id={id} title="Argument" field="argument" />;
}

function Plan({ id }) {
  return <Band id={id} title="Plan" field="plan" />;
}

function Observation({ id }) {
  return <Band id={id} title="Observation" field="observation" />;
}

function Artifacts({ id }) {
  return (
    <section className="card">
      <h2>Artifacts</h2>
      <p className="hint">Library SVG/PNG from this run only.</p>
      <img
        className="plot"
        alt={`Run ${id} artifact`}
        src={`/api/runs/${id}/artifact.svg`}
        width="200"
        height="80"
      />
    </section>
  );
}

function PhotoConfirm({ id }) {
  const [msg, setMsg] = useState("");
  return (
    <section className="card">
      <h2>Confirm topology</h2>
      <p className="hint">Writes confirmed.json. Does not run SPICE.</p>
      <button
        className="button-primary"
        type="button"
        onClick={() =>
          fetch(`/api/runs/${id}/confirm`, { method: "POST" })
            .then((r) => r.json())
            .then((d) => setMsg(JSON.stringify(d)))
        }
      >
        Confirm
      </button>
      {msg ? <pre className="number-display">{msg}</pre> : null}
    </section>
  );
}

register("root", Root);
register("sidebar", Sidebar);
register("workspace", Workspace);
register("run.detail", RunDetail);
register("run.evidentiary", Evidentiary);
register("run.argument", Argument);
register("run.plan", Plan);
register("run.observation", Observation);
register("run.artifacts", Artifacts);
register("photo.confirm", PhotoConfirm);
