import { Handle, Position } from "@xyflow/react";

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

export function SumNode({ data, selected }) {
  const signs = String(data?.params?.signs || "+-");
  return (
    <div className={`studio-node studio-sum${selected ? " is-selected" : ""}${data?.highlight ? " is-highlight" : ""}`}>
      {badge(data)}
      {pinNote(data)}
      <Handle type="target" position={Position.Left} id="in1" style={{ top: "32%" }} />
      <Handle type="target" position={Position.Left} id="feedback" style={{ top: "68%" }} />
      <Handle type="source" position={Position.Right} id="out" />
      <span className="studio-sum-glyphs">
        <span className="sign-plus">+</span>
        <span className="sign-minus">{signs.includes("-") ? "−" : "+"}</span>
      </span>
      {errs(data)}
    </div>
  );
}

export function GainNode({ data, selected }) {
  const k = data?.params?.k ?? data?.params?.gain ?? 1;
  return (
    <div className={`studio-node studio-gain${selected ? " is-selected" : ""}${data?.highlight ? " is-highlight" : ""}`}>
      {badge(data)}
      {pinNote(data)}
      <Handle type="target" position={Position.Left} id="in" />
      <Handle type="source" position={Position.Right} id="out" />
      <span className="gain-k">{k}</span>
      {errs(data)}
    </div>
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
  return (
    <div className={`studio-node studio-tf${selected ? " is-selected" : ""}${data?.highlight ? " is-highlight" : ""}`}>
      {badge(data)}
      {pinNote(data)}
      <Handle type="target" position={Position.Left} id="in" />
      <Handle type="source" position={Position.Right} id="out" />
      <div className="tf-frac">
        <span className="tf-num">{num}</span>
        <span className="tf-line" />
        <span className="tf-den">{den}</span>
      </div>
      {errs(data)}
    </div>
  );
}

export function PidNode({ data, selected }) {
  const p = data?.params || {};
  return (
    <div className={`studio-node studio-pid${selected ? " is-selected" : ""}${data?.highlight ? " is-highlight" : ""}`}>
      {badge(data)}
      {pinNote(data)}
      <Handle type="target" position={Position.Left} id="in" />
      <Handle type="source" position={Position.Right} id="out" />
      <span className="pid-label">PID</span>
      <span className="pid-tune">
        Kp={p.kp ?? 0} Ki={p.ki ?? 0}
      </span>
      {errs(data)}
    </div>
  );
}

export function SourceNode({ data, selected }) {
  return (
    <div className={`studio-node studio-source${selected ? " is-selected" : ""}${data?.highlight ? " is-highlight" : ""}`}>
      {badge(data)}
      <Handle type="source" position={Position.Right} id="out" />
      <span>{data?.label || data?.blockType}</span>
      {errs(data)}
    </div>
  );
}

export function ScopeNode({ data, selected }) {
  return (
    <div className={`studio-node studio-scope${selected ? " is-selected" : ""}${data?.highlight ? " is-highlight" : ""}`}>
      {pinNote(data)}
      <Handle type="target" position={Position.Left} id="in" />
      <span className="scope-glyph">◔</span>
      <span>y(t)</span>
      {errs(data)}
    </div>
  );
}

export function PlantNode({ data, selected }) {
  return (
    <div className={`studio-node studio-plant${selected ? " is-selected" : ""}${data?.highlight ? " is-highlight" : ""}`}>
      {badge(data)}
      {pinNote(data)}
      <Handle type="target" position={Position.Left} id="in" />
      <Handle type="source" position={Position.Right} id="out" />
      <span className="plant-label">{data?.label || data?.blockType}</span>
      {errs(data)}
    </div>
  );
}

export function GenericNode({ data, selected }) {
  return (
    <div className={`studio-node studio-generic${selected ? " is-selected" : ""}${data?.highlight ? " is-highlight" : ""}`}>
      {badge(data)}
      {pinNote(data)}
      <Handle type="target" position={Position.Left} id="in" />
      <Handle type="source" position={Position.Right} id="out" />
      <span>{data?.label || data?.blockType}</span>
      {data?.paramLine ? <span className="studio-param-line">{data.paramLine}</span> : null}
      {errs(data)}
    </div>
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
