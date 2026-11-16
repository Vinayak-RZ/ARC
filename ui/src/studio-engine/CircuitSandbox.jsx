import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  ReactFlow,
  ReactFlowProvider,
  Background,
  ConnectionLineType,
  ConnectionMode,
  addEdge,
  useEdgesState,
  useNodesState,
  useReactFlow,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { Palette } from "../slots/canvas/Palette.jsx";
import { Waveform } from "./renderers/Waveform.jsx";
import {
  fromFlow,
  MAX_EDGES,
  MAX_NODES,
  nextEdgeId,
  nextPartId,
  nextRefdes,
  partCount,
  PARTS,
  splitEdgeAt,
  toFlow,
} from "../slots/canvas/graph.js";
import { nodeTypes } from "../slots/canvas/nodes.jsx";
import { LabActivity } from "../components/LabActivity.jsx";
import { LabProvenanceBar } from "../components/LabProvenanceBar.jsx";
import { LabVerifyPanel } from "../components/LabVerifyPanel.jsx";
import "../control-studio/studio.css";

const EDGE_STYLE = { stroke: "var(--ee-color-ink)", strokeWidth: 1.5 };
const GRID = 16;
const STORAGE_KEY = "arc-circuit-sandbox-v1";

const SERIES_RLC = {
  schema: "arc.circuit.v1",
  nodes: [
    { id: "vin", type: "source_v", refdes: "V1", value: 10, unit: "V", x: 64, y: 120, rot: 0 },
    { id: "r1", type: "resistor", refdes: "R1", value: 10, unit: "ohm", x: 184, y: 72, rot: 0 },
    { id: "l1", type: "inductor", refdes: "L1", value: 0.01, unit: "H", x: 304, y: 72, rot: 0 },
    { id: "c1", type: "capacitor", refdes: "C1", value: 0.0001, unit: "F", x: 424, y: 72, rot: 0 },
    { id: "jret", type: "junction", refdes: "", value: 0, unit: "", x: 424, y: 168, rot: 0 },
    { id: "gnd", type: "ground", refdes: "GND", value: 0, unit: "", x: 64, y: 200, rot: 0 },
  ],
  edges: [
    { id: "e1", from: "vin.n1", to: "r1.n1" },
    { id: "e2", from: "r1.n2", to: "l1.n1" },
    { id: "e3", from: "l1.n2", to: "c1.n1" },
    { id: "e4", from: "c1.n2", to: "jret.n" },
    { id: "e5", from: "vin.n2", to: "jret.w" },
    { id: "e6", from: "jret.s", to: "gnd.n1" },
  ],
};

const RC_LOWPASS = {
  schema: "arc.circuit.v1",
  nodes: [
    { id: "vin", type: "source_v", refdes: "V1", value: 5, unit: "V", x: 40, y: 100, rot: 0 },
    { id: "r1", type: "resistor", refdes: "R1", value: 1000, unit: "ohm", x: 200, y: 40, rot: 0 },
    { id: "c1", type: "capacitor", refdes: "C1", value: 1e-6, unit: "F", x: 360, y: 120, rot: 90 },
    { id: "gnd", type: "ground", refdes: "Gnd", value: 0, unit: "", x: 40, y: 220, rot: 0 },
  ],
  edges: [
    { id: "e1", from: "vin.n1", to: "r1.n1" },
    { id: "e2", from: "r1.n2", to: "c1.n1" },
    { id: "e3", from: "c1.n2", to: "gnd.n1" },
    { id: "e4", from: "vin.n2", to: "gnd.n1" },
  ],
};

const PARALLEL_RC = {
  schema: "arc.circuit.v1",
  nodes: [
    { id: "vin", type: "source_v", refdes: "V1", value: 10, unit: "V", x: 40, y: 120, rot: 0 },
    { id: "r1", type: "resistor", refdes: "R1", value: 1000, unit: "ohm", x: 220, y: 40, rot: 90 },
    { id: "c1", type: "capacitor", refdes: "C1", value: 1e-6, unit: "F", x: 340, y: 40, rot: 90 },
    { id: "gnd", type: "ground", refdes: "Gnd", value: 0, unit: "", x: 40, y: 240, rot: 0 },
  ],
  edges: [
    { id: "e1", from: "vin.n1", to: "r1.n1" },
    { id: "e2", from: "vin.n1", to: "c1.n1" },
    { id: "e3", from: "r1.n2", to: "gnd.n1" },
    { id: "e4", from: "c1.n2", to: "gnd.n1" },
    { id: "e5", from: "vin.n2", to: "gnd.n1" },
  ],
};

