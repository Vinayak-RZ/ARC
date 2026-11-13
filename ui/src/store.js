import { create } from "zustand";

const SIDEBAR_KEY = "arc-sidebar-collapsed";

function readSidebarCollapsed() {
  try {
    return localStorage.getItem(SIDEBAR_KEY) === "1";
  } catch {
    return false;
  }
}

function writeSidebarCollapsed(collapsed) {
  try {
    localStorage.setItem(SIDEBAR_KEY, collapsed ? "1" : "0");
  } catch {
    /* ignore */
  }
}

export function normalizeView(view) {
  if (view === "runs") return "problems";
  if (view === "control-studio") return "studio";
  return view;
}

export const useLayout = create((set) => ({
  currentRunId: null,
  view: "home",
  sidebarCollapsed: readSidebarCollapsed(),
  themeMode: "system",
  commandOpen: false,
  parametersOpen: false,
  parametersStale: false,
  problemTab: "work",
  graphDirty: false,
  selectedNodeId: null,
  capMessage: "",
  flowNodes: [],
  flowEdges: [],
  inspectorEpoch: 0,
  setRun: (id) =>
    set({
      currentRunId: id,
      view: "problems",
      graphDirty: false,
      selectedNodeId: null,
      capMessage: "",
      flowNodes: [],
      flowEdges: [],
      parametersOpen: false,
      parametersStale: false,
    }),
  setParametersStale: (parametersStale) => set({ parametersStale }),
  setView: (view) => set({ view: normalizeView(view) }),
  toggleSidebar: () =>
    set((s) => {
      const sidebarCollapsed = !s.sidebarCollapsed;
      writeSidebarCollapsed(sidebarCollapsed);
      return { sidebarCollapsed };
    }),
  setSidebarCollapsed: (sidebarCollapsed) => {
    writeSidebarCollapsed(sidebarCollapsed);
    set({ sidebarCollapsed });
  },
  setThemeMode: (themeMode) => set({ themeMode }),
  setCommandOpen: (commandOpen) => set({ commandOpen }),
  setParametersOpen: (parametersOpen) => set({ parametersOpen }),
  setProblemTab: (problemTab) => set({ problemTab }),
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
