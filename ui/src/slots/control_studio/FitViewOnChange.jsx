import { useCallback, useEffect } from "react";
import { useNodesInitialized, useReactFlow } from "@xyflow/react";

const MIN_ZOOM = 0.85;
const MAX_ZOOM = 1.25;

export function useFitContent() {
  const { fitView, getEdges } = useReactFlow();
  return useCallback(
    (duration = 0) => {
      const edgeCount = getEdges().length;
      if (edgeCount < 1) return;
      fitView({ padding: 0.14, duration, minZoom: MIN_ZOOM, maxZoom: MAX_ZOOM, includeHiddenNodes: false });
    },
    [fitView, getEdges],
  );
}

export function FitViewOnChange({ revision, nodeCount, agentBump = 0, fitRef }) {
  const fit = useFitContent();
  const { getEdges } = useReactFlow();
  const nodesReady = useNodesInitialized();

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

  useEffect(() => {
    const pane = document.querySelector(".studio-canvas");
    if (!pane) return undefined;
    let t;
    const ro = new ResizeObserver(() => {
      clearTimeout(t);
      t = setTimeout(() => fit(0), 450);
    });
    ro.observe(pane);
    return () => {
      ro.disconnect();
      clearTimeout(t);
    };
  }, [fit]);

  return null;
}
