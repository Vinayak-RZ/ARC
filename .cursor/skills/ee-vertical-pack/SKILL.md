---
name: ee-vertical-pack
description: Installable Arc EE vertical pack — MCP, domain skills, benchmarks, optional MATLAB verifier.
---

# Arc vertical EE pack (B8)

Anthropic life-sciences style packaging for undergraduate EE: one install command bundles Arc MCP config, domain skills, specialist agents, and benchmark pointers.

## Install

From an Arc checkout (homework must not be this product repo):

```text
electrical-engineer hosts install --into /path/to/homework --host all
electrical-engineer hosts uninstall --into /path/to/homework
electrical-engineer hosts doctor
electrical-engineer hosts smoke
```

Writes:

- `.cursor/mcp.json`, `.mcp.json` (Claude), `.codex/config.toml` (Codex) with stdio `electrical-engineer mcp`
- Pack skills under each host skills dir (`arc-ee-*`)
- Twelve pack specialist agents (existing catalog)
- State file `.electrical-engineer/vertical-pack.json` for idempotent uninstall

Manifest: `hosts/pack/manifest.json`. Benchmark list: `hosts/pack/BENCHMARKS.md`.

## Domain skills (when to load)

| Domain | Skill path in repo | Engine / reference |
|--------|-------------------|-------------------|
| Power / PSA | `skills/power/`, `skills/swing-equation/`, `skills/agc-two-area/`, `skills/economic-dispatch-lambda/` | `power-network-study`, `engines/smib_swing`, `agc_two_area`, `ed_lambda` |
| Control | `skills/control/` | `run-python-control`, `lti-analysis` |
| Circuits | `skills/circuits/` | `run-spice`, lumped-circuit-sim |
| Machines | `skills/machines/` | `machine-model` |
| Power electronics | `skills/power_electronics/` | `converter-model` |
| Protection + standards | `skills/protection-standards/`, `skills/reference/` | `study-protection-setting`, `arc_reference_*` |
| Web-verify + citations | `skills/web-verify/` | workflow `web-verify`; provenance audit |

Every installed skill includes the provenance-honesty rule: no `Web-verify:` without session evidence; otherwise **unverified (from memory)** or `unchecked`.

## MATLAB (optional)

Hosts must **not** attach MATLAB MCP. Arc calls `matlab-mcp-server` inside `run-matlab-if-present` when the binary is on PATH. When absent, nodes return `unchecked` with a clear message. `hosts doctor` reports `matlab_optional` status. CI runs without MATLAB.

## Contract (CI)

```text
electrical-engineer hosts smoke
```

Emits JSON: `pack_install_smoke`, `matlab_optional` (both booleans from a real install/uninstall cycle).
