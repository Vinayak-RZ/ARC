import { useCallback, useEffect, useRef, useState } from "react";
import {
  ReactFlow,
  Background,
  ConnectionMode,
  addEdge,
  useEdgesState,
  useNodesState,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { useLayout } from "../../store.js";
import { Palette } from "./Palette.jsx";
import { fromFlow, MAX_EDGES, MAX_NODES, nextEdgeId, nextPartId, nextRefdes, PARTS, toFlow } from "./graph.js";
import { nodeTypes } from "./nodes.jsx";

function useRunGraph(id) {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetch(`/api/runs/${id}`)
      .then((r) => (r.ok ? r.json() : Promise.reject()))
      .then(setData)
      .catch(() => setData(null));
  }, [id]);
  return data;
}

export function Canvas({ id }) {
  const data = useRunGraph(id);
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [msg, setMsg] = useState("");
  const past = useRef([]);
  const future = useRef([]);
  const graphDirty = useLayout((s) => s.graphDirty);
  const setGraphDirty = useLayout((s) => s.setGraphDirty);
  const setSelectedNodeId = useLayout((s) => s.setSelectedNodeId);
  const setFlow = useLayout((s) => s.setFlow);
  const setCapMessage = useLayout((s) => s.setCapMessage);
  const capMessage = useLayout((s) => s.capMessage);
  const inspectorEpoch = useLayout((s) => s.inspectorEpoch);
  const loaded = useRef("");

  useEffect(() => {
    loaded.current = "";
  }, [id]);

  useEffect(() => {
    if (!data || loaded.current === id) return;
    const { nodes: n, edges: e } = toFlow(data.graph || {});
    setNodes(n);
    setEdges(e);
    setFlow(n, e);
    setGraphDirty(false);
    loaded.current = id;
  }, [data, id, setEdges, setFlow, setGraphDirty, setNodes]);

  useEffect(() => {
    if (!inspectorEpoch) return;
    setNodes(useLayout.getState().flowNodes);
  }, [inspectorEpoch, setNodes]);

  useEffect(() => {
    setFlow(nodes, edges);
  }, [nodes, edges, setFlow]);

  const snapshot = useCallback(() => {
    past.current = [...past.current, { nodes, edges }].slice(-40);
    future.current = [];
  }, [nodes, edges]);

  const undo = useCallback(() => {
    const prev = past.current.at(-1);
    if (!prev) return;
    future.current = [{ nodes, edges }, ...future.current];
    past.current = past.current.slice(0, -1);
    setNodes(prev.nodes);
    setEdges(prev.edges);
    setGraphDirty(true);
  }, [edges, nodes, setEdges, setGraphDirty, setNodes]);

  const redo = useCallback(() => {
    const next = future.current[0];
    if (!next) return;
    past.current = [...past.current, { nodes, edges }];
    future.current = future.current.slice(1);
    setNodes(next.nodes);
    setEdges(next.edges);
    setGraphDirty(true);
  }, [edges, nodes, setEdges, setGraphDirty, setNodes]);

  useEffect(() => {
    function onKey(ev) {
      const tag = ev.target && ev.target.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA") return;
      if ((ev.ctrlKey || ev.metaKey) && ev.key.toLowerCase() === "z") {
        ev.preventDefault();
        if (ev.shiftKey) redo();
        else undo();
      }
      if ((ev.ctrlKey || ev.metaKey) && ev.key.toLowerCase() === "y") {
        ev.preventDefault();
        redo();
      }
      if (ev.key === "Escape") setSelectedNodeId(null);
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [redo, setSelectedNodeId, undo]);

  const onConnect = useCallback(
    (conn) => {
      if (edges.length >= MAX_EDGES) {
        setCapMessage("16 parts or 24 wires is the cap for this lab.");
        return;
      }
      snapshot();
      setEdges((eds) => addEdge({ ...conn, id: nextEdgeId(eds) }, eds));
      setGraphDirty(true);
    },
    [edges.length, setCapMessage, setEdges, setGraphDirty, snapshot],
  );

  function addPart(type) {
    if (nodes.length >= MAX_NODES) {
      setCapMessage("16 parts or 24 wires is the cap for this lab.");
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
        value: type === "ground" ? 0 : type === "source_v" ? 10 : 1000,
        unit: spec?.unit || "",
      },
    };
    setNodes((ns) => [...ns, node]);
    setSelectedNodeId(node.id);
    setGraphDirty(true);
    setCapMessage("");
  }

  async function saveGraph() {
    const graph = fromFlow(nodes, edges);
    try {
      const r = await fetch(`/api/runs/${id}/graph`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(graph),
      });
      if (!r.ok) throw new Error("save");
      setGraphDirty(false);
      setMsg("");
    } catch {
      setMsg("Could not write graph.json. Check the run folder is writable.");
    }
  }

  async function confirm() {
    const graph = fromFlow(nodes, edges);
    try {
      const r = await fetch(`/api/runs/${id}/confirm`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ graph, simulate: false }),
      });
      const body = await r.json();
      setGraphDirty(false);
      setMsg(JSON.stringify(body));
    } catch {
      setMsg("Could not write graph.json. Check the run folder is writable.");
    }
  }

  const empty = nodes.length === 0;

  return (
    <div className="canvas-lab">
      <Palette onAdd={addPart} />
      <div className="flow-wrap">
        {data?.state === "waiting-human" ? <p className="hint">Waiting for topology confirm</p> : null}
        {empty ? (
          <p className="hint canvas-hint">
            Place parts from the palette. Confirm writes topology. It does not simulate.
          </p>
        ) : null}
        {capMessage ? <p className="hint">{capMessage}</p> : null}
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={(c) => {
            onNodesChange(c);
            setGraphDirty(true);
          }}
          onEdgesChange={(c) => {
            onEdgesChange(c);
            setGraphDirty(true);
          }}
          onConnect={onConnect}
          onNodeClick={(_, node) => setSelectedNodeId(node.id)}
          onPaneClick={() => setSelectedNodeId(null)}
          nodeTypes={nodeTypes}
          connectionMode={ConnectionMode.Loose}
          deleteKeyCode={["Backspace", "Delete"]}
          fitView
        >
          <Background gap={16} color="var(--ee-color-hairline)" />
        </ReactFlow>
      </div>
      <div className="confirm-row">
        <button className="button-secondary" type="button" onClick={saveGraph}>
          Save graph
        </button>
        <button className="button-primary" type="button" aria-label="Confirm topology" onClick={confirm} disabled={!graphDirty && data?.state !== "waiting-human"}>
          Confirm topology
        </button>
      </div>
      {msg ? <pre className="number-display">{msg}</pre> : null}
    </div>
  );
}
