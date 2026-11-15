import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  ReactFlow,
  ReactFlowProvider,
  Background,
  MiniMap,
  ConnectionLineType,
  MarkerType,
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
import { FitViewOnChange } from "./FitViewOnChange.jsx";
import { diagramToFlow, flowToDiagram, humanBlockLabel, issuesByBlock } from "./utils.js";
import { StudioToolbar } from "./StudioToolbar.jsx";
import { MascotState } from "../../components/MascotState.jsx";
import "../../control-studio/studio.css";

const GRID = 16;

function useNarrowViewport() {
  const [narrow, setNarrow] = useState(() =>
    typeof window !== "undefined" ? window.matchMedia("(max-width: 1199px)").matches : false,
  );
  useEffect(() => {
    const mq = window.matchMedia("(max-width: 1199px)");
    const fn = () => setNarrow(mq.matches);
    mq.addEventListener("change", fn);
    return () => mq.removeEventListener("change", fn);
  }, []);
  return narrow;
}

function formatOpTime(tsMs) {
  if (!tsMs) return "";
  try {
    return new Date(tsMs).toLocaleTimeString();
  } catch {
    return "";
  }
}

function formatOpSummary(op) {
  const bits = [op.op || "edit"];
  if (op.target) bits.push(op.target);
  if (op.detail && typeof op.detail === "object") {
    const params = Object.entries(op.detail)
      .map(([k, v]) => `${k}=${v}`)
      .join(", ");
    if (params) bits.push(params);
  }
  return bits.join(" · ");
}

function minimapColor(node) {
  switch (node.type) {
    case "sum":
      return "var(--cs-accent)";
    case "pid":
      return "#0d9488";
    case "plant":
      return "var(--cs-copper)";
    case "scope":
      return "var(--cs-text)";
    case "source":
      return "#6366f1";
    default:
      return "var(--cs-text-muted)";
  }
}

function targetsFromLastOp(payload, presenceNow) {
  const ids = new Set();
  const now = Date.now();
  if (!presenceNow?.highlight_until_ms || presenceNow.highlight_until_ms <= now) {
    return ids;
  }
  const last = (payload.op_log || []).slice(-1)[0];
  if (last?.target) ids.add(String(last.target));
  return ids;
}

function applySimAndAnalyze(sid, sim, setResults, setMargins, setStepData, setMsg, onSuccess) {
  if (!sim?.ok) {
    setMsg(sim?.error || "simulate failed");
    return;
  }
  const an = sim.analyze?.ok ? sim.analyze : sim.analyze || sim;
  if (sim.analyze && !sim.analyze.ok) {
    setMsg(sim.analyze.error || "analyze failed");
  }
  const ts = Date.now();
  setResults({
    ts,
    step: `/api/control-studio/sessions/${sid}/plot/step`,
    bode: `/api/control-studio/sessions/${sid}/plot/bode`,
    rlocus: `/api/control-studio/sessions/${sid}/plot/root_locus`,
  });
  setMargins(an);
  if (sim.step_series) setStepData?.(sim.step_series);
  setMsg("");
  onSuccess?.();
  return true;
}

