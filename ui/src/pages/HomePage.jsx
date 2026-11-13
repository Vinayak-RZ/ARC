import { useCallback, useEffect, useRef, useState } from "react";
import { ChevronDown } from "lucide-react";
import { displayTitle, subjectTag } from "../runDisplay.js";

const SUBJECTS = [
  { id: "circuits", label: "Circuits" },
  { id: "control", label: "Control" },
  { id: "power", label: "Power" },
  { id: "signals", label: "Signals" },
  { id: "machines", label: "Machines" },
];

const PLACEHOLDERS = [
  "Find Vout for a 10 V divider with 1 kΩ and 1 kΩ…",
  "Step response for a first-order plant…",
  "Clearing angle after a fault on an SMIB machine…",
];

function detectSubject(text) {
  const t = text.toLowerCase();
  if (t.includes("bode") || t.includes("transfer") || t.includes("step")) return "control";
  if (t.includes("swing") || t.includes("fault") || t.includes("bus")) return "power";
  if (t.includes("motor") || t.includes("drive")) return "machines";
  if (t.includes("fft") || t.includes("frequency")) return "signals";
  return "circuits";
}

export function HomePage({ runs, onRunsChange, onOpenProblem }) {
  const [examples, setExamples] = useState([]);
  const [prompt, setPrompt] = useState("");
  const [subject, setSubject] = useState("circuits");
  const [subjectLocked, setSubjectLocked] = useState(false);
  const [popover, setPopover] = useState(false);
  const [busy, setBusy] = useState(false);
  const areaRef = useRef(null);
  const recent = [...runs]
    .sort((a, b) => Number(b.modified_at || 0) - Number(a.modified_at || 0))
    .slice(0, 3);

  useEffect(() => {
    fetch("/api/examples")
      .then((r) => r.json())
      .then((d) => setExamples(d.examples || []))
      .catch(() => setExamples([]));
  }, []);

  const resizeArea = useCallback(() => {
    const el = areaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(240, Math.max(88, el.scrollHeight))}px`;
  }, []);

  useEffect(() => {
    resizeArea();
  }, [prompt, resizeArea]);

  useEffect(() => {
    if (!subjectLocked) setSubject(detectSubject(prompt));
  }, [prompt, subjectLocked]);

  useEffect(() => {
    function onKey(e) {
      if ((e.metaKey || e.ctrlKey) && e.key === "Enter" && prompt.trim()) {
        e.preventDefault();
        document.getElementById("home-solve-btn")?.click();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [prompt]);

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
    ev?.preventDefault();
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

  const subjectLabel = SUBJECTS.find((s) => s.id === subject)?.label || "Circuits";

  return (
    <div className="page-column home-product">
      <header className="page-header">
        <h1>Ask a problem</h1>
        <p className="home-lede">Arc checks answers with real engines. Your agent can edit the same problem.</p>
      </header>
      <form className="composer-card" onSubmit={askProblem}>
        <div className="composer-top">
          <div className="subject-chip-wrap" onBlur={() => setTimeout(() => setPopover(false), 150)}>
            <button
              type="button"
              className="subject-chip"
              aria-expanded={popover}
              onClick={() => setPopover((v) => !v)}
            >
              {subjectLabel}
              <ChevronDown size={14} strokeWidth={1.5} />
            </button>
            {popover ? (
              <ul className="subject-popover" role="listbox">
                {SUBJECTS.map((s) => (
                  <li key={s.id}>
                    <button
                      type="button"
                      role="option"
                      aria-selected={subject === s.id}
                      onClick={() => {
                        setSubject(s.id);
                        setSubjectLocked(true);
                        setPopover(false);
                      }}
                    >
                      {s.label}
                    </button>
                  </li>
                ))}
              </ul>
            ) : null}
          </div>
        </div>
        <textarea
          ref={areaRef}
          className="composer-input"
          value={prompt}
          placeholder={PLACEHOLDERS[0]}
          onChange={(e) => setPrompt(e.target.value)}
          rows={3}
        />
        <div className="composer-footer">
          <span className="hint">⌘ Enter to solve</span>
          <button id="home-solve-btn" type="submit" className="button-primary button-compact" disabled={busy || !prompt.trim()}>
            Solve
          </button>
        </div>
      </form>
      <section className="home-section">
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
              <div className="example-thumb-wrap">
                {ex.thumbnail ? (
                  <img className="example-thumb" src={ex.thumbnail} alt="" loading="eager" decoding="async" />
                ) : null}
              </div>
              <span className="subject-chip-muted">{ex.subject}</span>
              <span className="example-card-title">{ex.title}</span>
              <span className="hint">{ex.caption}</span>
            </button>
          ))}
        </div>
      </section>
      {recent.length > 0 ? (
        <section className="home-section continue-section">
          <h2>Continue</h2>
          <div className="continue-grid">
            {recent.map((run) => (
              <button key={run.id} type="button" className="continue-card" onClick={() => onOpenProblem(run.id)}>
                <span className="subject-chip-muted">{run.subject || subjectTag(run)}</span>
                <span className="example-card-title">{displayTitle(run)}</span>
                <span className={run.unchecked ? "status-badge unchecked" : "status-badge checked"}>
                  {run.unchecked ? "Unchecked" : "Checked"}
                </span>
              </button>
            ))}
          </div>
        </section>
      ) : null}
      <section className="home-section agent-card">
        <h2>Agent</h2>
        <p className="hint">
          Run <code>electrical-engineer mcp</code> in this repo and connect Cursor or Claude Code. CLI:{" "}
          <code className="home-cli">electrical-engineer run solve-circuit-problem</code>
        </p>
      </section>
    </div>
  );
}
