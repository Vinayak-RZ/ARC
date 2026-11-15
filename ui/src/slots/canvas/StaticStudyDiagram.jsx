/** Textbook-style study diagrams (control, power, protection, drives) as SVG. */

import { DiagramDefs, orthoPath, Wire } from "./diagram/orthoPaths.jsx";

function titleFor(diagram) {
  if (diagram?.title) return diagram.title;
  const kind = diagram?.diagramKind || "";
  if (kind === "unity_feedback") return "Unity feedback system";
  if (kind === "power_fault") return "LG fault study — single-line diagram (pu)";
  if (kind === "protection_5051") return "Feeder protection — CT, 50/51 relay, breaker";
  if (kind === "drives_dc") return "DC drive — armature circuit and load torque";
  if (kind === "smib_swing") return "SMIB — generator, transformer, line, infinite bus";
  if (kind === "digital_loop") return "Discrete loop — zero-order hold and G(z)";
  if (kind === "dispatch_ed") return "Economic dispatch — three units, one load";
  if (kind === "buck_ccm") return "Buck converter — switch, diode, L, C";
  if ((diagram?.nodes || []).some((n) => n.type === "equip")) {
    return "One-line study diagram (read-only)";
  }
  return "Closed-loop block diagram (read-only)";
}

function UnityFeedbackDiagram({ diagram }) {
  const nodes = diagram.nodes || [];
  const gNode = nodes.find((n) => n.type === "block" && n.id !== "H") || nodes.find((n) => n.type === "block");
  const hNode = nodes.find((n) => n.id === "H" || (n.type === "block" && n !== gNode));
  const gTf = gNode?.tf || "G(s)";
  const hTf = hNode?.tf || "1";
  const w = 680;
  const h = 300;
  const yMain = 118;
  const xR = 24;
  const xSum = 108;
  const xG = 200;
  const xC = 420;
  const xH = 200;
  const yH = 220;

  return (
    <svg className="static-diagram" viewBox={`0 0 ${w} ${h}`} width="100%" height="300" role="img">
      <DiagramDefs />
      <g style={{ color: "var(--ee-color-ink)" }}>
        <Wire d={orthoPath(xR + 48, yMain, xSum, yMain)} />
        <Wire d={orthoPath(xSum + 40, yMain, xG, yMain)} />
        <Wire d={orthoPath(xG + 100, yMain, xC, yMain)} />
        <Wire d={orthoPath(xC + 24, yMain + 20, xC + 24, yH)} />
        <Wire d={orthoPath(xC + 24, yH, xH + 100, yH)} />
        <Wire d={orthoPath(xH, yH, xH, yMain + 20)} />
        <Wire d={orthoPath(xH, yMain + 20, xSum + 20, yMain + 20)} />

        <text x={xR + 24} y={yMain - 34} textAnchor="middle" fontSize="13" fontWeight="500">R(s)</text>
        <circle cx={xSum + 20} cy={yMain} r="20" fill="var(--ee-color-canvas)" stroke="currentColor" strokeWidth="2" />
        <text x={xSum + 12} y={yMain - 4} fontSize="14" fontWeight="600">+</text>
        <text x={xSum + 26} y={yMain + 12} fontSize="14" fontWeight="600">−</text>

        <rect x={xG} y={yMain - 28} width="100" height="56" fill="var(--ee-color-canvas)" stroke="currentColor" strokeWidth="2" />
        <text x={xG + 50} y={yMain - 8} textAnchor="middle" fontSize="13" fontWeight="600">G(s)</text>
        <text x={xG + 50} y={yMain + 14} textAnchor="middle" fontSize="11">{gTf}</text>

        <text x={xC + 24} y={yMain - 34} textAnchor="middle" fontSize="13" fontWeight="500">C(s)</text>

        <rect x={xH} y={yH - 26} width="100" height="52" fill="var(--ee-color-canvas)" stroke="currentColor" strokeWidth="2" />
        <text x={xH + 50} y={yH - 6} textAnchor="middle" fontSize="13" fontWeight="600">H(s)</text>
        <text x={xH + 50} y={yH + 14} textAnchor="middle" fontSize="11">{hTf}</text>
      </g>
    </svg>
  );
}

