/*
 * Home example thumbnails: simple line drawings, 16:10 (160 x 100 viewBox).
 * Every shape sets its own class so no shape inherits a fill by accident
 * (the old .example-thumb-accent class filled every polyline, which turned
 * curves into solid wedges). Strokes are non-scaling, so 1.5px stays 1.5px.
 * Both themes use the same geometry and the same tokens.
 */
const FRAME = { w: 160, h: 100 };

function Frame({ children }) {
  return (
    <svg className="example-thumb-svg" viewBox={`0 0 ${FRAME.w} ${FRAME.h}`} role="img" aria-hidden>
      <rect x={0} y={0} width={FRAME.w} height={FRAME.h} className="example-thumb-bg" rx={4} />
      {children}
    </svg>
  );
}

const pt = (x, y) => `${x.toFixed(1)},${y.toFixed(1)}`;

/** Vertical zigzag resistor from (x, y0) to (x, y1). */
function zigzagV(x, y0, y1, amp = 4.5, teeth = 3) {
  const lead = 3;
  const a = y0 + lead;
  const b = y1 - lead;
  const n = teeth * 2;
  const pts = [pt(x, y0), pt(x, a)];
  for (let i = 0; i < n; i += 1) {
    const y = a + ((i + 0.5) * (b - a)) / n;
    pts.push(pt(x + (i % 2 === 0 ? amp : -amp), y));
  }
  pts.push(pt(x, b), pt(x, y1));
  return pts.join(" ");
}

function ThumbDivider() {
  const x = 78;
  return (
    <Frame>
      <text x={34} y={17} className="example-thumb-label">
        Vin
      </text>
      <polyline className="th-line" points="24,22 24,74 78,74" />
      <polyline className="th-line" points="24,22 78,22 78,26" />
      <polyline className="th-line" points={zigzagV(x, 22, 46)} />
      <polyline className="th-line" points={zigzagV(x, 54, 74)} />
      <line className="th-line" x1={x} y1={46} x2={x} y2={54} />
      <line className="th-line" x1={x} y1={50} x2={106} y2={50} />
      <circle className="th-dot" cx={x} cy={50} r={3} />
      <circle className="th-dot" cx={106} cy={50} r={3} />
      <text x={114} y={53.5} className="example-thumb-label">
        Vout
      </text>
      <line className="th-line" x1={x} y1={74} x2={x} y2={78} />
      <line className="th-line" x1={x - 8} y1={78} x2={x + 8} y2={78} />
      <line className="th-line" x1={x - 5} y1={82} x2={x + 5} y2={82} />
      <line className="th-line" x1={x - 2} y1={86} x2={x + 2} y2={86} />
    </Frame>
  );
}

function axes(x0, y0, x1, y1) {
  return (
    <>
      <line className="th-axis" x1={x0} y1={y0} x2={x1} y2={y0} />
      <line className="th-axis" x1={x0} y1={y0} x2={x0} y2={y1} />
    </>
  );
}

function expCurve(k, { x0 = 24, x1 = 140, y0 = 80, rise = 54, n = 40 } = {}) {
  return Array.from({ length: n + 1 }, (_, i) => {
    const t = i / n;
    return pt(x0 + t * (x1 - x0), y0 - (1 - Math.exp(-k * t)) * rise);
  }).join(" ");
}

function ThumbStep() {
  // 1 - e^(-t), drawn to about five time constants so it settles on the dashed line.
  const k = 5;
  const final = 80 - (1 - Math.exp(-k)) * 54;
  return (
    <Frame>
      {axes(24, 80, 146, 14)}
      <line className="th-dash" x1={24} y1={final} x2={146} y2={final} />
      <polyline className="th-line" points={expCurve(k)} />
    </Frame>
  );
}

/*
 * DC motor speed: an under-damped speed response with a small overshoot, then a load
 * step part-way along that dips the speed and recovers, so it cannot be mistaken for
 * the first-order step tile.
 */
function motorSpeedPoints() {
  const X0 = 24;
  const X1 = 142;
  const Y0 = 80;
  const rise = 44;
  const zeta = 0.45;
  const wn = 11;
  const wd = wn * Math.sqrt(1 - zeta * zeta);
  const tLoad = 0.62;
  const dip = 0.5;
  const n = 90;
  const pts = [];
  for (let i = 0; i <= n; i += 1) {
    const t = i / n;
    let v = 1 - Math.exp(-zeta * wn * t) * (Math.cos(wd * t) + ((zeta * wn) / wd) * Math.sin(wd * t));
    if (t > tLoad) {
      const u = t - tLoad;
      v -= dip * (1 - Math.exp(-14 * u)) * Math.exp(-7 * u);
    }
    pts.push(pt(X0 + t * (X1 - X0), Y0 - v * rise));
  }
  return { pts: pts.join(" "), final: Y0 - rise };
}

