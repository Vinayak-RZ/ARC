import { useEffect, useMemo } from "react";
import {
  ReactFlow,
  ReactFlowProvider,
  Background,
  Handle,
  MarkerType,
  Position,
  useReactFlow,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

const EDGE_STYLE = { stroke: "var(--ee-color-ink)", strokeWidth: 1.5 };

function SumNode({ data }) {
  const neg = data?.negative !== false;
  return (
    <div className="control-sum" aria-label="Summing junction">
      <Handle type="target" position={Position.Left} id="in" />
      <Handle type="target" position={Position.Bottom} id="feedback" />
      <Handle type="source" position={Position.Right} id="out" />
      <span className="control-sum-glyph">Σ</span>
      {neg ? <span className="control-sum-sign">−</span> : null}
    </div>
  );
}

function BlockNode({ data }) {
  return (
    <div className="control-block">
      <Handle type="target" position={Position.Left} id="in" />
      <Handle type="source" position={Position.Right} id="out" />
      <span className="control-block-label">{data?.label || "G"}</span>
      <span className="control-block-tf">{data?.tf || ""}</span>
    </div>
  );
}

function EquipNode({ data }) {
  return (
    <div className="control-equip">
      <Handle type="target" position={Position.Left} id="in" />
      <Handle type="source" position={Position.Right} id="out" />
      <span className="control-block-label">{data?.label || ""}</span>
      <span className="control-block-tf">{data?.tf || ""}</span>
    </div>
  );
}

function TapNode({ data }) {
  return (
    <div className="control-tap">
      <Handle type="target" position={Position.Left} id="in" />
      <Handle type="source" position={Position.Right} id="out" />
      {data?.label || "y"}
    </div>
  );
}

function RefNode() {
  return (
    <div className="control-ref">
      <Handle type="source" position={Position.Right} id="out" />
      r
    </div>
  );
}

const nodeTypes = {
  sum: SumNode,
  block: BlockNode,
  equip: EquipNode,
  tap: TapNode,
  ref: RefNode,
};

function diagramCaption(diagram) {
  const nodes = diagram?.nodes || [];
  if (nodes.some((n) => n.type === "equip")) {
    return "One-line study diagram from this run (read-only).";
  }
  return "Closed-loop block diagram from this run (read-only).";
}

function toFlow(diagram) {
  const nodes = [];
  const edges = [];
  const rawNodes = diagram?.nodes || [];
  const rawEdges = diagram?.edges || [];
  const ids = new Set(rawNodes.map((n) => n.id));
  const hasEquip = rawNodes.some((n) => n.type === "equip");
  for (const n of rawNodes) {
    const type =
      n.type === "sum"
        ? "sum"
        : n.type === "block"
          ? "block"
          : n.type === "equip"
            ? "equip"
            : "tap";
    nodes.push({
      id: n.id,
      type,
      position: { x: Number(n.x) || 0, y: Number(n.y) || 0 },
      data: {
        label: n.label,
        tf: n.tf,
        negative: n.negative,
      },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
    });
  }
  if (!hasEquip) {
    if (!ids.has("r")) {
      nodes.push({ id: "r", type: "ref", position: { x: 0, y: 140 }, data: {} });
    }
    if (!ids.has("y")) {
      nodes.push({ id: "y", type: "tap", position: { x: 520, y: 140 }, data: { label: "y" } });
    }
  }
  for (const e of rawEdges) {
    edges.push({
      id: e.id,
      source: e.from,
      target: e.to,
      sourceHandle: e.fromPort || "out",
      targetHandle: e.toPort === "feedback" ? "feedback" : e.toPort === "in" ? "in" : undefined,
      label: e.label || "",
      type: "smoothstep",
      style: EDGE_STYLE,
      markerEnd: { type: MarkerType.ArrowClosed, width: 16, height: 16 },
    });
  }
  return { nodes, edges };
}

function FitViewOnLoad({ nodeCount }) {
  const { fitView } = useReactFlow();
  useEffect(() => {
    if (!nodeCount) return;
    const t = window.setTimeout(() => {
      fitView({ padding: 0.18, duration: 0 });
    }, 50);
    return () => window.clearTimeout(t);
  }, [fitView, nodeCount]);
  return null;
}

function ControlDiagramInner({ diagram }) {
  const { nodes, edges } = useMemo(() => toFlow(diagram || {}), [diagram]);
  const caption = diagramCaption(diagram);
  return (
    <div className="control-diagram-wrap">
      <p className="hint">{caption}</p>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        nodesDraggable={false}
        nodesConnectable={false}
        elementsSelectable={false}
        panOnDrag
        zoomOnScroll
        proOptions={{ hideAttribution: true }}
        style={{ width: "100%", height: 340 }}
      >
        <Background gap={16} color="var(--ee-color-hairline)" />
        <FitViewOnLoad nodeCount={nodes.length} />
      </ReactFlow>
    </div>
  );
}

export function ControlDiagram({ diagram }) {
  return (
    <ReactFlowProvider>
      <ControlDiagramInner diagram={diagram} />
    </ReactFlowProvider>
  );
}
