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

function gatedSine(wt, Vm, alpha, halfWave) {
  const cycle = ((wt % (2 * PI)) + 2 * PI) % (2 * PI);
  const half = ((wt % PI) + PI) % PI;
  if (halfWave) {
    return cycle >= alpha && cycle < PI ? Math.max(0, Vm * Math.sin(wt)) : 0;
  }
  return half >= alpha ? Math.abs(Vm * Math.sin(wt)) : 0;
}

/** Six-pulse line-line envelope, firing delayed by alpha. */
function sixPulse(wt, VllPk, alpha) {
  const sector = Math.PI / 3;
  const local = ((wt - alpha) % sector + sector) % sector;
  return VllPk * Math.cos(local - sector / 2);
}

export function sampleWaveform(p, N = 720) {
  const { topology, v_rms, alpha_deg } = p;
  const alpha = (alpha_deg * PI) / 180;
  const three = topology.endsWith("3");
  const Vm = three ? Math.SQRT2 * v_rms : Math.SQRT2 * v_rms;
  const points = [];
  for (let i = 0; i < N; i += 1) {
    const wt = (2 * PI * i) / N;
    let vo = 0;
    if (topology === "full3" || topology === "semi3" || topology === "hw3") {
      vo = sixPulse(wt, Vm, alpha);
      if (topology === "hw3" && vo < 0) vo = 0;
    } else if (topology === "full1" || topology === "semi1") {
      vo = gatedSine(wt, Vm, alpha, false);
    } else {
      vo = gatedSine(wt, Vm, alpha, true);
    }
    points.push([(wt * 180) / PI, vo]);
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
