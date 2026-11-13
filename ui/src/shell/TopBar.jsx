import { SlidersHorizontal } from "lucide-react";
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
  const drawer = useLayout((s) => s.parametersOpen);
  const setDrawer = useLayout((s) => s.setParametersOpen);
  const crumbs = [];
  crumbs.push(VIEW_LABEL[view] || "Arc");
  if (view === "problems" && id && runMeta) {
    crumbs.push(displayTitle(runMeta));
  }
  const showParams = view === "problems" && Boolean(id);
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
        {showParams ? (
          <button
            type="button"
            className={drawer ? "button-secondary button-compact is-active" : "button-secondary button-compact topbar-params-toggle"}
            aria-pressed={drawer ? "true" : "false"}
            onClick={() => setDrawer(!drawer)}
          >
            <SlidersHorizontal size={16} strokeWidth={1.5} />
            Parameters
          </button>
        ) : null}
        {primaryLabel ? (
          <button type="button" className="button-primary button-compact" onClick={onPrimaryAction}>
            {primaryLabel}
          </button>
        ) : null}
      </div>
    </header>
  );
}
