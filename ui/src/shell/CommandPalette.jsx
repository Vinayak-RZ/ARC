import { useEffect, useMemo, useState } from "react";
import { Command } from "cmdk";
import { useLayout } from "../store.js";
import { displayTitle } from "../runDisplay.js";
import { applyTheme, resolveTheme } from "./theme.js";

export function CommandPalette({ runs, onNavigate }) {
  const open = useLayout((s) => s.commandOpen);
  const setOpen = useLayout((s) => s.setCommandOpen);
  const [query, setQuery] = useState("");
  useEffect(() => {
    function onKey(e) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setOpen(!useLayout.getState().commandOpen);
      }
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "b") {
        e.preventDefault();
        useLayout.getState().toggleSidebar();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [setOpen]);
  const items = useMemo(() => {
    const nav = [
      { id: "home", label: "Go to Home" },
      { id: "problems", label: "Go to Problems" },
      { id: "studio", label: "Go to Studio" },
      { id: "gallery", label: "Go to Gallery" },
      { id: "library", label: "Go to Library" },
      { id: "settings", label: "Go to Settings" },
    ];
    return [
      ...nav,
      ...runs.slice(0, 30).map((r) => ({
        id: `problem-${r.id}`,
        label: `Open ${displayTitle(r)}`,
        runId: r.id,
      })),
    ];
  }, [runs]);
  if (!open) return null;
  return (
    <div className="cmdk-overlay" role="presentation" onClick={() => setOpen(false)}>
      <Command className="cmdk-root" label="Command palette" onClick={(e) => e.stopPropagation()}>
        <Command.Input value={query} onValueChange={setQuery} placeholder="Jump to a page or problem…" />
        <Command.List>
          <Command.Empty>No matches.</Command.Empty>
          {items.map((item) => (
            <Command.Item
              key={item.id}
              value={item.label}
              onSelect={() => {
                if (item.runId) onNavigate({ view: "problems", runId: item.runId });
                else onNavigate({ view: item.id });
                setOpen(false);
              }}
            >
              {item.label}
            </Command.Item>
          ))}
          <Command.Item
            value="Toggle theme"
            onSelect={() => {
              const cur = resolveTheme(useLayout.getState().themeMode);
              const next = cur === "dark" ? "light" : "dark";
              useLayout.getState().setThemeMode(next);
              applyTheme(next);
              setOpen(false);
            }}
          >
            Toggle theme
          </Command.Item>
        </Command.List>
      </Command>
    </div>
  );
}
