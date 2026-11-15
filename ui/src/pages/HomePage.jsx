import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { ChevronDown } from "lucide-react";
import { Shortcut } from "../components/Shortcut.jsx";
import { ExampleThumb } from "../components/ExampleThumb.jsx";
import { MascotState } from "../components/MascotState.jsx";
import { ArcMascot } from "../mascot/index.js";
import { useCurriculum } from "../hooks/useLearn.js";
import { relativeTime } from "../units/format.js";
import { displayTitle, subjectTag } from "../runDisplay.js";

const PLACEHOLDERS = [
  "Find Vout for a 10 V divider with 1 kΩ and 1 kΩ…",
  "Step response for a first-order plant…",
  "Clearing angle after a fault on an SMIB machine…",
];

function detectSubject(text) {
  const t = text.toLowerCase();
  if (t.includes("bode") || t.includes("transfer") || t.includes("compensator")) return "control";
  if (t.includes("rectifier") || t.includes("converter") || t.includes("inverter")) return "power_electronics";
  if (t.includes("relay") || t.includes("swing") || t.includes("fault") || t.includes("dispatch")) return "power";
  if (t.includes("fourier") || t.includes("fft") || t.includes("frequency")) return "signals";
  if (t.includes("op-amp") || t.includes("opamp") || t.includes("amplifier")) return "electronics";
  if (t.includes("bridge") || t.includes("wheatstone")) return "measurements";
  if (t.includes("transmission") || t.includes("line param")) return "em";
  if (t.includes("laplace") || t.includes("complex")) return "maths";
  if (t.includes("motor") || t.includes("drive")) return "machines";
  return "circuits";
}

