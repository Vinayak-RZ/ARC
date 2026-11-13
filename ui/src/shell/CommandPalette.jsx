import { useEffect, useMemo, useState } from "react";
import { Command } from "cmdk";
import {
  BookOpen,
  FolderOpen,
  Home,
  Image,
  LayoutGrid,
  Moon,
  PanelLeft,
  Play,
  Plus,
  Settings,
  SlidersHorizontal,
} from "lucide-react";
import { useLayout } from "../store.js";
import { displayTitle } from "../runDisplay.js";
import { applyTheme, resolveTheme } from "./theme.js";

const SIDEBAR_TRANSITION_MS = 180;

const NAV = [
  { id: "home", label: "Home", keys: "G H", Icon: Home },
  { id: "problems", label: "Problems", keys: "G P", Icon: FolderOpen },
  { id: "studio", label: "Studio", keys: "G S", Icon: SlidersHorizontal },
  { id: "gallery", label: "Gallery", keys: "G A", Icon: Image },
  { id: "library", label: "Library", keys: "G L", Icon: BookOpen },
  { id: "settings", label: "Settings", keys: "G ,", Icon: Settings },
];

const ACTIONS = [
  { id: "new", label: "New problem", keys: "G N", Icon: Plus },
  { id: "studio", label: "Open in Studio", keys: "G S", Icon: LayoutGrid },
  { id: "sidebar", label: "Toggle sidebar", keys: "⌃B", Icon: PanelLeft },
  { id: "theme", label: "Toggle theme", keys: "T", Icon: Moon },
];

export function CommandPalette({ runs, onNavigate }) {
  const open = useLayout((s) => s.commandOpen);
  const setOpen = useLayout((s) => s.setCommandOpen);
  const [query, setQuery] = useState("");
  useEffect(() => {
    function scheduleOpen() {
      const { sidebarLastToggledAt, commandOpen } = useLayout.getState();
      const elapsed = Date.now() - (sidebarLastToggledAt || 0);
      const delay = Math.max(0, SIDEBAR_TRANSITION_MS - elapsed);
      if (commandOpen) {
        setOpen(false);
        return;
      }
      const openNow = () => setOpen(true);
      if (delay > 0) window.setTimeout(openNow, delay);
      else openNow();
    }
    function onKey(e) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        scheduleOpen();
      }
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "b") {
        e.preventDefault();
        useLayout.getState().toggleSidebar();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [setOpen]);
  const problems = useMemo(
    () =>
      runs.slice(0, 20).map((r) => ({
        id: r.id,
        label: displayTitle(r),
      })),
    [runs],
  );
  if (!open) return null;
  return (
    <div className="cmdk-overlay" role="presentation" onClick={() => setOpen(false)}>
      <Command className="cmdk-root" label="Command palette" onClick={(e) => e.stopPropagation()}>
        <Command.Input
          value={query}
          onValueChange={setQuery}
          placeholder="Search or run a command"
          className="cmdk-input-ghost"
        />
        <div className="cmdk-list-wrap">
          <Command.List>
            <Command.Empty>No matches.</Command.Empty>
            <Command.Group heading="Go to">
              {NAV.map((item) => (
                <Command.Item
                  key={item.id}
                  value={`${item.label} ${item.id}`}
                  onSelect={() => {
                    onNavigate({ view: item.id });
                    setOpen(false);
                  }}
                >
                  <item.Icon size={16} strokeWidth={1.5} className="cmdk-row-icon" aria-hidden />
                  <span>{item.label}</span>
                  <kbd className="cmdk-kbd">{item.keys}</kbd>
                </Command.Item>
              ))}
            </Command.Group>
            {problems.length > 0 ? (
              <Command.Group heading="Problems">
                {problems.map((item) => (
                  <Command.Item
                    key={item.id}
                    value={`${item.label} ${item.id}`}
                    onSelect={() => {
                      onNavigate({ view: "problems", runId: item.id });
                      setOpen(false);
                    }}
                  >
                    <Play size={16} strokeWidth={1.5} className="cmdk-row-icon" aria-hidden />
                    <span>{item.label}</span>
                  </Command.Item>
                ))}
              </Command.Group>
            ) : null}
            <Command.Group heading="Actions">
              {ACTIONS.map((item) => (
                <Command.Item
                  key={item.id}
                  value={item.label}
                  onSelect={() => {
                    if (item.id === "theme") {
                      const cur = resolveTheme(useLayout.getState().themeMode);
                      const next = cur === "dark" ? "light" : "dark";
                      useLayout.getState().setThemeMode(next);
                      applyTheme(next);
                    } else if (item.id === "sidebar") {
                      useLayout.getState().toggleSidebar();
                    } else if (item.id === "studio") {
                      onNavigate({ view: "studio" });
                    } else if (item.id === "new") {
                      onNavigate({ view: "home" });
                    }
                    setOpen(false);
                  }}
                >
                  <item.Icon size={16} strokeWidth={1.5} className="cmdk-row-icon" aria-hidden />
                  <span>{item.label}</span>
                  <kbd className="cmdk-kbd">{item.keys}</kbd>
                </Command.Item>
              ))}
            </Command.Group>
          </Command.List>
        </div>
        <footer className="cmdk-footer cmdk-footer-fade">
          <span>↑↓ navigate</span>
          <span>↵ open</span>
          <span>esc close</span>
        </footer>
      </Command>
    </div>
  );
}
