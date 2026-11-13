import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  ReactFlow,
  ReactFlowProvider,
  Background,
  Handle,
  MarkerType,
  Position,
  addEdge,
  useEdgesState,
  useNodesState,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

const GRID = 16;
const EDGE_STYLE = { stroke: "var(--ee-color-ink)", strokeWidth: 1.5 };

function portHandles(type) {
  if (type === "step" || type === "ramp" || type === "sine") return { src: ["out"], dst: [] };
  if (type === "scope") return { src: [], dst: ["in"] };
  if (type === "sum") return { src: ["out"], dst: ["in1", "feedback"] };
  return { src: ["out"], dst: ["in"] };
}

function BlockNode({ data, selected }) {
  const handles = portHandles(data.blockType);
  return (
    <div className={`studio-block${selected ? " is-selected" : ""}`}>
      {handles.dst.map((p) => (
        <Handle key={p} type="target" position={Position.Left} id={p} style={{ top: p === "feedback" ? "70%" : "35%" }} />
      ))}
      {handles.src.map((p) => (
        <Handle key={p} type="source" position={Position.Right} id={p} />
      ))}
      <span className="studio-block-type">{data.label || data.blockType}</span>
      <span className="studio-block-id">{data.blockId}</span>
      {data.paramLine ? <span className="studio-block-params">{data.paramLine}</span> : null}
    </div>
  );
}

const nodeTypes = { studio: BlockNode };

function paramLine(params) {
  if (!params || typeof params !== "object") return "";
  const keys = ["tf", "k", "kp", "ki", "kd", "k", "tau"];
  for (const k of keys) {
    if (params[k] != null) return `${k}=${params[k]}`;
  }
  return "";
}

function diagramToFlow(diagram) {
  const nodes = (diagram?.blocks || []).map((b) => ({
    id: b.id,
    type: "studio",
    position: { x: b.x || 0, y: b.y || 0 },
    data: {
      blockId: b.id,
      blockType: b.type,
      label: b.label || b.type,
      params: b.params || {},
      paramLine: paramLine(b.params),
    },
  }));
  const edges = (diagram?.wires || []).map((w) => {
    const [fb, fp] = w.from.split(":");
    const [tb, tp] = w.to.split(":");
    return {
      id: w.id,
      source: fb,
      target: tb,
      sourceHandle: fp,
      targetHandle: tp,
      markerEnd: { type: MarkerType.ArrowClosed, color: "var(--ee-color-ink)" },
      style: EDGE_STYLE,
    };
  });
  return { nodes, edges };
}

function flowToDiagram(nodes, edges, base) {
  const blocks = nodes.map((n) => ({
    id: n.id,
    type: n.data?.blockType || "gain",
    label: n.data?.label,
    x: n.position.x,
    y: n.position.y,
    params: n.data?.params || {},
  }));
  const wires = edges.map((e) => ({
    id: e.id,
    from: `${e.source}:${e.sourceHandle || "out"}`,
    to: `${e.target}:${e.targetHandle || "in"}`,
  }));
  return {
    schema: "arc.control_studio.v1",
    id: base?.id || "diagram",
    title: base?.title || "Control Studio",
    blocks,
    wires,
    notes: base?.notes || [],
    meta: base?.meta || {},
  };
}

