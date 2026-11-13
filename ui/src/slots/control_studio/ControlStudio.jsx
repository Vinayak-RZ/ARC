import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  ReactFlow,
  ReactFlowProvider,
  Background,
  MiniMap,
  ConnectionLineType,
  addEdge,
  useEdgesState,
  useNodesState,
  useReactFlow,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { StudioPalette } from "./Palette.jsx";
import { StudioInspector } from "./Inspector.jsx";
import { ResultsDock } from "./ResultsDock.jsx";
import { studioNodeTypes } from "./nodes.jsx";
import { studioEdgeTypes } from "./edges.jsx";
import { diagramToFlow, flowToDiagram, issuesByBlock } from "./utils.js";

const GRID = 16;

function formatOpTime(tsMs) {
  if (!tsMs) return "";
  try {
    return new Date(tsMs).toLocaleTimeString();
  } catch {
    return "";
  }
}

function CanvasDrop({ children, onDropBlock }) {
  const { screenToFlowPosition } = useReactFlow();
  return (
    <div
      className="studio-canvas-inner"
      onDragOver={(e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = "copy";
      }}
      onDrop={(e) => {
        e.preventDefault();
        const raw = e.dataTransfer.getData("application/control-studio-block");
        if (!raw) return;
        const item = JSON.parse(raw);
        const pos = screenToFlowPosition({ x: e.clientX, y: e.clientY });
        onDropBlock(item, pos);
      }}
    >
      {children}
    </div>
  );
}

