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
  seriesRlcParamsFromFlow,
  toFlow,
} from "../slots/canvas/graph.js";
import { decorateFlowNodes, diffCircuitGraphs, formatValueChip } from "../slots/canvas/graphDiff.js";
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
    { id: "vin", type: "source_v", refdes: "V1", value: 10, unit: "V", x: 56, y: 104, rot: 0 },
    { id: "r1", type: "resistor", refdes: "R1", value: 10, unit: "ohm", x: 176, y: 56, rot: 0 },
    { id: "l1", type: "inductor", refdes: "L1", value: 0.01, unit: "H", x: 296, y: 56, rot: 0 },
    { id: "c1", type: "capacitor", refdes: "C1", value: 0.0001, unit: "F", x: 416, y: 56, rot: 0 },
    { id: "gnd", type: "ground", refdes: "GND", value: 0, unit: "", x: 56, y: 220, rot: 0 },
  ],
  edges: [
    { id: "e1", from: "vin.n1", to: "r1.n1" },
    { id: "e2", from: "r1.n2", to: "l1.n1" },
    { id: "e3", from: "l1.n2", to: "c1.n1" },
    { id: "e4", from: "c1.n2", to: "gnd.n1" },
    { id: "e5", from: "vin.n2", to: "gnd.n1" },
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

const UNIT_LABEL = { ohm: "Ω", H: "H", F: "F", V: "V", A: "A" };

/** Inline value editor for the selected part (the human side of the shared lab). */
function PartValueStrip({ part, onCommit }) {
  const [text, setText] = useState(String(part.data?.value ?? ""));
  const unit = UNIT_LABEL[part.data?.unit] ?? part.data?.unit ?? "";
  const id = `part-value-${part.id}`;
  return (
    <form
      className="studio-circuit-inspector"
      aria-label={`Edit ${part.data?.refdes || part.id}`}
      onSubmit={(e) => {
        e.preventDefault();
        onCommit(part.id, text);
      }}
    >
      <label htmlFor={id}>{part.data?.refdes || part.id}</label>
      <input
        id={id}
        inputMode="decimal"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onBlur={() => onCommit(part.id, text)}
      />
      <span className="studio-circuit-inspector-unit">{unit}</span>
      <button type="submit" className="button-secondary">Apply</button>
    </form>
  );
}

/** Human label for the simulator that produced a result (never a raw engine id). */
function engineLabel(engine) {
  const id = String(engine || "").toLowerCase();
  if (id === "ngspice" || id === "circuit_graph_sim") return "Simulated with ngspice";
  if (id.includes("rk4") || id.includes("analytic") || id.includes("rlc")) return "Analytic step response";
  return "Simulated";
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
  const [linkedRunData, setLinkedRunData] = useState(null);
  const [runTitle, setRunTitle] = useState("");
  const [viewMode, setViewMode] = useState("yours");
  const [showAuthorship, setShowAuthorship] = useState(false);
  const past = useRef([]);
  const future = useRef([]);
  const hydrated = useRef(false);
  const graphReady = useRef(false);
  const revision = useRef(0);
  const autoSimForRun = useRef("");
  const simToken = useRef(0);
  const userTouched = useRef(false);
  const [wireHintOpen, setWireHintOpen] = useState(true);
  const wrapRef = useRef(null);
  const { screenToFlowPosition } = useReactFlow();

  function rlcResultHeadline(result, problem) {
    const vStep = Number(problem?.v_step ?? problem?.vin ?? 10);
    const peakV = Number(result?.Vc_peak_V);
    const noOvershoot = Number(result?.overshoot_pct ?? (peakV <= vStep * 1.005 ? 0 : 99)) < 0.5;
    if (noOvershoot) {
      const tSetMs =
        1000 *
        Number(result?.settling_2pct_entry_s ?? result?.settling_time_2pct_s ?? 0);
      return `No overshoot · Final value ${peakV.toFixed(2)} V · Settling (2%) ${tSetMs.toFixed(2)} ms`;
    }
    const tPkMs = 1000 * Number(result?.t_Vc_peak_s ?? problem?.t_s ?? 0);
    const tFmt = tPkMs.toFixed(3);
    return `Vc,peak = ${peakV.toFixed(3)} V at ${tFmt} ms`;
  }

  function applyLabSimulate(labSimulate, labVerify) {
    if (!labSimulate?.ok && !labSimulate?.simulated) return;
    const trace = labSimulate.trace || labSimulate.spice || labSimulate;
    const peakV = Number(labSimulate.simulated ?? trace?.Vc_peak_V ?? labVerify?.simulated);
    const tPeak = Number(trace?.t_Vc_peak_s ?? labSimulate.t_peak_s ?? 0);
    const vcMs = trace?.vc_trace_ms;
    const result = {
      Vc_peak_V: peakV,
      t_Vc_peak_s: tPeak,
      vc_trace_ms: vcMs,
      zeta: trace?.zeta,
      omega_n_rad_s: trace?.omega_n_rad_s,
      overshoot_pct: trace?.overshoot_pct,
      settling_2pct_entry_s: trace?.settling_2pct_entry_s ?? trace?.settling_time_2pct_s,
      settling_time_2pct_s: trace?.settling_time_2pct_s,
    };
    const problem = labSimulate.problem || labVerify?.derive || {};
    if (vcMs?.length) {
      setSim({
        ok: true,
        engine: labSimulate.engine || labSimulate.simulator?.backend || "ngspice",
        result,
        problem,
        headline: labSimulate.headline || rlcResultHeadline(result, problem),
      });
      return;
    }
    setSim({
      ok: true,
      engine: labSimulate.engine || "circuit_graph_sim",
      result,
      problem,
      headline: rlcResultHeadline(result, problem),
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
          const baseline = body?.lab_meta?.agent_seed_graph?.nodes?.length
            ? body.lab_meta.agent_seed_graph
            : body?.lab_meta?.agent_baseline_graph;
          const currentGraph = body?.graph || {};
          const graph =
            viewMode === "agent" && baseline
              ? baseline
              : currentGraph;
          graphReady.current = Boolean(graph?.nodes?.length);
          const { nodes: n, edges: e } = toFlow(graph);
          let flowNodes = n;
          if (viewMode === "changes" && baseline?.nodes?.length) {
            const diff = diffCircuitGraphs(baseline, currentGraph);
            flowNodes = decorateFlowNodes(n, diff, baseline);
          } else if (showAuthorship) {
            flowNodes = n.map((node) => ({ ...node, className: "has-author-dot is-agent-authored" }));
          }
          setNodes(flowNodes);
          setEdges(e);
          setLabMeta(body?.lab_meta || null);
          setLabVerify(body?.lab_verify || null);
          setLinkedRunData(
            detail
              ? {
                  ...detail,
                  lab: detail.lab || body?.lab_meta,
                  lab_simulate: detail.lab_simulate || body?.lab_simulate,
                }
              : null,
          );
          setRunTitle(detail?.title || "");
          hydrated.current = true;
          userTouched.current = false;
          setFitKey((k) => k + 1);
          const tracePts = body?.lab_simulate?.trace?.vc_trace_ms || body?.lab_simulate?.vc_trace_ms;
          if (tracePts?.length) {
            applyLabSimulate(body.lab_simulate, body.lab_verify);
          } else if (graph?.nodes?.length && autoSimForRun.current !== linkedRunId) {
            autoSimForRun.current = linkedRunId;
            void runSimulate(graph, { silent: true });
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
      es.onmessage = (ev) => {
        let data = {};
        try {
          data = JSON.parse(ev.data || "{}");
        } catch {
          data = {};
        }
        if (data.type === "hello" || data.type === "heartbeat") return;
        // Disk events come from an agent in another process (MCP); verify and simulate
        // results can change without a new revision, so always reload those.
        loadLinkedRun(data.source === "disk");
      };
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
      if (linkedRunId && !userTouched.current) return;
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

  const onNodesChangeWrapped = useCallback(
    (changes) => {
      if (hydrated.current && changes.some((c) => c.type === "position" || c.type === "remove" || c.type === "add")) {
        userTouched.current = true;
      }
      onNodesChange(changes);
    },
    [onNodesChange],
  );

  useEffect(() => {
    if (!hydrated.current) return;
    if (linkedRunId && (!graphReady.current || nodes.length === 0)) return;
    if (linkedRunId && !userTouched.current) return;
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
      userTouched.current = true;
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

  async function runSimulate(graphOverride = null, options = {}) {
    const silent = Boolean(options.silent);
    const token = (simToken.current += 1);
    if (!silent) setSimBusy(true);
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
        if (silent) {
          // Background auto-run on a circuit someone is still wiring: stay quiet and
          // try again on the next lab update instead of leaving a stale error.
          autoSimForRun.current = "";
        } else {
          setMsg(body.error || "Simulate failed");
        }
        setSim(null);
      } else {
        const params = seriesRlcParamsFromFlow(nodes, edges);
        if (params) {
          body.problem = { ...(body.problem || {}), ...params };
        }
        if (!body.headline && body.result) {
          body.headline = rlcResultHeadline(body.result, body.problem || params);
        }
        setSim(body);
        if (linkedRunId) {
          const vr = await fetch(`/api/runs/${linkedRunId}/lab/verify`, { method: "POST" });
          if (vr.ok) {
            const payload = await vr.json();
            setLabVerify(payload.lab_verify || null);
            const labSim = payload.lab_verify?.simulate;
            const labTrace = labSim?.trace || labSim;
            if (labTrace?.vc_trace_ms?.length) {
              applyLabSimulate(labSim, payload.lab_verify);
            }
          }
        }
      }
    } catch {
      setMsg("Could not reach the solver.");
      setSim(null);
    } finally {
      if (!silent && token === simToken.current) setSimBusy(false);
    }
  }

  const selectedPart = nodes.find((n) => n.selected && n.data?.kind && n.data.kind !== "ground" && n.data.kind !== "junction");

  const commitPartValue = useCallback(
    (nodeId, raw) => {
      const v = Number(String(raw).trim());
      if (!Number.isFinite(v) || v <= 0) {
        setMsg("Enter a positive number.");
        return;
      }
      const cur = nodes.find((n) => n.id === nodeId);
      if (!cur || Number(cur.data?.value) === v) return;
      snapshot();
      userTouched.current = true;
      const next = nodes.map((n) => (n.id === nodeId ? { ...n, data: { ...n.data, value: v } } : n));
      setNodes(next);
      setMsg("");
      persist(next, edges);
    },
    [nodes, edges, persist, setNodes, snapshot],
  );

  const diffChips = useMemo(() => {
    // "Agent's version" everywhere (bar pill, Changes, Agent's, Restore) is the agent's
    // original build; a re-derive on the human's edit must not erase the edit from Changes.
    const agentVersion = labMeta?.agent_seed_graph?.nodes?.length
      ? labMeta.agent_seed_graph
      : labMeta?.agent_baseline_graph;
    if (viewMode !== "changes" || !agentVersion) return [];
    const diff = diffCircuitGraphs(agentVersion, fromFlow(nodes, edges));
    return (diff.changed || []).map(formatValueChip);
  }, [viewMode, labMeta, nodes, edges]);

  const probeParams = useMemo(() => {
    const fromGraph = seriesRlcParamsFromFlow(nodes, edges);
    if (fromGraph) return fromGraph;
    return sim?.problem || {};
  }, [nodes, edges, sim?.problem]);

  const vcPanel = useMemo(() => {
    if (!sim?.result?.vc_trace_ms?.length) return null;
    const peakV = Number(sim.result.Vc_peak_V);
    const vStep = Number(probeParams.v_step ?? probeParams.vin ?? 10);
    const noOvershoot = Number(sim.result?.overshoot_pct ?? (peakV <= vStep * 1.005 ? 0 : 99)) < 0.5;
    const peakMs = 1000 * Number(sim.result.t_Vc_peak_s);
    const settleMs =
      1000 *
      Number(sim.result.settling_2pct_entry_s ?? sim.result.settling_time_2pct_s ?? sim.result.t_Vc_peak_s ?? 0);
    const tMax = Math.min(Math.max(5 * settleMs, peakMs * 1.2, 8), 80);
    const raw = sim.result.vc_trace_ms.filter(([t]) => t <= tMax);
    const step = Math.max(1, Math.ceil(raw.length / 3500));
    const points = step > 1 ? raw.filter((_, i) => i % step === 0) : raw;
    return {
      title: "Capacitor voltage",
      x: { label: "t", unit: "ms", scale: "linear" },
      y: { label: "Vc", unit: "V", scale: "linear" },
      series: [{ id: "vc", label: "Vc", points, style: "primary" }],
      markers: noOvershoot ? [] : [{ x: peakMs, label: "peak" }],
      hlines: [{ y: noOvershoot ? vStep : peakV, label: noOvershoot ? "Vc,final" : "Vc,peak" }],
    };
  }, [sim, probeParams]);

  const humanEdits = useMemo(() => {
    const seed = labMeta?.agent_seed_graph;
    if (seed?.nodes?.length) {
      const cur = fromFlow(nodes, edges);
      const diff = diffCircuitGraphs(seed, cur);
      if (!(diff.changed || []).length) return 0;
    }
    return (labMeta?.op_log || []).filter(
      (e) => e.author === "human" && e.op !== "restore" && e.electrical !== false,
    ).length;
  }, [labMeta, nodes, edges]);

  async function askAgentReDerive() {
    if (!linkedRunId) return;
    setMsg("");
    try {
      const r = await fetch(`/api/runs/${linkedRunId}/lab/re-derive`, { method: "POST" });
      const body = await r.json();
      if (!r.ok) {
        setMsg(body.error || "Re-derive failed");
        return;
      }
      setLabVerify(body.lab_verify || null);
      loadLinkedRun(true);
    } catch {
      setMsg("Could not reach re-derive.");
    }
  }

  async function restoreAgent() {
    if (!linkedRunId) return;
    if (!window.confirm("Replace your changes with the agent's version?")) return;
    setMsg("");
    try {
      const r = await fetch(`/api/runs/${linkedRunId}/lab/restore`, { method: "POST" });
      const body = await r.json();
      if (!r.ok) {
        setMsg(body.error || "Restore failed");
        return;
      }
      setLabVerify(body.lab_verify || null);
      setViewMode("yours");
      userTouched.current = false;
      loadLinkedRun(true);
      if (body.lab_verify?.simulate?.trace?.vc_trace_ms?.length) {
        applyLabSimulate(body.lab_verify.simulate, body.lab_verify);
      } else {
        void runSimulate(null, { silent: true });
      }
    } catch {
      setMsg("Could not restore agent version.");
    }
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
      {linkedRunId && viewMode === "changes" && diffChips.length ? (
        <div className="lab-changes-chip-row" role="status">
          {diffChips.map((chip) => (
            <span key={chip} className="lab-changes-chip">
              {chip}
            </span>
          ))}
        </div>
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
              onClick={() => runSimulate(null, { silent: false })}
            >
              {simBusy ? "Simulating…" : "Simulate"}
            </button>
          </div>
        </header>
        <Palette onAdd={addPart} disabled={simBusy} />
        <div className="studio-circuit-canvas flow-wrap" ref={wrapRef}>
          {selectedPart ? (
            <PartValueStrip key={`${selectedPart.id}:${selectedPart.data?.value}`} part={selectedPart} onCommit={commitPartValue} />
          ) : null}
          {wireHintOpen && !sim ? (
            <p className="hint studio-circuit-hint studio-canvas-hint">
              Drag ports to wire. Double-click a wire for a junction.
              <button type="button" className="text-link" onClick={() => setWireHintOpen(false)}>
                Dismiss
              </button>
            </p>
          ) : null}
          {msg ? <p className="hint studio-circuit-msg">{msg}</p> : null}
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChangeWrapped}
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
            <p className="hint">Press Simulate to plot capacitor voltage Vc(t).</p>
          ) : (
            <>
              {sim.param_strip ? (
                <div className="studio-circuit-probes studio-circuit-param-strip" aria-label="Probe readouts">
                  {sim.param_strip}
                </div>
              ) : null}
              <p className="hint">
                {engineLabel(sim.engine)}
                {Number.isFinite(sim.result?.zeta) && Number.isFinite(sim.result?.omega_n_rad_s) ? (
                  <>
                    {" "}· ζ = {sim.result.zeta.toFixed(2)}, ω<sub>n</sub> = {sim.result.omega_n_rad_s.toFixed(0)} rad/s
                  </>
                ) : null}
              </p>
              <p className="answer-line tabular-nums">
                {sim.headline || rlcResultHeadline(sim.result, sim.problem)}
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
          <LabVerifyPanel
            runId={linkedRunId}
            runData={linkedRunData}
            labVerify={labVerify}
            labMeta={labMeta}
            compact
            onAskAgent={linkedRunId ? () => void askAgentReDerive() : undefined}
            onReRun={linkedRunId ? () => void runSimulate(null, { silent: false }) : undefined}
            onAcceptSimulated={
              linkedRunId
                ? async () => {
                    await fetch(`/api/runs/${linkedRunId}/lab/accept-simulated`, { method: "POST" });
                    loadLinkedRun(true);
                  }
                : undefined
            }
          />
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