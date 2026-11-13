import { useEffect } from "react";
import { useReactFlow } from "@xyflow/react";

export function FitViewOnChange({ revision, nodeCount, agentBump = 0 }) {
  const { fitView } = useReactFlow();
  useEffect(() => {
    if (nodeCount < 1) return undefined;
    let cancelled = false;
    const run = (delay) => {
      window.setTimeout(() => {
        if (cancelled) return;
        fitView({
          padding: 0.1,
          includeHiddenNodes: false,
          minZoom: 0.25,
          maxZoom: 3,
          duration: 200,
        });
      }, delay);
    };
    run(80);
    run(450);
    run(1200);
    return () => {
      cancelled = true;
    };
  }, [revision, nodeCount, agentBump, fitView]);
  return null;
}
