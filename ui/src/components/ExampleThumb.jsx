const FRAME = { w: 160, h: 100 };

function Frame({ children }) {
  return (
    <svg className="example-thumb-svg" viewBox={`0 0 ${FRAME.w} ${FRAME.h}`} role="img" aria-hidden>
      <rect x={0} y={0} width={FRAME.w} height={FRAME.h} className="example-thumb-bg" rx={4} />
      {children}
    </svg>
  );
}

function ThumbDivider() {
  return (
    <Frame>
      <line x1={40} y1={30} x2={40} y2={70} className="example-thumb-ink" strokeWidth={2} />
      <line x1={120} y1={30} x2={120} y2={70} className="example-thumb-ink" strokeWidth={2} />
      <line x1={40} y1={50} x2={120} y2={50} className="example-thumb-accent" strokeWidth={2} />
      <circle cx={80} cy={50} r={4} className="example-thumb-accent" fill="currentColor" />
    </Frame>
  );
}

function ThumbStep() {
  const pts = Array.from({ length: 12 }, (_, i) => {
    const t = i / 11;
    const x = 20 + t * 120;
    const y = 78 - (1 - Math.exp(-t * 4)) * 52;
    return `${x},${y}`;
  }).join(" ");
  return (
    <Frame>
      <polyline points={pts} fill="none" className="example-thumb-accent" strokeWidth={2} />
      <line x1={16} y1={78} x2={144} y2={78} className="example-thumb-muted" strokeWidth={1} />
    </Frame>
  );
}

function ThumbSwing() {
  return (
    <Frame>
      <path
        d="M 24 70 Q 60 20 96 55 T 136 40"
        fill="none"
        className="example-thumb-accent"
        strokeWidth={2}
      />
      <line x1={24} y1={70} x2={136} y2={70} className="example-thumb-muted" strokeWidth={1} strokeDasharray="3 2" />
    </Frame>
  );
}

function ThumbMotorSpeed() {
  const pts = Array.from({ length: 12 }, (_, i) => {
    const t = i / 11;
    const x = 20 + t * 120;
    const y = 78 - t * 55;
    return `${x},${y}`;
  }).join(" ");
  return (
    <Frame>
      <text x={12} y={18} className="example-thumb-label">
        ω
      </text>
      <polyline points={pts} fill="none" className="example-thumb-accent" strokeWidth={2} />
    </Frame>
  );
}

function ThumbDigital() {
  return (
    <Frame>
      <circle cx={80} cy={50} r={32} fill="none" className="example-thumb-muted" strokeWidth={1} />
      <circle cx={62} cy={42} r={4} className="example-thumb-accent" fill="currentColor" />
      <circle cx={98} cy={58} r={4} className="example-thumb-accent" fill="currentColor" />
    </Frame>
  );
}

function ThumbSpectrum() {
  const bars = [12, 28, 42, 55, 40, 22, 14];
  return (
    <Frame>
      {bars.map((h, i) => (
        <rect
          key={i}
          x={24 + i * 16}
          y={78 - h}
          width={10}
          height={h}
          className="example-thumb-accent"
          opacity={0.7 + i * 0.03}
        />
      ))}
    </Frame>
  );
}

const MAP = {
  divider: ThumbDivider,
  "control-step": ThumbStep,
  "smib-swing": ThumbSwing,
  "dc-drive": ThumbMotorSpeed,
  "digital-stable": ThumbDigital,
  "signals-fft": ThumbSpectrum,
};

export function ExampleThumb({ id }) {
  const C = MAP[id] || ThumbStep;
  return <C />;
}
