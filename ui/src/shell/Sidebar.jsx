import {
  BookOpen,
  Home,
  Images,
  LifeBuoy,
  ListChecks,
  PanelLeftClose,
  PanelLeftOpen,
  Plug,
  Plus,
  Settings,
  Workflow,
} from "lucide-react";
import { useLayout } from "../store.js";
import { displayTitle, subjectTag } from "../runDisplay.js";

const PRIMARY = [
  { id: "home", label: "Home", icon: Home },
  { id: "problems", label: "Problems", icon: ListChecks },
  { id: "studio", label: "Studio", icon: Workflow },
  { id: "gallery", label: "Gallery", icon: Images },
  { id: "library", label: "Library", icon: BookOpen },
];

function statusDot(run) {
  if (run.unchecked) return "unchecked";
  return "checked";
}

export function Sidebar({ runs, onNavigate, onNewProblem }) {
  const collapsed = useLayout((s) => s.sidebarCollapsed);
  const view = useLayout((s) => s.view);
  const current = useLayout((s) => s.currentRunId);
  const toggle = useLayout((s) => s.toggleSidebar);
  const recent = [...runs]
    .sort((a, b) => Number(b.modified_at || 0) - Number(a.modified_at || 0))
    .slice(0, 5);
  return (
    <aside
      className={collapsed ? "product-sidebar is-collapsed" : "product-sidebar"}
      aria-label="Main navigation"
    >
      <div className="sidebar-head">
        <img className="brand-mark" src="/arc-icon.png" width="28" height="28" alt="Arc" />
        {!collapsed ? (
          <>
            <div className="sidebar-brand-text">
              <strong>Arc</strong>
              <span className="hint">EE coursework</span>
            </div>
          </>
        ) : null}
        <button type="button" className="icon-btn" title="Toggle sidebar (Ctrl+B)" onClick={toggle}>
          {collapsed ? <PanelLeftOpen size={18} strokeWidth={1.5} /> : <PanelLeftClose size={18} strokeWidth={1.5} />}
        </button>
      </div>
      <button
        type="button"
        className="sidebar-new-problem"
        title="New problem"
        onClick={onNewProblem}
      >
        <Plus size={18} strokeWidth={1.5} />
        {!collapsed ? <span>New problem</span> : null}
      </button>
      <nav className="sidebar-primary">
        {PRIMARY.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            type="button"
            title={collapsed ? label : undefined}
            className="sidebar-nav-item"
            aria-current={view === id ? "page" : undefined}
            onClick={() => onNavigate({ view: id })}
          >
            <Icon size={18} strokeWidth={1.5} />
            {!collapsed ? <span>{label}</span> : null}
          </button>
        ))}
      </nav>
      {!collapsed ? (
        <div className="sidebar-recent">
          <p className="sidebar-section-label">Recent</p>
          {recent.length === 0 ? <p className="hint">No problems yet.</p> : null}
          {recent.map((run) => (
            <button
              key={run.id}
              type="button"
              className="sidebar-recent-item"
              title={run.id}
              aria-current={current === run.id ? "true" : undefined}
              onClick={() => onNavigate({ view: "problems", runId: run.id })}
            >
              <span className={`status-dot ${statusDot(run)}`} aria-hidden="true" />
              <span className="sidebar-recent-title">{displayTitle(run)}</span>
              <span className="hint">{subjectTag(run)}</span>
            </button>
          ))}
        </div>
      ) : null}
      <footer className="sidebar-foot">
        <button type="button" className="sidebar-nav-item" title="Agent connected">
          <Plug size={18} strokeWidth={1.5} />
          {!collapsed ? <span>Agent connected</span> : null}
        </button>
        <button
          type="button"
          className="sidebar-nav-item"
          aria-current={view === "settings" ? "page" : undefined}
          onClick={() => onNavigate({ view: "settings" })}
        >
          <Settings size={18} strokeWidth={1.5} />
          {!collapsed ? <span>Settings</span> : null}
        </button>
        <a className="sidebar-nav-item" href="https://github.com/Vinayak-RZ/ARC" target="_blank" rel="noreferrer" title="Help">
          <LifeBuoy size={18} strokeWidth={1.5} />
          {!collapsed ? <span>Help</span> : null}
        </a>
      </footer>
    </aside>
  );
}