function PowerFaultDiagram({ diagram }) {
  const seq = diagram.sequence || {};
  const z1 = seq.z1 ?? 0.1;
  const z2 = seq.z2 ?? 0.1;
  const z0 = seq.z0 ?? 0.3;
  const fault = seq.fault || "LG";
  const w = 680;
  const h = 300;
  const yBus = 100;
  const xGen = 56;
  const xLine = 360;
  const xLoad = 520;

  return (
    <svg className="static-diagram" viewBox={`0 0 ${w} ${h}`} width="100%" height="300" role="img">
      <DiagramDefs />
      <g style={{ color: "var(--ee-color-ink)" }}>
        <line x1={xGen + 40} y1={yBus} x2={xLoad + 60} y2={yBus} stroke="currentColor" strokeWidth="6" />
        <text x={xGen + 40} y={yBus - 12} fontSize="11">Bus 1</text>

        <circle cx={xGen} cy={yBus} r="28" fill="var(--ee-color-canvas)" stroke="currentColor" strokeWidth="2" />
        <text x={xGen} y={yBus + 5} textAnchor="middle" fontSize="14" fontWeight="600">G</text>
        <text x={xGen} y={yBus + 44} textAnchor="middle" fontSize="11">1.0 pu</text>
        <Wire d={orthoPath(xGen + 28, yBus, xGen + 40, yBus)} marker={false} />

        <g transform={`translate(${xLine - 40},${yBus - 20})`}>
          <line x1="0" y1="20" x2="80" y2="20" stroke="currentColor" strokeWidth="2" />
          <line x1="20" y1="0" x2="20" y2="40" stroke="currentColor" strokeWidth="2" />
          <line x1="60" y1="0" x2="60" y2="40" stroke="currentColor" strokeWidth="2" />
          <text x="40" y="58" textAnchor="middle" fontSize="10">Z1={z1} Z2={z2}</text>
        </g>

        <rect x={xLoad} y={yBus - 24} width="56" height="48" fill="var(--ee-color-canvas)" stroke="currentColor" strokeWidth="2" />
        <text x={xLoad + 28} y={yBus + 5} textAnchor="middle" fontSize="12">Load</text>
        <text x={xLoad + 28} y={yBus + 44} textAnchor="middle" fontSize="10">Z0={z0} pu</text>

        <g transform={`translate(${xLine},${yBus + 28})`}>
          <line x1="0" y1="0" x2="0" y2="36" stroke="currentColor" strokeWidth="2" markerEnd="url(#ee-arrow)" />
          <path d="M -10 36 L 10 36 L 0 52 Z" fill="currentColor" />
          <text x="0" y="68" textAnchor="middle" fontSize="11">{fault} fault</text>
        </g>

        <rect x={48} y={200} width={584} height={72} fill="var(--ee-color-surface-soft)" stroke="currentColor" strokeWidth="1" rx="4" />
        <text x={64} y={222} fontSize="11" fontWeight="600">LG sequence network (series)</text>
        <g transform="translate(120,238)">
          {["Z1", "Z2", "Z0"].map((label, i) => (
            <g key={label} transform={`translate(${i * 140},0)`}>
              <rect width="72" height="28" fill="var(--ee-color-canvas)" stroke="currentColor" strokeWidth="1.5" />
              <text x="36" y="19" textAnchor="middle" fontSize="11">
                {label}={label === "Z1" ? z1 : label === "Z2" ? z2 : z0}
              </text>
              {i < 2 ? <line x1="72" y1="14" x2="88" y2="14" stroke="currentColor" strokeWidth="2" markerEnd="url(#ee-arrow)" /> : null}
            </g>
          ))}
        </g>
      </g>
    </svg>
  );
}

function ProtectionDiagram({ diagram }) {
  const meta = diagram.meta || {};
  const ct = meta.ct_ratio || "300/5 A";
  const pickup = meta.pickup_sec || "2 A sec";
  const y = 110;
  const w = 680;
  const h = 280;
  const xs = [48, 168, 288, 408, 528];

  return (
    <svg className="static-diagram" viewBox={`0 0 ${w} ${h}`} width="100%" height="280" role="img">
      <DiagramDefs />
      <g style={{ color: "var(--ee-color-ink)" }}>
        <line x1={xs[0] + 20} y1={y} x2={xs[4] + 80} y2={y} stroke="currentColor" strokeWidth="4" />
        <text x={xs[0]} y={y - 16} fontSize="11" fontWeight="600">Bus</text>

        <g transform={`translate(${xs[1]},${y - 18})`}>
          <rect x="8" y="4" width="48" height="28" fill="none" stroke="currentColor" strokeWidth="2" />
          <circle cx="32" cy="18" r="14" fill="none" stroke="currentColor" strokeWidth="2" />
          <text x="32" y="52" textAnchor="middle" fontSize="10">CT {ct}</text>
        </g>

        <rect x={xs[2]} y={y - 22} width="72" height="44" fill="var(--ee-color-canvas)" stroke="currentColor" strokeWidth="2" />
        <text x={xs[2] + 36} y={y + 4} textAnchor="middle" fontSize="12" fontWeight="600">50/51</text>
        <text x={xs[2] + 36} y={y + 44} textAnchor="middle" fontSize="10">pickup {pickup}</text>

        <g transform={`translate(${xs[3]},${y - 20})`}>
          <rect width="40" height="40" fill="var(--ee-color-canvas)" stroke="currentColor" strokeWidth="2" />
          <line x1="20" y1="0" x2="20" y2="-24" stroke="currentColor" strokeWidth="2" />
          <text x="20" y="58" textAnchor="middle" fontSize="11">CB</text>
        </g>

        <text x={xs[4] + 40} y={y + 5} textAnchor="middle" fontSize="12">Feeder → fault</text>

        <path
          d={`M ${xs[1] + 56} ${y + 36} V ${y + 72} H ${xs[2] + 36} V ${y + 44}`}
          fill="none"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeDasharray="6 4"
          markerEnd="url(#ee-arrow)"
        />
        <text x={xs[2] + 36} y={y + 88} textAnchor="middle" fontSize="10">Secondary to relay / trip coil</text>
      </g>
    </svg>
  );
}

