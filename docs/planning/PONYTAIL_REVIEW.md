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

---

# Ponytail review — skills / MATLAB graph

Scope: `cursor/ee-skills-matlab-mcp-37b3` vs `main`. Complexity only.

## Findings

- `src/electrical_engineer/matlab_mcp.py`: keep NDJSON stdio. Do not add the `mcp` PyPI SDK (stdlib `json` + `subprocess` is the stop).
- `src/electrical_engineer/hosts_install.py`: keep one body + per-pack files. Do not grow a Python specialist runtime.
- `tests/fixtures/fake_matlab_mcp.py`: keep. A live MATLAB binary is not a CI dep.
- `skills/<pack>/SKILL.md` retrieve scaffold: keep headings empty. Do not dump `knowledge/` chapters into skills.

No extra abstraction to delete this pass. HINTS in `hosts_install.py` exist so Task pickers see pack keywords.

Lean already. Ship.

net: -0 lines possible without dropping a Gate 0 requirement.
