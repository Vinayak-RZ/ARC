import { useEffect, useMemo, useState } from "react";
import { useCurriculum, useAchievements, postProgress, tryRecipe } from "../hooks/useLearn.js";
import { MascotState } from "../components/MascotState.jsx";

const CONTENT_TABS = [
  { id: "notes", label: "Notes" },
  { id: "practice", label: "Practice" },
  { id: "labs", label: "Labs" },
];

export function SubjectPage({ subjectId, onBack, onNavigate }) {
  const { data, error, loading, reload } = useCurriculum();
  const { reload: reloadAchievements } = useAchievements();
  const [topicId, setTopicId] = useState(null);
  const [tab, setTab] = useState("notes");
  const [toast, setToast] = useState("");
  const [busy, setBusy] = useState(false);
  const [labModal, setLabModal] = useState(null);

  const subject = useMemo(() => {
    if (!data) return null;
    for (const sem of data.semesters || []) {
      const hit = (sem.subjects || []).find((s) => s.id === subjectId);
      if (hit) return { ...hit, semester: sem.n };
    }
    return null;
  }, [data, subjectId]);

  useEffect(() => {
    if (subject?.topics?.length && !topicId) setTopicId(subject.topics[0].id);
  }, [subject, topicId]);

  useEffect(() => {
    if (!subject) return;
    const notes = (subject.notes || []).filter((n) => n.kind === "notes" && n.available);
    if (!notes.length && tab === "notes") setTab("practice");
  }, [subject, tab]);

  const topic = (subject?.topics || []).find((t) => t.id === topicId) || null;
  const notesFile = (subject?.notes || []).find((n) => n.kind === "notes" && n.available);
  const originalLabs = (subject?.notes || []).filter((n) => n.kind === "lab" && n.available);
  const iframeSrc = notesFile
    ? notesFile.url + (topic?.anchor ? `#${topic.anchor}` : "")
    : null;

  async function toggleDone(t, done) {
    const key = `${subject.id}/${t.id}`;
    try {
      await postProgress({ topic: key, done });
      await reload();
      await reloadAchievements();
    } catch {
      setToast("Could not save progress");
      setTimeout(() => setToast(""), 3000);
    }
  }

  async function onTry(recipeId) {
    setBusy(true);
    try {
      const r = await tryRecipe(recipeId);
      await reloadAchievements();
      onNavigate({ view: "problems", runId: r.run_id });
    } catch {
      setToast("Sample run failed (recipe may not be ready yet)");
      setTimeout(() => setToast(""), 3000);
    } finally {
      setBusy(false);
    }
  }

  async function openLab(labId) {
    try {
      await postProgress({ lab: labId });
      await reloadAchievements();
    } catch {
      /* ignore */
    }
    onNavigate({ view: "studio", tab: "labs", lab: labId });
  }

  if (loading) {
    return (
      <div className="learn-page">
        <div className="shimmer learn-shimmer" aria-busy="true" />
      </div>
    );
  }
  if (error || !subject) {
    return (
      <div className="learn-page">
        <button type="button" className="text-link" onClick={onBack}>
          ← Learn
        </button>
        <MascotState kind="error" title="Subject not found" actionLabel="Back" onAction={onBack} />
      </div>
    );
  }

  const labIds = topic?.labs?.length
    ? topic.labs
    : [...new Set((subject.topics || []).flatMap((t) => t.labs || []))];

  return (
    <div className="learn-subject-page">
      <header className="learn-subject-header">
        <nav className="learn-breadcrumb" aria-label="Breadcrumb">
          <button type="button" className="text-link" onClick={onBack}>
            Learn
          </button>
          <span aria-hidden> / </span>
          <span>S{subject.semester}</span>
          <span aria-hidden> / </span>
          <span>{subject.code || subject.title}</span>
        </nav>
        <h1>{subject.title}</h1>
        <p className="hint">
          {subject.source === "provided" ? "Your notes" : "Inferred syllabus"}
          {" · "}
          {subject.progress?.done || 0} / {subject.progress?.total || 0} topics
        </p>
      </header>

      <div className="learn-subject-layout">
        <aside className="learn-outline" aria-label="Topics">
          <ol>
            {(subject.topics || []).map((t) => (
              <li key={t.id} className={t.id === topicId ? "is-active" : undefined}>
                <button type="button" className="learn-outline-topic" onClick={() => setTopicId(t.id)}>
                  {t.title}
                </button>
                <label className="learn-done">
                  <input
                    type="checkbox"
                    checked={!!t.done}
                    onChange={(e) => toggleDone(t, e.target.checked)}
                  />
                  Done
                </label>
              </li>
            ))}
          </ol>
        </aside>

        <div className="learn-subject-main">
          <div className="tabs" role="tablist">
            {CONTENT_TABS.map((t) => {
              if (t.id === "notes" && !notesFile) return null;
              return (
                <button
                  key={t.id}
                  type="button"
                  role="tab"
                  aria-selected={tab === t.id}
                  className={tab === t.id ? "tab is-active" : "tab"}
                  onClick={() => setTab(t.id)}
                >
                  {t.label}
                </button>
              );
            })}
          </div>

          {tab === "notes" ? (
            notesFile ? (
              <iframe
                className="learn-notes-frame"
                title={`${subject.code || subject.title} study notes`}
                sandbox="allow-scripts"
                src={iframeSrc}
              />
            ) : (
              <MascotState
                kind="empty"
                title="Notes for this subject are not added. Topics come from the inferred syllabus."
              />
            )
          ) : null}

          {tab === "practice" ? (
            <div className="learn-practice">
              {!topic?.recipes?.length ? (
                <p className="hint">No Arc recipe for this topic yet.</p>
              ) : (
                <ul className="learn-recipe-list">
                  {topic.recipes.map((r) => (
                    <li key={r.id}>
                      <div>
                        <strong>{r.title}</strong>
                        {subject.pack ? <span className="tag copper">{subject.pack}</span> : null}
                      </div>
                      <div className="learn-recipe-actions">
                        <button
                          type="button"
                          className="button-primary"
                          disabled={busy}
                          onClick={() => onTry(r.id)}
                        >
                          Try sample
                        </button>
                        <button
                          type="button"
                          className="button-secondary"
                          onClick={() => onNavigate({ view: "home" })}
                        >
                          Ask your own
                        </button>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ) : null}

          {tab === "labs" ? (
            <div className="learn-labs">
              {!labIds.length && !originalLabs.length ? (
                <p className="hint">No labs linked for this subject.</p>
              ) : null}
              <div className="learn-lab-grid">
                {labIds.map((lab) => (
                  <button key={lab} type="button" className="learn-lab-card" onClick={() => openLab(lab)}>
                    <strong>{lab}</strong>
                    <span className="hint">Open in Studio</span>
                  </button>
                ))}
              </div>
              {originalLabs.map((lab) => (
                <button
                  key={lab.url}
                  type="button"
                  className="button-secondary"
                  onClick={() => setLabModal(lab)}
                >
                  Open original lab
                </button>
              ))}
            </div>
          ) : null}
        </div>
      </div>

      {toast ? (
        <div className="learn-toast" role="status">
          {toast}
        </div>
      ) : null}

      {labModal ? (
        <div className="learn-modal" role="dialog" aria-modal="true">
          <div className="learn-modal-panel">
            <header>
              <strong>{labModal.label}</strong>
              <button type="button" className="button-secondary" onClick={() => setLabModal(null)}>
                Close
              </button>
            </header>
            <iframe title={labModal.label} sandbox="allow-scripts" src={labModal.url} className="learn-notes-frame" />
          </div>
        </div>
      ) : null}
    </div>
  );
}
