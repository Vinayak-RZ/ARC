import { useCallback, useEffect, useRef, useState } from "react";
import {
  ReactFlow,
  ReactFlowProvider,
  Background,
  ConnectionLineType,
  ConnectionMode,
  addEdge,
  useEdgesState,
  useNodesState,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { Palette } from "../slots/canvas/Palette.jsx";
import {
  fromFlow,
  MAX_EDGES,
  MAX_NODES,
  nextEdgeId,
  nextPartId,
  nextRefdes,
  PARTS,
  toFlow,
} from "../slots/canvas/graph.js";
import { nodeTypes } from "../slots/canvas/nodes.jsx";

const EDGE_STYLE = { stroke: "var(--ee-color-ink)", strokeWidth: 1.5 };
const GRID = 16;
const STORAGE_KEY = "arc-circuit-sandbox-v1";

const DIVIDER_SEED = {
  schema: "arc.circuit.v1",
  nodes: [
    { id: "vin", type: "source_v", refdes: "V1", value: 10, unit: "V", x: 40, y: 80, rot: 0 },
    { id: "r1", type: "resistor", refdes: "R1", value: 1000, unit: "ohm", x: 200, y: 40, rot: 0 },
    { id: "r2", type: "resistor", refdes: "R2", value: 1000, unit: "ohm", x: 200, y: 160, rot: 90 },
    { id: "gnd", type: "ground", refdes: "Gnd1", value: 0, unit: "", x: 40, y: 200, rot: 0 },
  ],
  edges: [
    { id: "e1", from: "vin.n1", to: "r1.n1" },
    { id: "e2", from: "r1.n2", to: "r2.n1" },
    { id: "e3", from: "r2.n2", to: "gnd.n1" },
    { id: "e4", from: "vin.n2", to: "gnd.n1" },
  ],
};

function readStoredGraph() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function CircuitSandboxInner() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [msg, setMsg] = useState("");
  const past = useRef([]);
  const future = useRef([]);
  const hydrated = useRef(false);

  useEffect(() => {
    if (hydrated.current) return;
    const graph = readStoredGraph() || DIVIDER_SEED;
    const { nodes: n, edges: e } = toFlow(graph);
    setNodes(n);
    setEdges(e);
    hydrated.current = true;
  }, [setEdges, setNodes]);

  const snapshot = useCallback(() => {
    past.current = [...past.current, { nodes, edges }].slice(-40);
    future.current = [];
  }, [nodes, edges]);

  const persist = useCallback(
    (ns, es) => {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(fromFlow(ns, es)));
      } catch {
        /* ignore */
      }
    },
    [],
  );

  useEffect(() => {
    if (!hydrated.current) return;
    const t = window.setTimeout(() => persist(nodes, edges), 400);
    return () => window.clearTimeout(t);
  }, [nodes, edges, persist]);

  const onConnect = useCallback(
    (conn) => {
      if (edges.length >= MAX_EDGES) {
        setMsg("16 parts or 24 wires is the cap for this lab.");
        return;
      }
      snapshot();
      setEdges((eds) =>
        addEdge({ ...conn, id: nextEdgeId(eds), type: "step", style: EDGE_STYLE }, eds),
      );
      setMsg("");
    },
    [edges.length, setEdges, snapshot],
  );

  function addPart(type) {
    if (nodes.length >= MAX_NODES) {
      setMsg("16 parts or 24 wires is the cap for this lab.");
      return;
    }
    const spec = PARTS.find((p) => p.type === type);
    snapshot();
    const node = {
      id: nextPartId(nodes, type),
      type: "part",
      position: { x: 80 + (nodes.length % 6) * 72, y: 48 + Math.floor(nodes.length / 6) * 72 },
      data: {
        kind: type,
        refdes: nextRefdes(nodes, type),
        value: type === "ground" ? 0 : type === "source_v" ? 10 : type === "source_i" ? 0.001 : 1000,
        unit: spec?.unit || "",
        rot: 0,
      },
    };
    setNodes((ns) => [...ns, node]);
    setMsg("");
  }

  function loadDivider() {
    snapshot();
    const { nodes: n, edges: e } = toFlow(DIVIDER_SEED);
    setNodes(n);
    setEdges(e);
    setMsg("");
  }

  function clearCanvas() {
    snapshot();
    setNodes([]);
    setEdges([]);
    setMsg("");
  }

  return (
    <div className="lab-surface lab-surface-circuit">
      <div className="canvas-lab studio-circuit-sandbox">
        <Palette onAdd={addPart} />
        <div className="flow-wrap">
          <p className="canvas-wire-hint">
            Drag a port onto another port to connect. Click a wire, then Delete, to remove it.
          </p>
          {msg ? <p className="hint">{msg}</p> : null}
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            nodeTypes={nodeTypes}
            defaultEdgeOptions={{ type: "step", style: EDGE_STYLE, interactionWidth: 22 }}
            connectionLineType={ConnectionLineType.Step}
            connectionLineStyle={EDGE_STYLE}
            connectionMode={ConnectionMode.Loose}
            connectionRadius={28}
            snapToGrid
            snapGrid={[GRID, GRID]}
            deleteKeyCode={["Backspace", "Delete"]}
            edgesFocusable
            elementsSelectable
            fitView
            minZoom={0.4}
            maxZoom={1.6}
            proOptions={{ hideAttribution: true }}
          >
            <Background gap={16} color="var(--ee-color-hairline)" />
          </ReactFlow>
        </div>
        <div className="confirm-row">
          <button type="button" className="button-secondary" onClick={loadDivider}>
            Load divider example
          </button>
          <button type="button" className="button-secondary" onClick={clearCanvas}>
            Clear canvas
          </button>
        </div>
      </div>
    </div>
  );
}

export function CircuitSandbox() {
  return (
    <ReactFlowProvider>
      <CircuitSandboxInner />
    </ReactFlowProvider>
  );
}