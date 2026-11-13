import { useEffect, useMemo, useState } from "react";

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
  useEffect(() => {
    fetch("/api/visual-kit")
      .then((r) => r.json())
      .then(setData)
      .catch(() => setData({ components: [], goldens_base: "" }));
  }, []);
  const items = useMemo(() => {
    const list = data.components || [];
    if (pack === "All") return list;
    return list.filter((c) => packOf(c) === pack);
  }, [data.components, pack]);
  return (
    <section className="visual-gallery" aria-label="Arc Visual Kit gallery">
      <h1>Visuals</h1>
      <p className="visual-gallery-lede">Engine-bound figures. Numbers come from Arc kernels, not prompts.</p>
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
              <div className="gallery-card-media">
                <img src={`${data.goldens_base}${rel}`} alt={CAPTIONS[c.id] || c.id} loading="lazy" />
                {isGif ? <span className="gallery-gif-badge">GIF</span> : null}
              </div>
              <figcaption>
                <span className="gallery-card-title">{CAPTIONS[c.id] || c.id}</span>
                <span className="hint">{c.id}</span>
              </figcaption>
            </figure>
          );
        })}
      </div>
    </section>
  );
}
