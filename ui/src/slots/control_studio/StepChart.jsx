import { useEffect, useMemo, useRef, useState } from "react";

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

function fmtTime(v) {
  if (v == null || Number.isNaN(v)) return "—";
  return v < 0.1 ? Number(v).toPrecision(2) : Number(v).toFixed(2);
}

export function niceTicks(min, max, n = 5) {
  const step0 = (max - min) / Math.max(n - 1, 1);
  const mag = 10 ** Math.floor(Math.log10(step0 || 1));
  const norm = step0 / mag;
  const step = (norm < 1.5 ? 1 : norm < 3 ? 2 : norm < 7 ? 5 : 10) * mag;
  const out = [];
  for (let v = Math.ceil(min / step) * step; v <= max + 1e-9; v += step) out.push(+v.toFixed(10));
  return out;
}

export function StepChart({ data, margins, onWindowChange, windowS, tabBar = null }) {
  const [cursor, setCursor] = useState(null);
  const wrapRef = useRef(null);
  const plotRef = useRef(null);
  const [size, setSize] = useState({ w: 640, h: 180 });
  const { t, y, setpoint = 1, unit = "", metrics = {} } = data || {};
  const status = metrics.status || (metrics.settled ? "settled" : "not_settled");
  const yLabel = unit ? `Speed (${unit})` : "Output";
  const win = metrics.window_s || 10;
  const xLabel = win !== 10 ? `Time (s), ${fmt(win, 0)} s window` : "Time (s)";

  useEffect(() => {
    const el = plotRef.current;
    if (!el) return undefined;
    const ro = new ResizeObserver(() => {
      const r = el.getBoundingClientRect();
      setSize({ w: Math.max(560, Math.floor(r.width)), h: Math.max(160, Math.floor(r.height)) });
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

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

  const w = size.w;
  const h = size.h;
  // Bottom band: tick numbers (16 px under the plot) plus the axis title with room for descenders.
  const m = { l: 56, r: 16, t: 24, b: 56 };
  const plotW = w - m.l - m.r;
  const plotH = h - m.t - m.b;
  const x = (time) => m.l + ((time - series.t0) / (series.t1 - series.t0 || 1)) * plotW;
  const ypx = (val) => m.t + plotH - ((val - series.ymin) / (series.ymax - series.ymin || 1)) * plotH;
  const path = series.points.map((p, i) => `${i === 0 ? "M" : "L"} ${x(p.t).toFixed(1)} ${ypx(p.y).toFixed(1)}`).join(" ");
  const spY = ypx(setpoint);
  // Settling band, settle time and overshoot are measured against the FINAL value y_ss.
  // The setpoint is a separate line; their gap is the steady-state error e_ss.
  const flat = status !== "not_settled";
  const yss = flat ? Number(metrics.final_value) : null;
  const offTarget = flat && metrics.on_target === false;
  const bandLo = flat ? yss - 0.02 * Math.abs(yss) : null;
  const bandHi = flat ? yss + 0.02 * Math.abs(yss) : null;
  const unitSfx = unit ? ` ${unit}` : "";
  const finalText = flat ? `${Number(yss).toPrecision(3)}${unitSfx}` : "";
  // One summary line, drawn inside the plot's top margin so it can never wrap into the controls.
  const summary =
    flat && metrics.t_settle_s != null
      ? `Settling time ${fmtTime(metrics.t_settle_s)} s` +
        (offTarget
          ? ` · Final value ${finalText} · ${fmt(metrics.steady_state_error_pct, 1)}% ${metrics.direction || "below"} setpoint`
          : metrics.overshoot_pct != null
            ? ` · Overshoot ${fmt(metrics.overshoot_pct, 1)}%`
            : "")
      : "";
  const peak =
    flat && metrics.overshoot_pct > 0.05 && metrics.peak_t_s != null
      ? { px: x(metrics.peak_t_s), py: ypx(metrics.peak_value) }
      : null;
  const ts = metrics.t_settle_s;
  const settleX =
    flat && ts != null && ts >= series.t0 && ts <= series.t1 ? x(ts) : null;
  const xTicks = niceTicks(series.t0, series.t1, 5);
  const yTicks = niceTicks(series.ymin, series.ymax, 4);
  const aria = metrics.aria_summary || `Step response to ${fmt(setpoint)} ${unit}`.trim();

  return (
    <div className="studio-step-chart" ref={wrapRef}>
      <div className="studio-step-chart-head studio-step-chart-head-unified">
        {tabBar}
        <div className="studio-step-chart-head-right">
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
          {summary ? (
            <span className="studio-settled-pill visually-hidden" role="status">
              {summary}
            </span>
          ) : null}
        </div>
      </div>
      <div className="studio-step-plot" ref={plotRef}>
      <svg
        className="studio-step-svg"
        width={w}
        height={h}
        role="img"
        aria-label={aria}
        onMouseLeave={() => setCursor(null)}
        onMouseMove={(ev) => {
          const rect = ev.currentTarget.getBoundingClientRect();
          const px = ev.clientX - rect.left;
          const frac = (px - m.l) / plotW;
          const ti = series.t0 + frac * (series.t1 - series.t0);
          let idx = 0;
          for (let i = 0; i < series.points.length; i += 1) {
            if (series.points[i].t <= ti) idx = i;
          }
          setCursor(series.points[idx]);
        }}
      >
        {yTicks.map((yv) => {
          const gy = ypx(yv);
          return <line key={yv} x1={m.l} x2={w - m.r} y1={gy} y2={gy} className="studio-step-grid" />;
        })}
        {summary ? (
          <text x={m.l} y={15} className="studio-step-summary">
            {summary}
          </text>
        ) : null}
        {flat ? (
          <>
            <rect
              x={m.l}
              y={ypx(bandHi)}
              width={plotW}
              height={Math.max(0, ypx(bandLo) - ypx(bandHi))}
              className="studio-step-band"
            />
            <line x1={m.l} x2={w - m.r} y1={ypx(bandHi)} y2={ypx(bandHi)} className="studio-step-band-edge" />
            <line x1={m.l} x2={w - m.r} y1={ypx(bandLo)} y2={ypx(bandLo)} className="studio-step-band-edge" />
            <text x={m.l + plotW * 0.62} y={ypx(bandLo) + 14} className="studio-step-band-label">
              ±2% of final value
            </text>
          </>
        ) : null}
        <line x1={m.l} x2={w - m.r} y1={spY} y2={spY} className="studio-step-setpoint" strokeDasharray="4 3" />
        <text x={w - m.r - 4} y={spY - 6} className="studio-step-ref-label" textAnchor="end">
          Setpoint {fmt(setpoint, 2)}
        </text>
        {offTarget ? (
          <>
            <line x1={m.l} x2={w - m.r} y1={ypx(yss)} y2={ypx(yss)} className="studio-step-final" />
            <text x={w - m.r - 4} y={ypx(yss) + 15} className="studio-step-ref-label" textAnchor="end">
              Final value {finalText}
            </text>
            <text x={w - m.r - 4} y={ypx(yss) + 30} className="studio-step-sse" textAnchor="end">
              e_ss = {fmt(metrics.steady_state_error_pct, 1)}%
            </text>
          </>
        ) : null}
        {settleX != null ? (
          <>
            <line x1={settleX} x2={settleX} y1={m.t} y2={m.t + plotH} className="studio-step-settle" />
            <text
              x={settleX + (settleX > w - m.r - 60 ? -5 : 5)}
              y={m.t + plotH - 6}
              className="studio-step-settle-label"
              textAnchor={settleX > w - m.r - 60 ? "end" : "start"}
            >
              {fmtTime(metrics.t_settle_s)} s
            </text>
          </>
        ) : null}
        <path d={path} className="studio-step-line" fill="none" />
        {peak ? (
          <>
            <circle cx={peak.px} cy={peak.py} r={3.5} className="studio-step-peak" />
            <text x={peak.px + 8} y={peak.py + 4} className="studio-step-peak-label">
              {fmt(metrics.overshoot_pct, 1)}%
            </text>
          </>
        ) : null}
        {xTicks.map((tv) => (
          <text key={tv} x={x(tv)} y={m.t + plotH + 16} className="studio-step-tick" textAnchor="middle">
            {fmt(tv, tv < 10 ? 1 : 0)}
          </text>
        ))}
        {yTicks.map((yv) => (
          <text key={yv} x={m.l - 6} y={ypx(yv) + 4} className="studio-step-tick" textAnchor="end">
            {fmt(yv, 2)}
          </text>
        ))}
        <text x={w / 2} y={h - 14} className="studio-step-axis" textAnchor="middle">
          {xLabel}
        </text>
        <text
          x={14}
          y={m.t + plotH / 2}
          className="studio-step-axis"
          transform={`rotate(-90 14 ${m.t + plotH / 2})`}
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
      </div>
    </div>
  );
}
