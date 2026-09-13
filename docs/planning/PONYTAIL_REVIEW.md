# Ponytail review — D19/D20 branch

Readonly over-engineering review of `cursor/d19-loop-graph-572f` vs H1 freeze. Correctness is out of scope.

## Findings

- `ui/src/slots/root.jsx` Band: unused `json` prop. delete: drop the argument; `<pre>` already dumps the string.
- `ui/src/slots/root.jsx` useRun: five slots refetch `/api/runs/:id`. shrink: fetch once in Workspace and pass `data`.
- `src/electrical_engineer/mcp/server.py` `_graph_recipe`: bind loop duplicates `compose()`. yagni: return a Recipe from `compose` / a shared `bound_nodes()` helper.
- `src/electrical_engineer/runner/execute.py` `_UNCHECKED_REASONS`: tuple unused. delete or `assert reason in _UNCHECKED_REASONS`.
- `src/electrical_engineer/mcp/server.py` TOOLS: `run_workflow` plus `simulate_attachment` overlap. yagni: keep both this graph (rollback vs host path); do not add `clarify`/`summary` as extra list entries.

P0-blocking for M1: none. Public bind export is the integrate seam, not a deletion.

`net: ~40 lines possible.`