export function HomePage({
  runs,
  onRunsChange,
  onOpenProblem,
  onOpenLearn,
  onOpenSubject,
  seeding = false,
}) {
  const [examples, setExamples] = useState([]);
  const [packs, setPacks] = useState([]);
  const [prompt, setPrompt] = useState("");
  const [subject, setSubject] = useState("circuits");
  const [subjectLocked, setSubjectLocked] = useState(false);
  const [examplePack, setExamplePack] = useState(null);
  const [showAllExamples, setShowAllExamples] = useState(false);
  const [popover, setPopover] = useState(false);
  const [busy, setBusy] = useState(false);
  const [lastUnchecked, setLastUnchecked] = useState(null);
  const [phIndex, setPhIndex] = useState(0);
  const areaRef = useRef(null);
  const { data: curriculum, error: curriculumError } = useCurriculum();
  const recent = [...runs]
    .sort((a, b) => Number(b.modified_at || 0) - Number(a.modified_at || 0))
    .slice(0, 3);

  const currentSemester = useMemo(() => {
    if (!curriculum) return null;
    const n = curriculum.current_semester;
    return (curriculum.semesters || []).find((s) => s.n === n) || null;
  }, [curriculum]);

  const filteredExamples = useMemo(() => {
    if (!examplePack) return examples;
    return examples.filter((ex) => ex.pack === examplePack);
  }, [examples, examplePack]);

  const visibleExamples = useMemo(() => {
    if (examplePack || showAllExamples) return filteredExamples;
    return filteredExamples.slice(0, 6);
  }, [filteredExamples, examplePack, showAllExamples]);

  useEffect(() => {
    fetch("/api/examples")
      .then((r) => r.json())
      .then((d) => setExamples(d.examples || []))
      .catch(() => setExamples([]));
    fetch("/api/capabilities")
      .then((r) => r.json())
      .then((d) => setPacks(d.packs || []))
      .catch(() => setPacks([]));
  }, []);

  useEffect(() => {
    const t = setInterval(() => setPhIndex((i) => (i + 1) % PLACEHOLDERS.length), 5000);
    return () => clearInterval(t);
  }, []);

  const resizeArea = useCallback(() => {
    const el = areaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(200, Math.max(56, el.scrollHeight))}px`;
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
    setLastUnchecked(null);
    try {
      const r = await fetch("/api/problems", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt.trim(), subject }),
      });
      const body = await r.json();
      if (body.run_id) {
        setLastUnchecked(Boolean(body.unchecked));
        onRunsChange();
        onOpenProblem(body.run_id);
        setPrompt("");
      }
    } finally {
      setBusy(false);
    }
  }

  const subjectLabel = packs.find((s) => s.id === subject)?.label || "Circuits";
  const mascotMode = busy ? "thinking" : prompt.trim() ? "listening" : lastUnchecked === true ? "warning" : lastUnchecked === false ? "success" : "ambient";

  function selectPack(packId) {
    setSubject(packId);
    setSubjectLocked(true);
    setExamplePack(packId);
    setShowAllExamples(false);
  }

  return (
    <div className="page-column home-product">
      <header className="page-header home-header-with-mascot">
        <div>
          <h1>Ask a problem</h1>
          <p className="home-lede">Arc checks answers with real engines. Your agent can edit the same problem.</p>
        </div>
        <ArcMascot mode={mascotMode} size={64} label="Arc" arrive />
      </header>
      <form className="composer-card composer-card-compact" onSubmit={askProblem}>
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
                {packs.map((s) => (
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
          className="composer-input composer-input-inset"
          value={prompt}
          placeholder={PLACEHOLDERS[phIndex]}
          onChange={(e) => setPrompt(e.target.value)}
          rows={2}
        />
        <div className="composer-footer">
          <span className="hint">
            Press <Shortcut keys="Ctrl Enter" /> to solve
          </span>
          <button id="home-solve-btn" type="submit" className="button-primary button-compact" disabled={busy || !prompt.trim()}>
            Solve
          </button>
        </div>
      </form>
      {packs.length > 0 ? (
        <section className="home-section capabilities-section">
          <h2>What Arc can do</h2>
          <div className="capability-grid">
            {packs.map((p) => (
              <button key={p.id} type="button" className="capability-card" onClick={() => selectPack(p.id)}>
                <span className="capability-label">{p.label}</span>
                <span className="capability-count">{p.recipe_count} recipes</span>
                <span className="hint">{p.blurb}</span>
              </button>
            ))}
          </div>
        </section>
      ) : null}
      <section className="home-section">
        <h2>Try an example</h2>
        {packs.length > 0 ? (
          <div className="library-domain-chips home-pack-chips" role="group" aria-label="Filter examples by pack">
            <button
              type="button"
              className={examplePack ? "chip" : "chip is-pressed"}
              onClick={() => {
                setExamplePack(null);
                setShowAllExamples(false);
              }}
            >
              All
            </button>
            {packs.map((p) => (
              <button
                key={p.id}
                type="button"
                className={examplePack === p.id ? "chip is-pressed" : "chip"}
                onClick={() => selectPack(p.id)}
              >
                {p.label}
              </button>
            ))}
          </div>
        ) : null}
        <div className="example-grid example-grid-six">
          {visibleExamples.map((ex) => (
            <button
              key={ex.id}
              type="button"
              className="example-card"
              disabled={busy}
              onClick={() => solveExample(ex.id)}
            >
              <div className="example-thumb-frame example-thumb-wrap">
                <ExampleThumb id={ex.id} />
              </div>
              <span className="subject-chip-muted">{ex.subject}</span>
              <span className="example-card-title">{ex.title}</span>
              <span className="hint">{ex.caption}</span>
            </button>
          ))}
        </div>
        {!examplePack && !showAllExamples && examples.length > 6 ? (
          <button type="button" className="button-secondary home-show-all-examples" onClick={() => setShowAllExamples(true)}>
            Show all ({examples.length})
          </button>
        ) : null}
      </section>
      {curriculum && !curriculumError && currentSemester?.subjects?.length ? (
        <section className="home-section home-continue-learn">
          <div className="home-continue-learn-head">
            <h2>Continue learning</h2>
            {onOpenLearn ? (
              <button type="button" className="button-secondary" onClick={onOpenLearn}>
                Open Learn
              </button>
            ) : null}
          </div>
          <ul className="home-continue-rows">
            {currentSemester.subjects.map((subj) => (
              <li key={subj.id}>
                <button
                  type="button"
                  className="home-continue-row"
                  onClick={() => onOpenSubject?.(subj.id)}
                  disabled={!onOpenSubject}
                >
                  <span className="learn-code-label">{subj.code || subj.id}</span>
                  <span className="example-card-title">{subj.title}</span>
                  <span className="hint">
                    {subj.progress?.done || 0} / {subj.progress?.total || 0} topics
                  </span>
                </button>
              </li>
            ))}
          </ul>
        </section>
      ) : null}
      {seeding && recent.length === 0 ? (
        <section className="home-section">
          <MascotState kind="loading" size={56} title="Preparing sample problems…" message="Checking a few recipes so Recent is not empty." />
        </section>
      ) : null}
      {recent.length > 0 ? (
        <section className="home-section continue-section">
          <h2>Continue</h2>
          <div className="continue-grid">
            {recent.map((run) => (
              <button key={run.id} type="button" className="continue-card" onClick={() => onOpenProblem(run.id)}>
                <span className="subject-chip-muted">{run.subject || subjectTag(run)}</span>
                <span className="example-card-title">
                  {displayTitle(run)}
                  {run.sample ? <span className="sample-badge">Sample</span> : null}
                </span>
                <span className="hint continue-meta">{relativeTime(run.modified_at)}</span>
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
        <p className="hint">Connect your coding agent.</p>
        <p className="hint">
          <kbd className="home-agent-cmd">electrical-engineer mcp</kbd> — then connect Cursor or Claude Code.
        </p>
      </section>
    </div>
  );
}