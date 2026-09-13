# Design lock — closed

Status: **closed** (2026-09-10). Visual authority for the persistent localhost UI.

**Source of tokens:** [`docs/design/DESIGN-coinbase.md`](../design/DESIGN-coinbase.md) (vendored analysis; EE front-matter).  
**ADR seed:** [`DECISIONS.md`](../../DECISIONS.md) ADR-0008 (proposed; A1 accepts on Wave 0).  
**Node owners:** [U1](../../plans/nodes/U1.md) token map · [B_UI](../../plans/nodes/B_UI.md) CSS vars · [T1](../../plans/nodes/T1.md) chrome trial · [D1](../../plans/nodes/D1.md) / [H1](../../plans/nodes/H1.md) docs + static checks.

This lock does **not** start product `ui/` or Wave 0. Execution starts only when the owner says start / build / implement after reviewing the master graph.

## Contract

- White canvas `#ffffff`, ink `#0a0b0d`, scarce primary `#0052ff` (pills, 2px focus, inline links).
- Display weight 400. Numbers in mono (`number-display`). CTAs pill 44px. Cards `rounded.xl` 24px. One shadow tier + hairline.
- Fonts: Inter (display+body) + JetBrains Mono or Geist Mono. Never Coinbase Display/Sans/Mono/Icons or the Coinbase wordmark.
- Optional `surface-dark` only for the current-run hero — not a global dark theme.
- `unchecked` → `badge-pill`. Checked/failed numbers → semantic-up/down **text only**. Confirm → `button-primary`. Run list → `asset-row`.
- Workspace uses the token spacing scale. Do not apply 96px marketing section padding to chrome rows.
- CSS variables + CSS modules. No MUI/Ant/Tailwind-as-architecture. No GSAP marketing scroll.
- Treat DESIGN-coinbase as the DESIGN.md equivalent. Do not run `impeccable teach` to invent a second system.
- Header chrome identity is the Arc icon (`assets/brand/arc-icon.png`, served as `/arc-icon.png`). Do not use Coinbase wordmark.

## Non-goals

Coinbase marketing clone, licensed Coinbase fonts, second brand color, green/red CTA fills, image generation UI, Cordis/DSH runtime.
