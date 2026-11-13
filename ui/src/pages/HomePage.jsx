import { useEffect, useState } from "react";
import { displayTitle, subjectTag } from "../runDisplay.js";

export function HomePage({ runs, onRunsChange, onOpenProblem }) {
  const [examples, setExamples] = useState([]);
  const [prompt, setPrompt] = useState("");
  const [subject, setSubject] = useState("circuits");
  const [busy, setBusy] = useState(false);
  const recent = [...runs]
    .sort((a, b) => Number(b.modified_at || 0) - Number(a.modified_at || 0))
    .slice(0, 3);
  useEffect(() => {
    fetch("/api/examples")
      .then((r) => r.json())
      .then((d) => setExamples(d.examples || []))
      .catch(() => setExamples([]));
  }, []);
  async function solveExample(id) {
    setBusy(true);
    try {
      const r = await fetch(`/api/examples/${id}/run`, { method: "POST" });
      const body = await r.json();
      if (body.run_id) {
        onRunsChange();
        onOpenProblem(body.run_id);
      }
    } finally {
      setBusy(false);
    }
  }
  async function askProblem(ev) {
    ev.preventDefault();
    if (!prompt.trim()) return;
    setBusy(true);
    try {
      const r = await fetch("/api/problems", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt.trim(), subject }),
      });
      const body = await r.json();
      if (body.run_id) {
        onRunsChange();
        onOpenProblem(body.run_id);
        setPrompt("");
      }
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="home-product">
      <h1>Ask a problem</h1>
      <p className="home-lede">Arc checks answers with real engines. Your agent can edit the same problem.</p>
      <form className="ask-composer card" onSubmit={askProblem}>
        <label className="field">
          Subject
          <select value={subject} onChange={(e) => setSubject(e.target.value)}>
            <option value="circuits">Circuits</option>
            <option value="control">Control</option>
            <option value="power">Power</option>
            <option value="signals">Signals</option>
          </select>
        </label>
        <label className="field">
          Problem
          <textarea rows={3} value={prompt} placeholder="Describe what to solve…" onChange={(e) => setPrompt(e.target.value)} />
        </label>
        <button type="submit" className="button-primary" disabled={busy}>
          Solve
        </button>
      </form>
      <h2>Try an example</h2>
      <div className="example-grid example-grid-six">
        {examples.map((ex) => (
          <button
            key={ex.id}
            type="button"
            className="example-card"
            disabled={busy}
            onClick={() => solveExample(ex.id)}
          >
            {ex.thumbnail ? (
              <img className="example-thumb" src={ex.thumbnail} alt="" loading="lazy" />
            ) : null}
            <span className="subject-tag">{ex.subject}</span>
            <span className="example-card-title">{ex.title}</span>
            <span className="hint">{ex.caption}</span>
          </button>
        ))}
      </div>
      {recent.length > 0 ? (
        <>
          <h2>Continue</h2>
          <div className="continue-grid">
            {recent.map((run) => (
              <button key={run.id} type="button" className="continue-card" onClick={() => onOpenProblem(run.id)}>
                <span className="subject-tag">{run.subject || subjectTag(run)}</span>
                <span className="example-card-title">{displayTitle(run)}</span>
                <span className={run.unchecked ? "status-badge unchecked" : "status-badge checked"}>
                  {run.unchecked ? "Unchecked" : "Checked"}
                </span>
              </button>
            ))}
          </div>
        </>
      ) : null}
      <div className="agent-card card">
        <h2>Agent</h2>
        <p className="hint">
          Run <code>electrical-engineer mcp</code> in this repo and connect Cursor, Claude Code, or Codex. From the CLI:
          <code className="home-cli">electrical-engineer run solve-circuit-problem</code>
        </p>
      </div>
    </div>
  );
}
