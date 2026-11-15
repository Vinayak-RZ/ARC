import { useEffect, useMemo, useState } from "react";
import { MascotState } from "../components/MascotState.jsx";

const CAPTIONS = {
  "power.swing_equal_area": "Equal-area check after clearing a fault on an SMIB machine",
  "power.agc_trace": "Two-area frequency and tie-line response to a load step",
  "power.dispatch_curve": "Economic dispatch: incremental cost versus generator output",
  "power.swing_animation": "Rotor angle trace after the fault clears (animated)",
  "power.oneline_bus": "Three-bus one-line with a fault study at the load bus",
  "control.bode": "Open-loop Bode magnitude and phase",
  "control.nyquist": "Nyquist plot with encirclements for closed-loop stability",
  "control.step": "Closed-loop step response",
  "control.root_locus": "Root locus versus loop gain",
  "control.block_diagram": "Block diagram layout from the control spec",
  "schematic.divider": "Voltage divider schematic with solved Vout",
  "schematic.rlc_series": "Series RLC branch notation",
  "waveform.phasor": "Phasor diagram for AC steady state",
};

const POSTER = {
  "power.swing_animation": "swing/power.swing_equal_area.png",
};

const EXAMPLE_FOR = {
  "schematic.divider": "divider",
  "schematic.rlc_series": "rlc-step",
  "control.step": "control-step",
  "control.bode": "control-step",
  "control.root_locus": "control-step",
  "power.swing_equal_area": "smib-swing",
  "power.swing_animation": "smib-swing",
  "power.oneline_bus": "lg-fault",
  "power.dispatch_curve": "ed-dispatch",
};

const PACK_LABELS = {
  All: "All",
  power: "Power",
  control: "Control",
  circuits: "Circuits",
};

function packOf(component) {
  const id = String(component?.id || "");
  if (id.startsWith("power.")) return "power";
  if (id.startsWith("control.")) return "control";
  if (id.startsWith("schematic.") || id.startsWith("waveform.")) return "circuits";
  return "General";
}

export function VisualGallery() {
  const [data, setData] = useState({ components: [], goldens_base: "" });
  const [pack, setPack] = useState("All");
  const [status, setStatus] = useState("loading");
  const [active, setActive] = useState(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    setStatus("loading");
    fetch("/api/visual-kit")
      .then((r) => {
        if (!r.ok) throw new Error("failed");
        return r.json();
      })
      .then((d) => {
        setData(d);
        setStatus((d.components || []).length ? "ready" : "empty");
      })
      .catch(() => {
        setData({ components: [], goldens_base: "" });
        setStatus("error");
      });
  }, []);

  const items = useMemo(() => {
    const list = data.components || [];
    if (pack === "All") return list;
    return list.filter((c) => packOf(c) === pack);
  }, [data.components, pack]);

  async function tryAsProblem(componentId) {
    const exampleId = EXAMPLE_FOR[componentId];
    if (!exampleId) return;
    setBusy(true);
    try {
      const r = await fetch(`/api/examples/${exampleId}/run`, { method: "POST" });
      const body = await r.json();
      if (body.run_id) {
        const url = new URL(window.location.href);
        url.searchParams.set("problem", body.run_id);
        url.searchParams.delete("view");
        window.location.href = url.toString();
      }
    } finally {
      setBusy(false);
    }
  }

  if (status === "loading") {
    return (
      <section className="visual-gallery">
        <MascotState kind="loading" title="Loading gallery…" message="Fetching Visual Kit goldens." />
      </section>
    );
  }
  if (status === "error") {
    return (
      <section className="visual-gallery">
        <MascotState
          kind="error"
          title="Gallery did not load"
          message="Could not reach /api/visual-kit."
          actionLabel="Retry"
          onAction={() => window.location.reload()}
        />
      </section>
    );
  }
  if (status === "empty") {
    return (
      <section className="visual-gallery">
        <MascotState
          kind="empty"
          title="No figures yet"
          message="Regenerate visual goldens, then reopen Gallery."
        />
      </section>
    );
  }

  return (
    <section className="visual-gallery" aria-label="Arc Visual Kit gallery">
      <h1>Gallery</h1>
      <p className="visual-gallery-lede">Figures checked by the engines.</p>
      <div className="gallery-filters" role="group" aria-label="Filter by subject">
        {Object.entries(PACK_LABELS).map(([key, label]) => (
          <button
            key={key}
            type="button"
            className="gallery-filter-chip"
            aria-pressed={pack === key ? "true" : "false"}
            onClick={() => setPack(key)}
          >
            {label}
          </button>
        ))}
      </div>
      <div className="gallery-grid gallery-grid-wide">
        {items.map((c) => {
          const rel = POSTER[c.id] || c.golden;
          const isGif = String(c.golden || "").endsWith(".gif");
          return (
            <figure key={c.id} className="gallery-card">
              <button type="button" className="gallery-card-open" onClick={() => setActive(c)}>
                <div className="gallery-card-media">
                  <img src={`${data.goldens_base}${rel}`} alt={CAPTIONS[c.id] || c.id} loading="lazy" />
                  {isGif ? <span className="gallery-gif-badge">GIF</span> : null}
                </div>
                <figcaption>
                  <span className="gallery-card-title">{CAPTIONS[c.id] || c.title || c.id.split(".").pop()}</span>
                </figcaption>
              </button>
            </figure>
          );
        })}
      </div>
      {active ? (
        <div className="gallery-lightbox" role="dialog" aria-modal="true" aria-label={CAPTIONS[active.id] || active.id}>
          <button type="button" className="gallery-lightbox-backdrop" aria-label="Close" onClick={() => setActive(null)} />
          <div className="gallery-lightbox-panel">
            <img
              src={`${data.goldens_base}${POSTER[active.id] || active.golden}`}
              alt={CAPTIONS[active.id] || active.id}
            />
            <h2>{CAPTIONS[active.id] || active.title || active.id}</h2>
            <p className="hint">Engine-bound figure · {active.id}</p>
            <div className="gallery-lightbox-actions">
              {EXAMPLE_FOR[active.id] ? (
                <button type="button" className="button-primary button-compact" disabled={busy} onClick={() => tryAsProblem(active.id)}>
                  Try this as a problem
                </button>
              ) : null}
              <button type="button" className="button-secondary button-compact" onClick={() => setActive(null)}>
                Close
              </button>
            </div>
          </div>
        </div>
      ) : null}
    </section>
  );
}
