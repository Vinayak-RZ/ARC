import { useEffect } from "react";
import { useReactFlow } from "@xyflow/react";

export function FitViewOnChange({ revision, nodeCount }) {
  const { fitView } = useReactFlow();
  useEffect(() => {
    const t = window.setTimeout(() => {
      fitView({ padding: 0.22, includeHiddenNodes: false, minZoom: 0.5, maxZoom: 1.35, duration: 350 });
    }, 120);
    return () => window.clearTimeout(t);
  }, [revision, nodeCount, fitView]);
  return null;
}
