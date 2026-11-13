import { useEffect, useState } from "react";
import { useLayout } from "../store.js";
import { applyTheme } from "../shell/theme.js";

const TABS = [
  { id: "agents", label: "Agents" },
  { id: "engines", label: "Engines" },
  { id: "appearance", label: "Appearance" },
  { id: "data", label: "Data" },
  { id: "about", label: "About" },
];

export function SettingsPage() {
  const themeMode = useLayout((s) => s.themeMode);
  const setThemeMode = useLayout((s) => s.setThemeMode);
  const [tab, setTab] = useState("appearance");
  const [scorecard, setScorecard] = useState("");
  useEffect(() => {
    fetch("/api/frontier/scorecard")
      .then((r) => r.json())
      .then((d) => setScorecard(d.markdown || ""))
      .catch(() => setScorecard(""));
  }, []);
  function setTheme(mode) {
    setThemeMode(mode);
    applyTheme(mode);
  }
  return (
    <div className="settings-page">
      <h1>Settings</h1>
      <div className="settings-tabs tabs-underline" role="tablist">
        {TABS.map((t) => (
          <button
            key={t.id}
            type="button"
            role="tab"
            aria-selected={tab === t.id}
            className="tab-underline"
            onClick={() => setTab(t.id)}
          >
            {t.label}
          </button>
        ))}
      </div>
      {tab === "agents" ? (
        <section className="settings-section">
          <h2>Agents</h2>
          <p className="hint">Connect a coding agent via MCP. Config stays on your machine.</p>
          <pre className="home-cli">electrical-engineer mcp</pre>
        </section>
      ) : null}
      {tab === "engines" ? (
        <section className="settings-section">
          <h2>Engines</h2>
          <ul className="engine-status-list">
            <li>
              <span className="status-dot checked" /> Numeric (algebraic checks)
            </li>
            <li>
              <span className="status-dot checked" /> SPICE when ngspice is installed
            </li>
            <li>
              <span className="status-dot unchecked" /> MATLAB via Arc (optional)
            </li>
            <li>
              <span className="status-dot unchecked" /> Simulink via Arc (optional)
            </li>
          </ul>
        </section>
      ) : null}
      {tab === "appearance" ? (
        <section className="settings-section">
          <h2>Appearance</h2>
          <div className="theme-toggle-row">
            {["light", "dark", "system"].map((m) => (
              <button
                key={m}
                type="button"
                className="gallery-filter-chip"
                aria-pressed={themeMode === m ? "true" : "false"}
                onClick={() => setTheme(m)}
              >
                {m}
              </button>
            ))}
          </div>
        </section>
      ) : null}
      {tab === "data" ? (
        <section className="settings-section">
          <h2>Data</h2>
          <p className="hint">
            Problems are stored under <code>./runs</code> in this workspace.
          </p>
        </section>
      ) : null}
      {tab === "about" ? (
        <section className="settings-section">
          <h2>About</h2>
          <p className="hint">Frontier scorecard (measured, not marketing).</p>
          {scorecard ? (
            <pre className="scorecard-md">{scorecard}</pre>
          ) : (
            <p className="empty">Scorecard file not found.</p>
          )}
        </section>
      ) : null}
    </div>
  );
}
