/** Closed-form rectifier Vo / metrics (EEC-303 formula sheet). */

const PI = Math.PI;

export function voClosedForm(p) {
  const { topology, v_rms, alpha_deg, io_a = 0, ls_h = 0, f_hz = 50 } = p;
  const alpha = (alpha_deg * PI) / 180;
  const w = 2 * PI * f_hz;
  const cosA = Math.cos(alpha);
  if (topology === "hw1" || topology === "half1") {
    const Vm = Math.SQRT2 * v_rms;
    return (Vm / (2 * PI)) * (1 + cosA);
  }
  if (topology === "semi1") {
    const Vm = Math.SQRT2 * v_rms;
    return (Vm / PI) * (1 + cosA) - (w * ls_h * io_a) / PI;
  }
  if (topology === "full1") {
    const Vm = Math.SQRT2 * v_rms;
    // continuous conduction textbook form
    return (2 * Vm * cosA) / PI - (2 * w * ls_h * io_a) / PI;
  }
  if (topology === "hw3" || topology === "half3") {
    const Vm = Math.SQRT2 * (v_rms / Math.SQRT2); // v_rms is line-line for 3ph UI default 415
    // For 3ph half, plan uses phase Vm = Vll/√2? Standard: Vll,rms given.
    const Vll_pk = Math.SQRT2 * v_rms;
    const Vm_ph = Vll_pk / Math.SQRT3;
    return ((3 * Math.SQRT3 * Vm_ph) / (2 * PI)) * cosA - (3 * w * ls_h * io_a) / (2 * PI);
  }
  if (topology === "semi3") {
    const Vll_pk = Math.SQRT2 * v_rms;
    return ((3 * Vll_pk) / (2 * PI)) * (1 + cosA) - (3 * w * ls_h * io_a) / (2 * PI);
  }
  // full3
  const Vll_pk = Math.SQRT2 * v_rms;
  return ((3 * Vll_pk) / PI) * cosA - (3 * w * ls_h * io_a) / PI;
}

export function sampleWaveform(p, N = 720) {
  const { topology, v_rms, alpha_deg, f_hz = 50 } = p;
  const alpha = (alpha_deg * PI) / 180;
  const Vll_pk = Math.SQRT2 * v_rms;
  const points = [];
  for (let i = 0; i < N; i += 1) {
    const wt = (2 * PI * i) / N;
    const deg = (wt * 180) / PI;
    let vo = 0;
    if (topology.startsWith("full") && topology.includes("3")) {
      // 6-pulse envelope
      const phases = [0, 2 * PI / 3, 4 * PI / 3];
      let best = -Infinity;
      for (const ph of phases) {
        const v = Vll_pk * Math.cos(wt - ph - PI / 6);
        if (v > best) best = v;
      }
      const gateOk = ((wt % (PI / 3)) + alpha) < PI / 3 + alpha; // simplified
      vo = best * Math.cos(alpha); // approximate gated average shape
      // better: delayed envelope
      const sector = Math.floor(((wt - alpha + 2 * PI) % (2 * PI)) / (PI / 3));
      const mid = sector * (PI / 3) + alpha + PI / 6;
      vo = Vll_pk * Math.cos(wt - mid);
      if (vo < 0 && topology === "full3") vo = 0; // rough
    } else if (topology === "full1") {
      const Vm = Math.SQRT2 * v_rms;
      const fired = (wt % PI) >= alpha;
      vo = fired ? Math.abs(Vm * Math.sin(wt)) * Math.sign(Math.sin(wt) || 1) : 0;
      // continuous full bridge controlled:
      vo = fired ? Vm * Math.sin(wt) * (Math.sin(wt) >= 0 ? 1 : -1) : 0;
      // use |sin| after alpha each half
      const half = wt % PI;
      vo = half >= alpha ? Math.abs(Vm * Math.sin(wt)) : 0;
    } else {
      const Vm = Math.SQRT2 * v_rms;
      const half = wt % (2 * PI);
      vo = half >= alpha && half < PI + alpha ? Math.max(0, Vm * Math.sin(wt)) : 0;
    }
    points.push([deg, vo]);
  }
  return points;
}

export function computeRectifier(p) {
  const Vo = voClosedForm(p);
  const Io = p.load === "CC" ? p.io_a : Vo / Math.max(p.r_ohm || 1, 1e-9);
  const points = sampleWaveform(p);
  return {
    Vo,
    Io,
    points,
    PF: p.topology === "full3" ? (3 / PI) * Math.cos((p.alpha_deg * PI) / 180) : null,
  };
}
