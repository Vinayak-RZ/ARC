import { useEffect, useState } from "react";

function recipeKind(recipeId) {
  const id = String(recipeId || "");
  if (id.includes("protection")) return "protection";
  if (id.includes("drives")) return "drives";
  if (id.includes("control") || id.includes("digital")) return "control";
  if (id.includes("power")) return "power";
  if (id.includes("simulate-circuit") || id.includes("circuit")) return "circuits";
  return "";
}

export function EngineArtifacts({ id, recipeId }) {
  const kind = recipeKind(recipeId);
  const [power, setPower] = useState(null);
  const [protection, setProtection] = useState(null);
  const [drives, setDrives] = useState(null);
  useEffect(() => {
    if (!id) return;
    if (kind === "power") {
      fetch(`/api/runs/${id}/file/power_tables.json`)
        .then((r) => (r.ok ? r.json() : null))
        .then((d) => setPower(d))
        .catch(() => setPower(null));
    }
    if (kind === "protection") {
      fetch(`/api/runs/${id}/file/protection_tables.json`)
        .then((r) => (r.ok ? r.json() : null))
        .then((d) => setProtection(d))
        .catch(() => setProtection(null));
    }
    if (kind === "drives") {
      fetch(`/api/runs/${id}/file/drives_result.json`)
        .then((r) => (r.ok ? r.json() : null))
        .then((d) => setDrives(d))
        .catch(() => setDrives(null));
    }
  }, [id, kind]);

  if (!kind) return null;

  if (kind === "control") {
    return (
      <section className="engine-panel" aria-label="Control plots">
        <h2>Control response</h2>
        <div className="engine-grid">
          <figure>
            <img className="plot" src={`/api/runs/${id}/file/bode.png`} alt="Bode plot" width="480" height="320" />
            <figcaption>Bode magnitude and phase</figcaption>
          </figure>
          <figure>
            <img className="plot" src={`/api/runs/${id}/file/step.png`} alt="Step response" width="480" height="320" />
            <figcaption>Step response</figcaption>
          </figure>
        </div>
      </section>
    );
  }

  if (kind === "protection" && protection) {
    return (
      <section className="engine-panel" aria-label="Protection study">
        <h2>Protection settings</h2>
        <table className="data-table">
          <tbody>
            <tr><th>CT ratio</th><td>{Number(protection.ct_ratio).toFixed(1)}</td></tr>
            <tr><th>Pickup (primary A)</th><td>{Number(protection.pickup_primary_a).toFixed(2)}</td></tr>
            <tr><th>Fault current (A)</th><td>{Number(protection.fault_current_a).toFixed(2)}</td></tr>
            <tr><th>Overcurrent trip</th><td>{protection.overcurrent_trip ? "yes" : "no"}</td></tr>
          </tbody>
        </table>
        <img className="plot" src={`/api/runs/${id}/artifact.svg`} alt="Protection summary" width="360" height="120" />
      </section>
    );
  }

  if (kind === "drives" && drives) {
    return (
      <section className="engine-panel" aria-label="Drive study">
        <h2>Drive steady-state</h2>
        <p className="hint">Speed: <strong>{Number(drives.rpm).toFixed(2)} rpm</strong></p>
        <img className="plot" src={`/api/runs/${id}/artifact.svg`} alt="Drive summary" width="320" height="120" />
      </section>
    );
  }

  if (kind === "power") {
    const fault = power?.fault || {};
    const buses = (power?.buses || []).filter((row) => row.bus != null);
    return (
      <section className="engine-panel" aria-label="Power study">
        <h2>Power network study</h2>
        {fault.fault_type ? (
          <p className="hint">
            Fault <strong>{fault.fault_type}</strong>: |I| = {Number(fault.i_fault_pu || 0).toFixed(4)} pu
          </p>
        ) : null}
        {buses.length ? (
          <table className="data-table">
            <thead>
              <tr>
                <th>Bus</th>
                <th>|V| (pu)</th>
                <th>Angle (deg)</th>
              </tr>
            </thead>
            <tbody>
              {buses.map((row) => (
                <tr key={row.bus}>
                  <td>{row.bus}</td>
                  <td>{Number(row.vm_pu).toFixed(4)}</td>
                  <td>{Number(row.va_degree).toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="empty">Load-flow table not available for this run.</p>
        )}
        <img className="plot" src={`/api/runs/${id}/artifact.svg`} alt="Power study summary" width="360" height="140" />
      </section>
    );
  }

  return (
    <section className="engine-panel" aria-label="SPICE result">
      <h2>Circuit simulation</h2>
      <img className="plot" src={`/api/runs/${id}/artifact.svg`} alt="SPICE probe" width="360" height="140" />
    </section>
  );
}
