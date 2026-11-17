/** Steady-state rectifier v_o (EEC-303 gate model; keep in sync with rectifier_gate.py). */

import { linePeakFromLineVll, voFull3Analytic, phasePeakFromLineVll } from "./rectifier-analytic.js";

const PI = Math.PI;
const DEG = PI / 180;
const SQRT2 = Math.SQRT2;
const SQRT3 = Math.sqrt(3);

const CFG = {
  hw1: { fam: 1, pos: [{ ph: 0, b: 0, dio: false }], neg: null, gw: 180, fwd: true },
  semi1: {
    fam: 1,
    pos: [
      { ph: 0, b: 0, dio: false },
      { ph: 1, b: 180, dio: false },
    ],
    neg: [
      { ph: 0, b: 0, dio: true },
      { ph: 1, b: 180, dio: true },
    ],
    gw: 180,
    fwd: false,
  },
  full1: {
    fam: 1,
    pos: [
      { ph: 0, b: 0, dio: false },
      { ph: 1, b: 180, dio: false },
    ],
    neg: [
      { ph: 0, b: 180, dio: false },
      { ph: 1, b: 0, dio: false },
    ],
    gw: 180,
    fwd: true,
  },
  hw3: {
    fam: 3,
    pos: [
      { ph: 0, b: 30, dio: false },
      { ph: 1, b: 150, dio: false },
      { ph: 2, b: 270, dio: false },
    ],
    neg: null,
    gw: 120,
    fwd: true,
  },
  semi3: {
    fam: 3,
    pos: [
      { ph: 0, b: 30, dio: false },
      { ph: 1, b: 150, dio: false },
      { ph: 2, b: 270, dio: false },
    ],
    neg: [
      { ph: 0, b: 0, dio: true },
      { ph: 1, b: 0, dio: true },
      { ph: 2, b: 0, dio: true },
    ],
    gw: 120,
    fwd: false,
  },
  full3: { fam: 3, pos: [], neg: [], gw: 120, fwd: true },
};

function normTopo(t) {
  const m = { half1: "hw1", half3: "hw3", half: "hw3", full: "full3", semi: "semi3" };
  return m[t] || t || "full3";
}

function phaseVoltages(conv, vRms, n) {
  const fam = CFG[conv].fam;
  const vm = fam === 1 ? vRms * SQRT2 : (vRms * SQRT2) / SQRT3;
  const out = [];
  for (let i = 0; i < n; i += 1) {
    const th = (2 * PI * i) / n;
    if (conv === "hw1") out.push([vm * Math.sin(th)]);
    else if (fam === 1) {
      const half = (vm * Math.sin(th)) / 2;
      out.push([half, -half]);
    } else {
      out.push([0, 1, 2].map((m) => vm * Math.sin(th - m * 120 * DEG)));
    }
  }
  return out;
}

