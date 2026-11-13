import { useEffect } from "react";
import { useNodesInitialized, useReactFlow } from "@xyflow/react";

export function FitViewOnChange({ revision, nodeCount, agentBump = 0 }) {
  const { fitView } = useReactFlow();
  const ready = useNodesInitialized();
  useEffect(() => {
    if (!ready || nodeCount < 1) return undefined;
    const t = window.setTimeout(() => {
      fitView({
        padding: 0.12,
        includeHiddenNodes: false,
        minZoom: 0.6,
        maxZoom: 1.05,
        duration: 300,
      });
    }, 50);
    return () => window.clearTimeout(t);
  }, [ready, revision, nodeCount, agentBump, fitView]);
  return null;
}
