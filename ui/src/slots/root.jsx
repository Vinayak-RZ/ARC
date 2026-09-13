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
        <img className="brand-mark" src="/arc-icon.png" width="32" height="32" alt="" />
        <strong>Arc</strong>
        <span className="hint">127.0.0.1 · named runs · exact token unchecked</span>
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
    <nav className="sidebar" aria-label="Runs">
      <h2>Runs</h2>
      {runs.length === 0 ? <p className="hint">No runs yet. Use the CLI.</p> : null}
      {runs.map((id) => (
        <button
          key={id}
          className="asset-row"
          aria-current={current === id ? "true" : undefined}
          onClick={() => setRun(id)}
        >
          {id}
        </button>
      ))}
    </nav>
  );
}

function Workspace() {
  const id = useLayout((s) => s.currentRunId);
  if (!id) {
    return (
      <p className="empty">
        Select a run. Summaries show a checked number or the exact token{" "}
        <span className="badge-pill">unchecked</span>. Photo confirm never
        simulates by itself.
      </p>
    );
  }
  return (
    <div>
      {renderSlot("run.detail", { id })}
      {renderSlot("run.artifacts", { id })}
      {renderSlot("photo.confirm", { id })}
    </div>
  );
}

function RunDetail({ id }) {
  const [summary, setSummary] = useState("");
  useEffect(() => {
    fetch(`/api/runs/${id}`)
      .then((r) => r.json())
      .then((d) => setSummary(d.summary || JSON.stringify(d)))
      .catch(() => setSummary(""));
  }, [id]);
  const unchecked = (() => {
    try {
      const obj = JSON.parse(summary);
      return obj.unchecked === true || obj.token === "unchecked";
    } catch {
      return false;
    }
  })();
  return (
    <section className="card" aria-live="polite">
      <div className="row-title">
        <h1>{id}</h1>
        {unchecked ? <span className="badge-pill">unchecked</span> : null}
      </div>
      <pre className="number-display">{summary}</pre>
    </section>
  );
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
register("run.artifacts", Artifacts);
register("photo.confirm", PhotoConfirm);
