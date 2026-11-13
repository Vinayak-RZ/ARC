import { Position } from "@xyflow/react";
import { InPort, OutPort } from "./ports.jsx";

function badge(data) {
  if (!data?.flashAuthor) return null;
  return <span className={`studio-author-badge is-${data.flashAuthor}`}>{data.flashAuthor}</span>;
}

function errs(data) {
  const issues = data?.issues || [];
  if (!issues.length) return null;
  return (
    <ul className="studio-block-errors" role="alert">
      {issues.map((e) => (
        <li key={e.code}>{e.message}</li>
      ))}
    </ul>
  );
}

function pinNote(data) {
  const note = (data?.notes || []).find((n) => n.block_id === data.blockId);
  if (!note) return null;
  return <span className="studio-note-pin" title={note.text}>💬</span>;
}

function shell(cls, selected, data, children, ports) {
  return (
    <div
      className={`studio-block ${cls}${selected ? " is-selected" : ""}${data?.highlight ? " is-highlight" : ""}`}
      style={{ zIndex: 2 }}
    >
      {badge(data)}
      {pinNote(data)}
      {ports}
      <div className="studio-block-body">{children}</div>
      {errs(data)}
    </div>
  );
}

export function SumNode({ data, selected }) {
  const signs = String(data?.params?.signs || "+-");
  return shell(
    "studio-sum",
    selected,
    data,
    <span className="studio-sum-icon" aria-hidden>
      Σ
    </span>,
    <>
      <div className="studio-port-col studio-port-col-left">
        <InPort id="in1" sign="+" />
      </div>
      <div className="studio-port-col studio-port-col-bottom">
        <InPort id="feedback" sign={signs.includes("-") ? "−" : "+"} position={Position.Bottom} />
      </div>
      <OutPort id="out" />
    </>,
  );
}

export function GainNode({ data, selected }) {
  const k = data?.params?.k ?? data?.params?.gain ?? 1;
  return shell(
    "studio-gain",
    selected,
    data,
  <>
      <span className="studio-block-kind">Gain</span>
      <span className="studio-param-line">k = {k}</span>
  </>,
    <>
      <InPort id="in" />
      <OutPort id="out" />
    </>,
  );
}

function tfFrac(tf) {
  const raw = String(tf || "1/(s+1)");
  if (raw.includes("/")) {
    const [num, den] = raw.split("/");
    return { num: num.replace(/[()]/g, "").trim(), den: den.replace(/[()]/g, "").trim() };
  }
  return { num: raw, den: "1" };
}

export function TfNode({ data, selected }) {
  const { num, den } = tfFrac(data?.params?.tf);
  return shell(
    "studio-tf",
    selected,
    data,
    <div className="tf-frac">
      <span className="tf-num">{num}</span>
      <span className="tf-line" />
      <span className="tf-den">{den}</span>
    </div>,
    <>
      <InPort id="in" />
      <OutPort id="out" />
    </>,
  );
}

export function PidNode({ data, selected }) {
  const p = data?.params || {};
  return shell(
    "studio-pid",
    selected,
    data,
    <>
      <span className="studio-block-kind">PID</span>
      <span className="studio-param-line">Kp = {p.kp ?? 0}</span>
      <span className="studio-param-line">Ki = {p.ki ?? 0}</span>
      <span className="studio-param-line">Kd = {p.kd ?? 0}</span>
    </>,
    <>
      <InPort id="in" />
      <OutPort id="out" />
    </>,
  );
}

export function SourceNode({ data, selected }) {
  return shell(
    "studio-source",
    selected,
    data,
    <>
      <span className="studio-block-icon">▸</span>
      <span>{data?.label || data?.blockType}</span>
    </>,
    <OutPort id="out" />,
  );
}

export function ScopeNode({ data, selected }) {
  return shell(
    "studio-scope",
    selected,
    data,
    <>
      <span className="scope-glyph" aria-hidden>
        ◔
      </span>
      <span className="scope-title">Scope</span>
    </>,
    <InPort id="in" />,
  );
}

export function PlantNode({ data, selected }) {
  return shell(
    "studio-plant",
    selected,
    data,
    <>
      <span className="studio-block-icon">⚙</span>
      <span className="plant-label">{data?.label || data?.blockType}</span>
    </>,
    <>
      <InPort id="in" />
      <OutPort id="out" />
      <OutPort id="tap" tap />
    </>,
  );
}

export function GenericNode({ data, selected }) {
  return shell(
    "studio-generic",
    selected,
    data,
    <>
      <span>{data?.label || data?.blockType}</span>
      {data?.paramLine ? <span className="studio-param-line">{data.paramLine}</span> : null}
    </>,
    <>
      <InPort id="in" />
      <OutPort id="out" />
    </>,
  );
}

export function nodeForType(type) {
  if (type === "sum") return "sum";
  if (type === "gain") return "gain";
  if (type === "transfer_function") return "tf";
  if (type === "pid") return "pid";
  if (type === "step" || type === "ramp" || type === "sine") return "source";
  if (type === "scope") return "scope";
  if (type.startsWith("plant_")) return "plant";
  return "generic";
}

export const studioNodeTypes = {
  sum: SumNode,
  gain: GainNode,
  tf: TfNode,
  pid: PidNode,
  source: SourceNode,
  scope: ScopeNode,
  plant: PlantNode,
  generic: GenericNode,
};
