# Design critique — round 1

**Score:** 25/50 (threshold for polish: 30)

Structure before polish. Round 2 addresses trust, work narrative, Studio workbench, diagram container, shell geometry, home tiles, problem header, tokens, Cmd+K, lists, secondary pages, and figure theming.

## Prioritised fixes (in order)

### 1. Trust bugs on the problem page

- The drawer fields must show the same value and unit as the Inputs card. Today R1 reads `1.000 Ω` against `1000 Ω`; display `1` with a `kΩ` suffix, or `1000` with `Ω`, never `1.000 Ω`.
- Parameter inputs are 36px high with 0 12px padding, and the unit is a right-aligned suffix inside the input (`--text-secondary`).
- Remove `· unchecked` from the solve step. When the badge says Checked, no step may say unchecked. Step copy: "Solved with Kirchhoff's laws", "Checked with SPICE".

### 2. Work tab: replace the event dump with a step timeline

- Hide run.start, node.start and node.end entirely. Put them in one collapsed monospace "Diagnostics" disclosure at the bottom of the Activity tab.
- Steps are 40px rows: 20px index circle, heading 14/22 600, one-line result in `--text-secondary`, author tag (Agent, Human or Engine), chevron to expand.
- Example steps: "Read the circuit", "Write the divider equation", "Substitute values", "Check with SPICE".
- Typeset equations with subscripts, e.g. V<sub>out</sub> = V<sub>in</sub> R<sub>2</sub> / (R<sub>1</sub> + R<sub>2</sub>).

### 3. Rebuild Studio as a workbench

- Layout: 44px toolbar, collapsible 220px palette, full-bleed canvas, 280px inspector on selection, 280px results drawer at bottom.
- Delete "Control Studio" title, session id, "Live sync (SSE)". Banner becomes results drawer empty state.
- Blocks: 96×56, 8px grid, ports, orthogonal wires, Lucide palette icons, etc. (see product spec.)

### 4. Diagram tab — single container

- Full column width (~640×360), no floating refdes hint. Inspector docked 280px on selection only.
- IEEE zigzag resistors, consistent wire weight, V<sub>in</sub> beside source.

### 5. Pin the shell and fix sidebar widths

- `height:100dvh; overflow:hidden`. Sidebar 240px / 56px with 180ms transition; assert in test.

### 6. Home and example tiles

- One thumbnail renderer, six unique images, 3×2 grid, composer placeholder, no top-bar New problem on Home, Continue rows, sidebar Recent layout.

### 7. Problem header and answer card

- Eyebrow, display title, meta line, answer typography, verification strip, top bar actions.

### 8. Tokens

- `--text-muted: #767672`, `--text-faint`, dark primary button text `#0B1222`, focus ring.

### 9. Cmd+K

- Grouped palette with shortcuts and footer.

### 10. Problems list

- Full table columns, filters, hover actions.

### 11. Gallery, Library, Settings

- Nav-aligned titles, gallery frames, library table, settings tabs.

### 12. Theme the figures (Visual Kit)

- SVG/token colours, no embedded titles, axis styling.

## Copy bans (user surfaces)

SSE, kernels, refdes, chunks, recipe ids, session ids, raw enums, branch names, em dashes.
