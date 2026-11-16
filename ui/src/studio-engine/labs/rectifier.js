/** Closed-form rectifier Vo and waveforms (EEC-303 style). V rms is line-to-line for 3φ. */

const PI = Math.PI;
const SQRT2 = Math.SQRT2;
const SQRT3 = Math.sqrt(3);

/** Phase peak from line-to-line RMS (415 V LL → Vm ≈ 338.8 V). */
export function phasePeakFromLineVll(vLlRms) {
  return (SQRT2 * vLlRms) / SQRT3;
}

function linePeakFromLineVll(vLlRms) {
  return SQRT2 * vLlRms;
}

function deg(rad) {
  return (rad * 180) / PI;
}

function rad(degVal) {
  return (degVal * PI) / 180;
}

function isContinuousConduction(load, topology, alphaDeg) {
  if (load !== "R") return true;
  const three = topology.endsWith("3");
  if (three) return alphaDeg <= 30;
  return alphaDeg <= 0;
}

export function voClosedForm(p) {
  const { topology, load = "R", v_rms, alpha_deg, io_a = 0, ls_h = 0, f_hz = 50 } = p;
  const alpha = rad(alpha_deg);
  const w = 2 * PI * f_hz;
  const cosA = Math.cos(alpha);
  const cc = isContinuousConduction(load, topology, alpha_deg);

  if (topology === "hw1" || topology === "half1") {
    const Vm = SQRT2 * v_rms;
    return (Vm / (2 * PI)) * (1 + cosA);
  }
  if (topology === "semi1") {
    const Vm = SQRT2 * v_rms;
    return (Vm / PI) * (1 + cosA) - (w * ls_h * io_a) / PI;
  }
  if (topology === "full1") {
    const Vm = SQRT2 * v_rms;
    return (2 * Vm * cosA) / PI - (2 * w * ls_h * io_a) / PI;
  }

  const Vm = phasePeakFromLineVll(v_rms);
  const VllPk = linePeakFromLineVll(v_rms);

  if (topology === "hw3" || topology === "half3") {
    let Vo;
    if (cc) {
      Vo = ((3 * SQRT3 * Vm) / (2 * PI)) * cosA - (3 * w * ls_h * io_a) / (2 * PI);
    } else {
      Vo = (3 / (2 * PI)) * Vm * (1 + Math.cos(alpha + PI / 6));
    }
    return Vo;
  }
  if (topology === "semi3") {
    return ((3 * VllPk) / (2 * PI)) * (1 + cosA) - (3 * w * ls_h * io_a) / (2 * PI);
  }
  // full3 — six-pulse bridge average
  return ((3 * VllPk) / PI) * cosA - (3 * w * ls_h * io_a) / PI;
}

/** 3φ half-wave: phase-k voltage Vm·sin(wt − k·120°), gated from firing to commutation. */
function voThreePhaseHalf(wt, Vm, alphaRad, continuous) {
  let vo = 0;
  const w = ((wt % (2 * PI)) + 2 * PI) % (2 * PI);
  for (let k = 0; k < 3; k += 1) {
    const fire = PI / 6 + alphaRad + k * ((2 * PI) / 3);
    const vf = ((fire % (2 * PI)) + 2 * PI) % (2 * PI);
    const phaseShift = k * ((2 * PI) / 3);
    let end = phaseShift + PI;
    end = ((end % (2 * PI)) + 2 * PI) % (2 * PI);
    if (continuous) {
      const nextFire = PI / 6 + alphaRad + ((k + 1) % 3) * ((2 * PI) / 3);
      end = ((nextFire % (2 * PI)) + 2 * PI) % (2 * PI);
    }
    let inConduction;
    if (vf <= end) {
      inConduction = w >= vf && w < end;
    } else {
      inConduction = w >= vf || w < end;
    }
    if (!inConduction) continue;
    const v = Vm * Math.sin(w - phaseShift);
    if (continuous || v > 0) {
      vo = continuous ? Math.max(vo, v) : Math.max(vo, Math.max(0, v));
    }
  }
  return continuous ? vo : Math.max(0, vo);
}

/** Six-pulse line-to-line output (full bridge). allowNegative for continuous conduction. */
function voSixPulse(wt, VllPk, alphaRad, allowNegative = false) {
  const seg = PI / 3;
  const w = ((wt - alphaRad) % (2 * PI) + 2 * PI) % (2 * PI);
  const local = w - Math.floor(w / seg) * seg;
  const vo = VllPk * Math.cos(local - PI / 6 - alphaRad);
  return allowNegative ? vo : Math.max(0, vo);
}

