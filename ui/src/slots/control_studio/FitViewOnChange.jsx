import { useCallback, useEffect } from "react";
import { useNodesInitialized, useReactFlow, useUpdateNodeInternals } from "@xyflow/react";

const MIN_ZOOM = 0.85;
const MAX_ZOOM = 1.25;

export function useFitContent() {
  const { fitView, getEdges } = useReactFlow();
  return useCallback(
    (duration = 0) => {
      const edgeCount = getEdges().length;
      if (edgeCount < 1) return;
      fitView({ padding: 0.1, duration, minZoom: MIN_ZOOM, maxZoom: MAX_ZOOM, includeHiddenNodes: false });
    },
    [fitView, getEdges],
  );
}

export function FitViewOnChange({ revision, nodeCount, agentBump = 0, nodesEpoch = 0, fitRef }) {
  const fit = useFitContent();
  const { getEdges, getNodes } = useReactFlow();
  const updateNodeInternals = useUpdateNodeInternals();
  const nodesReady = useNodesInitialized();

  // Replacing the node objects (initial paint, validation resync) makes React Flow drop the
  // handle bounds it measured. The DOM size is unchanged, so nothing re-measures them and every
  // wire stays undrawn (seen in about 1 in 40 page loads). Re-measure after each replacement.
  useEffect(() => {
    if (!nodesEpoch) return undefined;
    const id = requestAnimationFrame(() => updateNodeInternals(getNodes().map((n) => n.id)));
    return () => cancelAnimationFrame(id);
  }, [nodesEpoch, getNodes, updateNodeInternals]);

  useEffect(() => {
    if (fitRef) fitRef.current = () => fit(180);
  }, [fit, fitRef]);

  useEffect(() => {
    if (!nodesReady || nodeCount < 1) return undefined;
    let cancelled = false;
    let tries = 0;
    const pump = () => {
      if (cancelled) return;
      const want = getEdges().length;
      const got = document.querySelectorAll(".studio-canvas .react-flow__edge-path").length;
      if (want > 0 && got >= want) {
        fit(tries === 0 ? 180 : 0);
        return;
      }
      tries += 1;
      if (tries < 120) requestAnimationFrame(pump);
    };
    const start = requestAnimationFrame(pump);
    return () => {
      cancelled = true;
      cancelAnimationFrame(start);
    };
  }, [revision, nodeCount, agentBump, nodesReady, fit, getEdges]);

  const remeasureAndFit = useCallback(() => {
    const ids = getNodes().map((n) => n.id);
    if (ids.length) updateNodeInternals(ids);
    let cancelled = false;
    let tries = 0;
    const pump = () => {
      if (cancelled) return;
      const want = getEdges().length;
      const got = document.querySelectorAll(".studio-canvas .react-flow__edge-path").length;
      if (want > 0 && got >= want) {
        fit(0);
        return;
      }
      tries += 1;
      if (tries < 120) requestAnimationFrame(pump);
      else if (want > 0) fit(0);
    };
    requestAnimationFrame(pump);
    return () => {
      cancelled = true;
    };
  }, [fit, getEdges, getNodes, updateNodeInternals]);

  useEffect(() => {
    const pane = document.querySelector(".studio-canvas");
    if (!pane) return undefined;
    let t;
    let cancelPump = () => {};
    const schedule = () => {
      clearTimeout(t);
      cancelPump();
      t = setTimeout(() => {
        cancelPump = remeasureAndFit() || (() => {});
      }, 80);
    };
    const ro = new ResizeObserver(schedule);
    ro.observe(pane);
    window.addEventListener("resize", schedule);
    return () => {
      ro.disconnect();
      window.removeEventListener("resize", schedule);
      clearTimeout(t);
      cancelPump();
    };
  }, [remeasureAndFit]);

  return null;
}
