import { useEffect, useState } from "react";

function recipeKind(recipeId) {
  const id = String(recipeId || "");
  if (id.includes("digital")) return "digital";
  if (id.includes("swing") || id.includes("smib")) return "swing";
  if (id.includes("ed-lambda") || id.includes("dispatch")) return "dispatch";
  if (id.includes("power-electronic") || id.includes("electronics")) return "buck";
  if (id.includes("protection")) return "protection";
  if (id.includes("drives") || id.includes("machines")) return "drives";
  if (id.includes("simulate-circuit")) return "rlc";
  if (id.includes("control")) return "control";
  if (id.includes("power") || id.includes("fault")) return "power";
  if (id.includes("circuit")) return "circuits";
  return "";
}

function Fig({ src, alt, caption, wide = false }) {
  const [ok, setOk] = useState(true);
  if (!ok) return <p className="hint">No {caption.toLowerCase()} file on this run.</p>;
  return (
    <figure>
      <img
        className={wide ? "plot plot-lg plot-wide" : "plot plot-lg"}
        src={src}
        alt={alt}
        onError={() => setOk(false)}
      />
      <figcaption>{caption}</figcaption>
    </figure>
  );
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
      <section className="engine-panel engine-panel-plots" aria-label="Control plots">
        <h2>Bode and step response</h2>
        <div className="engine-grid engine-grid-plots">
          <Fig src={`/api/runs/${id}/file/bode.png`} alt="Bode plot" caption="Magnitude and phase" />
          <Fig src={`/api/runs/${id}/file/step.png`} alt="Step response" caption="Closed-loop step" />
        </div>
      </section>
    );
  }

  if (kind === "digital") {
    return (
      <section className="engine-panel engine-panel-plots" aria-label="Discrete plots">
        <h2>Discrete step and z-plane poles</h2>
        <div className="engine-grid engine-grid-plots">
          <Fig src={`/api/runs/${id}/file/step.png`} alt="Discrete step" caption="Sampled step response" />
          <Fig src={`/api/runs/${id}/file/bode.png`} alt="z-plane poles" caption="Poles on the z plane" />
        </div>
      </section>
    );
  }

  if (kind === "swing") {
    return (
      <section className="engine-panel engine-panel-plots" aria-label="Equal area">
        <h2>Equal-area criterion</h2>
        <Fig
          wide
          src={`/api/runs/${id}/file/power.swing_equal_area.png`}
          alt="SMIB equal-area plot"
          caption="Pre-fault, fault, and post-fault power"
        />
      </section>
    );
  }

  if (kind === "dispatch") {
    return (
      <section className="engine-panel engine-panel-plots" aria-label="Dispatch curve">
        <h2>Incremental cost</h2>
        <Fig
          wide
          src={`/api/runs/${id}/file/power.dispatch_curve.png`}
          alt="Economic dispatch curve"
          caption="λ where the unit costs meet the load"
        />
      </section>
    );
  }

  if (kind === "buck") {
    return (
      <section className="engine-panel engine-panel-plots" aria-label="Buck ripple">
        <h2>Inductor current</h2>
        <Fig wide src={`/api/runs/${id}/file/buck.png`} alt="Buck inductor current" caption="One switching period, CCM" />
      </section>
    );
  }

  if (kind === "rlc") {
    return (
      <section className="engine-panel engine-panel-plots" aria-label="RLC waveform">
        <h2>Capacitor voltage</h2>
        <Fig wide src={`/api/runs/${id}/file/step.png`} alt="Series RLC capacitor voltage" caption="Step response of Vc" />
      </section>
    );
  }

  if (kind === "protection" && protection) {
    return (
      <section className="engine-panel" aria-label="Protection study">
        <h2>Protection study results</h2>
        <table className="data-table">
          <tbody>
            <tr><th>CT ratio</th><td>{Number(protection.ct_ratio).toFixed(1)}</td></tr>
            <tr><th>Pickup (primary A)</th><td>{Number(protection.pickup_primary_a).toFixed(2)}</td></tr>
            <tr><th>Fault current (A)</th><td>{Number(protection.fault_current_a).toFixed(2)}</td></tr>
            <tr><th>Overcurrent trip</th><td>{protection.overcurrent_trip ? "yes" : "no"}</td></tr>
          </tbody>
        </table>
      </section>
    );
  }

  if (kind === "drives" && drives) {
    return (
      <section className="engine-panel" aria-label="Drive study">
        <h2>Drive steady-state</h2>
        <p className="hint">Speed: <strong>{Number(drives.rpm).toFixed(2)} rpm</strong></p>
        <Fig src={`/api/runs/${id}/file/artifact.svg`} alt="Drive summary" caption="Steady speed" />
      </section>
    );
  }

  if (kind === "power") {
    const fault = power?.fault || {};
    const buses = (power?.buses || []).filter((row) => row.bus != null);
    return (
      <section className="engine-panel" aria-label="Power study">
        <h2>Fault study results</h2>
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
      </section>
    );
  }

  if (kind === "circuits") {
    return (
      <section className="engine-panel engine-panel-plots" aria-label="SPICE result">
        <h2>Solved circuit</h2>
        <Fig wide src={`/api/runs/${id}/file/artifact.svg`} alt="Divider operating point" caption="Solved operating point" />
      </section>
    );
  }

  return null;
}
