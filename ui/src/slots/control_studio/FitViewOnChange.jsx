import { useCallback, useEffect } from "react";
import { useReactFlow } from "@xyflow/react";

const MIN_ZOOM = 0.85;
const MAX_ZOOM = 1.25;
const PAD = 24;

function contentBounds(screenToFlowPosition) {
  const sel =
    ".studio-canvas .studio-block, .studio-canvas .react-flow__edge-path, " +
    ".studio-canvas .react-flow__arrowhead, .studio-canvas .react-flow__edge circle";
  const rects = [...document.querySelectorAll(sel)]
    .map((el) => el.getBoundingClientRect())
    .filter((r) => r.width || r.height);
  if (!rects.length) return null;
  const a = screenToFlowPosition({
    x: Math.min(...rects.map((r) => r.left)),
    y: Math.min(...rects.map((r) => r.top)),
  });
  const b = screenToFlowPosition({
    x: Math.max(...rects.map((r) => r.right)),
    y: Math.max(...rects.map((r) => r.bottom)),
  });
  return { x: a.x, y: a.y, w: b.x - a.x, h: b.y - a.y };
}

export function useFitContent() {
  const { setViewport, screenToFlowPosition } = useReactFlow();
  return useCallback(
    (duration = 0) => {
      const pane = document.querySelector(".studio-canvas")?.getBoundingClientRect();
      const c = pane && contentBounds(screenToFlowPosition);
      if (!pane || !c || c.w <= 0 || c.h <= 0) return;
      const zoom = Math.min(
        MAX_ZOOM,
        Math.max(MIN_ZOOM, Math.min((pane.width - 2 * PAD) / c.w, (pane.height - 2 * PAD) / c.h)),
      );
      setViewport(
        {
          zoom,
          x: pane.width / 2 - (c.x + c.w / 2) * zoom,
          y: pane.height / 2 - (c.y + c.h / 2) * zoom,
        },
        { duration },
      );
    },
    [setViewport, screenToFlowPosition],
  );
}

export function FitViewOnChange({ revision, nodeCount, agentBump = 0, fitRef }) {
  const fit = useFitContent();
  useEffect(() => {
    if (fitRef) fitRef.current = () => fit(180);
  }, [fit, fitRef]);
  useEffect(() => {
    if (nodeCount < 1) return undefined;
    const ts = [100, 600, 1400].map((ms) => setTimeout(() => fit(ms === 100 ? 180 : 0), ms));
    return () => ts.forEach(clearTimeout);
  }, [revision, nodeCount, agentBump, fit]);
  useEffect(() => {
    const pane = document.querySelector(".studio-canvas");
    if (!pane) return undefined;
    let t;
    const ro = new ResizeObserver(() => {
      clearTimeout(t);
      t = setTimeout(() => fit(0), 120);
    });
    ro.observe(pane);
    return () => {
      ro.disconnect();
      clearTimeout(t);
    };
  }, [fit]);
  return null;
}
