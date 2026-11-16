import { useMemo, useState } from "react";
import { LabShell } from "./LabShell.jsx";
import { Waveform } from "../renderers/Waveform.jsx";
import { converterMetrics } from "./converter.js";
import { registerLab } from "./registry.js";
import { postProgress } from "../../hooks/useLearn.js";
import { openMatchingProblem } from "./openExample.js";

function rippleWave(d, deltaIl, periods = 3, n = 120) {
  const pts = [];
  for (let i = 0; i < n; i += 1) {
    const t = (periods * i) / (n - 1);
    const cycle = t % 1;
    const y = cycle < d ? -0.5 + cycle / d : 0.5 - (cycle - d) / (1 - d);
    pts.push([t, y * deltaIl]);
  }
  return pts;
}

export function ConverterLab() {
  const [topology, setTopology] = useState("buck");
  const [vin, setVin] = useState(12);
  const [d, setD] = useState(0.5);
  const [lUh, setLUh] = useState(100);
  const [cUf, setCUf] = useState(47);
  const [fsKhz, setFsKhz] = useState(100);
  const [r, setR] = useState(5);

  useMemo(() => {
    postProgress({ lab: "converter" }).catch(() => {});
    return null;
  }, []);

  const result = useMemo(
    () =>
      converterMetrics({
        topology,
        vin,
        d,
        l: lUh * 1e-6,
        c: cUf * 1e-6,
        fs: fsKhz * 1e3,
        r,
      }),
    [topology, vin, d, lUh, cUf, fsKhz, r],
  );

  const iL = rippleWave(d, result.deltaIl);
  const vo = rippleWave(d, result.deltaVo).map(([t, y]) => [t, result.Vo + y]);

  const controls = (
    <>
      <fieldset>
        <legend>Topology</legend>
        {["buck", "boost", "buck-boost"].map((t) => (
          <label key={t}>
            <input type="radio" name="topo" checked={topology === t} onChange={() => setTopology(t)} />
            {t}
          </label>
        ))}
      </fieldset>
      <label>
        Vin (V)
        <div className="lab-slider-row">
          <input type="range" min={5} max={48} step={0.5} value={vin} onChange={(e) => setVin(+e.target.value)} />
          <input type="number" value={vin} onChange={(e) => setVin(+e.target.value)} />
        </div>
      </label>
      <label>
        D
        <div className="lab-slider-row">
          <input type="range" min={0.1} max={0.9} step={0.01} value={d} onChange={(e) => setD(+e.target.value)} />
          <input type="number" step={0.01} value={d} onChange={(e) => setD(+e.target.value)} />
        </div>
      </label>
      <label>
        L (µH)
        <div className="lab-slider-row">
          <input type="range" min={10} max={500} value={lUh} onChange={(e) => setLUh(+e.target.value)} />
          <input type="number" value={lUh} onChange={(e) => setLUh(+e.target.value)} />
        </div>
      </label>
      <label>
        C (µF)
        <div className="lab-slider-row">
          <input type="range" min={10} max={470} value={cUf} onChange={(e) => setCUf(+e.target.value)} />
          <input type="number" value={cUf} onChange={(e) => setCUf(+e.target.value)} />
        </div>
      </label>
      <label>
        fs (kHz)
        <div className="lab-slider-row">
          <input type="range" min={20} max={500} value={fsKhz} onChange={(e) => setFsKhz(+e.target.value)} />
          <input type="number" value={fsKhz} onChange={(e) => setFsKhz(+e.target.value)} />
        </div>
      </label>
      <label>
        R (Ω)
        <div className="lab-slider-row">
          <input type="range" min={1} max={50} step={0.5} value={r} onChange={(e) => setR(+e.target.value)} />
          <input type="number" value={r} onChange={(e) => setR(+e.target.value)} />
        </div>
      </label>
    </>
  );

  return (
    <LabShell
      title="DC–DC converter lab"
      controls={controls}
      readouts={
        <>
          <div className="card">
            <div className="learn-code-label">Vo</div>
            <strong>{result.Vo.toFixed(3)} V</strong>
          </div>
          <div className="card">
            <div className="learn-code-label">ΔiL</div>
            <strong>{result.deltaIl.toFixed(4)} A</strong>
          </div>
          <div className="card">
            <div className="learn-code-label">ΔVo</div>
            <strong>{result.deltaVo.toFixed(4)} V</strong>
          </div>
          <div className="card">
            <div className="learn-code-label">Mode</div>
            <strong className={result.ccm ? "lab-badge-ok" : "lab-badge-warn"}>{result.ccm ? "CCM" : "DCM"}</strong>
          </div>
        </>
      }
      exampleId="converter"
      onOpenExample={openMatchingProblem}
      check={
        <p className="hint">
          Closed-form CCM formulas from the EEC-303 sheet. Lcrit = {result.Lcrit.toExponential(3)} H.
          {result.ccm ? " L ≥ Lcrit — CCM." : " L < Lcrit — DCM (waveform sketch still CCM-shaped)."}
        </p>
      }
    >
      <Waveform
        panel={{
          title: "iL ripple",
          kind: "waveform",
          x: { label: "t", unit: "periods", scale: "linear" },
          y: { label: "iL", unit: "A", scale: "linear" },
          series: [{ id: "il", label: "ΔiL", points: iL, style: "primary" }],
        }}
      />
      <Waveform
        panel={{
          title: "vo",
          kind: "waveform",
          x: { label: "t", unit: "periods", scale: "linear" },
          y: { label: "vo", unit: "V", scale: "linear" },
          series: [{ id: "vo", label: "vo", points: vo, style: "primary" }],
          hlines: [{ y: result.Vo, label: "Vo" }],
        }}
      />
    </LabShell>
  );
}

registerLab({
  id: "converter",
  title: "DC–DC converter",
  pack: "power_electronics",
  subject: "eec-303",
  Component: ConverterLab,
});