function DrivesDiagram({ diagram }) {
  const meta = diagram.meta || {};
  const va = meta.v_dc ?? 120;
  const ra = meta.ra_ohm ?? 1;
  const tLoad = meta.t_load ?? 5;
  const speed = meta.speed_rpm;
  const w = 640;
  const h = 260;
  const y = 120;

  return (
    <svg className="static-diagram" viewBox={`0 0 ${w} ${h}`} width="100%" height="260" role="img">
      <DiagramDefs />
      <g style={{ color: "var(--ee-color-ink)" }}>
        <Wire d={orthoPath(40, y, 120, y)} />
        <text x={52} y={y - 28} fontSize="12" fontWeight="600">V_a</text>
        <text x={52} y={y - 12} fontSize="11">{va} V</text>
        <line x1={40} y1={y - 16} x2={40} y2={y + 16} stroke="currentColor" strokeWidth="3" />
        <line x1={32} y1={y - 16} x2={48} y2={y - 16} stroke="currentColor" strokeWidth="2" />

        <Wire d={orthoPath(120, y, 200, y)} />
        <rect x={128} y={y - 22} width="64" height="44" fill="var(--ee-color-canvas)" stroke="currentColor" strokeWidth="2" />
        <text x={160} y={y - 4} textAnchor="middle" fontSize="11">R_a</text>
        <text x={160} y={y + 12} textAnchor="middle" fontSize="10">{ra} Ω</text>

        <Wire d={orthoPath(200, y, 280, y)} />
        <circle cx={320} cy={y} r="32" fill="var(--ee-color-canvas)" stroke="currentColor" strokeWidth="2" />
        <text x={320} y={y + 6} textAnchor="middle" fontSize="13" fontWeight="600">M</text>
        <text x={320} y={y + 48} textAnchor="middle" fontSize="10">DC motor</text>
        {speed != null ? (
          <text x={320} y={y + 62} textAnchor="middle" fontSize="10">ω ≈ {Number(speed).toFixed(0)} rpm</text>
        ) : null}

        <Wire d={orthoPath(352, y, 440, y)} />
        <rect x={448} y={y - 28} width="80" height="56" fill="var(--ee-color-canvas)" stroke="currentColor" strokeWidth="2" />
        <text x={488} y={y - 4} textAnchor="middle" fontSize="12">T_L</text>
        <text x={488} y={y + 14} textAnchor="middle" fontSize="11">{tLoad} N·m</text>
      </g>
    </svg>
  );
}

