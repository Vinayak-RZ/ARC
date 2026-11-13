import { BaseEdge, EdgeLabelRenderer } from "@xyflow/react";

function feedbackPath(sourceX, sourceY, targetX, targetY) {
  const drop = 72;
  const midY = Math.max(sourceY, targetY) + drop;
  return `M ${sourceX} ${sourceY} V ${midY} H ${targetX} V ${targetY}`;
}

export function SignalEdge({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  targetHandleId,
  data,
  markerEnd,
}) {
  const below = data?.route === "below" || targetHandleId === "feedback";
  const label = data?.label || "";
  if (below) {
    const path = feedbackPath(sourceX, sourceY, targetX, targetY);
    return (
      <>
        <circle
          cx={sourceX}
          cy={sourceY}
          r={4.5}
          fill="var(--cs-copper)"
          stroke="var(--cs-surface)"
          strokeWidth={1.5}
        />
        <BaseEdge
          id={id}
          path={path}
          markerEnd={markerEnd}
          style={{ stroke: "var(--cs-text)", strokeWidth: 2, zIndex: 0 }}
        />
      </>
    );
  }
  const railY = sourceY;
  const path = `M ${sourceX} ${railY} L ${targetX} ${railY}`;
  const labelX = (sourceX + targetX) / 2;
  const labelY = railY;
  return (
    <>
      <BaseEdge id={id} path={path} markerEnd={markerEnd} style={{ stroke: "var(--cs-text)", strokeWidth: 2, zIndex: 0 }} />
      {label ? (
        <EdgeLabelRenderer>
          <span
            className="studio-edge-signal"
            style={{
              transform: `translate(-50%, calc(-100% - 10px)) translate(${labelX}px,${labelY}px)`,
            }}
          >
            {label}
          </span>
        </EdgeLabelRenderer>
      ) : null}
    </>
  );
}

export const studioEdgeTypes = { signal: SignalEdge };

export function wireLabel(from, to, blocksById) {
  const [tb, tp] = to.split(":");
  if (tp === "feedback") return "";
  const [fb] = from.split(":");
  const src = blocksById[fb];
  const tgt = blocksById[tb];
  if (src?.type === "step") return "r";
  if (src?.type === "sum" && tgt?.type === "pid") return "e";
  if (src?.type === "pid") return "u";
  if (src?.type?.startsWith("plant") && tgt?.type === "scope") return "y";
  return "";
}