function FlowZoomHelpers({ zoomApi, setZoomPct }) {
  const { zoomIn, zoomOut } = useReactFlow();
  useEffect(() => {
    zoomApi.current = {
      in: () => zoomIn({ duration: 120 }),
      out: () => zoomOut({ duration: 120 }),
    };
    setZoomPct((z) => z || 1);
  }, [setZoomPct, zoomApi, zoomIn, zoomOut]);
  return null;
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

const GOLDEN_TEMPLATES = [
  {
    id: "pid_dc_motor",
    title: "PID · DC motor",
    blurb: "Summing junction, PID, DC motor plant, and scope — the default simulate loop.",
  },
];

function ControlStudioInner({ sessionId, onSession, autoBoot = false }) {
  const [session, setSession] = useState(null);
  const [groups, setGroups] = useState([]);
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [msg, setMsg] = useState("");
  const [booting, setBooting] = useState(!sessionId);
  const [bootError, setBootError] = useState("");
  const [bootKey, setBootKey] = useState(0);
  const sseDebounce = useRef(null);
  const [results, setResults] = useState(null);
  const [stepData, setStepData] = useState(null);
  const [margins, setMargins] = useState(null);
  const [revision, setRevision] = useState(0);
  const [lastSimRevision, setLastSimRevision] = useState(null);
  const [connecting, setConnecting] = useState(false);
  const [fitBump, setFitBump] = useState(0);
  // Bumped whenever the node objects are replaced from the diagram; see FitViewOnChange.
  const [nodesEpoch, setNodesEpoch] = useState(0);
  const [zoomPct, setZoomPct] = useState(1);
  const [selectedId, setSelectedId] = useState(null);
  const selectedIdRef = useRef(null);
  selectedIdRef.current = selectedId;
  const fitRef = useRef(() => {});
  const zoomApi = useRef({ in: () => {}, out: () => {} });
  const withSelection = useCallback(
    (list) => list.map((n) => ({ ...n, selected: n.id === selectedIdRef.current })),
    [],
  );
  const [validation, setValidation] = useState({ ok: true, issues: [], warnings: [] });
  const [highlight, setHighlight] = useState({ ids: new Set(), author: null });
  const diagramBase = useRef({});
  const blockIssues = useMemo(() => issuesByBlock(validation), [validation]);
  // paint() must keep a stable identity: it feeds loadSession, which feeds the effect that
  // fetches the session. If paint changed whenever validation changed, each validate response
  // would trigger another session fetch and another validate, in an endless loop that
  // re-creates every node and wire (the cause of wires disappearing).
  const blockIssuesRef = useRef(blockIssues);
  blockIssuesRef.current = blockIssues;

  const paint = useCallback(
    (payload, { author = null } = {}) => {
      diagramBase.current = payload.diagram || {};
      const presence = payload.presence || {};
      const ids = targetsFromLastOp(payload, presence);
      const flow = diagramToFlow(payload.diagram, {
        issuesByBlock: blockIssuesRef.current,
        notes: payload.diagram?.notes,
        highlightSet: ids,
        flashAuthor: ids.size ? presence.last_author || author : null,
      });
      setNodes(withSelection(flow.nodes));
      setNodesEpoch((n) => n + 1);
      setEdges(flow.edges);
      setRevision(payload.revision || 0);
      setSession(payload);
      setHighlight({ ids, author: presence.last_author });
      if (presence.agent_editing) setMsg("Agent editing…");
    },
    [setNodes, setEdges, withSelection],
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
      setBooting(false);
      setBootError("");
      loadSession(sessionId);
      return undefined;
    }
    if (!autoBoot && bootKey === 0) {
      setBooting(false);
      setBootError("");
      return undefined;
    }
    let cancelled = false;
    setBooting(true);
    setBootError("");
    const timeout = setTimeout(() => {
      if (!cancelled) {
        setBootError("Studio took too long to start.");
        setBooting(false);
      }
    }, 20_000);
    fetch("/api/control-studio/sessions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: "PID · DC motor", golden: "pid_dc_motor" }),
    })
      .then((r) => r.json())
      .then((p) => {
        if (cancelled) return null;
        const url = new URL(window.location.href);
        url.searchParams.set("session", p.session_id);
        window.history.replaceState({}, "", url);
        onSession?.(p.session_id);
        paint(p);
        refreshValidation(p.session_id);
        setBooting(false);
        fetch(`/api/control-studio/sessions/${p.session_id}/simulate`, { method: "POST" })
          .then((r) => r.json())
          .then((sim) => {
            if (cancelled) return;
            applySimAndAnalyze(p.session_id, sim, setResults, setMargins, setStepData, setMsg, () =>
              setLastSimRevision(p.revision || 0),
            );
          })
          .catch(() => {});
        return null;
      })
      .catch(() => {
        if (!cancelled) {
          setBootError("Could not create session");
          setBooting(false);
          setMsg("Could not create session");
        }
      })
      .finally(() => clearTimeout(timeout));
    return () => {
      cancelled = true;
      clearTimeout(timeout);
    };
  }, [sessionId, loadSession, onSession, paint, refreshValidation, bootKey, autoBoot]);

  function startTemplate() {
    setBootError("");
    setBootKey((k) => k + 1);
  }

  const resyncFlowFromDiagram = useCallback(
    (diagram) => {
      if (!diagram) return;
      const flow = diagramToFlow(diagram, {
        issuesByBlock: blockIssues,
        notes: diagram?.notes,
        highlightSet: highlight.ids,
        flashAuthor: highlight.author,
      });
      setNodes(withSelection(flow.nodes));
      setNodesEpoch((n) => n + 1);
      setEdges(flow.edges);
    },
    [blockIssues, highlight.author, highlight.ids, setEdges, setNodes, withSelection],
  );

  useEffect(() => {
    if (!session?.diagram) return;
    resyncFlowFromDiagram(session.diagram);
  }, [validation, session?.diagram, session?.presence, highlight.ids.size, resyncFlowFromDiagram]);


  useEffect(() => {
    if (!selectedId) return undefined;
    const t1 = setTimeout(() => fitRef.current?.(0), 60);
    const t2 = setTimeout(() => fitRef.current?.(0), 450);
    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
    };
  }, [selectedId]);

  useEffect(() => {
    if (!session?.session_id) return undefined;
    const sid = session.session_id;
    const es = new EventSource(`/api/control-studio/sessions/${sid}/events`);
    es.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data);
        if (data.type === "hello") return;
        if ((data.revision || 0) > revision) {
          setFitBump((n) => n + 1);
          if (sseDebounce.current) clearTimeout(sseDebounce.current);
          sseDebounce.current = setTimeout(() => loadSession(sid), 250);
        }
      } catch {
        /* ignore */
      }
    };
    return () => {
      es.close();
      if (sseDebounce.current) clearTimeout(sseDebounce.current);
    };
  }, [session?.session_id, revision, loadSession]);

  const persist = useCallback(
    (diagram, meta = {}) => {
      const { op = "edit", target = null, detail = null } = typeof meta === "string" ? { op: meta } : meta;
      const sid = session?.session_id;
      if (!sid) return;
      fetch(`/api/control-studio/sessions/${sid}/diagram`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ diagram, author: "human", op, target, detail }),
      })
        .then((r) => r.json())
        .then((out) => {
          diagramBase.current = out.diagram;
          const nextRev = out.revision || revision + 1;
          setRevision(nextRev);
          // Keep session.diagram current: the resync effect rebuilds nodes from it whenever
          // validation changes, so a stale copy would revert the edit that was just saved.
          setSession((prev) => (prev ? { ...prev, diagram: out.diagram, revision: nextRev } : prev));
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
        persist(flowToDiagram(nodes, next, diagramBase.current), {
          op: "connect",
          target: `${conn.source}→${conn.target}`,
        });
        return next;
      });
    },
    [nodes, persist, setEdges],
  );

  const onNodeDragStop = useCallback(() => {
    persist(flowToDiagram(nodes, edges, diagramBase.current), { op: "move" });
  }, [nodes, edges, persist]);

  const nodesRef = useRef(nodes);
  const edgesRef = useRef(edges);
  nodesRef.current = nodes;
  edgesRef.current = edges;

  const onEdgesDelete = useCallback(
    (deleted) => {
      const ids = new Set(deleted.map((e) => e.id));
      const next = edgesRef.current.filter((e) => !ids.has(e.id));
      persist(flowToDiagram(nodesRef.current, next, diagramBase.current), { op: "disconnect" });
    },
    [persist],
  );

  function placeBlock(item, position) {
    const id = `${item.type}${nodes.length + 1}`;
    const nx = {
      id,
      type: item.type === "sum" ? "sum" : item.type === "gain" ? "gain" : item.type === "transfer_function" ? "tf" : item.type === "pid" ? "pid" : item.type === "scope" ? "scope" : item.type.startsWith("plant_") ? "plant" : ["step", "ramp", "sine"].includes(item.type) ? "source" : "generic",
      position: position || { x: 120 + nodes.length * 36, y: 120 },
      data: {
        blockId: id,
        blockType: item.type,
        label: humanBlockLabel(item.type, item.label),
        params: { ...(item.default_params || {}) },
      },
    };
    const nextNodes = [...nodes, nx];
    setNodes(nextNodes);
    persist(flowToDiagram(nextNodes, edges, diagramBase.current), { op: "add_block", target: id });
  }

  function runSim() {
    const sid = session?.session_id;
    if (!sid) return;
    const diagram = flowToDiagram(nodes, edges, diagramBase.current);
    fetch(`/api/control-studio/sessions/${sid}/diagram`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ diagram, author: "human", op: "edit" }),
    })
      .then((r) => r.json())
        .then((out) => {
        diagramBase.current = out.diagram;
        const simRev = out.revision || revision;
        setRevision(simRev);
        setSession((prev) => (prev ? { ...prev, diagram: out.diagram, revision: simRev } : prev));
        return fetch(`/api/control-studio/sessions/${sid}/simulate`, { method: "POST" })
          .then((r) => r.json())
          .then((sim) => {
            applySimAndAnalyze(sid, sim, setResults, setMargins, setStepData, setMsg, () => setLastSimRevision(simRev));
          });
      })
      .catch(() => setMsg("Save failed"));
  }

  function undo() {
    fetch(`/api/control-studio/sessions/${session.session_id}/undo`, { method: "POST", body: "{}" })
      .then((r) => r.json())
      .then(() => loadSession(session.session_id));
  }

  const selected = useMemo(() => nodes.find((n) => n.id === selectedId) ?? null, [nodes, selectedId]);
  function patchSelected(params) {
    if (!selected) return;
    const next = nodes.map((n) =>
      n.id === selected.id ? { ...n, data: { ...n.data, params: { ...n.data.params, ...params } } } : n,
    );
    setNodes(next);
    persist(flowToDiagram(next, edges, diagramBase.current), {
      op: "set_param",
      target: selected.id,
      detail: params,
    });
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
  const resultsStale = lastSimRevision != null && revision > lastSimRevision;
  const narrowViewport = useNarrowViewport();
  const inspectorFloating = Boolean(selected) && narrowViewport;

  function redo() {
    fetch(`/api/control-studio/sessions/${session.session_id}/redo`, { method: "POST", body: "{}" })
      .then((r) => r.json())
      .then(() => loadSession(session.session_id))
      .catch(() => {});
  }

  if (!sessionId && !session && !booting && bootKey === 0) {
    return (
      <section className="cs-app control-studio studio-idle card-surface">
        <h2>Control block diagrams</h2>
        <p className="hint">Start a session, wire blocks, then simulate step response and margins.</p>
        <div className="learn-lab-grid studio-pick-grid">
          {GOLDEN_TEMPLATES.map((t) => (
            <button key={t.id} type="button" className="learn-lab-card" onClick={startTemplate}>
              <strong>{t.title}</strong>
              <span className="hint">{t.blurb}</span>
            </button>
          ))}
        </div>
      </section>
    );
  }

  if (booting) {
    return (
      <section className="cs-app control-studio studio studio-booting">
        <MascotState kind="loading" title="Building PID · DC motor loop…" message="Creating the golden session and first simulate." />
      </section>
    );
  }
  if (bootError && !session) {
    return (
      <section className="cs-app control-studio studio studio-booting">
        <MascotState
          kind="error"
          title="Studio did not start"
          message={bootError}
          actionLabel="Retry"
          onAction={() => {
            setBootError("");
            setBootKey((k) => k + 1);
            setBooting(true);
          }}
        />
      </section>
    );
  }

  return (
    <section
      className={`cs-app control-studio studio${selected ? " has-selection" : ""}`}
    >
      <ReactFlowProvider>
        <StudioToolbar
          title={session?.diagram?.title}
          resultsStale={resultsStale}
          zoomPct={zoomPct}
          onUndo={undo}
          onRedo={redo}
          canRedo={false}
          onSimulate={runSim}
          onFit={() => fitRef.current?.()}
          onZoomIn={() => zoomApi.current.in?.()}
          onZoomOut={() => zoomApi.current.out?.()}
        />
        <StudioPalette groups={groups} onDragStart={(item) => placeBlock(item)} />
        <div className={`studio-canvas${connecting ? " is-connecting" : ""}`}>
          <p className="studio-wire-hint">Drag a port onto another port. Click a wire, then Delete, to remove it.</p>
          <CanvasDrop onDropBlock={placeBlock}>
            <FlowZoomHelpers zoomApi={zoomApi} setZoomPct={setZoomPct} />
            <ReactFlow
              nodes={nodes}
              edges={edges}
              nodeTypes={studioNodeTypes}
              edgeTypes={studioEdgeTypes}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              onEdgesDelete={onEdgesDelete}
              onConnectStart={() => setConnecting(true)}
              onConnectEnd={() => setConnecting(false)}
              deleteKeyCode={["Backspace", "Delete"]}
              edgesFocusable
              elementsSelectable
              connectionRadius={32}
              onNodeDragStop={onNodeDragStop}
              onNodeClick={(_, node) => {
                setSelectedId(node.id);
                setNodes((nds) => nds.map((n) => ({ ...n, selected: n.id === node.id })));
              }}
              onPaneClick={() => {
                setSelectedId(null);
                setNodes((nds) => nds.map((n) => ({ ...n, selected: false })));
              }}
              onMove={(_, vp) => setZoomPct(vp.zoom)}
              snapToGrid
              snapGrid={[GRID, GRID]}
              connectionLineType={ConnectionLineType.Straight}
              elevateEdgesOnSelect={false}
              elevateNodesOnSelect
              defaultEdgeOptions={{
                type: "signal",
                zIndex: 0,
                markerEnd: { type: MarkerType.ArrowClosed, color: "currentColor", width: 14, height: 14 },
              }}
              minZoom={0.2}
              maxZoom={1.25}
              proOptions={{ hideAttribution: true }}
            >
              <Background gap={8} color="var(--cs-border)" size={1} />
              <Background gap={32} color="var(--cs-border-strong)" size={1} offset={0} />
              <FitViewOnChange
                revision={revision}
                nodeCount={nodes.length}
                agentBump={fitBump}
                nodesEpoch={nodesEpoch}
                fitRef={fitRef}
              />
            </ReactFlow>
          </CanvasDrop>
        </div>
        <StudioInspector
          selected={selected}
          blockIssues={blockIssues}
          onPatch={patchSelected}
          onComment={pinComment}
          notes={session?.diagram?.notes}
          floating={inspectorFloating}
        />
        <ResultsDock
          results={results}
          stepData={stepData}
          margins={margins}
          stale={resultsStale}
          sessionId={session?.session_id}
          onResimulate={(sim) => {
            if (!sim?.ok) {
              setMsg(sim?.error || "simulate failed");
              return;
            }
            const an = sim.analyze?.ok ? sim.analyze : sim.analyze || sim;
            setMargins(an);
            if (sim.step_series) setStepData(sim.step_series);
            setResults((prev) => ({ ...prev, ts: Date.now() }));
            setMsg("");
          }}
        />
        {msg ? <p className="studio-toast cs-status-msg">{msg}</p> : null}
      </ReactFlowProvider>
    </section>
  );
}

export function ControlStudio({ autoBoot = false }) {
  const [sessionId, setSessionId] = useState(() => {
    const q = new URLSearchParams(window.location.search);
    return q.get("session") || "";
  });
  useEffect(() => {
    const sync = () => setSessionId(new URLSearchParams(window.location.search).get("session") || "");
    sync();
    window.addEventListener("popstate", sync);
    window.addEventListener("arc-url", sync);
    return () => {
      window.removeEventListener("popstate", sync);
      window.removeEventListener("arc-url", sync);
    };
  }, []);
  return <ControlStudioInner sessionId={sessionId} onSession={setSessionId} autoBoot={autoBoot} />;
}
