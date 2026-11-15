import { useCallback, useEffect } from "react";
import { CommandPalette } from "./CommandPalette.jsx";
import { Sidebar } from "./Sidebar.jsx";
import { TopBar } from "./TopBar.jsx";
import { useRunsList } from "../hooks/useRun.js";
import { useRun } from "../hooks/useRun.js";
import { useLayout } from "../store.js";
import { applyTheme, getStoredTheme } from "./theme.js";
import { HomePage } from "../pages/HomePage.jsx";
import { ProblemsPage } from "../pages/ProblemsPage.jsx";
import { ProblemDetailPage } from "../pages/ProblemDetailPage.jsx";
import { SettingsPage } from "../pages/SettingsPage.jsx";
import { renderSlot } from "../slots/registry.js";

function readUrlState() {
  const q = new URLSearchParams(window.location.search);
  const view = q.get("view");
  const problem = q.get("problem") || q.get("run");
  return { view, problem };
}

export function AppShell() {
  const view = useLayout((s) => s.view);
  const id = useLayout((s) => s.currentRunId);
  const setView = useLayout((s) => s.setView);
  const setRun = useLayout((s) => s.setRun);
  const clearRun = useLayout((s) => s.clearRun);
  const setThemeMode = useLayout((s) => s.setThemeMode);
  const collapsed = useLayout((s) => s.sidebarCollapsed);
  const { runs, loading: runsLoading, error: runsError, reload, seeding } = useRunsList();
  const { data } = useRun(id);

  const applyRoute = useCallback(
    ({ view: nextView, runId }, { push = true } = {}) => {
      const url = new URL(window.location.href);
      if (runId) {
        setRun(runId);
        url.searchParams.set("problem", runId);
        url.searchParams.delete("view");
        url.searchParams.delete("run");
      } else {
        const v = nextView || "home";
        setView(v);
        clearRun();
        url.searchParams.set("view", v);
        url.searchParams.delete("problem");
        url.searchParams.delete("run");
      }
      if (push) window.history.pushState({}, "", url);
      else window.history.replaceState({}, "", url);
    },
    [clearRun, setRun, setView],
  );

  const navigate = useCallback((opts) => applyRoute(opts, { push: true }), [applyRoute]);

  useEffect(() => {
    const mode = getStoredTheme();
    setThemeMode(mode);
    applyTheme(mode);
    const { view: v, problem } = readUrlState();
    if (problem) setRun(problem);
    else if (v) setView(v);
  }, [setRun, setThemeMode, setView]);

  useEffect(() => {
    function onPop() {
      const { view: v, problem } = readUrlState();
      if (problem) {
        setRun(problem);
      } else {
        clearRun();
        setView(v || "home");
      }
    }
    window.addEventListener("popstate", onPop);
    return () => window.removeEventListener("popstate", onPop);
  }, [clearRun, setRun, setView]);

  const openProblem = (runId) => navigate({ view: "problems", runId });
  const stale = useLayout((s) => s.parametersStale);
  const runMeta = id ? runs.find((r) => r.id === id) || { id, title: data?.title, modified_at: data?.modified_at } : null;
  let primaryLabel = null;
  let onPrimary = null;
  if (view === "problems" && id) {
    primaryLabel = "Run again";
    onPrimary = () => openProblem(id);
  }
  let workspace = null;
  if (view === "home") {
    workspace = <HomePage runs={runs} onRunsChange={reload} onOpenProblem={openProblem} seeding={seeding} />;
  } else if (view === "problems" && !id) {
    workspace = (
      <ProblemsPage
        runs={runs}
        loading={runsLoading}
        error={runsError}
        onReload={reload}
        onOpenProblem={openProblem}
        onTryExample={() => navigate({ view: "home" })}
        seeding={seeding}
      />
    );
  } else if (view === "problems" && id) {
    workspace = <ProblemDetailPage id={id} data={data} runMeta={runMeta} />;
  } else if (view === "studio") workspace = renderSlot("control.studio");
  else if (view === "gallery") workspace = renderSlot("visual.gallery");
  else if (view === "library") workspace = renderSlot("rag.inventory");
  else if (view === "settings") workspace = <SettingsPage onRunsChange={reload} />;
  return (
    <div className={collapsed ? "product-shell is-sidebar-collapsed" : "product-shell"}>
      <a className="skip" href="#workspace">
        Skip to workspace
      </a>
      <Sidebar runs={runs} onNavigate={navigate} onNewProblem={() => navigate({ view: "home" })} seeding={seeding} />
      <div className="product-main">
        <TopBar
          runMeta={runMeta}
          primaryLabel={primaryLabel}
          onPrimaryAction={onPrimary}
          runAgainPrimary={view === "problems" && id && stale}
          onNavigate={navigate}
        />
        <main id="workspace" className="workspace product-workspace">
          {workspace}
        </main>
      </div>
      <CommandPalette runs={runs} onNavigate={navigate} />
    </div>
  );
}
