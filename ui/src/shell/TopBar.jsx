import { useLayout } from "../store.js";
import { displayTitle } from "../runDisplay.js";

const VIEW_LABEL = {
  home: "Home",
  problems: "Problems",
  studio: "Studio",
  gallery: "Gallery",
  library: "Library",
  settings: "Settings",
};

export function TopBar({ runMeta, onPrimaryAction, primaryLabel }) {
  const view = useLayout((s) => s.view);
  const id = useLayout((s) => s.currentRunId);
  const crumbs = [];
  crumbs.push(VIEW_LABEL[view] || "Arc");
  if (view === "problems" && id && runMeta) {
    crumbs.push(displayTitle(runMeta));
  }
  return (
    <header className="product-topbar">
      <nav className="breadcrumb" aria-label="Breadcrumb">
        {crumbs.map((c, i) => (
          <span key={c}>
            {i > 0 ? <span className="breadcrumb-sep">/</span> : null}
            <span className={i === crumbs.length - 1 ? "breadcrumb-current" : ""}>{c}</span>
          </span>
        ))}
      </nav>
      <div className="topbar-actions">
        <span className="presence-chip" title="Live collaboration">
          Agent ready
        </span>
        {primaryLabel ? (
          <button type="button" className="button-primary" onClick={onPrimaryAction}>
            {primaryLabel}
          </button>
        ) : null}
      </div>
    </header>
  );
}