function ThumbMotorSpeed() {
  const { pts, final } = motorSpeedPoints();
  return (
    <Frame>
      {axes(24, 80, 146, 14)}
      <line className="th-dash" x1={24} y1={final} x2={146} y2={final} />
      <polyline className="th-line" points={pts} />
    </Frame>
  );
}

/*
 * Equal-area picture: during the fault Pe is about 0, so the accelerating area is the
 * rectangle Pm * (dc - d0). After clearing, Pe = sin(d) lies above Pm and the
 * decelerating area runs from dc to the max swing dm, where the two areas are equal.
 */
function swingGeometry() {
  const pm = 0.45;
  const d0 = Math.asin(pm);
  const dc = 1.4;
  const acc = pm * (dc - d0);
  const dec = (dm) => Math.cos(dc) - Math.cos(dm) - pm * (dm - dc);
  let lo = dc;
  let hi = Math.PI - d0;
  for (let i = 0; i < 40; i += 1) {
    const mid = (lo + hi) / 2;
    if (dec(mid) < acc) lo = mid;
    else hi = mid;
  }
  return { pm, d0, dc, dm: (lo + hi) / 2 };
}

function ThumbSwing() {
  const X0 = 24;
  const X1 = 140;
  const Y0 = 80;
  const A = 58;
  const px = (d) => X0 + (d / Math.PI) * (X1 - X0);
  const py = (p) => Y0 - p * A;
  const { pm, d0, dc, dm } = swingGeometry();
  const curve = (a, b, n = 24) =>
    Array.from({ length: n + 1 }, (_, i) => {
      const d = a + ((b - a) * i) / n;
      return pt(px(d), py(Math.sin(d)));
    });
  const whole = curve(0, Math.PI, 48).join(" ");
  const accel = [pt(px(d0), py(pm)), pt(px(dc), py(pm)), pt(px(dc), Y0), pt(px(d0), Y0)].join(" ");
  const decel = [pt(px(dc), py(pm)), ...curve(dc, dm), pt(px(dm), py(pm))].join(" ");
  return (
    <Frame>
      {axes(X0, Y0, 146, 14)}
      <polygon className="th-tint" points={accel} />
      <polygon className="th-tint" points={decel} />
      <line className="th-dash" x1={X0} y1={py(pm)} x2={146} y2={py(pm)} />
      <line className="th-dash" x1={px(dc)} y1={py(Math.sin(dc))} x2={px(dc)} y2={Y0} />
      <polyline className="th-line" points={whole} />
    </Frame>
  );
}

function ThumbDigital() {
  const cx = 80;
  const cy = 50;
  const r = 32;
  const cross = (x, y) => (
    <g key={`${x}-${y}`}>
      <line className="th-line" x1={x - 3.5} y1={y - 3.5} x2={x + 3.5} y2={y + 3.5} />
      <line className="th-line" x1={x - 3.5} y1={y + 3.5} x2={x + 3.5} y2={y - 3.5} />
    </g>
  );
  return (
    <Frame>
      <line className="th-axis" x1={cx - 44} y1={cy} x2={cx + 44} y2={cy} />
      <line className="th-axis" x1={cx} y1={cy - 40} x2={cx} y2={cy + 40} />
      <circle className="th-axis" cx={cx} cy={cy} r={r} />
      {cross(cx + 0.55 * r, cy - 0.55 * r)}
      {cross(cx + 0.55 * r, cy + 0.55 * r)}
      {cross(cx - 0.35 * r, cy)}
    </Frame>
  );
}

function ThumbSpectrum() {
  const heights = [8, 14, 56, 12, 34, 9, 6, 5];
  return (
    <Frame>
      <line className="th-axis" x1={20} y1={80} x2={146} y2={80} />
      {heights.map((h, i) => {
        const x = 34 + i * 14;
        return (
          <g key={i}>
            <line className="th-line" x1={x} y1={80} x2={x} y2={80 - h} />
            <circle className="th-dot" cx={x} cy={80 - h} r={2.4} />
          </g>
        );
      })}
    </Frame>
  );
}

const THUMBS = {
  divider: ThumbDivider,
  "control-step": ThumbStep,
  "smib-swing": ThumbSwing,
  "dc-drive": ThumbMotorSpeed,
  "digital-stable": ThumbDigital,
  "signals-fft": ThumbSpectrum,
};

export function ExampleThumb({ id }) {
  const C = THUMBS[id] || ThumbStep;
  return <C />;
}
