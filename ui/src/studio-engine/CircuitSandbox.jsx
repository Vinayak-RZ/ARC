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

const EDGE_STYLE = { stroke: "var(--ee-color-ink)", strokeWidth: 1.5 };
const GRID = 16;
const STORAGE_KEY = "arc-circuit-sandbox-v1";

const SERIES_RLC = {
  schema: "arc.circuit.v1",
  nodes: [
    { id: "vin", type: "source_v", refdes: "V1", value: 10, unit: "V", x: 40, y: 120, rot: 0 },
    { id: "r1", type: "resistor", refdes: "R1", value: 10, unit: "ohm", x: 180, y: 40, rot: 0 },
    { id: "l1", type: "inductor", refdes: "L1", value: 0.01, unit: "H", x: 320, y: 40, rot: 0 },
    { id: "c1", type: "capacitor", refdes: "C1", value: 0.0001, unit: "F", x: 460, y: 120, rot: 90 },
    { id: "jret", type: "junction", refdes: "", value: 0, unit: "", x: 24, y: 188, rot: 0 },
    { id: "gnd", type: "ground", refdes: "Gnd", value: 0, unit: "", x: 40, y: 220, rot: 0 },
  ],
  edges: [
    { id: "e1", from: "vin.n1", to: "r1.n1" },
    { id: "e2", from: "r1.n2", to: "l1.n1" },
    { id: "e3", from: "l1.n2", to: "c1.n1" },
    { id: "e4", from: "c1.n2", to: "gnd.n1" },
    { id: "e5", from: "vin.n2", to: "jret.w" },
    { id: "e5b", from: "jret.e", to: "gnd.n1" },
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

function CircuitSandboxInner() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [msg, setMsg] = useState("");
  const [fitKey, setFitKey] = useState(0);
  const [sim, setSim] = useState(null);
  const [simBusy, setSimBusy] = useState(false);
  const past = useRef([]);
  const future = useRef([]);
  const hydrated = useRef(false);
  const wrapRef = useRef(null);
  const { screenToFlowPosition } = useReactFlow();

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

  async function runSimulate() {
    setSimBusy(true);
    setMsg("");
    const graph = fromFlow(nodes, edges);
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

  function clearCanvas() {
    snapshot();
    setNodes([]);
    setEdges([]);
    setSim(null);
    setMsg("");
    setFitKey((k) => k + 1);
  }

  return (
    <div className="lab-surface lab-surface-circuit">
      <div className="canvas-lab studio-circuit-sandbox">
        <div className="studio-circuit-toolbar">
          <Palette onAdd={addPart} />
          <button
            type="button"
            className="cs-btn cs-btn-primary cs-simulate-btn studio-circuit-simulate-btn"
            disabled={simBusy}
            onClick={runSimulate}
          >
            {simBusy ? "Simulating…" : "Simulate"}
          </button>
        </div>
        <p className="canvas-wire-hint studio-circuit-hint">
          Drag a port onto another port. Double-click a wire to add a junction. Click a wire, then Delete, to remove it.
        </p>
        <div className="flow-wrap" ref={wrapRef}>
          {msg ? <p className="hint">{msg}</p> : null}
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
        <section className="studio-circuit-results card-surface" aria-live="polite">
          {!sim ? (
            <p className="hint">Press Simulate to see the step response (built-in RLC solver).</p>
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
        <div className="confirm-row">
          {EXAMPLES.map(([id, label]) => (
            <button key={id} type="button" className="button-secondary" onClick={() => loadExample(id)}>
              {label}
            </button>
          ))}
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