const EXAMPLES = [
  ["divider", "Load divider", null],
  ["rlc", "Series RLC", SERIES_RLC],
  ["rc", "RC low-pass", RC_LOWPASS],
  ["prc", "Parallel RC", PARALLEL_RC],
];

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

function FitViewOnChange({ signal }) {
  const { fitView } = useReactFlow();
  useEffect(() => {
    const id = requestAnimationFrame(() => fitView({ padding: 0.2, duration: 0 }));
    return () => cancelAnimationFrame(id);
  }, [signal, fitView]);
  return null;
}

function CircuitSandboxInner({ linkedRunId = "" }) {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [msg, setMsg] = useState("");
  const [fitKey, setFitKey] = useState(0);
  const [sim, setSim] = useState(null);
  const [simBusy, setSimBusy] = useState(false);
  const [labMeta, setLabMeta] = useState(null);
  const [labVerify, setLabVerify] = useState(null);
  const [runTitle, setRunTitle] = useState("");
  const [viewMode, setViewMode] = useState("yours");
  const [showAuthorship, setShowAuthorship] = useState(false);
  const past = useRef([]);
  const future = useRef([]);
  const hydrated = useRef(false);
  const graphReady = useRef(false);
  const revision = useRef(0);
  const wrapRef = useRef(null);
  const { screenToFlowPosition } = useReactFlow();

  function applyLabSimulate(labSimulate, labVerify) {
    if (!labSimulate?.ok && !labSimulate?.simulated) return;
    const trace = labSimulate.trace || labSimulate.spice || labSimulate;
    const peakV = Number(labSimulate.simulated ?? trace?.Vc_peak_V ?? labVerify?.simulated);
    const tPeak = Number(trace?.t_Vc_peak_s ?? labVerify?.derive?.t_s ?? 0);
    const vcMs = trace?.vc_trace_ms;
    if (vcMs?.length) {
      setSim({
        ok: true,
        engine: labSimulate.engine || labSimulate.simulator?.backend || "ngspice",
        result: {
          Vc_peak_V: peakV,
          t_Vc_peak_s: tPeak,
          vc_trace_ms: vcMs,
          zeta: trace?.zeta,
          omega_n_rad_s: trace?.omega_n_rad_s,
        },
        problem: labSimulate.problem,
      });
      return;
    }
    setSim({
      ok: true,
      engine: labSimulate.engine || "circuit_graph_sim",
      result: { Vc_peak_V: peakV, t_Vc_peak_s: tPeak },
    });
  }

  const loadLinkedRun = useCallback(
    (force = false) => {
      if (!linkedRunId) return;
      graphReady.current = false;
      Promise.all([
        fetch(`/api/runs/${linkedRunId}/lab`).then((r) => (r.ok ? r.json() : Promise.reject())),
        fetch(`/api/runs/${linkedRunId}`).then((r) => (r.ok ? r.json() : null)),
      ])
        .then(([body, detail]) => {
          const rev = body?.lab_meta?.revision ?? 0;
          if (!force && rev <= revision.current && hydrated.current) return;
          revision.current = rev;
          const graph =
            viewMode === "agent" && body?.lab_meta?.agent_baseline_graph
              ? body.lab_meta.agent_baseline_graph
              : body?.graph || {};
          graphReady.current = Boolean(graph?.nodes?.length);
          const { nodes: n, edges: e } = toFlow(graph);
          const withMarks = showAuthorship
            ? n.map((node) => ({ ...node, className: "has-author-dot is-agent-authored" }))
            : n;
          setNodes(withMarks);
          setEdges(e);
          setLabMeta(body?.lab_meta || null);
          setLabVerify(body?.lab_verify || null);
          setRunTitle(detail?.title || linkedRunId);
          hydrated.current = true;
          setFitKey((k) => k + 1);
          const tracePts = body?.lab_simulate?.trace?.vc_trace_ms || body?.lab_simulate?.vc_trace_ms;
          if (tracePts?.length) {
            applyLabSimulate(body.lab_simulate, body.lab_verify);
          } else if (graph?.nodes?.length) {
            void runSimulate(graph);
          }
        })
        .catch(() => setMsg("Could not load shared circuit for this run."));
    },
    [linkedRunId, setEdges, setNodes, showAuthorship, viewMode],
  );

  useEffect(() => {
    if (linkedRunId) loadLinkedRun(true);
  }, [viewMode, linkedRunId, loadLinkedRun]);

  useEffect(() => {
    if (linkedRunId) {
      loadLinkedRun(true);
      const es = new EventSource(`/api/runs/${linkedRunId}/events`);
      es.onmessage = () => loadLinkedRun(false);
      return () => es.close();
    }
    if (hydrated.current) return;
    const graph = readStoredGraph() || DIVIDER_SEED;
    const { nodes: n, edges: e } = toFlow(graph);
    setNodes(n);
    setEdges(e);
    hydrated.current = true;
    return undefined;
  }, [linkedRunId, loadLinkedRun, setEdges, setNodes]);

  const snapshot = useCallback(() => {
    past.current = [...past.current, { nodes, edges }].slice(-40);
    future.current = [];
  }, [nodes, edges]);

  const persist = useCallback(
    (ns, es) => {
      const graph = fromFlow(ns, es);
      if (linkedRunId) {
        fetch(`/api/runs/${linkedRunId}/graph`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(graph),
        }).catch(() => setMsg("Could not save shared circuit."));
        return;
      }
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(graph));
      } catch {
        /* ignore */
      }
    },
    [linkedRunId],
  );

  useEffect(() => {
    if (!hydrated.current) return;
    if (linkedRunId && (!graphReady.current || nodes.length === 0)) return;
    const t = window.setTimeout(() => persist(nodes, edges), 400);
    return () => window.clearTimeout(t);
  }, [nodes, edges, persist, linkedRunId]);

  useEffect(() => {
    const el = wrapRef.current;
    if (!el) return undefined;
    const ro = new ResizeObserver(() => setFitKey((k) => k + 1));
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

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

  const onEdgeDoubleClick = useCallback(
    (event, edge) => {
      const point = screenToFlowPosition({ x: event.clientX, y: event.clientY });
      const next = splitEdgeAt(nodes, edges, edge.id, point);
      if (!next) return;
      if (next.edges.length > MAX_EDGES) {
        setMsg("16 parts or 24 wires is the cap for this lab.");
        return;
      }
      snapshot();
      setNodes(next.nodes);
      setEdges(next.edges.map((e) => ({ ...e, style: EDGE_STYLE })));
      setMsg("");
    },
    [edges, nodes, screenToFlowPosition, setEdges, setNodes, snapshot],
  );

  function addPart(type) {
    if (partCount(nodes) >= MAX_NODES) {
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

  function loadExample(id) {
    const seed = id === "divider" ? DIVIDER_SEED : EXAMPLES.find((row) => row[0] === id)?.[2];
    if (!seed) return;
    snapshot();
    const { nodes: n, edges: e } = toFlow(seed);
    setNodes(n);
    setEdges(e);
    setSim(null);
    setMsg("");
    setFitKey((k) => k + 1);
  }

  async function runSimulate(graphOverride = null) {
    setSimBusy(true);
    setMsg("");
    const graph =
      graphOverride && typeof graphOverride === "object" && graphOverride.schema
        ? graphOverride
        : fromFlow(nodes, edges);
    try {
      const r = await fetch("/api/circuit-sandbox/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ graph }),
      });
      const body = await r.json();
      if (!r.ok || !body.ok) {
        setMsg(body.error || "Simulate failed");
        setSim(null);
      } else {
        setSim(body);
      }
    } catch {
      setMsg("Could not reach the solver.");
      setSim(null);
    } finally {
      setSimBusy(false);
    }
  }

  const vcPanel = useMemo(() => {
    if (!sim?.result?.vc_trace_ms?.length) return null;
    const peakMs = 1000 * Number(sim.result.t_Vc_peak_s);
    const peakV = Number(sim.result.Vc_peak_V);
    return {
      title: "Capacitor voltage",
      x: { label: "t", unit: "ms", scale: "linear" },
      y: { label: "Vc", unit: "V", scale: "linear" },
      series: [{ id: "vc", label: "Vc", points: sim.result.vc_trace_ms, style: "primary" }],
      markers: [{ x: peakMs, label: "peak" }],
      hlines: [{ y: peakV, label: "Vc,peak" }],
    };
  }, [sim]);

  const humanEdits = (labMeta?.op_log || []).filter((e) => e.author === "human" && e.op !== "restore").length;

  async function restoreAgent() {
    if (!linkedRunId) return;
    if (!window.confirm("Replace your changes with the agent's version?")) return;
    await fetch(`/api/runs/${linkedRunId}/lab/restore`, { method: "POST" });
    loadLinkedRun(true);
  }

  function clearCanvas() {
    snapshot();
    setNodes([]);
    setEdges([]);
    setSim(null);
    setMsg("");
    setFitKey((k) => k + 1);
  }

  return (
    <div className={`lab-surface lab-surface-circuit${linkedRunId ? " has-linked-run" : ""}`}>
      {linkedRunId ? (
        <LabProvenanceBar
          runTitle={runTitle}
          problemId={linkedRunId}
          revision={labMeta?.revision}
          humanEdits={humanEdits}
          viewMode={viewMode}
          onViewMode={setViewMode}
          onBackToProblem={() => {
            window.location.href = `/?problem=${linkedRunId}`;
          }}
          onRestore={restoreAgent}
          restoreDisabled={humanEdits === 0}
        />
      ) : null}
      {linkedRunId && viewMode === "agent" ? (
        <p className="lab-agent-view-strip" role="status">
          Viewing the agent&apos;s version. Switch to Yours to keep editing.
        </p>
      ) : null}
      <div className={`studio-circuit-lab-shell${linkedRunId ? " is-collab" : ""}`}>
      <div className="cs-app control-studio studio studio-circuit-app">
        <header className="studio-bar" aria-label="Circuit toolbar">
          <div className="studio-crumb">
            <span className="breadcrumb-current">Circuit sandbox</span>
          </div>
          <div className="studio-bar-actions">
            {linkedRunId ? (
              <button
                type="button"
                className={showAuthorship ? "button-primary" : "button-secondary"}
                onClick={() => setShowAuthorship((v) => !v)}
              >
                Show authorship
              </button>
            ) : null}
            <button
              type="button"
              className="cs-btn cs-btn-primary cs-simulate-btn studio-circuit-simulate-btn"
              disabled={simBusy}
              onClick={() => runSimulate()}
            >
              {simBusy ? "Simulating…" : "Simulate"}
            </button>
          </div>
        </header>
        <Palette onAdd={addPart} disabled={simBusy} />
        <div className="studio-circuit-canvas flow-wrap" ref={wrapRef}>
          {!sim ? (
            <p className="canvas-wire-hint studio-circuit-hint">
              Drag a port onto another port. Double-click a wire to add a junction. Click a wire, then Delete, to
              remove it.
            </p>
          ) : null}
          {msg ? <p className="hint studio-circuit-msg">{msg}</p> : null}
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onEdgeDoubleClick={onEdgeDoubleClick}
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
            minZoom={0.4}
            maxZoom={1.6}
            proOptions={{ hideAttribution: true }}
          >
            <FitViewOnChange signal={fitKey} />
            <Background gap={16} color="var(--ee-color-hairline)" />
          </ReactFlow>
        </div>
        <section className="studio-results studio-circuit-results card-surface" aria-live="polite">
          {!sim ? (
            <p className="hint">Press Simulate to plot capacitor voltage Vc(t) from this netlist.</p>
          ) : (
            <>
              <div className="studio-circuit-probes" aria-label="Probe readouts">
                <span>
                  V<sub>step</sub> = {sim.problem?.v_step ?? "—"} V
                </span>
                <span>R = {sim.problem?.r_ohm ?? "—"} Ω</span>
                <span>L = {((sim.problem?.l_h ?? 0) * 1000).toFixed(1)} mH</span>
                <span>C = {((sim.problem?.c_f ?? 0) * 1e6).toFixed(0)} µF</span>
              </div>
              <p className="hint">
                Engine: {sim.engine}. ζ = {sim.result?.zeta?.toFixed(2)}, ω<sub>n</sub> ={" "}
                {sim.result?.omega_n_rad_s?.toFixed(0)} rad/s
              </p>
              <p className="answer-line">
                <span className="answer-name">Vc,peak</span>
                <span className="answer-eq"> = </span>
                <span className="answer-num tabular-nums">{Number(sim.result?.Vc_peak_V).toFixed(3)}</span>
                <span className="answer-unit"> V</span>
                <span className="hint">
                  {" "}
                  at {(1000 * Number(sim.result?.t_Vc_peak_s)).toFixed(2)} ms
                </span>
              </p>
              {vcPanel ? <Waveform panel={vcPanel} /> : null}
            </>
          )}
        </section>
      </div>
      <div className="studio-circuit-presets confirm-row">
        {EXAMPLES.map(([id, label]) => (
          <button key={id} type="button" className="button-secondary" onClick={() => loadExample(id)}>
            {label}
          </button>
        ))}
        <button type="button" className="button-secondary" onClick={clearCanvas}>
          Clear canvas
        </button>
      </div>
      {linkedRunId ? (
        <aside className="studio-lab-drawer card-surface" aria-label="Lab collaboration">
          <LabVerifyPanel labVerify={labVerify} labMeta={labMeta} compact />
          <h3>Activity</h3>
          <LabActivity labMeta={labMeta} onRestore={() => restoreAgent()} />
        </aside>
      ) : null}
      </div>
    </div>
  );
}

export function CircuitSandbox({ linkedRunId = "" }) {
  return (
    <ReactFlowProvider>
      <CircuitSandboxInner linkedRunId={linkedRunId || ""} />
    </ReactFlowProvider>
  );
}