function SmibDiagram({ diagram }) {
  const meta = diagram.meta || {};
  const w = 680;
  const h = 240;
  const y = 100;
  return (
    <svg className="static-diagram" viewBox={`0 0 ${w} ${h}`} width="100%" height="240" role="img" aria-label="SMIB one-line">
      <g style={{ color: "var(--ee-color-ink)" }}>
        <line x1="80" y1={y} x2="600" y2={y} stroke="currentColor" strokeWidth="3" />
        <circle cx="70" cy={y} r="28" fill="var(--ee-color-canvas)" stroke="currentColor" strokeWidth="2" />
        <text x="70" y={y + 5} textAnchor="middle" fontSize="14" fontWeight="600">G</text>
        <text x="70" y={y + 48} textAnchor="middle" fontSize="11">H={meta.h ?? 5} s</text>
        <g transform="translate(210,78)">
          <circle cx="16" cy="22" r="16" fill="none" stroke="currentColor" strokeWidth="2" />
          <circle cx="34" cy="22" r="16" fill="none" stroke="currentColor" strokeWidth="2" />
          <text x="25" y="58" textAnchor="middle" fontSize="11">Transformer</text>
        </g>
        <g transform="translate(360,88)">
          <line x1="0" y1="4" x2="90" y2="4" stroke="currentColor" strokeWidth="2" />
          <line x1="0" y1="16" x2="90" y2="16" stroke="currentColor" strokeWidth="2" />
          <text x="45" y="40" textAnchor="middle" fontSize="11">Double circuit</text>
        </g>
        <g transform="translate(560,78)">
          <line x1="0" y1="0" x2="0" y2="44" stroke="currentColor" strokeWidth="3" />
          <line x1="8" y1="6" x2="8" y2="38" stroke="currentColor" strokeWidth="2" />
          <line x1="16" y1="12" x2="16" y2="32" stroke="currentColor" strokeWidth="2" />
          <text x="8" y="64" textAnchor="middle" fontSize="11">Infinite bus</text>
        </g>
        <text x="24" y="200" fontSize="12">
          Pm={meta.pm ?? "—"} pu · Pmax pre/fault/post {meta.pmax_pre ?? "—"} / {meta.pmax_fault ?? "—"} / {meta.pmax_post ?? "—"} pu
        </text>
      </g>
    </svg>
  );
}

function DigitalLoopDiagram({ diagram }) {
  const meta = diagram.meta || {};
  const w = 680;
  const h = 260;
  const y = 90;
  return (
    <svg className="static-diagram" viewBox={`0 0 ${w} ${h}`} width="100%" height="260" role="img" aria-label="Discrete control loop">
      <g style={{ color: "var(--ee-color-ink)" }}>
        <text x="36" y={y - 28} fontSize="13" fontWeight="500">R(z)</text>
        <line x1="70" y1={y} x2="120" y2={y} stroke="currentColor" strokeWidth="2" />
        <circle cx="148" cy={y} r="22" fill="var(--ee-color-canvas)" stroke="currentColor" strokeWidth="2" />
        <text x="140" y={y - 2} fontSize="14" fontWeight="600">+</text>
        <text x="156" y={y + 14} fontSize="14" fontWeight="600">−</text>
        <line x1="170" y1={y} x2="230" y2={y} stroke="currentColor" strokeWidth="2" />
        <rect x="230" y={y - 28} width="90" height="56" fill="var(--ee-color-canvas)" stroke="currentColor" strokeWidth="2" />
        <text x="275" y={y - 4} textAnchor="middle" fontSize="13" fontWeight="600">ZOH</text>
        <text x="275" y={y + 14} textAnchor="middle" fontSize="11">Ts={meta.ts ?? "—"} s</text>
        <line x1="320" y1={y} x2="390" y2={y} stroke="currentColor" strokeWidth="2" />
        <rect x="390" y={y - 28} width="140" height="56" fill="var(--ee-color-canvas)" stroke="currentColor" strokeWidth="2" />
        <text x="460" y={y - 4} textAnchor="middle" fontSize="13" fontWeight="600">G(z)</text>
        <text x="460" y={y + 16} textAnchor="middle" fontSize="10">{meta.gz || "H(z)"}</text>
        <line x1="530" y1={y} x2="620" y2={y} stroke="currentColor" strokeWidth="2" />
        <text x="620" y={y - 16} textAnchor="end" fontSize="13" fontWeight="500">C(z)</text>
        <path d="M 600 90 V 190 H 148 V 112" fill="none" stroke="currentColor" strokeWidth="1.5" />
        <text x="360" y="206" textAnchor="middle" fontSize="12">feedback 1</text>
      </g>
    </svg>
  );
}

function DispatchDiagram({ diagram }) {
  const pd = diagram.meta?.pd_mw ?? 500;
  const w = 640;
  const h = 260;
  return (
    <svg className="static-diagram" viewBox={`0 0 ${w} ${h}`} width="100%" height="260" role="img" aria-label="Economic dispatch one-line">
      <g style={{ color: "var(--ee-color-ink)" }}>
        {[0, 1, 2].map((i) => (
          <g key={i} transform={`translate(48, ${36 + i * 72})`}>
            <circle cx="24" cy="24" r="22" fill="var(--ee-color-canvas)" stroke="currentColor" strokeWidth="2" />
            <text x="24" y="29" textAnchor="middle" fontSize="13" fontWeight="600">G{i + 1}</text>
            <line x1="46" y1="24" x2="280" y2="24" stroke="currentColor" strokeWidth="2" />
          </g>
        ))}
        <line x1="280" y1="40" x2="280" y2="200" stroke="currentColor" strokeWidth="4" />
        <text x="292" y="36" fontSize="12" fontWeight="600">Bus</text>
        <rect x="400" y="96" width="160" height="56" fill="var(--ee-color-canvas)" stroke="currentColor" strokeWidth="2" />
        <text x="480" y="118" textAnchor="middle" fontSize="13" fontWeight="600">Load</text>
        <text x="480" y="138" textAnchor="middle" fontSize="12">Pd = {pd} MW</text>
        <line x1="280" y1="124" x2="400" y2="124" stroke="currentColor" strokeWidth="2" />
      </g>
    </svg>
  );
}

