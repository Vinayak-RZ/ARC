/** Placeholder until commit c09 fills the Subject page. */
export function SubjectPage({ subjectId, onBack }) {
  return (
    <div className="learn-page">
      <button type="button" className="text-link" onClick={onBack}>
        ← Learn
      </button>
      <h1>{subjectId}</h1>
      <p className="hint">Loading subject…</p>
    </div>
  );
}