function ControlStudioInner({ sessionId, onSession }) {
  const [session, setSession] = useState(null);
  const [palette, setPalette] = useState([]);
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [msg, setMsg] = useState("");
  const [plots, setPlots] = useState(null);
  const [revision, setRevision] = useState(0);
  const pollRef = useRef(null);
  const diagramBase = useRef({});

  const loadSession = useCallback(
    (sid) => {
      fetch(`/api/control-studio/sessions/${sid}`)
        .then((r) => (r.ok ? r.json() : Promise.reject()))
        .then((payload) => {
          setSession(payload);
          diagramBase.current = payload.diagram || {};
          const flow = diagramToFlow(payload.diagram);
          setNodes(flow.nodes);
          setEdges(flow.edges);
          setRevision(payload.revision || 0);
        })
        .catch(() => setMsg("Session load failed"));
    },
    [setNodes, setEdges],
  );

  useEffect(() => {
    fetch("/api/control-studio/palette")
      .then((r) => r.json())
      .then((d) => setPalette(d.palette || []))
      .catch(() => setPalette([]));
  }, []);

  useEffect(() => {
    if (sessionId) {
      loadSession(sessionId);
      return undefined;
    }
    fetch("/api/control-studio/sessions", { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" })
      .then((r) => r.json())
      .then((p) => {
        onSession?.(p.session_id);
        loadSession(p.session_id);
      })
      .catch(() => setMsg("Could not create session"));
    return undefined;
  }, [sessionId, loadSession, onSession]);

  useEffect(() => {
    if (!session?.session_id) return undefined;
    pollRef.current = setInterval(() => {
      fetch(`/api/control-studio/sessions/${session.session_id}`)
        .then((r) => r.json())
        .then((payload) => {
          if ((payload.revision || 0) > revision) {
            diagramBase.current = payload.diagram || {};
            const flow = diagramToFlow(payload.diagram);
            setNodes(flow.nodes);
            setEdges(flow.edges);
            setRevision(payload.revision || 0);
            setMsg("Diagram updated (agent or other client)");
          }
        })
        .catch(() => {});
    }, 2000);
    return () => clearInterval(pollRef.current);
  }, [session?.session_id, revision, setNodes, setEdges]);

  const persist = useCallback(
  (diagram, op = "edit") => {
    if (!session?.session_id) return;
    fetch(`/api/control-studio/sessions/${session.session_id}/diagram`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ diagram, author: "human", op }),
    })
      .then((r) => r.json())
      .then((out) => {
        setRevision(out.revision || revision + 1);
        diagramBase.current = out.diagram;
      })
      .catch(() => setMsg("Save failed"));
  },
    [session?.session_id, revision],
  );

  const onConnect = useCallback(
    (conn) => {
      setEdges((eds) => {
        const next = addEdge(
          { ...conn, id: `w-${eds.length + 1}`, style: EDGE_STYLE, markerEnd: { type: MarkerType.ArrowClosed } },
          eds,
        );
        persist(flowToDiagram(nodes, next, diagramBase.current));
        return next;
      });
    },
    [nodes, persist, setEdges],
  );

  const onNodeDragStop = useCallback(() => {
    persist(flowToDiagram(nodes, edges, diagramBase.current));
  }, [nodes, edges, persist]);

  function addPaletteItem(item) {
    const id = `${item.type}${nodes.length + 1}`;
    const nx = {
      id,
      type: "studio",
      position: { x: 80 + nodes.length * 40, y: 80 + (nodes.length % 3) * 100 },
      data: {
        blockId: id,
        blockType: item.type,
        label: item.label,
        params: { ...(item.default_params || {}) },
        paramLine: paramLine(item.default_params),
      },
    };
    const nextNodes = [...nodes, nx];
    setNodes(nextNodes);
    persist(flowToDiagram(nextNodes, edges, diagramBase.current), "add_block");
  }

  function runSim() {
    const sid = session?.session_id;
    if (!sid) return;
    persist(flowToDiagram(nodes, edges, diagramBase.current));
    fetch(`/api/control-studio/sessions/${sid}/simulate`, { method: "POST" })
      .then((r) => r.json())
      .then((out) => {
        if (out.ok) setPlots({ step: `/api/control-studio/sessions/${sid}/plot/step` });
        else setMsg(out.error || "simulate failed");
      });
  }

  function runAnalyze() {
    const sid = session?.session_id;
    if (!sid) return;
    fetch(`/api/control-studio/sessions/${sid}/analyze`, { method: "POST" })
      .then((r) => r.json())
      .then((out) => {
        if (out.ok)
          setPlots({
            step: plots?.step,
            bode: `/api/control-studio/sessions/${sid}/plot/bode`,
            nyquist: `/api/control-studio/sessions/${sid}/plot/nyquist`,
          });
        else setMsg(out.error || "analyze failed");
      });
  }

  function undo() {
    fetch(`/api/control-studio/sessions/${session.session_id}/undo`, { method: "POST", body: "{}" })
      .then((r) => r.json())
      .then((out) => loadSession(session.session_id));
  }

  const selected = nodes.find((n) => n.selected);
  function patchSelected(params) {
    if (!selected) return;
    const next = nodes.map((n) =>
      n.id === selected.id
        ? {
            ...n,
            data: {
              ...n.data,
              params: { ...n.data.params, ...params },
              paramLine: paramLine({ ...n.data.params, ...params }),
            },
          }
        : n,
    );
    setNodes(next);
    persist(flowToDiagram(next, edges, diagramBase.current), "set_param");
  }

  return (
    <motion className="control-studio">
      <header className="studio-toolbar">
        <h2>Control Studio</h2>
        <span className="hint">session {session?.session_id}</span>
        <button type="button" className="button-secondary" onClick={undo}>
          Undo
        </button>
        <button type="button" className="palette-btn" onClick={runSim}>
          Simulate
        </button>
        <button type="button" className="button-secondary" onClick={runAnalyze}>
          Analyze
        </button>
        {msg ? <span className="hint">{msg}</span> : null}
      </header>
      <div className="studio-layout">
        <aside className="studio-palette" aria-label="Block palette">
          {palette.map((item) => (
            <button key={item.type} type="button" className="palette-item" onClick={() => addPaletteItem(item)}>
              {item.label}
            </button>
          ))}
        </aside>
        <div className="studio-canvas">
          <ReactFlowProvider>
            <ReactFlow
              nodes={nodes}
              edges={edges}
              nodeTypes={nodeTypes}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              onNodeDragStop={onNodeDragStop}
              snapToGrid
              snapGrid={[GRID, GRID]}
              fitView
            >
              <Background gap={GRID} color="var(--ee-color-hairline)" />
            </ReactFlow>
          </ReactFlowProvider>
        </div>
        <aside className="studio-inspector">
          <h3>Parameters</h3>
          {selected ? (
            <>
              <p className="hint">{selected.data.blockType}</p>
              {selected.data.blockType === "pid" ? (
                <>
                  <label>
                    Kp
                    <input
                      type="number"
                      step="0.01"
                      defaultValue={selected.data.params?.kp ?? 1}
                      onChange={(e) => patchSelected({ kp: Number(e.target.value) })}
                    />
                  </label>
                  <label>
                    Ki
                    <input
                      type="number"
                      step="0.01"
                      defaultValue={selected.data.params?.ki ?? 0}
                      onChange={(e) => patchSelected({ ki: Number(e.target.value) })}
                    />
                  </label>
                </>
              ) : null}
              {selected.data.blockType === "gain" || selected.data.blockType === "plant_first_order" ? (
                <label>
                  k
                  <input
                    type="number"
                    defaultValue={selected.data.params?.k ?? 1}
                    onChange={(e) => patchSelected({ k: Number(e.target.value) })}
                  />
                </label>
              ) : null}
              {selected.data.blockType === "transfer_function" ? (
                <label>
                  tf
                  <input
                    type="text"
                    defaultValue={selected.data.params?.tf ?? "1/(s+1)"}
                    onChange={(e) => patchSelected({ tf: e.target.value })}
                  />
                </label>
              ) : null}
            </>
          ) : (
            <p className="hint">Select a block to edit parameters.</p>
          )}
          {plots ? (
            <div className="studio-plots">
              <h3>Results</h3>
              {plots.step ? <img src={plots.step} alt="Step response" className="plot" /> : null}
              {plots.bode ? <img src={plots.bode} alt="Bode" className="plot" /> : null}
              {plots.nyquist ? <img src={plots.nyquist} alt="Nyquist" className="plot" /> : null}
            </div>
          ) : null}
        </aside>
      </div>
      <details className="studio-oplog">
        <summary>Operation log ({(session?.op_log || []).length})</summary>
        <pre>{JSON.stringify(session?.op_log?.slice(-12) || [], null, 2)}</pre>
      </details>
    </motion>
  );
}

function motion({ children, className }) {
  return <section className={className}>{children}</section>;
}

export function ControlStudio() {
  const [sessionId, setSessionId] = useState(() => {
    const q = new URLSearchParams(window.location.search);
    return q.get("session") || "";
  });
  return <ControlStudioInner sessionId={sessionId} onSession={setSessionId} />;
}
