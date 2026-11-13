import { BaseEdge, EdgeLabelRenderer, getSmoothStepPath } from "@xyflow/react";

function feedbackPath(sourceX, sourceY, targetX, targetY) {
  const drop = 96;
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
    const lx = (sourceX + targetX) / 2;
    const ly = Math.max(sourceY, targetY) + 72;
    return (
      <>
        <BaseEdge id={id} path={path} markerEnd={markerEnd} style={{ stroke: "var(--ee-color-ink)", strokeWidth: 1.75 }} />
        {label ? (
          <EdgeLabelRenderer>
            <div
              className="studio-edge-label is-feedback"
              style={{ transform: `translate(-50%, -50%) translate(${lx}px,${ly}px)` }}
            >
              {label}
            </div>
          </EdgeLabelRenderer>
        ) : null}
      </>
    );
  }
  const [path, labelX, labelY] = getSmoothStepPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
    borderRadius: 12,
  });
  return (
    <>
      <BaseEdge id={id} path={path} markerEnd={markerEnd} style={{ stroke: "var(--ee-color-ink)", strokeWidth: 1.75 }} />
      {label ? (
        <EdgeLabelRenderer>
          <div className="studio-edge-label" style={{ transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)` }}>
            {label}
          </div>
        </EdgeLabelRenderer>
      ) : null}
    </>
  );
}

export const studioEdgeTypes = { signal: SignalEdge };

export function wireLabel(from, to, blocksById) {
  const [fb, fp] = from.split(":");
  const [, tp] = to.split(":");
  if (tp === "feedback" || fp === "feedback") return "fb";
  const src = blocksById[fb];
  if (src?.type === "step") return "r";
  return "";
}
