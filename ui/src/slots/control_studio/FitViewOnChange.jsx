import { useEffect } from "react";
import { useNodesInitialized, useReactFlow } from "@xyflow/react";

export function FitViewOnChange({ revision, nodeCount, agentBump = 0 }) {
  const { fitView } = useReactFlow();
  const ready = useNodesInitialized();
  useEffect(() => {
    if (!ready || nodeCount < 1) return undefined;
    const t = window.setTimeout(() => {
      fitView({
        padding: 0.1,
        includeHiddenNodes: false,
        minZoom: 0.35,
        maxZoom: 2.2,
        duration: 300,
      });
    }, 50);
    return () => window.clearTimeout(t);
  }, [ready, revision, nodeCount, agentBump, fitView]);
  return null;
}
