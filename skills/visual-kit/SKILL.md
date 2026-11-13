---
name: visual-kit
description: Arc Visual Kit registry and engine-bound figure render.
---

# Arc Visual Kit

Numeric labels on figures must come from Arc engines, not free text.

1. List components: MCP `list_visual_components` or read `src/electrical_engineer/visual_kit/manifest.json`.
2. Render: MCP `render_visual` with `component_id` and optional engine props.
3. PSA P0 ids: `power.swing_equal_area`, `power.agc_trace`, `power.dispatch_curve`.

Artifacts land under the run directory as PNG paths in the tool response.
