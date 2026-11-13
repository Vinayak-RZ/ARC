import { useMemo, useState } from "react";

const WINDOWS = [
  { id: 10, label: "10 s" },
  { id: 30, label: "30 s" },
  { id: 100, label: "100 s" },
  { id: "auto", label: "Auto" },
];

function fmt(v, d = 2) {
  if (v == null || Number.isNaN(v)) return "—";
  return Number(v).toFixed(d);
}

export function StepChart({ data, margins, onWindowChange, windowS }) {
  const [cursor, setCursor] = useState(null);
  const { t, y, setpoint = 1, unit = "", metrics = {} } = data || {};
  const status = metrics.status || (metrics.settled ? "settled" : "not_settled");
  const yLabel = unit ? `Speed (${unit})` : "Output";
  const xLabel = metrics.window_s && metrics.window_s !== 10
    ? `Time (s), window ${fmt(metrics.window_s, 0)} s`
  : "Time (s)";
  const series = useMemo(() => {
    if (!t?.length || !y?.length) return null;
    const t0 = t[0];
    const t1 = t[t.length - 1];
    const ymin = Math.min(...y);
    const ymax = Math.max(...y, setpoint);
    const padY = (ymax - ymin) * 0.08 || 0.1;
    return { t0, t1, ymin: ymin - padY, ymax: ymax + padY, points: t.map((ti, i) => ({ t: ti, y: y[i] })) };
  }, [t, y, setpoint]);

  if (!series) return <p className="cs-margins-hint">No step data.</p>;

  const w = 640;
  const h = 160;
  const m = { l: 48, r: 16, t: 28, b: 36 };
  const plotW = w - m.l - m.r;
  const plotH = h - m.t - m.b;
  const x = (time) => m.l + ((time - series.t0) / (series.t1 - series.t0 || 1)) * plotW;
  const ypx = (val) => m.t + plotH - ((val - series.ymin) / (series.ymax - series.ymin || 1)) * plotH;
  const path = series.points.map((p, i) => `${i === 0 ? "M" : "L"} ${x(p.t).toFixed(1)} ${ypx(p.y).toFixed(1)}`).join(" ");
  const spY = ypx(setpoint);
  const aria = metrics.aria_summary || `Step response to ${fmt(setpoint)} ${unit}`.trim();

  return (
    <div className="studio-step-chart">
      <div className="studio-step-chart-head">
        <div className="studio-window-segment" role="group" aria-label="Simulation window">
          {WINDOWS.map((wopt) => (
            <button
              key={wopt.id}
              type="button"
              className={windowS === wopt.id ? "is-active" : ""}
              onClick={() => onWindowChange?.(wopt.id)}
            >
              {wopt.label}
            </button>
          ))}
        </div>
        {status === "not_settled" ? (
          <span className="studio-unsettled-pill" role="status">
            Not settled within {fmt(metrics.window_s || 10, 0)} s
          </span>
        ) : null}
        {status === "settled_off_target" ? (
          <span className="studio-offtarget-pill" role="status">
            Settles at {fmt(metrics.final_value ?? metrics.value_at_end, 2)}, {fmt(metrics.steady_state_error_pct, 0)}%
            below the setpoint
          </span>
        ) : null}
      </div>
      <svg
        className="studio-step-svg"
        width="100%"
        height={h}
        viewBox={`0 0 ${w} ${h}`}
        role="img"
        aria-label={aria}
        onMouseLeave={() => setCursor(null)}
        onMouseMove={(ev) => {
          const rect = ev.currentTarget.getBoundingClientRect();
          const px = ((ev.clientX - rect.left) / rect.width) * w;
          const frac = (px - m.l) / plotW;
          const ti = series.t0 + frac * (series.t1 - series.t0);
          let idx = 0;
          for (let i = 0; i < series.points.length; i += 1) {
            if (series.points[i].t <= ti) idx = i;
          }
          setCursor(series.points[idx]);
        }}
      >
        {[0, 0.25, 0.5, 0.75, 1].map((f) => {
          const gy = m.t + plotH * f;
          return <line key={f} x1={m.l} x2={w - m.r} y1={gy} y2={gy} className="studio-step-grid" />;
        })}
        <line x1={m.l} x2={w - m.r} y1={spY} y2={spY} className="studio-step-setpoint" strokeDasharray="4 3" />
        <text x={w - m.r - 4} y={spY - 4} className="studio-step-label" textAnchor="end">
          Setpoint {fmt(setpoint)}
        </text>
        <path d={path} className="studio-step-line" fill="none" />
        <text x={m.l} y={h - 8} className="studio-step-axis">
          {xLabel}
        </text>
        <text
          x={12}
          y={m.t + plotH / 2}
          className="studio-step-axis"
          transform={`rotate(-90 12 ${m.t + plotH / 2})`}
          textAnchor="middle"
        >
          {yLabel}
        </text>
        {cursor ? (
          <>
            <line x1={x(cursor.t)} x2={x(cursor.t)} y1={m.t} y2={m.t + plotH} className="studio-step-cursor" />
            <text x={x(cursor.t) + 6} y={m.t + 14} className="studio-step-readout">
              t = {fmt(cursor.t)} s, {fmt(cursor.y)} {unit}
            </text>
          </>
        ) : null}
      </svg>
      {status === "not_settled" && (metrics.tail_slope ?? 0) > 0 ? (
        <p className="studio-step-foot">
          Still rising at {fmt(metrics.window_s || 10, 0)} s: {fmt(metrics.value_at_end)} of a setpoint of {fmt(setpoint)}.
        </p>
      ) : null}
    </div>
  );
}
