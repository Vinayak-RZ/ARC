export function LabShell({ title, controls, children, readouts, check, exampleId, onOpenExample }) {
  return (
    <div className="lab-shell">
      <h2>{title}</h2>
      <div className="lab-shell-grid">
        <aside className="lab-controls">{controls}</aside>
        <div className="lab-main">
          {children}
          {readouts ? <div className="lab-readouts">{readouts}</div> : null}
          {check ? <div className="lab-check">{check}</div> : null}
          {exampleId && onOpenExample ? (
            <button type="button" className="button-secondary" onClick={() => onOpenExample(exampleId)}>
              Open matching problem
            </button>
          ) : null}
        </div>
      </div>
    </div>
  );
}
