import { useEffect } from "react";
import { useReactFlow } from "@xyflow/react";

const WIDTH_FILL = 0.92;

function measureBlockSpan() {
  const pane = document.querySelector(".studio-canvas .react-flow__pane");
  if (!pane) return null;
  const pr = pane.getBoundingClientRect();
  const blocks = [...document.querySelectorAll(".react-flow__node .studio-block")];
  if (!blocks.length) return null;
  let minL = Infinity;
  let maxR = -Infinity;
  let minT = Infinity;
  let maxB = -Infinity;
  for (const n of blocks) {
    const r = n.getBoundingClientRect();
    minL = Math.min(minL, r.left);
    maxR = Math.max(maxR, r.right);
    minT = Math.min(minT, r.top);
    maxB = Math.max(maxB, r.bottom);
  }
  return {
    paneW: pr.width,
    paneH: pr.height,
    spanW: maxR - minL,
    spanH: maxB - minT,
    midX: (minL + maxR) / 2,
    midY: (minT + maxB) / 2,
  };
}

export function FitViewOnChange({ revision, nodeCount, agentBump = 0 }) {
  const { getViewport, setCenter, screenToFlowPosition } = useReactFlow();
  useEffect(() => {
    if (nodeCount < 1) return undefined;
    let cancelled = false;
    const fitToScreenWidth = (attempt) => {
      if (cancelled) return;
      const m = measureBlockSpan();
      if (!m || m.spanW <= 0 || m.paneW <= 0) return;
      const ratio = m.spanW / m.paneW;
      if (ratio >= WIDTH_FILL * 0.97 && ratio <= WIDTH_FILL * 1.03) return;
      const vp = getViewport();
      const target = m.paneW * WIDTH_FILL;
      const scale = target / m.spanW;
      const newZoom = Math.min(Math.max(vp.zoom * scale, 0.85), 1.25);
      const flow = screenToFlowPosition({ x: m.midX, y: m.midY });
      setCenter(flow.x, flow.y, { zoom: newZoom, duration: attempt === 0 ? 180 : 0 });
      if (attempt < 8) {
        window.setTimeout(() => fitToScreenWidth(attempt + 1), 120);
      }
    };
    const t0 = window.setTimeout(() => fitToScreenWidth(0), 100);
    const t1 = window.setTimeout(() => fitToScreenWidth(0), 600);
    const t2 = window.setTimeout(() => fitToScreenWidth(0), 1400);
    return () => {
      cancelled = true;
      window.clearTimeout(t0);
      window.clearTimeout(t1);
      window.clearTimeout(t2);
    };
  }, [revision, nodeCount, agentBump, getViewport, setCenter, screenToFlowPosition]);
  return null;
}