function ControlStudioInner({ sessionId, onSession }) {
  const [session, setSession] = useState(null);
  const [groups, setGroups] = useState([]);
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [msg, setMsg] = useState("");
  const [results, setResults] = useState(null);
  const [margins, setMargins] = useState(null);
  const [revision, setRevision] = useState(0);
  const [validation, setValidation] = useState({ ok: true, issues: [], warnings: [] });
  const [highlight, setHighlight] = useState({ ids: new Set(), author: null });
  const diagramBase = useRef({});
  const blockIssues = useMemo(() => issuesByBlock(validation), [validation]);

  const paint = useCallback(
    (payload, { author = null } = {}) => {
      diagramBase.current = payload.diagram || {};
      const presence = payload.presence || {};
      const now = Date.now();
      const ids = new Set();
      if (presence.highlight_until_ms && presence.highlight_until_ms > now) {
        (payload.diagram?.blocks || []).forEach((b) => ids.add(b.id));
      }
      const flow = diagramToFlow(payload.diagram, {
        issuesByBlock: blockIssues,
        notes: payload.diagram?.notes,
        highlightSet: ids,
        flashAuthor: presence.last_author || author,
      });
      setNodes(flow.nodes);
      setEdges(flow.edges);
      setRevision(payload.revision || 0);
      setSession(payload);
      setHighlight({ ids, author: presence.last_author });
      if (presence.agent_editing) setMsg("Agent editing…");
    },
    [blockIssues, setNodes, setEdges],
  );

  const refreshValidation = useCallback(
    (sid) => {
      fetch(`/api/control-studio/sessions/${sid}/validate`, { method: "POST" })
        .then((r) => r.json())
        .then(setValidation)
        .catch(() => {});
    },
    [],
  );

  const loadSession = useCallback(
    (sid) => {
      fetch(`/api/control-studio/sessions/${sid}`)
        .then((r) => (r.ok ? r.json() : Promise.reject()))
        .then((payload) => {
          paint(payload);
          refreshValidation(sid);
        })
        .catch(() => setMsg("Session load failed"));
    },
    [paint, refreshValidation],
  );

  useEffect(() => {
    fetch("/api/control-studio/palette")
      .then((r) => r.json())
      .then((d) => setGroups(d.groups || []))
      .catch(() => setGroups([]));
  }, []);

  useEffect(() => {
    if (sessionId) {
      loadSession(sessionId);
      return undefined;
    }
    fetch("/api/control-studio/sessions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: "PID · DC motor", golden: "pid_dc_motor" }),
    })
      .then((r) => r.json())
      .then((p) => {
        const url = new URL(window.location.href);
        url.searchParams.set("session", p.session_id);
        window.history.replaceState({}, "", url);
        onSession?.(p.session_id);
        paint(p);
        refreshValidation(p.session_id);
        fetch(`/api/control-studio/sessions/${p.session_id}/simulate`, { method: "POST" })
          .then((r) => r.json())
          .then(() =>
            fetch(`/api/control-studio/sessions/${p.session_id}/analyze`, { method: "POST" }).then((r) => r.json()),
          )
          .then((an) => {
            if (an.ok) {
              const sid = p.session_id;
              const ts = Date.now();
              setResults({
                ts,
                step: `/api/control-studio/sessions/${sid}/plot/step`,
                bode: `/api/control-studio/sessions/${sid}/plot/bode`,
                rlocus: `/api/control-studio/sessions/${sid}/plot/root_locus`,
              });
              setMargins(an);
            }
          });
      })
      .catch(() => setMsg("Could not create session"));
    return undefined;
  }, [sessionId, loadSession, onSession, paint, refreshValidation]);

  useEffect(() => {
    if (!session?.diagram) return;
    const flow = diagramToFlow(session.diagram, {
      issuesByBlock: blockIssues,
      notes: session.diagram?.notes,
      highlightSet: highlight.ids,
      flashAuthor: highlight.author,
    });
    setNodes(flow.nodes);
    setEdges(flow.edges);
  }, [validation, session?.diagram, session?.presence, highlight, blockIssues, setNodes, setEdges]);

  useEffect(() => {
    if (!session?.session_id) return undefined;
    const sid = session.session_id;
    const es = new EventSource(`/api/control-studio/sessions/${sid}/events`);
    es.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data);
        if (data.type === "hello") return;
        if ((data.revision || 0) > revision) {
          loadSession(sid);
        }
      } catch {
        /* ignore */
      }
    };
    return () => es.close();
  }, [session?.session_id, revision, loadSession]);

  const persist = useCallback(
    (diagram, op = "edit") => {
      const sid = session?.session_id;
      if (!sid) return;
      fetch(`/api/control-studio/sessions/${sid}/diagram`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ diagram, author: "human", op }),
      })
        .then((r) => r.json())
        .then((out) => {
          diagramBase.current = out.diagram;
          setRevision(out.revision || revision + 1);
          refreshValidation(sid);
        })
        .catch(() => setMsg("Save failed"));
    },
    [session?.session_id, revision, refreshValidation],
  );

  const onConnect = useCallback(
    (conn) => {
      setEdges((eds) => {
        const next = addEdge({ ...conn, id: `w-${eds.length + 1}`, type: "signal" }, eds);
        persist(flowToDiagram(nodes, next, diagramBase.current), "connect");
        return next;
      });
    },
    [nodes, persist, setEdges],
  );

  const onNodeDragStop = useCallback(() => {
    persist(flowToDiagram(nodes, edges, diagramBase.current), "move");
  }, [nodes, edges, persist]);

  function placeBlock(item, position) {
    const id = `${item.type}${nodes.length + 1}`;
    const nx = {
      id,
      type: item.type === "sum" ? "sum" : item.type === "gain" ? "gain" : item.type === "transfer_function" ? "tf" : item.type === "pid" ? "pid" : item.type === "scope" ? "scope" : item.type.startsWith("plant_") ? "plant" : ["step", "ramp", "sine"].includes(item.type) ? "source" : "generic",
      position: position || { x: 120 + nodes.length * 36, y: 120 },
      data: {
        blockId: id,
        blockType: item.type,
        label: item.label,
        params: { ...(item.default_params || {}) },
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
      .then((sim) => {
        if (!sim.ok) {
          setMsg(sim.error || "simulate failed");
          return null;
        }
        return fetch(`/api/control-studio/sessions/${sid}/analyze`, { method: "POST" }).then((r) => r.json());
      })
      .then((an) => {
        if (an?.ok) {
          const ts = Date.now();
          setResults({
            ts,
            step: `/api/control-studio/sessions/${sid}/plot/step`,
            bode: `/api/control-studio/sessions/${sid}/plot/bode`,
            rlocus: `/api/control-studio/sessions/${sid}/plot/root_locus`,
          });
          setMargins(an);
          setMsg("");
        }
      });
  }

  function undo() {
    fetch(`/api/control-studio/sessions/${session.session_id}/undo`, { method: "POST", body: "{}" })
      .then((r) => r.json())
      .then(() => loadSession(session.session_id));
  }

  const selected = nodes.find((n) => n.selected);
  function patchSelected(params) {
    if (!selected) return;
    const next = nodes.map((n) =>
      n.id === selected.id ? { ...n, data: { ...n.data, params: { ...n.data.params, ...params } } } : n,
    );
    setNodes(next);
    persist(flowToDiagram(next, edges, diagramBase.current), "set_param");
  }

  function pinComment(text) {
    if (!selected || !text.trim()) return;
    fetch(`/api/control-studio/sessions/${session.session_id}/notes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ block_id: selected.id, text, author: "human" }),
    }).then(() => loadSession(session.session_id));
  }

  const agentActive =
    session?.presence?.agent_editing ||
    (session?.presence?.agent_editing_until_ms && session.presence.agent_editing_until_ms > Date.now());

  return (
    <section className="control-studio">
      <header className="studio-toolbar">
        <div>
          <h2>Control Studio</h2>
          <p className="hint">{session?.diagram?.title || "PID · DC motor"}</p>
        </div>
        <span className="hint">session {session?.session_id}</span>
        {agentActive ? <span className="studio-presence">● Agent editing</span> : <span className="studio-presence idle">● Live sync (SSE)</span>}
        <button type="button" className="button-secondary" onClick={undo}>
          Undo
        </button>
        <button type="button" className="palette-btn" onClick={runSim}>
          Simulate
        </button>
        {msg ? <span className="hint">{msg}</span> : null}
      </header>
      <div className="studio-layout">
        <StudioPalette groups={groups} onDragStart={(item, opts) => opts?.placeCenter && placeBlock(item)} />
        <div className="studio-canvas">
          <ReactFlowProvider>
            <CanvasDrop onDropBlock={placeBlock}>
              <ReactFlow
                nodes={nodes}
                edges={edges}
                nodeTypes={studioNodeTypes}
                edgeTypes={studioEdgeTypes}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                onNodeDragStop={onNodeDragStop}
                snapToGrid
                snapGrid={[GRID, GRID]}
                connectionLineType={ConnectionLineType.SmoothStep}
                fitView
                proOptions={{ hideAttribution: true }}
              >
                <Background gap={GRID} color="var(--ee-color-hairline)" size={1} />
                <MiniMap className="studio-minimap" pannable zoomable />
              </ReactFlow>
            </CanvasDrop>
          </ReactFlowProvider>
        </div>
        <StudioInspector
          selected={selected}
          blockIssues={blockIssues}
          onPatch={patchSelected}
          onComment={pinComment}
          notes={session?.diagram?.notes}
        />
      </div>
      <ResultsDock sessionId={session?.session_id} results={results} margins={margins} />
      <section className="studio-oplog" aria-label="Operation log">
        <h3>Operation log</h3>
        <ul className="oplog-list">
          {(session?.op_log || []).slice(-10).reverse().map((op) => (
            <li key={op.id}>
              <span className={`studio-author-badge is-${op.author}`}>{op.author}</span>
              <span className="op-name">{op.op}</span>
              <time dateTime={new Date(op.ts_ms).toISOString()}>{formatOpTime(op.ts_ms)}</time>
            </li>
          ))}
        </ul>
      </section>
    </section>
  );
}

export function ControlStudio() {
  const [sessionId, setSessionId] = useState(() => {
    const q = new URLSearchParams(window.location.search);
    return q.get("session") || "";
  });
  return <ControlStudioInner sessionId={sessionId} onSession={setSessionId} />;
}
