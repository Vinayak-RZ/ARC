import { useEffect } from "react";
import { useReactFlow } from "@xyflow/react";

export function FitViewOnChange({ revision, nodeCount }) {
  const { fitView } = useReactFlow();
  useEffect(() => {
    const t = window.setTimeout(() => {
      fitView({ padding: 0.12, minZoom: 0.75, maxZoom: 1.85, duration: 320 });
    }, 60);
    return () => window.clearTimeout(t);
  }, [revision, nodeCount, fitView]);
  return null;
}
