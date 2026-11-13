const FRAME = { w: 160, h: 100 };

function Frame({ children }) {
  return (
    <svg className="example-thumb-svg" viewBox={`0 0 ${FRAME.w} ${FRAME.h}`} role="img" aria-hidden>
      <rect x={0} y={0} width={FRAME.w} height={FRAME.h} className="example-thumb-bg" rx={4} />
      <rect x={4} y={4} width={FRAME.w - 8} height={FRAME.h - 8} className="example-thumb-well" rx={3} fill="none" />
      {children}
    </svg>
  );
}

function ThumbDivider() {
  return (
    <Frame>
      <text x={14} y={22} className="example-thumb-label">
        Vin
      </text>
      <line x1={28} y1={50} x2={52} y2={50} className="example-thumb-accent" strokeWidth={1.5} />
      <polyline
        points="40,44 44,56 36,56 40,44"
        className="example-thumb-accent"
        fill="none"
        strokeWidth={1.5}
      />
      <line x1={52} y1={50} x2={88} y2={50} className="example-thumb-accent" strokeWidth={1.5} />
      <polyline
        points="70,44 74,56 66,56 70,44"
        className="example-thumb-accent"
        fill="none"
        strokeWidth={1.5}
      />
      <line x1={88} y1={50} x2={112} y2={50} className="example-thumb-accent" strokeWidth={1.5} />
      <circle cx={70} cy={50} r={3.5} className="example-thumb-accent" fill="currentColor" />
      <text x={118} y={56} className="example-thumb-label">
        Vout
      </text>
      <line x1={112} y1={78} x2={112} y2={86} className="example-thumb-muted" strokeWidth={1} />
      <line x1={104} y1={86} x2={120} y2={86} className="example-thumb-muted" strokeWidth={1} />
    </Frame>
  );
}

function ThumbStep() {
  const pts = Array.from({ length: 16 }, (_, i) => {
    const t = i / 15;
    const x = 24 + t * 112;
    const y = 78 - (1 - Math.exp(-t * 3.2)) * 50;
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(" ");
  return (
    <Frame>
      <line x1={20} y1={78} x2={140} y2={78} className="example-thumb-muted" strokeWidth={1} />
      <line x1={20} y1={78} x2={20} y2={28} className="example-thumb-muted" strokeWidth={1} />
      <line x1={20} y1={34} x2={140} y2={34} className="example-thumb-accent" strokeWidth={1} strokeDasharray="4 3" />
      <polyline points={pts} fill="none" className="example-thumb-accent" strokeWidth={1.5} />
    </Frame>
  );
}

function ThumbSwing() {
  return (
    <Frame>
      <line x1={24} y1={72} x2={136} y2={72} className="example-thumb-muted" strokeWidth={1} />
      <path d="M 28 72 Q 52 30 80 48 T 132 38" fill="none" className="example-thumb-accent" strokeWidth={1.5} />
      <path d="M 28 72 Q 52 72 80 54 T 132 70" fill="var(--accent-50, rgba(47,111,235,0.12))" stroke="none" />
      <line x1={108} y1={34} x2={108} y2={72} className="example-thumb-accent" strokeWidth={1} strokeDasharray="3 2" />
    </Frame>
  );
}

function ThumbMotorSpeed() {
  const pts = Array.from({ length: 14 }, (_, i) => {
    const t = i / 13;
    const x = 24 + t * 110;
    const y = 78 - (1 - Math.exp(-t * 2.5)) * 48;
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(" ");
  return (
    <Frame>
      <line x1={22} y1={78} x2={138} y2={78} className="example-thumb-muted" strokeWidth={1} />
      <line x1={22} y1={78} x2={22} y2={30} className="example-thumb-muted" strokeWidth={1} />
      <line x1={22} y1={36} x2={138} y2={36} className="example-thumb-muted" strokeWidth={1} strokeDasharray="4 3" />
      <polyline points={pts} fill="none" className="example-thumb-accent" strokeWidth={1.5} />
    </Frame>
  );
}

function ThumbDigital() {
  return (
    <Frame>
      <line x1={80} y1={22} x2={80} y2={78} className="example-thumb-muted" strokeWidth={1} />
      <line x1={48} y1={50} x2={112} y2={50} className="example-thumb-muted" strokeWidth={1} />
      <circle cx={80} cy={50} r={30} fill="none" className="example-thumb-muted" strokeWidth={1} />
      <text x={92} y={42} className="example-thumb-accent" fontSize={11}>
        ×
      </text>
      <text x={66} y={58} className="example-thumb-accent" fontSize={11}>
        ×
      </text>
    </Frame>
  );
}

function ThumbSpectrum() {
  const heights = [8, 22, 38, 52, 40, 26, 14];
  return (
    <Frame>
      <line x1={20} y1={78} x2={140} y2={78} className="example-thumb-muted" strokeWidth={1} />
      {heights.map((h, i) => (
        <line
          key={i}
          x1={28 + i * 16}
          x2={28 + i * 16}
          y1={78}
          y2={78 - h}
          className="example-thumb-accent"
          strokeWidth={2}
        />
      ))}
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
