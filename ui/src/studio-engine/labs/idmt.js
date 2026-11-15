const CURVES = {
  standard: { k: 0.14, a: 0.02 },
  very: { k: 13.5, a: 1 },
  extreme: { k: 80, a: 2 },
  long: { k: 120, a: 1 },
};

export function idmtTime({ i_fault_a, ct_primary_a, plug_setting = 1, tms, curve = "standard" }) {
  const { k, a } = CURVES[curve] || CURVES.standard;
  const psm = i_fault_a / (ct_primary_a * plug_setting);
  if (psm <= 1) throw new Error("relay does not operate");
  return (k * tms) / (psm ** a - 1);
}

export function coordination(p) {
  const t1 = idmtTime({
    i_fault_a: p.i_fault_a,
    ct_primary_a: p.r1_ct_primary_a,
    plug_setting: p.r1_plug_setting,
    tms: p.r1_tms,
    curve: p.r1_curve,
  });
  const { k, a } = CURVES[p.r2_curve] || CURVES.standard;
  const psm2 = p.i_fault_a / (p.r2_ct_primary_a * p.r2_plug_setting);
  const t2Needed = t1 + (p.cti_s || 0.3);
  const r2_tms = (t2Needed * (psm2 ** a - 1)) / k;
  const t2 = idmtTime({
    i_fault_a: p.i_fault_a,
    ct_primary_a: p.r2_ct_primary_a,
    plug_setting: p.r2_plug_setting,
    tms: r2_tms,
    curve: p.r2_curve,
  });
  return { t1, t2, r2_tms, cti: t2 - t1 };
}

export function curvePoints(relay, iMin, iMax, n = 40) {
  const pts = [];
  for (let i = 0; i < n; i += 1) {
    const frac = i / (n - 1);
    const I = iMin * (iMax / iMin) ** frac;
    try {
      pts.push([I, idmtTime({ ...relay, i_fault_a: I })]);
    } catch {
      /* skip */
    }
  }
  return pts;
}
