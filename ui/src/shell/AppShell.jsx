import { lazy, Suspense, useCallback, useEffect, useState } from "react";
import { CommandPalette } from "./CommandPalette.jsx";
import { Sidebar } from "./Sidebar.jsx";
import { TopBar } from "./TopBar.jsx";
import { useRunsList } from "../hooks/useRun.js";
import { useRun } from "../hooks/useRun.js";
import { useLayout } from "../store.js";
import { applyTheme, getStoredTheme } from "./theme.js";
const HomePage = lazy(() => import("../pages/HomePage.jsx").then((m) => ({ default: m.HomePage })));
const ProblemsPage = lazy(() => import("../pages/ProblemsPage.jsx").then((m) => ({ default: m.ProblemsPage })));
const ProblemDetailPage = lazy(() => import("../pages/ProblemDetailPage.jsx").then((m) => ({ default: m.ProblemDetailPage })));
const SettingsPage = lazy(() => import("../pages/SettingsPage.jsx").then((m) => ({ default: m.SettingsPage })));
const LearnPage = lazy(() => import("../pages/LearnPage.jsx").then((m) => ({ default: m.LearnPage })));
const SubjectPage = lazy(() => import("../pages/SubjectPage.jsx").then((m) => ({ default: m.SubjectPage })));
const StudioPage = lazy(() => import("../pages/StudioPage.jsx").then((m) => ({ default: m.StudioPage })));
import { AchievementsPanel } from "../components/AchievementsPanel.jsx";
import { UnlockToast } from "../components/UnlockToast.jsx";
import { renderSlot } from "../slots/registry.js";

function readUrlState() {
  const q = new URLSearchParams(window.location.search);
  const view = q.get("view");
  const runParam = q.get("run");
  const problem = q.get("problem") || (view === "studio" ? null : runParam);
  const subject = q.get("subject");
  const tab = q.get("tab");
  const lab = q.get("lab");
  const studioRun = view === "studio" ? runParam : null;
  return { view, problem, subject, tab, lab, studioRun };
}

export function AppShell() {
  const view = useLayout((s) => s.view);
  const id = useLayout((s) => s.currentRunId);
  const learnSubjectId = useLayout((s) => s.learnSubjectId);
  const setView = useLayout((s) => s.setView);
  const setRun = useLayout((s) => s.setRun);
  const clearRun = useLayout((s) => s.clearRun);
  const setLearnSubject = useLayout((s) => s.setLearnSubject);
  const setStudio = useLayout((s) => s.setStudio);
  const setThemeMode = useLayout((s) => s.setThemeMode);
  const collapsed = useLayout((s) => s.sidebarCollapsed);
  const { runs, loading: runsLoading, error: runsError, reload, seeding } = useRunsList();
  const { data } = useRun(id);
  const [achievementsOpen, setAchievementsOpen] = useState(false);

  const applyRoute = useCallback(
    ({ view: nextView, runId, subject, tab, lab }, { push = true } = {}) => {
      const url = new URL(window.location.href);
      if (runId) {
        setRun(runId);
        setLearnSubject(null);
        url.searchParams.set("problem", runId);
        url.searchParams.delete("view");
        url.searchParams.delete("run");
        url.searchParams.delete("subject");
        url.searchParams.delete("tab");
        url.searchParams.delete("lab");
      } else {
        const v = nextView || "home";
        setView(v);
        clearRun();
        url.searchParams.set("view", v);
        url.searchParams.delete("problem");
        url.searchParams.delete("run");
        if (v === "learn") {
          if (subject) {
            setLearnSubject(subject);
            url.searchParams.set("subject", subject);
          } else {
            setLearnSubject(null);
            url.searchParams.delete("subject");
          }
        } else {
          setLearnSubject(null);
          url.searchParams.delete("subject");
        }
        if (v === "studio") {
          const sessionParam = url.searchParams.get("session");
          const nextTab = tab || (sessionParam ? "control" : "home");
          const nextLab = lab || null;
          setStudio({ tab: nextTab, lab: nextLab });
          if (nextTab === "home" && !sessionParam) {
            url.searchParams.delete("tab");
            url.searchParams.delete("session");
          } else {
            url.searchParams.set("tab", nextTab);
          }
          if (nextLab) url.searchParams.set("lab", nextLab);
          else url.searchParams.delete("lab");
        } else {
          url.searchParams.delete("session");
          url.searchParams.delete("tab");
          url.searchParams.delete("lab");
        }
      }
      if (push) window.history.pushState({}, "", url);
      else window.history.replaceState({}, "", url);
    },
    [clearRun, setLearnSubject, setRun, setStudio, setView],
  );

  const navigate = useCallback((opts) => applyRoute(opts, { push: true }), [applyRoute]);

  useEffect(() => {
    const mode = getStoredTheme();
    setThemeMode(mode);
    applyTheme(mode);
    const { view: v, problem, subject, tab, lab } = readUrlState();
    if (problem) setRun(problem);
    else if (v) {
      setView(v);
      if (v === "learn" && subject) setLearnSubject(subject);
      if (v === "studio") {
        const session = new URLSearchParams(window.location.search).get("session");
        setStudio({ tab: tab || (session ? "control" : "home"), lab: lab || null });
      }
    }
  }, [setLearnSubject, setRun, setStudio, setThemeMode, setView]);

  useEffect(() => {
    function onPop() {
      const { view: v, problem, subject, tab, lab } = readUrlState();
      if (problem) {
        setRun(problem);
      } else {
        clearRun();
        setView(v || "home");
        setLearnSubject(v === "learn" ? subject || null : null);
        if (v === "studio") {
          const session = new URLSearchParams(window.location.search).get("session");
          setStudio({ tab: tab || (session ? "control" : "home"), lab: lab || null });
        }
      }
    }
    window.addEventListener("popstate", onPop);
    return () => window.removeEventListener("popstate", onPop);
  }, [clearRun, setLearnSubject, setRun, setStudio, setView]);

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
    workspace = (
      <HomePage
        runs={runs}
        onRunsChange={reload}
        onOpenProblem={openProblem}
        onOpenLearn={() => navigate({ view: "learn" })}
        onOpenSubject={(sid) => navigate({ view: "learn", subject: sid })}
        seeding={seeding}
      />
    );
  } else if (view === "learn" && !learnSubjectId) {
    workspace = (
      <LearnPage
        onOpenSubject={(sid) => navigate({ view: "learn", subject: sid })}
        onOpenAchievements={() => setAchievementsOpen(true)}
      />
    );
  } else if (view === "learn" && learnSubjectId) {
    workspace = (
      <SubjectPage
        subjectId={learnSubjectId}
        onBack={() => navigate({ view: "learn" })}
        onNavigate={navigate}
      />
    );
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
  } else if (view === "studio") workspace = <StudioPage onNavigate={navigate} />;
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
          <Suspense fallback={null}>{workspace}</Suspense>
        </main>
      </div>
      <CommandPalette runs={runs} onNavigate={navigate} />
      <AchievementsPanel open={achievementsOpen} onClose={() => setAchievementsOpen(false)} />
      <UnlockToast />
    </div>
  );
}
