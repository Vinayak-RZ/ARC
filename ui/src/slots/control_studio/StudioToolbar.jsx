export function StudioToolbar({ title, resultsStale, zoomPct, onUndo, onRedo, onSimulate, onFit, onZoomIn, onZoomOut, canRedo }) {
  const pct = Math.round((zoomPct || 1) * 100);
  return (
    <header className="studio-bar" aria-label="Studio toolbar">
      <nav className="studio-crumb" aria-label="Breadcrumb">
        <span>Studio</span>
        <span className="breadcrumb-sep">/</span>
        <span className="breadcrumb-current">{title || "PID · DC motor"}</span>
      </nav>
      <div className="studio-segment" role="group" aria-label="Diagram mode">
        <button type="button" className="is-active" aria-pressed="true">
          Block diagram
        </button>
        <button type="button" aria-pressed="false" disabled>
          Circuit
        </button>
      </div>
      <div className="studio-bar-actions">
        <button type="button" className="cs-btn cs-btn-secondary" onClick={onUndo}>
          Undo
        </button>
        <button type="button" className="cs-btn cs-btn-secondary" onClick={onRedo} disabled={!canRedo}>
          Redo
        </button>
        <button type="button" className="cs-btn cs-btn-secondary" onClick={onFit}>
          Fit
        </button>
        <span className="studio-zoom-label tabular-nums">{pct}%</span>
        <button type="button" className="cs-btn cs-btn-secondary" onClick={onZoomOut} aria-label="Zoom out">
          −
        </button>
        <button type="button" className="cs-btn cs-btn-secondary" onClick={onZoomIn} aria-label="Zoom in">
          +
        </button>
        <button
          type="button"
          className={`cs-btn cs-btn-primary cs-simulate-btn${resultsStale ? " is-stale" : ""}`}
          onClick={onSimulate}
        >
          {resultsStale ? "Simulate again" : "Simulate"}
        </button>
      </div>
    </header>
  );
}
