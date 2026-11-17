/** Build sparkline series + markers for Simulated vs derived aside. */

import { computeRectifier } from "../studio-engine/labs/rectifier.js";

function downsample(points, maxN = 64) {
  if (!points?.length) return [];
  if (points.length <= maxN) return points;
  const step = Math.ceil(points.length / maxN);
  return points.filter((_, i) => i % step === 0);
}

export function sparklineFromLabVerify(runData, labVerify) {
  if (!labVerify) return null;
  const kind = labVerify.lab_kind || runData?.lab?.kind || "";
  const recipe = (() => {
    try {
      return JSON.parse(runData?.summary || "{}").recipe_id || "";
    } catch {
      return "";
    }
  })();

  if (kind === "control" || recipe.includes("control")) {
    const series = labVerify.simulate?.step_series;
    const t = series?.t;
    const y = series?.y;
    if (!t?.length || !y?.length) return null;
    const pts = downsample(
      t.map((ti, i) => [ti, y[i]]),
      80,
    );
    const derivedY = Number(labVerify.derived ?? labVerify.metrics?.[0]?.derived);
    const simY = Number(labVerify.simulated ?? labVerify.metrics?.[0]?.simulated);
    const yLine = Number.isFinite(derivedY) ? derivedY : simY;
    let markerX = t[t.length - 1];
    const tSettle = series.metrics?.t_settle_s;
    if (tSettle != null) markerX = Number(tSettle);
    return {
      kind: "control",
      points: pts,
      yLabel: "y",
      hline: Number.isFinite(yLine) ? yLine : null,
      marker: { x: markerX, label: Number.isFinite(derivedY) ? "y_ss" : "t_s" },
    };
  }

  if (kind === "circuit" || runData?.problem?.kind === "series_rlc" || recipe.includes("simulate-circuit")) {
    const sim = runData?.lab_simulate;
    const trace = sim?.trace?.vc_trace_ms || sim?.vc_trace_ms || runData?.rlc_transient?.vc_trace_ms;
    if (!trace?.length) return null;
    const pts = downsample(trace, 80);
    const primary = (labVerify.metrics || []).find((m) => m.id === "primary") || labVerify.metrics?.[0];
    const isFinal = String(primary?.label || "").toLowerCase().includes("final");
    const derived = Number(primary?.derived ?? labVerify.derived);
    const peakRow = (labVerify.metrics || []).find((m) => m.id === "t_peak");
    const tPeakMs =
      1000 *
      Number(
        peakRow?.derived ??
          sim?.t_peak_s ??
          runData?.circuit_derive?.t_s ??
          runData?.rlc_transient?.t_Vc_peak_s ??
          0,
      );
    return {
      kind: "rlc",
      points: pts,
      yLabel: "Vc",
      hline: Number.isFinite(derived) ? derived : null,
      marker: isFinal
        ? { x: pts[pts.length - 1]?.[0] ?? 0, label: "2%" }
        : { x: tPeakMs, label: "peak" },
    };
  }

  if (recipe.includes("rectifier") || runData?.problem?.kind?.includes("rectifier")) {
    const prob = runData?.problem || {};
    const p = {
      topology: prob.topology || "full3",
      load: prob.load || "R",
      v_rms: prob.v_rms || prob.v_ll_rms || 415,
      alpha_deg: prob.alpha_deg ?? 30,
      r_ohm: prob.r_ohm ?? 10,
      io_a: prob.io_a ?? 0,
      ls_h: prob.ls_h ?? 0,
    };
    const { points, Vo } = computeRectifier(p);
    if (!points.length) return null;
    const pts = downsample(points, 80);
    return {
      kind: "rectifier",
      points: pts,
      yLabel: "v_o",
      hline: Number.isFinite(Vo) ? Vo : null,
      marker: null,
    };
  }

  return null;
}