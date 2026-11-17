import { useMemo, useState } from "react";
import { LabShell } from "./LabShell.jsx";
import { Waveform } from "../renderers/Waveform.jsx";
import { computeRectifier, firingAnglesDeg } from "./rectifier.js";
import { registerLab } from "./registry.js";
import { postProgress } from "../../hooks/useLearn.js";
import { openMatchingProblem } from "./openExample.js";
import { fixedYAxisFromSearch } from "./rectifier-axis.js";

function firingMarkers(topology, alphaDeg) {
  return firingAnglesDeg(topology, alphaDeg).map((x, i) => ({
    x,
    label: i === 0 ? `α = ${alphaDeg}° after natural commutation` : undefined,
  }));
}

const TOPOS = [
  { id: "hw1", label: "1φ half" },
  { id: "semi1", label: "1φ semi" },
  { id: "full1", label: "1φ full" },
  { id: "hw3", label: "3φ half" },
  { id: "semi3", label: "3φ semi" },
  { id: "full3", label: "3φ full" },
];

export function RectifierLab() {
  const [topology, setTopology] = useState("hw3");
  const [load, setLoad] = useState("R");
  const [vRms, setVRms] = useState(415);
  const [alpha, setAlpha] = useState(45);
  const [rOhm, setROhm] = useState(10);
  const [io, setIo] = useState(20);
  const [ls, setLs] = useState(2);
  const [useLs, setUseLs] = useState(false);
  // Optional ?ymax= (and ?ymin=) holds the y axis fixed, e.g. for recordings of an alpha sweep.
  const fixedY = useMemo(
    () => fixedYAxisFromSearch(typeof window === "undefined" ? "" : window.location.search),
    [],
  );

  useMemo(() => {
    postProgress({ lab: "rectifier" }).catch(() => {});
    return null;
  }, []);

  const result = useMemo(
    () =>
      computeRectifier({
        topology,
        load,
        v_rms: vRms,
        alpha_deg: alpha,
        r_ohm: rOhm,
        io_a: io,
        ls_h: useLs ? ls / 1000 : 0,
        f_hz: 50,
      }),
    [topology, load, vRms, alpha, rOhm, io, ls, useLs],
  );

  const controls = (
    <>
      <fieldset>
        <legend>Converter</legend>
        {TOPOS.map((t) => (
          <label key={t.id}>
            <input type="radio" name="topo" checked={topology === t.id} onChange={() => setTopology(t.id)} />
            {t.label}
          </label>
        ))}
      </fieldset>
      <fieldset>
        <legend>Load</legend>
        {["R", "RL", "RLE", "CC"].map((l) => (
          <label key={l}>
            <input type="radio" name="load" checked={load === l} onChange={() => setLoad(l)} />
            {l}
          </label>
        ))}
      </fieldset>
      <label>
        Line voltage (V rms, line-to-line)
        <div className="lab-slider-row">
          <input type="range" min={50} max={500} step={5} value={vRms} onChange={(e) => setVRms(+e.target.value)} />
          <input type="number" value={vRms} onChange={(e) => setVRms(+e.target.value)} />
          <span className="lab-field-unit">V</span>
        </div>
      </label>
      <p className="hint">Phase peak Vm = {result.phasePeakVm.toFixed(1)} V</p>
      <label>
        α (deg)
        <div className="lab-slider-row">
          <input type="range" min={0} max={180} value={alpha} onChange={(e) => setAlpha(+e.target.value)} />
          <input type="number" value={alpha} onChange={(e) => setAlpha(+e.target.value)} />
        </div>
      </label>
      <label>
        R (Ω)
        <div className="lab-slider-row">
          <input type="range" min={0.5} max={100} step={0.5} value={rOhm} onChange={(e) => setROhm(+e.target.value)} />
          <input type="number" value={rOhm} onChange={(e) => setROhm(+e.target.value)} />
        </div>
      </label>
      {load === "CC" ? (
        <label>
          Io (A)
          <div className="lab-slider-row">
            <input type="range" min={1} max={100} value={io} onChange={(e) => setIo(+e.target.value)} />
            <input type="number" value={io} onChange={(e) => setIo(+e.target.value)} />
            <span className="lab-field-unit">A</span>
          </div>
        </label>
      ) : null}
      <label className="lab-checkbox-row">
        <input type="checkbox" checked={useLs} onChange={(e) => setUseLs(e.target.checked)} />
        Source inductance Ls (mH)
      </label>
      {useLs ? (
        <label>
          <span className="visually-hidden">Source inductance Ls (mH)</span>
          <div className="lab-slider-row">
            <input type="range" min={0.1} max={10} step={0.1} value={ls} onChange={(e) => setLs(+e.target.value)} />
            <input type="number" value={ls} onChange={(e) => setLs(+e.target.value)} />
          </div>
        </label>
      ) : null}
    </>
  );

  return (
    <LabShell
      title="Rectifier waveform lab"
      controls={controls}
      readouts={
        <>
          <div className="card">
            <div className="learn-code-label">Vo</div>
            <strong>{result.VoFinite ? `${result.Vo.toFixed(2)} V` : "—"}</strong>
          </div>
          <div className="card">
            <div className="learn-code-label">Io</div>
            <strong>{result.VoFinite ? `${result.Io.toFixed(2)} A` : "—"}</strong>
          </div>
          {result.PF != null ? (
            <div className="card">
              <div className="learn-code-label">PF</div>
              <strong>{result.PF.toFixed(3)}</strong>
            </div>
          ) : null}
          {result.rlConduction ? (
            <div className="card">
              <div className="learn-code-label">Conduction</div>
              <strong>{result.rlConduction.label}</strong>
              {result.rlConduction.mode === "Discontinuous" && result.rlConduction.beta_deg != null ? (
                <p className="hint">β = {result.rlConduction.beta_deg.toFixed(1)}°</p>
              ) : null}
            </div>
          ) : null}
        </>
      }
      exampleId="rectifier"
      onOpenExample={openMatchingProblem}
      check={
        <p className="hint">
          Vo is the time-average of the plotted v_o waveform; RL mode follows the gate ODE steady state.
        </p>
      }
    >
      <Waveform
        panel={{
          kind: "waveform",
          title: "Rectifier output",
          x: { label: "ωt", unit: "°", scale: "linear" },
          y: { label: "v", sub: "o", unit: "V", scale: "linear", ...(fixedY || {}) },
          series: [{ id: "vo", label: "vo", points: result.points, style: "primary" }],
          hlines: [{ y: result.Vo, label: "Vo avg" }],
          markers: firingMarkers(topology, alpha),
        }}
      />
    </LabShell>
  );
}

registerLab({
  id: "rectifier",
  title: "Rectifier waveform",
  pack: "power_electronics",
  subject: "eec-303",
  Component: RectifierLab,
});
