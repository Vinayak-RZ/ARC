import { useEffect, useMemo, useRef, useState } from "react";
import { MAX_POINTS } from "../spec.js";
import { niceTicks, logTicks } from "../math/ticks.js";

const STYLE_COLOR = {
  primary: "var(--ee-color-primary)",
  secondary: "var(--ee-color-copper)",
  positive: "var(--ee-semantic-up)",
  "muted-dashed": "var(--ee-color-muted)",
};

function mapX(x, xMin, xMax, w, pad, log) {
  if (log) {
    const a = Math.log10(Math.max(xMin, 1e-12));
    const b = Math.log10(Math.max(xMax, 1e-12));
    return pad + ((Math.log10(Math.max(x, 1e-12)) - a) / (b - a || 1)) * (w - 2 * pad);
  }
  return pad + ((x - xMin) / (xMax - xMin || 1)) * (w - 2 * pad);
}

function mapY(y, yMin, yMax, h, pad, log) {
  if (log) {
    const a = Math.log10(Math.max(yMin, 1e-12));
    const b = Math.log10(Math.max(yMax, 1e-12));
    return h - pad - ((Math.log10(Math.max(y, 1e-12)) - a) / (b - a || 1)) * (h - 2 * pad);
  }
  return h - pad - ((y - yMin) / (yMax - yMin || 1)) * (h - 2 * pad);
}

