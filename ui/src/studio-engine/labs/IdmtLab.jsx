import { useMemo, useState } from "react";
import { LabShell } from "./LabShell.jsx";
import { Waveform } from "../renderers/Waveform.jsx";
import { coordination, curvePoints, idmtTime } from "./idmt.js";
import { registerLab } from "./registry.js";
import { postProgress } from "../../hooks/useLearn.js";
import { openMatchingProblem } from "./openExample.js";

const CURVES = ["standard", "very", "extreme", "long"];

export function IdmtLab() {
  const [iFault, setIFault] = useState(1000);
  const [r1Ct, setR1Ct] = useState(100);
  const [r1Plug, setR1Plug] = useState(1);
  const [r1Tms, setR1Tms] = useState(0.1);
  const [r1Curve, setR1Curve] = useState("standard");
  const [r2Ct, setR2Ct] = useState(200);
  const [r2Plug, setR2Plug] = useState(1);
  const [r2Curve, setR2Curve] = useState("standard");
  const [ctiTarget, setCtiTarget] = useState(0.3);

  useMemo(() => {
    postProgress({ lab: "idmt" }).catch(() => {});
    return null;
  }, []);

  const result = useMemo(() => {
    try {
      return coordination({
        i_fault_a: iFault,
        r1_ct_primary_a: r1Ct,
        r1_plug_setting: r1Plug,
        r1_tms: r1Tms,
        r1_curve: r1Curve,
        r2_ct_primary_a: r2Ct,
        r2_plug_setting: r2Plug,
        r2_curve: r2Curve,
        cti_s: ctiTarget,
      });
    } catch (err) {
      return { error: String(err.message || err) };
    }
  }, [iFault, r1Ct, r1Plug, r1Tms, r1Curve, r2Ct, r2Plug, r2Curve, ctiTarget]);

  const r1Pts = useMemo(
    () =>
      curvePoints(
        { ct_primary_a: r1Ct, plug_setting: r1Plug, tms: r1Tms, curve: r1Curve },
        r1Ct * r1Plug * 1.05,
        iFault * 3,
      ),
    [r1Ct, r1Plug, r1Tms, r1Curve, iFault],
  );
  const r2Pts = useMemo(() => {
    if (result.error || result.r2_tms == null) return [];
    return curvePoints(
      { ct_primary_a: r2Ct, plug_setting: r2Plug, tms: result.r2_tms, curve: r2Curve },
      r2Ct * r2Plug * 1.05,
      iFault * 3,
    );
  }, [r2Ct, r2Plug, r2Curve, result, iFault]);

  const controls = (
    <>
      <label>
        Fault I (A)
        <div className="lab-slider-row">
          <input type="range" min={100} max={5000} step={10} value={iFault} onChange={(e) => setIFault(+e.target.value)} />
          <input type="number" value={iFault} onChange={(e) => setIFault(+e.target.value)} />
        </div>
      </label>
      <fieldset>
        <legend>Downstream R1</legend>
        <label>
          CT primary
          <input type="number" value={r1Ct} onChange={(e) => setR1Ct(+e.target.value)} />
        </label>
        <label>
          Plug
          <input type="range" min={0.5} max={2} step={0.05} value={r1Plug} onChange={(e) => setR1Plug(+e.target.value)} />
        </label>
        <label>
          TMS
          <input type="range" min={0.05} max={1} step={0.01} value={r1Tms} onChange={(e) => setR1Tms(+e.target.value)} />
        </label>
        <label>
          Curve
          <select value={r1Curve} onChange={(e) => setR1Curve(e.target.value)}>
            {CURVES.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </label>
      </fieldset>
      <fieldset>
        <legend>Upstream R2</legend>
        <label>
          CT primary
          <input type="number" value={r2Ct} onChange={(e) => setR2Ct(+e.target.value)} />
        </label>
        <label>
          Plug
          <input type="range" min={0.5} max={2} step={0.05} value={r2Plug} onChange={(e) => setR2Plug(+e.target.value)} />
        </label>
        <label>
          Curve
          <select value={r2Curve} onChange={(e) => setR2Curve(e.target.value)}>
            {CURVES.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </label>
      </fieldset>
      <label>
        CTI target (s)
        <input type="number" step={0.05} value={ctiTarget} onChange={(e) => setCtiTarget(+e.target.value)} />
      </label>
    </>
  );

  const ctiOk = !result.error && result.cti >= ctiTarget - 1e-9;

  return (
    <LabShell
      title="IDMT coordination lab"
      controls={controls}
      readouts={
        result.error ? (
          <div className="card">
            <strong>{result.error}</strong>
          </div>
        ) : (
          <>
            <div className="card">
              <div className="learn-code-label">t1</div>
              <strong>{result.t1.toFixed(3)} s</strong>
            </div>
            <div className="card">
              <div className="learn-code-label">t2</div>
              <strong>{result.t2.toFixed(3)} s</strong>
            </div>
            <div className="card">
              <div className="learn-code-label">CTI</div>
              <strong className={ctiOk ? "lab-badge-ok" : "lab-badge-warn"}>
                {result.cti.toFixed(3)} s · {ctiOk ? "OK" : "Too small"}
              </strong>
            </div>
            <div className="card">
              <div className="learn-code-label">R2 TMS</div>
              <strong>{result.r2_tms.toFixed(3)}</strong>
            </div>
          </>
        )
      }
      exampleId="idmt"
      onOpenExample={openMatchingProblem}
      check={
        <p className="hint">
          IEC IDMT: t = k·TMS / (PSM^a − 1). R2 TMS is sized for CTI ≥ {ctiTarget} s at the fault current.
          Spot check: PSM 10, TMS 1, standard → {idmtTime({ i_fault_a: 1000, ct_primary_a: 100, plug_setting: 1, tms: 1, curve: "standard" }).toFixed(3)} s.
        </p>
      }
    >
      <Waveform
        panel={{
          title: "t vs I",
          kind: "waveform",
          x: { label: "I", unit: "A", scale: "log" },
          y: { label: "t", unit: "s", scale: "log" },
          series: [
            { id: "r1", label: "R1", points: r1Pts, style: "primary" },
            { id: "r2", label: "R2", points: r2Pts, style: "secondary" },
          ],
          markers: [{ x: iFault, label: "If" }],
        }}
      />
    </LabShell>
  );
}

registerLab({
  id: "idmt",
  title: "IDMT coordination",
  pack: "power",
  subject: "eec-301",
  Component: IdmtLab,
});
