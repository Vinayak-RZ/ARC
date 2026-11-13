import { useEffect, useState } from "react";
import { Copy } from "lucide-react";
import { useLayout } from "../store.js";
import { applyTheme } from "../shell/theme.js";

const TABS = [
  { id: "agents", label: "Agents" },
  { id: "engines", label: "Engines" },
  { id: "appearance", label: "Appearance" },
  { id: "data", label: "Data" },
  { id: "about", label: "About" },
];

const ABOUT_ROWS = [
  { check: "CLI smoke", result: "pass", status: "ok" },
  { check: "SPICE when installed", result: "conditional", status: "ok" },
  { check: "Control Studio simulate", result: "pass", status: "ok" },
  { check: "Visual goldens", result: "pass", status: "ok" },
];

const ENGINES = [
  { name: "Numeric (algebraic checks)", available: true },
  { name: "SPICE (ngspice)", available: true },
  { name: "python-control", available: true },
  { name: "MATLAB engine", available: false },
  { name: "Simulink engine", available: false },
];

export function SettingsPage() {
  const themeMode = useLayout((s) => s.themeMode);
  const setThemeMode = useLayout((s) => s.setThemeMode);
  const [tab, setTab] = useState("agents");
  const [scorecardDetail, setScorecardDetail] = useState("");
  useEffect(() => {
    fetch("/api/frontier/scorecard")
      .then((r) => r.json())
      .then((d) => setScorecardDetail(d.markdown || ""))
      .catch(() => setScorecardDetail(""));
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
          <div className="home-cli-wrap">
            <pre className="home-cli">electrical-engineer mcp</pre>
            <button
              type="button"
              className="button-quiet settings-copy"
              onClick={() => navigator.clipboard?.writeText("electrical-engineer mcp")}
            >
              <Copy size={14} aria-hidden /> Copy
            </button>
          </div>
        </section>
      ) : null}
      {tab === "engines" ? (
        <section className="settings-section">
          <h2>Engines</h2>
          <table className="settings-engine-table">
            <thead>
              <tr>
                <th>Engine</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {ENGINES.map((row) => (
                <tr key={row.name}>
                  <td>{row.name}</td>
                  <td>
                    <span className={`engine-tag${row.available ? " is-on" : ""}`}>
                      {row.available ? "Available" : "Not installed"}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      ) : null}
      {tab === "appearance" ? (
        <section className="settings-section">
          <h2>Appearance</h2>
          <p className="hint">Light, dark, or follow the system preference.</p>
          <div className="settings-segmented" role="group" aria-label="Theme">
            {["light", "dark", "system"].map((m) => (
              <button
                key={m}
                type="button"
                className="settings-segmented-btn"
                aria-pressed={themeMode === m ? "true" : "false"}
                onClick={() => setTheme(m)}
              >
                {m.charAt(0).toUpperCase() + m.slice(1)}
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
          <p className="settings-version">Arc 0.1</p>
          <table className="settings-about-table">
            <thead>
              <tr>
                <th>Check</th>
                <th>Result</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {ABOUT_ROWS.map((row) => (
                <tr key={row.check}>
                  <td>{row.check}</td>
                  <td>{row.result}</td>
                  <td>{row.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {scorecardDetail ? (
            <details className="settings-scorecard-details">
              <summary>Details</summary>
              <pre className="scorecard-md is-collapsed">{scorecardDetail.slice(0, 1200)}…</pre>
            </details>
          ) : null}
        </section>
      ) : null}
    </div>
  );
}
