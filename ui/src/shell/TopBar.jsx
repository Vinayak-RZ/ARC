import { SlidersHorizontal, MoreHorizontal } from "lucide-react";
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

export function TopBar({ runMeta, onPrimaryAction, primaryLabel, runAgainPrimary }) {
  const view = useLayout((s) => s.view);
  const id = useLayout((s) => s.currentRunId);
  const drawer = useLayout((s) => s.parametersOpen);
  const setDrawer = useLayout((s) => s.setParametersOpen);
  const setView = useLayout((s) => s.setView);
  const agentEditing = useLayout((s) => s.agentEditing);
  const crumbs = [];
  crumbs.push(VIEW_LABEL[view] || "Arc");
  if (view === "problems" && id && runMeta) {
    crumbs.push(displayTitle(runMeta));
  }
  const showParams = view === "problems" && Boolean(id);
  const runAgainClass = runAgainPrimary ? "button-primary button-compact" : "button-secondary button-compact";
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
        {agentEditing ? <span className="presence-chip">Agent editing</span> : null}
        {showParams ? (
          <>
            <button type="button" className="button-secondary button-compact" onClick={() => setView("studio")}>
              Open in Studio
            </button>
            <button
              type="button"
              className={drawer ? "button-secondary button-compact is-active topbar-params-toggle" : "button-secondary button-compact topbar-params-toggle"}
              aria-pressed={drawer ? "true" : "false"}
              onClick={() => setDrawer(!drawer)}
            >
              <SlidersHorizontal size={16} strokeWidth={1.5} />
              Parameters
            </button>
            {primaryLabel ? (
              <button type="button" className={runAgainClass} onClick={onPrimaryAction}>
                {primaryLabel}
              </button>
            ) : null}
            <button type="button" className="button-secondary button-compact" aria-label="More actions">
              <MoreHorizontal size={16} />
            </button>
          </>
        ) : view === "problems" && !id ? (
          <button type="button" className="button-primary button-compact" onClick={() => setView("home")}>
            New problem
          </button>
        ) : null}
      </div>
    </header>
  );
}
