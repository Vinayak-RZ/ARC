import { Handle, Position } from "@xyflow/react";

export function InPort({ id, sign, position = Position.Left }) {
  return (
    <div className={`studio-port studio-port-in${position === Position.Bottom ? " is-bottom" : ""}`}>
      <Handle type="target" position={position} id={id} className="studio-port-handle target" isConnectableStart={false} />
      {sign ? <span className="studio-port-sign">{sign}</span> : null}
    </div>
  );
}

export function OutPort({ id, tap }) {
  const position = tap ? Position.Bottom : Position.Right;
  return (
    <div className={`studio-port studio-port-out${tap ? " is-tap" : ""}`}>
      <Handle type="source" position={position} id={id} className={`studio-port-handle source${tap ? " is-tap" : ""}`} />
    </div>
  );
}
