import { useEffect } from "react";
import { useReactFlow } from "@xyflow/react";

const WIDTH_FILL = 0.8;
const HEIGHT_FILL = 0.6;
const ZOOM_FUDGE = 0.97;

export function FitViewOnChange({ revision, nodeCount, agentBump = 0 }) {
  const { getNodes, getNodesBounds, setViewport } = useReactFlow();
  useEffect(() => {
    if (nodeCount < 1) return undefined;
    let cancelled = false;
    const fit = () => {
      const pane = document.querySelector(".studio-canvas .react-flow__pane");
      const nodes = getNodes();
      if (!pane || !nodes.length) return;
      const bounds = getNodesBounds(nodes);
      if (!bounds?.width || !bounds?.height) return;
      const { width: pw, height: ph } = pane.getBoundingClientRect();
      const zoom = Math.min((pw * WIDTH_FILL) / bounds.width, (ph * HEIGHT_FILL) / bounds.height, 3.5) * ZOOM_FUDGE;
      const clamped = Math.max(zoom, 0.3);
      const cx = bounds.x + bounds.width / 2;
      const cy = bounds.y + bounds.height / 2;
      setViewport(
        {
          x: pw / 2 - cx * clamped,
          y: ph / 2 - cy * clamped,
          zoom: clamped,
        },
        { duration: 200 },
      );
    };
    const run = (delay) => window.setTimeout(() => !cancelled && fit(), delay);
    const t1 = run(80);
    const t2 = run(450);
    const t3 = run(1200);
    return () => {
      cancelled = true;
      window.clearTimeout(t1);
      window.clearTimeout(t2);
      window.clearTimeout(t3);
    };
  }, [revision, nodeCount, agentBump, getNodes, getNodesBounds, setViewport]);
  return null;
}
