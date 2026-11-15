import { useMemo, useState } from "react";
import { LabShell } from "./LabShell.jsx";
import { Waveform } from "../renderers/Waveform.jsx";
import { bodeSeries, leadDesign } from "./lead.js";
import { registerLab } from "./registry.js";
import { postProgress } from "../../hooks/useLearn.js";
import { openMatchingProblem } from "./openExample.js";

export function LeadLab() {
  const [K, setK] = useState(10);
  const [a, setA] = useState(1);
  const [b, setB] = useState(0);
  const [pmTarget, setPmTarget] = useState(50);
  const [epsilon, setEpsilon] = useState(8);

  useMemo(() => {
    postProgress({ lab: "lead" }).catch(() => {});
    return null;
  }, []);

  const design = useMemo(
    () => leadDesign({ K, a, b, pmTarget, epsilon, pmUnc: b === 0 && K === 10 && a === 1 ? 17.96 : null }),
    [K, a, b, pmTarget, epsilon],
  );

  const bode = useMemo(
    () => bodeSeries(K, a, b, design.alpha, design.tau),
    [K, a, b, design.alpha, design.tau],
  );

  const controls = (
    <>
      <fieldset>
        <legend>Plant K / (s(s+a)(s+b))</legend>
        <label>
          K
          <div className="lab-slider-row">
            <input type="range" min={1} max={50} step={0.5} value={K} onChange={(e) => setK(+e.target.value)} />
            <input type="number" value={K} onChange={(e) => setK(+e.target.value)} />
          </div>
        </label>
        <label>
          a
          <div className="lab-slider-row">
            <input type="range" min={0.1} max={10} step={0.1} value={a} onChange={(e) => setA(+e.target.value)} />
            <input type="number" value={a} onChange={(e) => setA(+e.target.value)} />
          </div>
        </label>
        <label>
          b (0 = omit)
          <div className="lab-slider-row">
            <input type="range" min={0} max={10} step={0.1} value={b} onChange={(e) => setB(+e.target.value)} />
            <input type="number" value={b} onChange={(e) => setB(+e.target.value)} />
          </div>
        </label>
      </fieldset>
      <label>
        PM target (°)
        <div className="lab-slider-row">
          <input type="range" min={30} max={70} value={pmTarget} onChange={(e) => setPmTarget(+e.target.value)} />
          <input type="number" value={pmTarget} onChange={(e) => setPmTarget(+e.target.value)} />
        </div>
      </label>
      <label>
        ε (°)
        <div className="lab-slider-row">
          <input type="range" min={5} max={12} value={epsilon} onChange={(e) => setEpsilon(+e.target.value)} />
          <input type="number" value={epsilon} onChange={(e) => setEpsilon(+e.target.value)} />
        </div>
      </label>
    </>
  );

  return (
    <LabShell
      title="Lead compensator lab"
      controls={controls}
      readouts={
        <>
          <div className="card">
            <div className="learn-code-label">PM unc</div>
            <strong>{design.pmUnc.toFixed(2)}°</strong>
          </div>
          <div className="card">
            <div className="learn-code-label">PM comp</div>
            <strong>{design.pmComp != null ? `${design.pmComp.toFixed(2)}°` : "—"}</strong>
          </div>
          <div className="card">
            <div className="learn-code-label">α</div>
            <strong>{design.alpha.toFixed(3)}</strong>
          </div>
          <div className="card">
            <div className="learn-code-label">τ</div>
            <strong>{design.tau.toFixed(4)}</strong>
          </div>
          <div className="card">
            <div className="learn-code-label">ωm</div>
            <strong>{design.wm.toFixed(3)} rad/s</strong>
          </div>
          <div className="card">
            <div className="learn-code-label">1/α</div>
            <strong>{design.networkGain.toFixed(3)}</strong>
          </div>
        </>
      }
      exampleId="lead"
      onOpenExample={openMatchingProblem}
      check={
        <p className="hint">
          EET-123 lead design: φm = PMtarget − PMunc + ε → α → ωm at −10 log10(α) → τ = 1/(ωm√α).
          Default plant K=10, a=1, b=0 uses hard-coded PMunc = 17.96°.
        </p>
      }
    >
      <Waveform
        panel={{
          title: "Bode magnitude",
          kind: "waveform",
          x: { label: "ω", unit: "rad/s", scale: "log" },
          y: { label: "|G|", unit: "dB", scale: "linear" },
          series: [
            { id: "unc", label: "unc", points: bode.magUnc, style: "secondary" },
            { id: "comp", label: "comp", points: bode.magComp, style: "primary" },
          ],
          hlines: [{ y: 0, label: "0 dB" }],
        }}
      />
      <Waveform
        panel={{
          title: "Bode phase",
          kind: "waveform",
          x: { label: "ω", unit: "rad/s", scale: "log" },
          y: { label: "∠G", unit: "deg", scale: "linear" },
          series: [
            { id: "unc", label: "unc", points: bode.phUnc, style: "secondary" },
            { id: "comp", label: "comp", points: bode.phComp, style: "primary" },
          ],
        }}
      />
    </LabShell>
  );
}

registerLab({
  id: "lead",
  title: "Lead compensator",
  pack: "control",
  subject: "eet-123",
  Component: LeadLab,
});