export function Waveform({ panel }) {
  const ref = useRef(null);
  const [size, setSize] = useState({ w: 480, h: 220 });
  const [showTable, setShowTable] = useState(false);
  const series = panel.series || [];
  const overflow = series.some((s) => (s.points || []).length > MAX_POINTS);

  useEffect(() => {
    const el = ref.current;
    if (!el) return undefined;
    const ro = new ResizeObserver((entries) => {
      const r = entries[0]?.contentRect;
      if (r) setSize({ w: Math.max(200, r.width), h: Math.max(160, r.height) });
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  const bounds = useMemo(() => {
    let xMin = Infinity;
    let xMax = -Infinity;
    let yMin = Infinity;
    let yMax = -Infinity;
    for (const s of series) {
      for (const [x, y] of s.points || []) {
        xMin = Math.min(xMin, x);
        xMax = Math.max(xMax, x);
        yMin = Math.min(yMin, y);
        yMax = Math.max(yMax, y);
      }
    }
    if (!Number.isFinite(xMin)) return { xMin: 0, xMax: 1, yMin: 0, yMax: 1 };
    if (yMin === yMax) {
      yMin -= 1;
      yMax += 1;
    }
    return { xMin, xMax, yMin, yMax };
  }, [series]);

  if (overflow) {
    return <p className="hint">Waveform has too many points (max {MAX_POINTS}).</p>;
  }

  const pad = 36;
  const logX = panel.x?.scale === "log";
  const logY = panel.y?.scale === "log";
  const xt = logX ? logTicks(bounds.xMin, bounds.xMax) : niceTicks(bounds.xMin, bounds.xMax, 5);
  const yt = logY ? logTicks(bounds.yMin, bounds.yMax) : niceTicks(bounds.yMin, bounds.yMax, 5);
  const { w, h } = size;
  const xTitle = [panel.x?.label, panel.x?.unit].filter(Boolean).join(" (");
  const xAxis = panel.x?.unit ? `${xTitle})` : panel.x?.label || "x";
  const yTitle = [panel.y?.label, panel.y?.unit].filter(Boolean).join(" (");
  const yAxis = panel.y?.unit ? `${yTitle})` : panel.y?.label || "y";

  return (
    <div className="se-waveform" ref={ref}>
      <div className="se-waveform-head">
        {panel.title ? <h4 className="se-waveform-title">{panel.title}</h4> : null}
        <span className="se-waveform-axes" aria-hidden>
          {yAxis} vs {xAxis}
        </span>
        <button type="button" className="button-secondary button-compact" onClick={() => setShowTable((v) => !v)}>
          {showTable ? "Hide values" : "Show values"}
        </button>
      </div>
      <svg
        width="100%"
        height={h}
        viewBox={`0 0 ${w} ${h}`}
        role="img"
        aria-label={`${panel.title || "Waveform"}; ${panel.x?.label || "x"} vs ${panel.y?.label || "y"}`}
      >
        <g style={{ color: "var(--ee-color-hairline)" }}>
          {xt.map((t) => {
            const x = mapX(t, bounds.xMin, bounds.xMax, w, pad, logX);
            return <line key={`x${t}`} x1={x} y1={pad} x2={x} y2={h - pad} stroke="currentColor" strokeWidth={0.5} />;
          })}
          {yt.map((t) => {
            const y = mapY(t, bounds.yMin, bounds.yMax, h, pad, logY);
            return <line key={`y${t}`} x1={pad} y1={y} x2={w - pad} y2={y} stroke="currentColor" strokeWidth={0.5} />;
          })}
        </g>
        <g style={{ color: "var(--ee-color-muted)", fontSize: 12 }}>
          {xt.map((t) => (
            <text key={`xl${t}`} x={mapX(t, bounds.xMin, bounds.xMax, w, pad, logX)} y={h - 8} textAnchor="middle">
              {t}
            </text>
          ))}
          {yt.map((t) => (
            <text key={`yl${t}`} x={8} y={mapY(t, bounds.yMin, bounds.yMax, h, pad, logY) + 3}>
              {t}
            </text>
          ))}
        </g>
        {(panel.hlines || []).map((hl, i) => {
          const y = mapY(hl.y, bounds.yMin, bounds.yMax, h, pad, logY);
          return (
            <g key={i}>
              <line x1={pad} y1={y} x2={w - pad} y2={y} stroke="var(--ee-color-muted)" strokeDasharray="4 4" />
              <text x={w - pad} y={y - 4} textAnchor="end" fontSize={11} fill="var(--ee-color-body)">
                {hl.label}
              </text>
            </g>
          );
        })}
        {(panel.markers || []).map((m, i) => {
          const x = mapX(m.x, bounds.xMin, bounds.xMax, w, pad, logX);
          return (
            <g key={i}>
              <line x1={x} y1={pad} x2={x} y2={h - pad} stroke="var(--ee-color-copper)" strokeDasharray="3 3" />
              <text x={x + 4} y={pad + 12} fontSize={11} fill="var(--ee-color-copper)">
                {m.label}
              </text>
            </g>
          );
        })}
        {series.map((s) => {
          const pts = s.points || [];
          if (!pts.length) return null;
          const d = pts
            .map((p, i) => {
              const x = mapX(p[0], bounds.xMin, bounds.xMax, w, pad, logX);
              const y = mapY(p[1], bounds.yMin, bounds.yMax, h, pad, logY);
              return `${i ? "L" : "M"} ${x} ${y}`;
            })
            .join(" ");
          const style = s.style || "primary";
          const last = pts[pts.length - 1];
          return (
            <g key={s.id}>
              <path
                d={d}
                fill="none"
                stroke={STYLE_COLOR[style]}
                strokeWidth={1.75}
                strokeDasharray={style === "muted-dashed" ? "6 4" : undefined}
                vectorEffect="non-scaling-stroke"
              />
              <text
                x={mapX(last[0], bounds.xMin, bounds.xMax, w, pad, logX)}
                y={mapY(last[1], bounds.yMin, bounds.yMax, h, pad, logY) - 6}
                fontSize={12}
                fill={STYLE_COLOR[style]}
              >
                {s.label || s.id}
              </text>
            </g>
          );
        })}
        <text x={w / 2} y={h - 2} textAnchor="middle" fontSize={12} fill="var(--ee-color-body)">
          {xAxis}
        </text>
        <text
          x={14}
          y={h / 2}
          textAnchor="middle"
          fontSize={12}
          fill="var(--ee-color-body)"
          transform={`rotate(-90 14 ${h / 2})`}
        >
          {yAxis}
        </text>
      </svg>
      {showTable ? (
        <table className="se-wave-table">
          <thead>
            <tr>
              <th>{panel.x?.label || "x"}</th>
              {series.map((s) => (
                <th key={s.id}>{s.label || s.id}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {Array.from({ length: Math.min(50, Math.max(...series.map((s) => (s.points || []).length), 0)) }).map(
              (_, i) => (
                <tr key={i}>
                  <td>{series[0]?.points?.[i]?.[0]}</td>
                  {series.map((s) => (
                    <td key={s.id}>{s.points?.[i]?.[1]}</td>
                  ))}
                </tr>
              ),
            )}
          </tbody>
        </table>
      ) : null}
    </div>
  );
}
