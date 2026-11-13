# Node plan: B8: vertical EE pack

| Field | Value |
|-------|-------|
| **Node id** | `B8` |
| **Job** | Frontier skill bundle + MCP smoke + optional MATLAB provider |
| **Wave** | 3 |
| **Depends on (data)** | `capability_delta_spec`, Gate 0 Q4 |
| **Write paths** | `skills/**`, `hosts/adapters/**`, `.cursor/mcp.json`, `pyproject.toml` extras |
| **Model** | inherit |

## Objective

Anthropic life-sciences style packaging: connectors + skills + benchmarks pointers (report #01).

## Contract

**Output:** `{ "pack_install_smoke": true, "matlab_optional": true }`

## Commits

| # | Commit | Gate |
|---|--------|------|
| 23-24 | skill bundle, MATLAB wire | `hosts install` smoke |
