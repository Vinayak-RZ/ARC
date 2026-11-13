export function marginLine(margins) {
  const d = margins?.display;
  if (d) {
    return { gm: d.gm_db, pm: d.pm_deg, wcg: d.wcg, wcp: d.wcp };
  }
  const fmt = (v, digits, unit) =>
    v != null && Number.isFinite(v) ? `${v.toFixed(digits)}${unit}` : "—";
  return {
    gm: fmt(margins?.gain_margin_db, 2, " dB"),
    pm: fmt(margins?.phase_margin_deg, 1, "°"),
    wcg: fmt(margins?.gain_crossover_rad_s, 2, " rad/s"),
    wcp: fmt(margins?.phase_crossover_rad_s, 2, " rad/s"),
  };
}