function BuckDiagram({ diagram }) {
  const meta = diagram.meta || {};
  const w = 680;
  const h = 240;
  const y = 80;
  return (
    <svg className="static-diagram" viewBox={`0 0 ${w} ${h}`} width="100%" height="240" role="img" aria-label="Buck converter">
      <g style={{ color: "var(--ee-color-ink)" }}>
        <line x1="40" y1={y} x2="560" y2={y} stroke="currentColor" strokeWidth="2" />
        <line x1="40" y1={y} x2="40" y2="180" stroke="currentColor" strokeWidth="2" />
        <line x1="40" y1="180" x2="560" y2="180" stroke="currentColor" strokeWidth="2" />
        <line x1="560" y1={y} x2="560" y2="180" stroke="currentColor" strokeWidth="2" />
        <text x="48" y={y - 16} fontSize="13" fontWeight="600">Vin {meta.vin ?? "—"} V</text>
        <g transform="translate(150,62)">
          <line x1="0" y1="18" x2="28" y2="0" stroke="currentColor" strokeWidth="2" />
          <line x1="28" y1="0" x2="28" y2="36" stroke="currentColor" strokeWidth="2" />
          <text x="14" y="56" textAnchor="middle" fontSize="11">S · {meta.fs_khz ?? "—"} kHz</text>
        </g>
        <g transform="translate(250,150)">
          <polygon points="16,0 32,28 0,28" fill="none" stroke="currentColor" strokeWidth="2" />
          <line x1="4" y1="32" x2="28" y2="4" stroke="currentColor" strokeWidth="2" />
          <text x="16" y="52" textAnchor="middle" fontSize="11">D</text>
        </g>
        <g transform="translate(340,68)">
          <path d="M0 12 h8 q10 -16 20 0 q10 16 20 0 h8" fill="none" stroke="currentColor" strokeWidth="2" />
          <text x="28" y="40" textAnchor="middle" fontSize="11">L {meta.l_uh ?? "—"} µH</text>
        </g>
        <g transform="translate(470,96)">
          <line x1="20" y1="0" x2="20" y2="16" stroke="currentColor" strokeWidth="2" />
          <line x1="8" y1="16" x2="32" y2="16" stroke="currentColor" strokeWidth="2" />
          <line x1="8" y1="28" x2="32" y2="28" stroke="currentColor" strokeWidth="2" />
          <line x1="20" y1="28" x2="20" y2="44" stroke="currentColor" strokeWidth="2" />
          <text x="20" y="64" textAnchor="middle" fontSize="11">C</text>
        </g>
        <text x="500" y={y - 16} fontSize="13" fontWeight="600">Vout {meta.vout ?? "—"} V</text>
      </g>
    </svg>
  );
}

export function StaticStudyDiagram({ diagram }) {
  const kind = diagram?.diagramKind || "";
  const title = titleFor(diagram);

  let body;
  if (kind === "unity_feedback") body = <UnityFeedbackDiagram diagram={diagram} />;
  else if (kind === "power_fault") body = <PowerFaultDiagram diagram={diagram} />;
  else if (kind === "protection_5051") body = <ProtectionDiagram diagram={diagram} />;
  else if (kind === "drives_dc") body = <DrivesDiagram diagram={diagram} />;
  else if (kind === "smib_swing") body = <SmibDiagram diagram={diagram} />;
  else if (kind === "digital_loop") body = <DigitalLoopDiagram diagram={diagram} />;
  else if (kind === "dispatch_ed") body = <DispatchDiagram diagram={diagram} />;
  else if (kind === "buck_ccm") body = <BuckDiagram diagram={diagram} />;
  else body = <UnityFeedbackDiagram diagram={diagram} />;

  return (
    <div className="static-diagram-wrap">
      <p className="hint">{title}</p>
      {body}
    </div>
  );
}
