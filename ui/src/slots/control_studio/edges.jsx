import { BaseEdge, EdgeLabelRenderer, getSmoothStepPath } from "@xyflow/react";

export function SignalEdge({ id, sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition, data, markerEnd }) {
  const [path, labelX, labelY] = getSmoothStepPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
    borderRadius: 8,
  });
  const label = data?.label || "";
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
  const [tb] = to.split(":");
  const src = blocksById[fb];
  const dst = blocksById[tb];
  if (dst?.type === "scope") return "y";
  if (src?.type === "step") return "r";
  if (fp === "feedback" || fp === "in2") return "fb";
  if (src?.type === "sum" && fp === "out") return "e";
  if (src?.type === "pid") return "u";
  return "";
}
