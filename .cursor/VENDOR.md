# Vendored Cursor coding config

Source: https://github.com/Vinayak-RZ/cursor-config-coding
Commit: 280dbc5cb9c99de5ee33bee0e0d5d6f589ba4fa8
Vendored: 2026-09-10

Overlay: `.cursor/skills/graph-of-loops/` from coding-config
`1b303c3fc575bc7cdb57689b89b8484e48f03d84` (2026-09-13). XOR with
`graph-engineering`. Product `AGENTS.md` is not replaced by the coding-config
index.

Cloud Agents load `.cursor/rules` and `.cursor/skills` from this repository.
Do not symlink to an external clone; keep the files in git history.

Supporting docs: `docs/cursor-config/`
Helper scripts: `scripts/cursor-config/`
Manifest: `skills-manifest.json`

This pin is the 2026 config audit (PR #1): nawab **lite** default, three
always-on rule stubs, Spec Kit **v1.0.6**, opt-in `graph-engineering`, plus
this overlay of opt-in `graph-of-loops`.
Keep Arc overlays here: `VENDOR.md`, `environment.json`,
and root `AGENTS.md` (product notes — do not replace with the coding-config
index).