/** Gate-model samples [[deg, V], ...]; full3 uses analytic path (caller handles). */
export function gateSampleWaveform(p, N = 720) {
  const conv = normTopo(p.topology);
  const load = p.load || "R";
  const alpha = +p.alpha_deg || 0;
  const vRms = p.v_rms ?? (conv.endsWith("3") ? 415 : 230);
  const rOhm = p.r_ohm ?? 10;
  const eV = p.e_v ?? 0;
  const lsSource = p.ls_h ?? 0;
  let lh = p.l_h ?? 0;
  if (lh <= 0 && (load === "RL" || load === "RLE")) lh = 0.01;
  if (load === "R" || load === "CC") lh = 0;
  const io = p.io_a ?? 15;
  const cc = load === "CC";
  const fHz = p.f_hz ?? 50;

  if (conv === "full3" && lsSource <= 0 && !cc) {
    const vll = linePeakFromLineVll(vRms);
    return Array.from({ length: N }, (_, i) => {
      const wt = (2 * PI * i) / N;
      return [(360 * i) / N, voFull3Analytic(wt, vll, alpha)];
    });
  }

  const cfg = CFG[conv];
  const vt = phaseVoltages(conv, vRms, N);
  const { pos, neg } = cfg;
  const np = pos.length;
  const nn = neg ? neg.length : 0;

  const gates = (dev) => {
    const g = [];
    for (let s = 0; s < N; s += 1) {
      if (dev.dio) {
        g.push(true);
        continue;
      }
      const x = ((s * 360) / N - (dev.b + alpha) + 360) % 360;
      g.push(x < cfg.gw - 1e-9);
    }
    return g;
  };
  const gp = pos.map(gates);
  const gn = neg ? neg.map(gates) : [];

  let on = false;
  let fwd = false;
  let pI = -1;
  let nI = -1;
  let i = 0;
  const w0 = 2 * PI * fHz;
  const hr = (2 * PI) / N;

  const bestPos = (s, v) => {
    let k = -1;
    let bv = -Infinity;
    for (let j = 0; j < np; j += 1) {
      if (gp[j][s] && v[pos[j].ph] > bv) {
        bv = v[pos[j].ph];
        k = j;
      }
    }
    return k;
  };
  const bestNeg = (s, v) => {
    let k = -1;
    let bv = Infinity;
    for (let j = 0; j < nn; j += 1) {
      if (gn[j][s] && v[neg[j].ph] < bv) {
        bv = v[neg[j].ph];
        k = j;
      }
    }
    return k;
  };
  const kill = () => {
    on = false;
    fwd = false;
    pI = -1;
    nI = -1;
  };

  const stepCore = (recordVo) => {
    const voOut = recordVo ? [] : null;
    for (let s = 0; s < N; s += 1) {
      const v = vt[s];
      if (!on && !fwd && !cc) {
        const kp = bestPos(s, v);
        const kn = neg ? bestNeg(s, v) : -1;
        if (kp >= 0 && (!neg || kn >= 0)) {
          const vp = v[pos[kp].ph];
          const vn = neg && kn >= 0 ? v[neg[kn].ph] : 0;
          if (vp - vn > eV + 1e-9) {
            on = true;
            pI = kp;
            nI = kn;
          }
        }
      }
      if (fwd) {
        const kp = bestPos(s, v);
        const kn = neg ? bestNeg(s, v) : -1;
        if (kp >= 0 && (!neg || kn >= 0)) {
          const vp = v[pos[kp].ph];
          const vn = neg && kn >= 0 ? v[neg[kn].ph] : 0;
          if (vp - vn > 1e-9) {
            fwd = false;
            on = true;
            pI = kp;
            nI = kn;
          }
        }
      }
      let vpath = 0;
      if (on) {
        let cur = v[pos[pI].ph];
        for (let j = 0; j < np; j += 1) {
          if (j !== pI && gp[j][s] && v[pos[j].ph] > cur + 1e-9) {
            pI = j;
            cur = v[pos[pI].ph];
          }
        }
        if (neg && nI >= 0) {
          let curn = v[neg[nI].ph];
          for (let j = 0; j < nn; j += 1) {
            if (j !== nI && gn[j][s] && v[neg[j].ph] < curn - 1e-9) {
              nI = j;
              curn = v[neg[nI].ph];
            }
          }
        }
        const rp = v[pos[pI].ph];
        const rn = neg && nI >= 0 ? v[neg[nI].ph] : 0;
        vpath = rp - rn;
        if (cfg.fwd && vpath < 0) {
          on = false;
          fwd = true;
          pI = -1;
          nI = -1;
          vpath = 0;
        }
      }
      let vo;
      if (cc) {
        i = io;
        vo = on ? vpath : 0;
      } else if (on || fwd) {
        if (lh <= 0) {
          i = (vpath - eV) / rOhm;
          vo = vpath;
          if (i <= 0) {
            i = 0;
            kill();
            vo = eV;
          }
        } else {
          const iss = (vpath - eV) / rOhm;
          const ex = Math.exp((-rOhm * hr) / (w0 * lh));
          i = iss + (i - iss) * ex;
          vo = vpath;
          if (i <= 0) {
            i = 0;
            kill();
          }
        }
      } else {
        i = 0;
        vo = eV;
      }
      if (recordVo) voOut.push([(360 * s) / N, vo]);
    }
    return voOut;
  };

  for (let c = 0; c < 2000; c += 1) {
    const prev = i;
    stepCore(false);
    if (Math.abs(i - prev) < 1e-8 * (1 + Math.abs(i))) break;
  }
  kill();
  i = Math.max(i, 1e-6);
  return stepCore(true);
}