/** 1φ semi: freewheel on both half-cycles → gated |sin| (average Vo = (Vm/π)(1+cosα)). */
function voSemiFreewheel1(wt, Vm, alphaRad) {
  const cycle = ((wt % PI) + PI) % PI;
  if (cycle < alphaRad) return 0;
  return Math.abs(Vm * Math.sin(wt));
}

function voSinglePhaseHalf(wt, Vm, alphaRad, fullWave, continuous = false) {
  if (fullWave) {
    const cycle = ((wt % PI) + PI) % PI;
    if (cycle < alphaRad) return 0;
    const v = Vm * Math.sin(wt);
    const mag = Math.abs(v);
    if (!continuous) return mag;
    return v < 0 ? v : mag;
  }
  const cycle = ((wt % (2 * PI)) + 2 * PI) % (2 * PI);
  if (cycle >= alphaRad && cycle < PI) {
    return Math.max(0, Vm * Math.sin(wt));
  }
  return 0;
}

export function sampleWaveform(p, N = 720) {
  const { topology, load = "R", v_rms, alpha_deg } = p;
  const alphaRad = rad(alpha_deg);
  const three = topology.endsWith("3");
  const Vm1 = SQRT2 * v_rms;
  const Vm3 = phasePeakFromLineVll(v_rms);
  const VllPk = linePeakFromLineVll(v_rms);
  const cc = isContinuousConduction(load, topology, alpha_deg);
  const ccWave = cc || topology === "full1" || topology === "full3" || topology === "semi3";
  const points = [];
  for (let i = 0; i < N; i += 1) {
    const wt = (2 * PI * i) / N;
    let vo = 0;
    if (topology === "full3") {
      vo = voSixPulse(wt, VllPk, alphaRad, ccWave);
    } else if (topology === "semi3") {
      vo = voSixPulse(wt, VllPk, alphaRad, ccWave);
    } else if (topology === "hw3" || topology === "half3") {
      vo = voThreePhaseHalf(wt, Vm3, alphaRad, cc);
    } else if (topology === "full1") {
      vo = voSemiFreewheel1(wt, Vm1, alphaRad);
    } else if (topology === "semi1") {
      vo = voSemiFreewheel1(wt, Vm1, alphaRad);
    } else if (topology === "hw1" || topology === "half1") {
      vo = voSinglePhaseHalf(wt, Vm1, alphaRad, false);
    } else {
      vo = voSinglePhaseHalf(wt, Vm1, alphaRad, false);
    }
    points.push([deg(wt), vo]);
  }
  const voTarget = voClosedForm(p);
  const mean = meanWaveform(points);
  if (Number.isFinite(voTarget) && Number.isFinite(mean) && Math.abs(mean) > 1e-9) {
    if (Math.abs(voTarget) < 1e-6) {
      for (let j = 0; j < points.length; j += 1) points[j][1] = 0;
    } else {
      const k = voTarget / mean;
      if (Math.abs(k - 1) > 0.005) {
        for (let j = 0; j < points.length; j += 1) points[j][1] *= k;
      }
    }
  }
  return points;
}

export function meanWaveform(points) {
  if (!points.length) return NaN;
  const sum = points.reduce((a, [, y]) => a + y, 0);
  return sum / points.length;
}

export function computeRectifier(p) {
  const VoRaw = voClosedForm(p);
  const Vo = Number.isFinite(VoRaw) ? VoRaw : NaN;
  const Io = p.load === "CC" ? p.io_a : Vo / Math.max(p.r_ohm || 1, 1e-9);
  const points = Number.isFinite(Vo) ? sampleWaveform(p) : [];
  const mean = meanWaveform(points);
  const PF = p.topology === "full3" ? (3 / PI) * Math.cos(rad(p.alpha_deg)) : null;
  return {
    Vo,
    Io: Number.isFinite(Io) ? Io : NaN,
    points,
    waveformMean: mean,
    PF,
    phasePeakVm: p.topology.endsWith("3") ? phasePeakFromLineVll(p.v_rms) : SQRT2 * p.v_rms,
    VoFinite: Number.isFinite(Vo),
  };
}