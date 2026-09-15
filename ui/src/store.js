import { create } from "zustand";

export const useLayout = create((set) => ({
  currentRunId: null,
  view: "runs",
  graphDirty: false,
  selectedNodeId: null,
  capMessage: "",
  flowNodes: [],
  flowEdges: [],
  inspectorEpoch: 0,
  setRun: (id) =>
    set({
      currentRunId: id,
      view: "runs",
      graphDirty: false,
      selectedNodeId: null,
      capMessage: "",
      flowNodes: [],
      flowEdges: [],
    }),
  setView: (view) => set({ view }),
  setGraphDirty: (graphDirty) => set({ graphDirty }),
  setSelectedNodeId: (selectedNodeId) => set({ selectedNodeId }),
  setCapMessage: (capMessage) => set({ capMessage }),
  setFlow: (flowNodes, flowEdges) => set({ flowNodes, flowEdges }),
  applyPartPatch: (id, patch) =>
    set((s) => ({
      flowNodes: s.flowNodes.map((n) =>
        n.id === id ? { ...n, data: { ...n.data, ...patch } } : n,
      ),
      graphDirty: true,
      inspectorEpoch: s.inspectorEpoch + 1,
    })),
}));
