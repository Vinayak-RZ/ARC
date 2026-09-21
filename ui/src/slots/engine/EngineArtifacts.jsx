import { useEffect, useState } from "react";

function recipeKind(recipeId) {
  const id = String(recipeId || "");
  if (id.includes("control")) return "control";
  if (id.includes("power")) return "power";
  if (id.includes("simulate-circuit") || id.includes("circuit")) return "circuits";
  return "";
}

export function EngineArtifacts({ id, recipeId }) {
  const kind = recipeKind(recipeId);
  const [power, setPower] = useState(null);
  useEffect(() => {
    if (kind !== "power" || !id) return;
    fetch(`/api/runs/${id}/file/power_tables.json`)
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => setPower(d))
      .catch(() => setPower(null));
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
