import { useEffect, useState } from "react";
import { Copy } from "lucide-react";
import { useLayout } from "../store.js";
import { applyTheme } from "../shell/theme.js";
import { ArcMascot } from "../mascot/index.js";

const TABS = [
  { id: "agents", label: "Agents" },
  { id: "engines", label: "Engines" },
  { id: "appearance", label: "Appearance" },
  { id: "data", label: "Data" },
  { id: "about", label: "About" },
];

export function SettingsPage({ onRunsChange }) {
  const themeMode = useLayout((s) => s.themeMode);
  const setThemeMode = useLayout((s) => s.setThemeMode);
  const [tab, setTab] = useState("agents");
  const [scorecardDetail, setScorecardDetail] = useState("");
  const [engines, setEngines] = useState([]);
  const [version, setVersion] = useState("");
  const [dataMsg, setDataMsg] = useState("");

  useEffect(() => {
    fetch("/api/frontier/scorecard")
      .then((r) => r.json())
      .then((d) => setScorecardDetail(d.markdown || ""))
      .catch(() => setScorecardDetail(""));
    fetch("/api/engines")
      .then((r) => r.json())
      .then((d) => {
        setEngines(d.engines || []);
        setVersion(d.version || "");
      })
      .catch(() => setEngines([]));
  }, []);

  function setTheme(mode) {
    setThemeMode(mode);
    applyTheme(mode);
  }

  async function clearSamples() {
    setDataMsg("");
    const r = await fetch("/api/runs/samples", { method: "DELETE" });
    const body = await r.json();
    setDataMsg(`Removed ${body.removed || 0} sample run(s).`);
    onRunsChange?.();
  }

  async function reseedSamples() {
    setDataMsg("Seeding…");
    const r = await fetch("/api/runs/samples", { method: "POST" });
    const body = await r.json();
    if (!r.ok) {
      setDataMsg(body.error || "Seed failed");
      return;
    }
    setDataMsg(`Seeded ${body.seeded || 0} sample run(s).`);
    onRunsChange?.();
  }

  function copy(text) {
    navigator.clipboard?.writeText(text);
  }

  return (
    <div className="settings-page settings-page-rail">
      <header className="settings-hero">
        <div>
          <h1>Settings</h1>
          <p className="hint">Local lab preferences. Nothing leaves this machine unless you copy it.</p>
        </div>
        <ArcMascot mode="ambient" size={48} label="Arc" />
      </header>
      <div className="settings-layout">
        <nav className="settings-rail" aria-label="Settings sections">
          {TABS.map((t) => (
            <button
              key={t.id}
              type="button"
              className="settings-rail-item"
              aria-current={tab === t.id ? "page" : undefined}
              onClick={() => setTab(t.id)}
            >
              {t.label}
            </button>
          ))}
        </nav>
        <div className="settings-main">
          {tab === "agents" ? (
            <section className="settings-section card-surface">
              <h2>Agents</h2>
              <p className="hint">Connect a coding agent via MCP. Config stays on your machine.</p>
              <div className="home-cli-wrap">
                <pre className="home-cli">electrical-engineer mcp</pre>
                <button type="button" className="button-quiet settings-copy" onClick={() => copy("electrical-engineer mcp")}>
                  <Copy size={14} aria-hidden /> Copy
                </button>
              </div>
              <div className="home-cli-wrap">
                <pre className="home-cli">electrical-engineer hosts install --host all</pre>
                <button
                  type="button"
                  className="button-quiet settings-copy"
                  onClick={() => copy("electrical-engineer hosts install --host all")}
                >
                  <Copy size={14} aria-hidden /> Copy
                </button>
              </div>
            </section>
          ) : null}
          {tab === "engines" ? (
            <section className="settings-section card-surface">
              <h2>Engines</h2>
              <p className="hint">Live availability from this Python environment.</p>
              <table className="settings-engine-table">
                <thead>
                  <tr>
                    <th>Engine</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {engines.map((row) => (
                    <tr key={row.name}>
                      <td>{row.name}</td>
                      <td>
                        <span className={`engine-tag${row.available ? " is-on" : ""}`}>
                          {row.available ? "Available" : row.detail || "Not installed"}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>
          ) : null}
          {tab === "appearance" ? (
            <section className="settings-section card-surface">
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
            <section className="settings-section card-surface">
              <h2>Data</h2>
              <p className="hint">Runs live under ./runs in the working directory.</p>
              <div className="settings-data-actions">
                <button type="button" className="button-secondary" onClick={clearSamples}>
                  Clear samples
                </button>
                <button type="button" className="button-primary" onClick={reseedSamples}>
                  Re-add samples
                </button>
              </div>
              {dataMsg ? <p className="hint">{dataMsg}</p> : null}
            </section>
          ) : null}
          {tab === "about" ? (
            <section className="settings-section card-surface">
              <h2>About</h2>
              <p className="hint">electrical-engineer {version || "…"}</p>
              {scorecardDetail ? <pre className="settings-scorecard">{scorecardDetail}</pre> : <p className="hint">Scorecard unavailable.</p>}
            </section>
          ) : null}
        </div>
      </div>
    </div>
  );
}
