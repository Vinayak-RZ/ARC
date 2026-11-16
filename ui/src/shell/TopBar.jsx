import { SlidersHorizontal, MoreHorizontal } from "lucide-react";
import { useLayout } from "../store.js";
import { displayTitle } from "../runDisplay.js";
import { ArcMascot } from "../mascot/index.js";

const VIEW_LABEL = {
  home: "Home",
  problems: "Problems",
  studio: "Studio",
  gallery: "Gallery",
  library: "Library",
  learn: "Learn",
  settings: "Settings",
};

export function TopBar({ runMeta, onPrimaryAction, primaryLabel, runAgainPrimary, onNavigate }) {
  const view = useLayout((s) => s.view);
  const id = useLayout((s) => s.currentRunId);
  const drawer = useLayout((s) => s.parametersOpen);
  const setDrawer = useLayout((s) => s.setParametersOpen);
  const agentEditing = useLayout((s) => s.agentEditing);
  const go = onNavigate || (() => {});
  const crumbs = [];
  crumbs.push({ label: VIEW_LABEL[view] || "Arc", view, clickable: Boolean(id && view === "problems") });
  if (view === "problems" && id && runMeta) {
    crumbs.push({ label: displayTitle(runMeta), view: null, clickable: false });
  }
  const showParams = view === "problems" && Boolean(id);
  const runAgainClass = runAgainPrimary ? "button-primary button-compact" : "button-secondary button-compact";
  return (
    <header className="product-topbar">
      <nav className="breadcrumb" aria-label="Breadcrumb">
        {crumbs.map((c, i) => (
          <span key={`${c.label}-${i}`}>
            {i > 0 ? <span className="breadcrumb-sep">/</span> : null}
            {c.clickable ? (
              <button type="button" className="breadcrumb-link" onClick={() => go({ view: c.view || "problems" })}>
                {c.label}
              </button>
            ) : (
              <span className={i === crumbs.length - 1 ? "breadcrumb-current" : ""}>{c.label}</span>
            )}
          </span>
        ))}
      </nav>
      <div className="topbar-actions">
        {agentEditing ? (
          <>
            <ArcMascot className="topbar-mascot" size={28} mode="thinking" label="Agent busy" />
            <span className="presence-chip">Agent editing</span>
          </>
        ) : null}
        {showParams ? (
          <>
            <button type="button" className="button-secondary button-compact" onClick={() => go({ view: "studio" })}>
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
          <button type="button" className="button-primary button-compact" onClick={() => go({ view: "home" })}>
            New problem
          </button>
        ) : null}
      </div>
    </header>
  );
}
