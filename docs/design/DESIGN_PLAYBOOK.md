# Arc design playbook (v1, 13 Nov 2026)

Owner: Design lead (critiques every round against section 5). Audience: the cloud agent that builds the UI, and EE Project who writes its prompts.
Target feel: Linear, Vercel, Notion, Figma, Hex. Calm, dense, technical, trustworthy.

How to read this file:
- **MUST / MUST NOT** are hard rules. A screenshot that breaks one loses points in the rubric (section 5).
- **SHOULD** is the default. Deviate only with a stated reason.
- Section 1 says which source wins when the docs disagree. Read it before you touch a token.
- Every number here is either from the Learning Lab cobalt system (`ux-kit/cobalt-ui-design-system.md`, `DESIGN.md`), from the Arc product spec, or marked **Arc rule** (my decision, with the reason). Public evidence is cited in section 10. Nothing is quoted from a source unless it is in quotation marks and linked.

---

## 0. The ten-line version

1. The problem page leads with the answer: `name = value unit`, then the engine-verified status, then the work.
2. Neutral first. Warm-grey structure, 1px hairlines, white sections on the `#FAFAF9` canvas. Cobalt `#2F6FEB` marks where you are, what is selected, and the one primary action per region.
3. Spacing only from `4 8 12 16 24 32 48 64`. Radii only 4px (controls), 6px (sections and menus), full (dots, avatars, count badges).
4. Shadow only on things that float (menus, popovers, palette, dialogs, toasts, floating canvas controls). Never on a section.
5. Geist (Inter fallback), 14px body, 13px secondary, 12px metadata, 11px uppercase labels only. Tabular numbers for every number.
6. Lucide icons, 16px inline, 18px in the sidebar, rendered stroke 1.5px.
7. Motion is 120ms (hover, press) and 180ms (appear, expand), `cubic-bezier(0.22, 1, 0.36, 1)`, opacity and position only, and it stops under `prefers-reduced-motion`.
8. Keyboard first: Cmd/Ctrl+K opens the palette, Cmd/Ctrl+B toggles the sidebar, every control has a visible focus ring.
9. Plots and diagrams are drawn in the same palette and type as the UI, with units on every axis, wires under blocks, right-angle wiring, and nothing smaller than 11px at 100% zoom.
10. No raw ids, JSON, recipe names or engine jargon on a user surface. They live behind a "Diagnostics" disclosure.

---

## 1. Source reconciliation (who wins when docs disagree)

Order of authority: **Arc product spec (13 Nov, owner-signed) > cobalt system v1.2 > DESIGN.md > this playbook's own additions**. Where I override, the reason is given. The builder MUST encode the resolved value once in tokens.

| # | Topic | Docs say | Arc decision | Why |
|---|---|---|---|---|
| C1 | Spacing grid | Spec: "8 px spacing grid". Cobalt and DESIGN.md: scale `4 8 12 16 24 32 48 64`. | Scale is the token list. Layout blocks align to 8, fine details (icon to label, dot to text, tag padding) use 4. | The spec sentence and the scale are compatible: 8 is the layout rhythm, 4 is the base unit. |
| C2 | Body size | DESIGN.md body 16/26. Cobalt body 14/22, `body-lg` 16/26. | UI default is 14/22. 16/26 only for the plain-English explanation of an answer and long prose. | DESIGN.md is written for a reading tool. Arc is a workbench. Geist's own most-used text styles are 14px ("Copy 14 ... most commonly used", Vercel typography page). |
| C3 | Sidebar width | Spec: 240 expanded, 56 collapsed. Cobalt: rail 56 only, items 40x40, icons 20px. | 240 and 56 as the spec says. Nav rows 32px tall expanded. Collapsed icon buttons 32x32 centred in the 56px rail (12px each side). Nav icons 18px in both states. | Spec is later and owner-signed. Same icon size in both states stops icons jumping when the sidebar toggles. 32px is dense but still above the WCAG 2.2 AA 24x24 minimum (SC 2.5.8). |
| C4 | Icon size | Spec: 16 to 18px. Cobalt: 16 inline, 20 rail, 14 dense table controls. | 16px inline and in buttons, 18px sidebar nav, 14px in 28px-high dense table actions. Never 20px or 24px in chrome. | Spec wins. 14px is kept from cobalt for dense rows. |
| C5 | Icon stroke | Spec and cobalt: 1.5. Lucide's own default is 2 in a 24px box. | Rendered stroke 1.5px. In Lucide, `strokeWidth` is measured in the 24px viewBox, so `strokeWidth={1.5}` at `size={16}` draws about 1px on screen. Set `absoluteStrokeWidth` with `strokeWidth={1.5}` at the provider level. If that reads too heavy in review, fall back to Lucide's default 2 (about 1.33px at 16px), not to a thinner value. | Lucide documents the 2px default and the `absoluteStrokeWidth` and `nonScalingStroke` props (see section 10). A 1px icon on a 1x display looks faint. |
| C6 | Focus ring | Cobalt token `--focus-ring` is cobalt at 45% opacity. | `:focus-visible { outline: 2px solid var(--accent-500); outline-offset: 2px; }`. Change `--focus-ring` to `var(--accent-500)`. | I computed contrast: 45% cobalt on white is about 1.9:1, below the 3:1 that WCAG expects for focus indicators and UI boundaries. Solid cobalt is 4.57:1 on white. |
| C7 | Muted text | `--text-muted` `#8A8A86` is 3.47:1 on white, 3.32:1 on canvas, 3.18:1 on `#F5F5F4`. Cobalt allows it for metadata. | Add `--text-muted: #70706C` (4.97:1 on white, 4.76:1 on canvas, 4.56:1 on `#F5F5F4`). Revised in round 2: my first value `#767672` was 4.37:1 on the canvas and 4.18:1 on the sidebar, so it still missed AA. Use `#8A8A86` only for icons, disabled text and placeholder-adjacent decoration, renamed `--text-faint`. Timestamps and metadata use `--text-muted`. | Metadata is still text and must pass 4.5:1. Cobalt itself says muted must never carry decision-critical info. This keeps that and fixes the rest.  |
| C8 | Breadcrumb style | Cobalt: crumbs in uppercase `label` style. | Crumbs are sentence case, 13/20, weight 500. Past crumbs `--text-muted`, current `--text-primary`. Uppercase labels stay for eyebrows, table headers, section labels. | Problem titles are user content ("Voltage divider"). Uppercasing them is shouty and breaks units (kHz becomes KHZ). |
| C9 | Workspace panel | Cobalt: one white panel inset 8px from the canvas, with a border. Spec: Studio is full-bleed. | Inset panel on Home, Problems, Problem, Gallery, Library, Settings. Studio canvas is full-bleed inside the panel: no inner section border, no padding. | A canvas needs every pixel. Everything else keeps cobalt's calm panel. Draw each border once: the sidebar's right border and the panel's left border MUST NOT stack (Geist colour guidance: "draw each border once"). |
| C10 | Cards | Cobalt: sections, not cards, no hover lift, "card-heavy" is a miss. Spec: Home has example cards, Gallery has figure cards. | Tiles are allowed on Home and Gallery as flat 6px-radius bordered tiles. No shadow, no hover lift. Hover is `--border-strong` plus `--surface-subtle` fill. One tile grid per page region. Never a card inside a card inside a card. | The spec needs thumbnails, so tiles stay. The cobalt rule survives as "flat". |
| C11 | Accent presence | Cobalt: accent MUST be on every screen. User brief: cobalt used sparingly. | Both. The minimum-presence list (brand tile, active nav item, active tab, first chart series, focus ring) is the floor. Ceiling about 10% of visible pixels, filled about 2%. | They do not conflict: trace everywhere, fill rarely. |
| C12 | Sidebar "New problem" | Spec: a "New problem" button in the sidebar. Cobalt: one filled primary per region. | The sidebar button is **secondary** (white, 1px border, `C` shortcut hint on the right). The page's own primary action stays filled. | Two filled blue buttons in one window means no single next action. |
| C13 | Chart gridlines | Cobalt: horizontal only, no chart border. | Horizontal gridlines on linear axes. On a log axis (Bode, root-locus frequency), add vertical decade lines in `--border` at 1px, and minor ticks as 4px tick marks, not lines. | A log axis without decade lines cannot be read. Cobalt's rule was written for time series. |
| C14 | Max text size | Cobalt: nothing above 28px, weight 600 max. Spec: answers in "display type". | Answer values use `kpi` (28/32, 500, tabular, -0.02em). Do not go bigger. The answer card is made prominent by position, whitespace and a tint, not by size. | Keeps one scale. 28px tabular figures in a flat card still lead the page. |
| C15 | Skeleton animation | Cobalt R12 "no pulsing". Cobalt 9.18 allows a 1.2s opacity fade skeleton. | Skeleton is static `--surface-subtle`, or an opacity fade between 100% and 60% over 1.2s. No shimmer sweep. Static under reduced motion. | 9.18 is the specific rule and overrides R12 for loading only. |
| C16 | Radius on floating layers | Geist materials use 12px on menus and modals. Cobalt: 6px. | 6px everywhere. | Cobalt is Arc's language. Arc does not copy Geist radii. |
| C17 | Phone layout | DESIGN.md: 44px phone targets, bottom bar. Spec: 1280 to 1600px. | Not in scope for v1. Minimum supported width 1100px. Below 1100 the sidebar force-collapses and the Parameters drawer becomes an overlay. | Spec scope. Do not spend time on phone. |
| C18 | Token naming | DESIGN.md: `cobalt-50`, `text-inverse`. Cobalt: `--accent-50`, `--accent-500`. | Use cobalt's `--accent-*` names in CSS. `cobalt-*` are aliases in the TS tokens module only. | One CSS vocabulary. |

### Arc additions to the token block (add to `:root`)

```css
:root {
  --text-muted: #70706C;      /* AA on white, canvas and sidebar (C7) */
  --text-faint: #8A8A86;      /* icons, disabled, decoration only */
  --focus-ring: var(--accent-500);   /* C6 */
  --sidebar-w: 240px;
  --sidebar-w-collapsed: 56px;
  --topbar-h: 44px;           /* = cobalt --crumb-h */
  --drawer-w: 320px;          /* Parameters drawer */
  --palette-dock-w: 220px;    /* Studio left palette */
  --inspector-w: 280px;       /* Studio right inspector */
  --results-h: 280px;         /* Studio bottom drawer default */
  --content-w-narrow: 960px;  /* Home, Settings */
  --content-w-wide: 1280px;   /* tables, galleries */
  --canvas-grid: 8px;         /* Studio snap grid */
  --duration-fast: 120ms;
  --duration: 180ms;
  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
}
```
Dark theme: use cobalt section 16.1 values unchanged. Plots MUST read these tokens at draw time (section 4).

---

## 2. Foundations (numeric rules)

### 2.1 Spacing

| Token | px | Use in Arc |
|---|---|---|
| space-1 | 4 | Icon to label, dot to text, tag inner gap |
| space-2 | 8 | Button group gap, sidebar item padding, metadata separators |
| space-3 | 12 | Label to content, section header to body, input padding |
| space-4 | 16 | Gap between list groups, compact section padding, paragraph gap |
| space-5 | 24 | Default section padding, gap between regions |
| space-6 | 32 | Page gutter, gap between major regions |
| space-7 | 48 | Space above a page title on Home only |
| space-8 | 64 | Separation between unrelated areas, empty-state vertical padding |

Rules:
- MUST: every `margin`, `padding`, `gap` is a token. No `13px`, `18px`, `20px`, `22px` gaps.
- MUST: related items are tighter than unrelated items. Gap inside a group is at most half the gap between groups.
- MUST: left and top edges of items in a row align. A page that mixes left-pinned and centred blocks fails.
- MUST: content is centred in the panel with the max widths in section 4. No content pinned left with a dead slab on the right.
- Page gutter 32px at 1280 and above, 24px below.
- Density: comfortable is default. Section padding 24, rows 40. Compact (settable): section padding 16, rows 32.

### 2.2 Type ramp (Geist, Inter as fallback with `font-feature-settings: "cv11", "ss01"`)

| Style | Size / line | Weight | Tracking | Use in Arc |
|---|---|---|---|---|
| display | 28 / 36 | 500 | -0.02em | Page title, one per page (Home greeting, problem title) |
| kpi | 28 / 32 | 500 | -0.02em, tabular | Answer values only |
| title | 20 / 28 | 600 | -0.01em | Section titles, dialog titles |
| heading | 16 / 24 | 600 | -0.005em | Sub-sections, step titles, tile titles |
| body-lg | 16 / 26 | 400 | 0 | Plain-English explanation of an answer |
| body | 14 / 22 | 400 | 0 | Default UI text, table cells |
| body-strong | 14 / 22 | 600 | 0 | Names, key values inside a sentence |
| small | 13 / 20 | 500 | 0 | Buttons, sidebar items, crumbs, secondary lines |
| meta | 12 / 16 | 400 | 0 | Timestamps, counts, axis tick labels, tag text (500) |
| label | 11 / 16 | 600 | 0.06em, uppercase | Eyebrows, table headers, section labels. 11px is allowed only here |

Rules:
- MUST: `font-variant-numeric: tabular-nums` on every number (tables, answers, plots, timestamps, parameter inputs).
- MUST: at most three text styles inside one section.
- MUST NOT: weight above 600, size above 28px, italics for emphasis, monospace labels.
- Geist Mono only for ids, netlist or code, and raw engine output. Never for titles, tags, sidebar rows or metadata.
- Units are set in the same text style as their value, with a thin gap: `5.00 V` (a normal space is acceptable, but never split value and unit across lines: `white-space: nowrap`). Symbols and subscripts use real typography: `V_out` is rendered with `<sub>`, `Ω`, `μ`, `°`, `√`. Never `Vout`, `ohm`, `uF`.
- Line length for prose: 60 to 75 characters (max-width about 65ch at 14px, 760px at 16px).

### 2.3 Density and sizes

| Element | Size |
|---|---|
| Button default / dense table / form | 32 / 28 / 36 px high, padding 0 12px (0 16px at 36), 14px text |
| Input | 36px high, padding 0 12px |
| Tabs | 40px high, 2px accent underline on active |
| Table header / row | 36px / 40px (compact 32px) |
| Tag | 22px high, padding 0 8px, 12px/500 text |
| Chip (filter) | 28px high |
| Avatar | 20px inline, 28px in lists, initials 11/600 |
| Sidebar row | 32px high, padding 0 8px, 4px radius |
| Tooltip delay | 400ms |

One primary action per region (page header, dialog, answer card, a single list item). A page has at most one filled cobalt button visible at a time, apart from a dialog layered over it.

### 2.4 Borders, radii, shadows

- Structure is a 1px `--border` (`#E4E4E2`) hairline. 2px only for focus rings, the active tab underline and the 2px active mark.
- **Draw each border once.** Adjacent panels share one line. No border on top of a border, no border plus shadow on the same element.
- Radius: 4px buttons, inputs, tags, chips, insets. 6px sections, panels, tiles, menus, dialogs, palette. Full only for dots, avatars, count badges. A radius of 8, 12, 16px anywhere is a defect.
- Shadow: `--elevation-1` (`0 1px 2px rgba(32,32,32,0.04), 0 4px 12px rgba(32,32,32,0.05)`) on floating layers only: menus, popovers, tooltips, the Cmd+K palette, dialogs, toasts, the Studio zoom pill, the Parameters drawer when it overlays. Sections, tiles, tables, plots, and the answer card have no shadow.
- Surface steps do the depth work: canvas `#FAFAF9`, section `#FFFFFF`, inset and table header `#F5F5F4`, sunken (code, track) `#EFEFED`.
- Nesting: at most two levels of bordered boxes (panel, then section). An inset is a tint, not a border.

### 2.5 Colour

| Role | Token | Rule |
|---|---|---|
| Structure | canvas, surface, surface-subtle, border | 90% of pixels |
| Text | primary `#202020`, secondary `#5F5F5C`, muted `#70706C` | Never pure black |
| Accent trace | accent-500 lines, accent-600 icons, accent-700 text | Active nav, active tab, links, focus, first chart series, selected rows |
| Accent tint | accent-50, accent-100 | Selected row, selected chip, active nav background, the answer's verified strip (not the whole card) |
| Accent fill | accent-500 + white | Primary button, brand tile, checked controls, open-count badge |
| Status | success `#2F9E6A`, warning `#E0A526`, critical `#D0312D`, info `#3B79C4` (text and tint variants) | Dot or icon plus a word. Never colour alone |
| Categories | accent, copper `#E07A3F`, teal `#2A9D8F`, ochre, plum, olive | Chart series, subject dots, avatars. Never section backgrounds |

Arc mappings:
- Subject colours (sidebar dots, subject tags): Circuits copper, Control teal, Power systems ochre, Machines plum, Power electronics olive, Signals `--cat-other` grey. Cobalt is never a subject colour because it is the accent. Fix the mapping once in a token map and never change it. Agent badges therefore use a neutral tag with a bot icon rather than plum, to avoid clashing with Machines.
- Problem status tags: **Checked** = success tag with check icon. **Running** = info tag with a 14px spinner. **Failed** = critical tag with an x-circle icon. **Unchecked** = neutral tag with a hollow ring in the list, and on the problem page an amber `warning-tint` strip with the words "Not verified by an engine yet" and a "How to check" action. Unchecked is not an error, so it is never red.
- Author badges: Agent = neutral tag with a 14px bot icon and the word "Agent". Human = neutral tag with the person's initials. Never fill a badge with accent.
- Never put a filled accent element next to a critical element.
- The old UI filled an inline "unchecked" pill with saturated blue. That is the main thing to avoid: a status is a tinted tag with a word, never an accent fill.

### 2.6 Icons

- Lucide only (ISC). One family. No emoji, no letter glyphs (`∫`, `d/dt`, `PID`) as toolbar icons: use Lucide icons or a custom 18px icon that matches 1.5px stroke, round caps and joins.
- Sizes: 14 (dense table actions), 16 (inline and buttons), 18 (sidebar). Rendered stroke 1.5px (rule C5). `currentColor` always.
- Colour: `--text-secondary` at rest, `--text-primary` on hover, `--accent-600` when active or selected, status solid tones for status icons.
- Icon plus label gap 8px. Icon-only buttons are 32x32 with a tooltip and `aria-label`.
- Sidebar glyphs from the spec: Home `house`, Problems `list-checks`, Studio `workflow`, Gallery `images`, Library `book-open`, Settings `settings`, Help `life-buoy`, Agent `plug`.

### 2.7 States (every control, no exceptions)

| State | Rule |
|---|---|
| Hover | Background or border changes within 120ms. Primary: `--accent-600`. Secondary: border to `--border-strong`. Quiet: `--surface-subtle`. Row: `--surface-subtle`. Never move or resize the element. |
| Focus-visible | 2px solid `--accent-500`, 2px offset, on every interactive element, including tiles, rows, tabs, canvas blocks. Not removed anywhere. Mouse clicks do not show it (`:focus-visible`). |
| Active (pressed) | Primary `--accent-700`. Others `--surface-sunken`. No scale transforms. |
| Selected | `--accent-50` fill, 1px `--accent-200` border for chips, accent tint row for tables, accent-600 icon in nav. |
| Disabled | 40% opacity, `cursor: not-allowed`, no hover change, and a tooltip saying why when the reason is not obvious ("Run again is available once the agent is connected"). |
| Loading (button) | A 14px spinner replaces the icon. Width does not change. Label stays. |
| Loading (content) | Skeleton at final content size (rule C15). Appear only if loading exceeds 150ms. No layout shift when real content lands. |
| Empty | One sentence, one action, at most one secondary link, centred in the region, 64px vertical padding. Example: "No problems yet. Try an example to see Arc check an answer." with the button "Try an example". Never developer instructions ("Use the CLI"). |
| Error | Plain sentence that says what failed and what to do, plus "Try again" and a "Details" disclosure holding the technical message. Critical tint banner, 16px alert icon, 1px critical border. |
| Stale | Hollow ring plus "Stale, parameters changed. Run again to update." Stale results stay visible but get a 60% opacity answer value and the Run again button gains the primary fill. |

### 2.8 Motion

| Event | Duration | Easing | Property |
|---|---|---|---|
| Hover, press | 120ms | ease-out | colour, background, border |
| Tooltip appear | 120ms after a 400ms delay | ease-out | opacity |
| Menu, popover, dropdown | 120ms in, 80ms out | ease-out | opacity, translateY 4px |
| Cmd+K palette | 120ms in, 80ms out | ease-out | opacity, translateY 4px (no scale) |
| Sidebar collapse or expand | 180ms | ease-out | width, label opacity (labels `white-space: nowrap`, clipped, so text never re-wraps mid-animation) |
| Drawer, accordion, step expand | 180ms | ease-out | height or translateX, opacity |
| Tab underline | 180ms | ease-out | translateX and width |
| Toast | 180ms in, 120ms out | ease-out | opacity, translateY 4px |
| New list or timeline item | 180ms | ease-out | opacity, translateY 4px |
| Skeleton | 1.2s loop | ease-in-out | opacity 100% to 60% |

- Animate opacity and position only, except the sidebar width. Nothing bounces, springs, pulses, glows or loops (apart from the skeleton and the 14px spinner).
- `@media (prefers-reduced-motion: reduce)`: every transition and animation duration becomes 0.01ms, the skeleton is static, the spinner becomes a static arc plus the word "Working".
- No motion longer than 200ms except the skeleton.

### 2.9 Cmd+K and keyboard-first patterns

Command palette (cmdk or equivalent):
- Opens on Cmd/Ctrl+K from anywhere, including inside inputs. Toggles closed on a second press. Esc closes. Focus returns to the element that had it.
- Layer: 560px wide, `--radius-md`, `--surface`, `--elevation-1`, centred horizontally, top at 20vh, backdrop `--overlay` (`rgba(32,32,32,0.28)`), `z-index` 40.
- Input row 48px, 16px text, magnifier icon 16px, placeholder "Search or run a command". No border on the input, a 1px bottom `--border`.
- Results: max height 400px, scroll inside. Group labels (`label` style): Actions, Problems, Figures, Examples, Pages. Rows 36px, 14px text, subject dot or icon on the left, type or shortcut hint right-aligned in `meta` text. Selected row `--accent-50` with `--accent-700` text, accent check not needed.
- Empty query shows Recent (last 5 problems) then Actions. Fuzzy matching, matches in the title bold (600), not coloured.
- Keys: up and down move (wrap around), Enter runs, Cmd+Enter opens in a new tab where it applies, Backspace on an empty input steps back from a sub-menu, Esc closes.
- Actions it MUST contain: New problem, Run again (when a problem is open), Open in Studio, Export (PDF, PNG, Markdown), Toggle sidebar, Toggle theme, Go to each page, Connect an agent.
- Empty result: "No matches for 'xyz'" plus a "Ask as a new problem" row that carries the query into the Home composer.
- Accessible: `role="dialog"`, combobox with listbox, `aria-activedescendant`, focus trap.

Global shortcuts (Arc rule, shown in tooltips and in a `?` sheet):

| Keys | Action |
|---|---|
| Cmd/Ctrl+K | Command palette |
| Cmd/Ctrl+B | Toggle sidebar |
| C | New problem (when no field is focused) |
| / | Focus the search field on the page |
| G then H, P, S, G, L | Go to Home, Problems, Studio, Gallery, Library |
| J, K or arrows | Move through list rows. Enter opens |
| Cmd/Ctrl+Enter | Solve or Run again |
| `[` and `]` | Previous and next tab on a problem |
| Cmd/Ctrl+Z, Shift+Cmd/Ctrl+Z | Undo, redo in Studio |
| Esc | Close the top layer, then deselect |
| ? | Shortcut sheet |

Every shortcut is also reachable by a visible control. Hints appear in tooltips as `Run again  Cmd+Enter` with a 12px `kbd` style: 1px border, 4px radius, `--surface-subtle`, 12px Geist (not mono). Tab order follows visual order. Skip link "Skip to content" appears on first Tab.

---

## 3. Shell and pages

### 3.1 Shell

```
┌────────────┬──────────────────────────────────────────────────────────────┐
│ [■] EE co..│ Problems / Voltage divider            [Agent editing] [Run again ▸] [⋯] │  top bar 44px
│ [+ New  C ]├──────────────────────────────────────────────────────────────┤
│ ⌂ Home     │                                                              │
│ ☰ Problems │   page content, centred, max width per page, gutter 32px      │
│ ⋈ Studio   │                                                              │
│ ▣ Gallery  │                                                              │
│ ▤ Library  │                                                              │
│ RECENT     │                                                              │
│ • Divider ✓│                                                              │
│ • PID step ✓                                                              │
│ ─────────  │                                                              │
│ ⏚ Agent ● │                                                              │
│ ⚙ Settings │                                                              │
│ ? Help  ◐  │                                                              │
└────────────┴──────────────────────────────────────────────────────────────┘
 240px expanded (collapsed: 56px icon rail with tooltips)
```

| Region | Spec |
|---|---|
| Sidebar expanded | 240px, `--surface`, 1px right `--border`. Padding 8px. Brand tile 28px `--accent-500` with white mark, then workspace name (13/20, 600), then a collapse button (16px `panel-left`, 32x32). |
| Sidebar collapsed | 56px. Brand tile centred. Icons 18px in 32x32 buttons, centred. Tooltips after 400ms with the page name and shortcut. "New problem" becomes an icon-only 32x32 `plus` button. Recent section is hidden, replaced by one hairline. |
| Toggle | Button at top plus Cmd/Ctrl+B. State in `localStorage` (`arc.sidebar`). 180ms. Default expanded at 1280 and above. |
| Nav items | 32px high, 13/20 500, `--text-secondary`. Hover `--surface-subtle`. Active: `--accent-50` background, `--accent-600` icon, `--text-primary` label at 600. No side stripe on sidebar items. |
| New problem | Secondary button, full width, 32px, icon `plus` 16px, label "New problem", `C` hint right in `meta`. |
| Recent | `label` heading "RECENT", last 5 problems by human title (13/20, truncated with ellipsis and a tooltip with the full title), 6px subject dot on the left, status icon on the right (16px check, spinner, or hollow ring). Never ids. |
| Bottom group | Agent status row: 16px `plug`, "Cursor agent" plus a 6px dot (success when connected, `--text-faint` grey when not) and the word "Connected" or "Not connected". Then Settings, Help and docs, theme toggle (16px, `aria-pressed`). |
| Top bar | 44px, `--surface`, 1px bottom `--border`. Left: crumbs (sentence case 13/20). Right: presence chips, then at most one primary and one secondary or overflow button. The page title is NOT repeated in the top bar. |
| Presence chip | 22px high tag, neutral, 6px success dot plus "Agent editing" while the agent is acting. Never animated. |
| Panel | Inset 8px from the canvas, `--surface`, 1px `--border`, 6px radius. The sidebar and top bar are inside the window, not inside the panel. |
| Scroll | The panel content scrolls. The window never scrolls. The sidebar list scrolls on its own. The page MUST NOT be longer than its content (the old UI produced a 15,954px page because the run list was in the page flow). |
| Content widths | Home and Settings 960px. Problems, Gallery, Library 1280px. Problem page main column up to 840px, plus the 320px drawer when docked. Studio full width. |
| Breakpoints | 1100 minimum. At 1100 to 1359 the Parameters drawer overlays instead of docking. At 1600 and above content stays centred at its max width; extra space is canvas, never stretched cards. |

### 3.2 Home

Job: orient and start. Nothing else.

```
┌ top bar: Home ─────────────────────────────────────────────────────────────┐
│                                                                            │
│              EE COURSEWORK                         (label)                │
│              Good afternoon, Vinayak.              (display 28)            │
│                                                                            │
│   ┌──────────────────────────────────────────────────────────────────┐   │
│   │ Paste or type a problem                                          │   │
│   │                                                                  │   │
│   │ [Circuits ▾ auto]  [attach]                      [ Solve ▸ ]     │   │  composer: 120px min
│   └──────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│   TRY AN EXAMPLE                                                           │
│   ┌────────┐ ┌────────┐ ┌────────┐       2 rows x 3, equal height          │
│   │ thumb  │ │ thumb  │ │ thumb  │       thumbnail 96px tall, same crop    │
│   │ title  │ │ title  │ │ title  │       same aspect ratio, same style     │
│   │ subject│ │ subject│ │ subject│                                          │
│   └────────┘ └────────┘ └────────┘                                          │
│                                                                            │
│   CONTINUE                                                  View all ▸     │
│   [problem row]  [problem row]  [problem row]   (compact rows, not cards)   │
│                                                                            │
│   Agent: "Cursor agent connected" (one line)  |  or the 3-step setup card   │
└────────────────────────────────────────────────────────────────────────────┘
```

| Level | Content |
|---|---|
| Primary | The composer and its single filled **Solve** button |
| Secondary | Example tiles (6), then Continue (3 rows) |
| Tertiary | Agent status line, eyebrow label |

Rules:
- Composer: 960px max, `--surface`, 1px border, 6px radius, focus ring on the whole box. Solve is filled only when there is text (otherwise disabled, 40% opacity). Cmd/Ctrl+Enter submits.
- Example tiles: all six thumbnails render from the same engine pipeline at the **same pixel size and aspect ratio (160 x 96)**, same line weight, same palette, same padding, on `--surface-subtle`. A tile where the figure is a different size or style from its neighbours fails the screen. Tiles are 6px radius, hover `--border-strong`, whole tile is the link, title 14/22 600 on one line, subject tag 22px under it.
- Continue: reuse the Problems row component (title, subject, status, relative time). Not a second card style.
- First-run (no agent): replace the status line with a setup section: three numbered steps, each with a copy button (`copy` 16px) for Cursor, Claude Code and Codex MCP config. Not on Home: the full gallery, scorecard, CLI docs, diagnostics, long explanations.
- Greeting is plain: no emoji, no "Welcome back!". Name only if known.

### 3.3 Problems (list)

```
┌ Problems / (top bar)                                         [ New problem ] ┐
│  Problems  42                                                               │
│  [🔍 Search problems  /]   [Subject ▾] [Status ▾] [Made by ▾]   [density]   │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ TITLE                        SUBJECT      STATUS     MADE BY    UPDATED │ │ 36px header
│  │ TODAY                                                                    │ │ group label 32px
│  │ ● Voltage divider, Vout      Circuits     ✓ Checked  [Agent]    4 min   │ │ 40px rows
│  │ ● PID on a DC motor          Control      ✓ Checked  [VR]       1 h     │ │
│  │ THIS WEEK                                                                │ │
│  │ ● Three-phase fault          Power sys    ○ Unchecked [Agent]   2 d     │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────┘
```

- Columns: title (flex, 14/22 600, truncated with tooltip), subject (tag with 6px dot), status (tag), made by (20px avatar plus the word Agent or the first name), updated (12px relative, `--text-muted`, right-aligned, tabular).
- Group headers Today, This week, Earlier: `label` style, sticky under the table header, 32px.
- Row hover: `--surface-subtle`, reveal three 28px quiet icon actions at the right (open `arrow-up-right`, re-run `rotate-cw`, duplicate `copy`) with tooltips. Row is also focusable: J and K move, Enter opens.
- Filters are 28px chips. Selected = `--accent-50` fill, `--accent-200` border, `--accent-700` text, with a count. A "Clear filters" quiet button appears when any is active.
- Primary action: **New problem** (the only filled button; the sidebar one is secondary).
- Empty (no problems): "No problems yet. Try an example to see Arc check an answer." button "Try an example". Empty (filters): "No problems match these filters." button "Clear filters". Loading: 8 skeleton rows at 40px. Error: banner with "Try again".
- Titles are human ("Voltage divider, Vout"), never run ids. If the agent gave no title, derive one from the question text, first 60 characters.

### 3.4 Problem page (the core loop)

Lead with the answer (all numbers in the wireframes below are illustrative layout placeholders, never UI data). A student opens this page to learn "what is the answer, can I trust it, how did we get there".

```
┌ Problems / Voltage divider, Vout          [Agent editing]  [Parameters 3] [Run again ▸] [⋯] ┐
│                                                                                              │
│  CIRCUITS · Made by Agent · Updated 4 min ago                                  (meta)       │
│  Voltage divider, Vout                                         (display 28/36)              │
│                                                                                              │
│  ┌ ANSWER ────────────────────────────────────────────────────────────────────────────────┐ │
│  │  V_out = 5.00 V        I = 2.50 mA                          (kpi 28/32, tabular)        │ │
│  │                                                                                          │ │
│  │  Vout is the voltage across R2: 10 V × 2 kΩ / (2 kΩ + 2 kΩ).     (body-lg, 1 to 2 lines) │ │
│  │ ┌──────────────────────────────────────────────────────────────────────────────────┐   │ │
│  │ │ ✓ Checked   Solved in SPICE (ngspice) and matched the hand calculation          │   │ │ inset, --accent-50
│  │ │             within 0.1%.  Checked 4 min ago.  [View engine output]                 │   │ │ strip, NOT the card
│  │ └──────────────────────────────────────────────────────────────────────────────────┘   │ │
│  └────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                              │
│  Work   Figures 2   Diagram   Activity 6                          (tabs 40px, accent underline)│
│  ──────────────────────────────────────────────────────────────────────────────────────────  │
│  1  Read the circuit                                                       [Agent]  ▾       │
│  2  Write the divider equation        V_out = V_in R2 / (R1 + R2)          [Agent]  ▾       │
│  3  Substitute values                 5.00 V                                [Agent]  ▾       │
│  4  Check with SPICE                  ✓ matched, error 0.0%   ngspice       [Engine] ▾       │
│  ┌ Figure: Voltage at each node ──────────────────────────────┐  ┌ Schematic ───────────┐  │
│                                                                                              │
│ [ Ask the agent about this problem…                                             Send ▸ ]     │  ask bar 56px, pinned
└──────────────────────────────────────────────────────────────────────────────────────────────┘
 Parameters drawer (docked right, 320px) holds editable inputs with units and a Run again button.
```

| Level | Content |
|---|---|
| Primary | Answer values, the verified status strip, the single filled **Run again** (filled only when parameters changed or the result is stale; otherwise secondary) |
| Secondary | The Work tab: numbered steps, each with author, one-line summary, expandable detail. Plots and schematic in Figures and Diagram |
| Tertiary | Activity log, the agent conversation thread, engine diagnostics, ids, export |

**Header.** Eyebrow (`label`: subject), title (`display`), one meta line (`meta`: made by, updated time). Status badge sits at the right end of the answer card header, not in the top bar. Actions: Run again, Open in Studio, Export (menu: PDF, PNG, Markdown), overflow.

**Answer card (`--surface`, 1px border, 6px radius, padding 24).**
- Each requested quantity as `symbol = value unit`. Symbol in `--text-secondary`, value in `--text-primary`, unit in `--text-secondary`, all tabular, 28/32. Up to 4 per row, wrap to a new row at 24px gap. Significant figures match the engine's tolerance (do not show 5.000000 V).
- One sentence of plain English under the values (16/26, max two lines): what the quantity means and how it was found.
- **Verification strip** (inset, 4px radius, padding 12 16): status tag, then one sentence naming **which engine** and **what it checked**, the tolerance, and when. Example: "Solved in SPICE (ngspice) and matched the hand calculation within 0.1%." A link "View engine output" opens a drawer with the raw output (monospace, behind Diagnostics).
- Tint: Checked uses `--success-tint` with a `--success-text` check icon and the word Checked. Unchecked uses `--warning-tint`, a 16px `circle-help` icon, the words "Not verified by an engine yet" and a quiet button "How to check". Failed uses `--critical-tint`, `x-circle`, the words "The engine disagreed" and the two numbers side by side ("Agent: 5.00 V. SPICE: 4.62 V"), plus "Ask the agent to fix it". Running shows a 14px spinner and "Checking with SPICE".
- Never show the status as colour alone. Never show a verified-looking number that is unchecked.

**Tabs.**
- **Work**: vertical step timeline, 24px gaps. Each step: index in a 20px circle (`--surface-subtle`, 12px tabular), heading 14/22 600, one-line result in `--text-secondary`, author tag at the right (Agent, Human, Engine) with 20px avatar or icon, chevron to expand. Expanded body shows the equation (typeset), the engine call in plain English ("Ran an AC sweep from 10 Hz to 100 kHz") and an inline figure when relevant. Raw events such as `run.start` or `node.start`, JSON, ids and file paths MUST NOT appear here. They sit under one "Diagnostics" disclosure at the bottom of Activity.
- **Figures**: large plots, one per row at full column width, 16:9 or 2:1, titled with a human name, caption in 13/20, click opens a lightbox with download PNG and SVG.
- **Diagram**: the editable schematic or block diagram inline in one container, toolbar above (zoom, fit, "Open in Studio" as a quiet button). No second empty card beside it, no free-floating hint text. If an inspector exists, it docks inside the container at 280px and is hidden until something is selected.
- **Activity**: op log with author, time, change in a table, then the conversation with the agent (message bubbles are flat: no avatars bigger than 28px, agent messages left, human right, 14/22, max width 560px), then the Diagnostics disclosure.
- Conversation access: the ask bar at the bottom (56px, section pinned, `--radius-md`) is always visible on the problem page. Sending adds to Activity and shows the latest agent reply as a one-line toast.

**Parameters drawer (320px).** Header "Parameters" (title 16/24 600) and a close button. Each parameter: label 13/20 500, input 36px with the unit as a right-aligned suffix inside the input (`meta`, `--text-secondary`), help text below if needed. Changing any input sets the page to stale (section 2.7), enables **Run again** as primary and shows a "Reset" quiet button. Docked at 1360px and above; an overlay with elevation below that. The drawer pushes content, it never covers the answer.

### 3.5 Studio

```
┌ Studio / PID · DC motor     [Block diagram | Circuit]  ↶ ↷   [Fit] [100%]  [Simulate ▸]  │ toolbar 44px
├────────┬──────────────────────────────────────────────────────────┬──────────────────────┤
│ PALETTE│                                                          │ INSPECTOR            │
│ 220px  │      grid dots 8px / major 32px                          │ 280px, shown on      │
│ search │                                                          │ selection            │
│ Sources│        ┌────┐   ◯   ┌─────┐      ┌───────┐   ┌───────┐   │ Block: PID           │
│ Math   │  ───▶ │Step│──▶(+)─▶│ PID │─────▶│ Motor │──▶│ Scope │   │ Kp   [ 2.0   ]       │
│ Dynamics│       └────┘   ▲   └─────┘      └───┬───┘   └───────┘   │ Ki   [ 0.5   ]       │
│ ...    │                 └──────────────────────┘                  │ Kd   [ 0.1   ]       │
│        │                                  [− 100% + ⤢]  (floating) │                      │
├────────┴──────────────────────────────────────────────────────────┴──────────────────────┤
│ RESULTS   Step | Bode | Root locus | Margins                                ⌃ resize ✕   │ drawer 280px
│  [ plot, full width of the drawer, same width as the canvas ]     [ margin table ]          │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```

- Toolbar (44px): mode switch (segmented control, 28px), undo and redo, zoom and fit, presence chip, **Simulate** (the one filled button). Crumb on the left.
- Left palette 220px, collapsible (Cmd/Ctrl+\\). Search field, grouped lists with 32px rows: 16px Lucide or custom icon plus the block name. Drag to place. The palette never shows bare glyphs without a name.
- Canvas: full-bleed, `--canvas` background with a dot grid (1px dots, `--border`, every 8px, a stronger dot `--border-strong` every 32px). Selection is a 1px accent outline plus corner handles, not a thick box.
- Inspector 280px: hidden when nothing is selected, or shows the diagram's own summary. Never an empty box with a hint sentence floating in it. Fields are 36px with units, apply on blur or Enter, with an inline error under a field.
- Results drawer: opens at the bottom, default 280px, drag handle 8px high, min 160px, max 60% of the window. It spans the **same width as the canvas plus inspector** (the full width between palette and right edge). Plots are fitted to the drawer with a 16px inset. A margin table (gain margin, phase margin, crossover frequencies) sits to the right at 280px, not above the canvas as four tall cards.
- Margin numbers use `kpi`-sized values only in the results drawer, with units (dB, deg, rad/s). "Infinite" or "No crossover" appears as the value with a one-line `meta` explanation, never a paragraph.
- Op log is a quiet panel in the right inspector's bottom, or the Activity page, not on the canvas.

### 3.6 Gallery

- Page header: title "Gallery", subtitle one line. Filters: subject chips, type chips (Plot, Diagram, Animation), search.
- Grid: 3 columns at 1280 and wider, 2 below, gap 24px. Each tile: image area at a fixed 16:10 aspect on `--surface-subtle`, caption 14/22 600 on one line, subject tag, type icon. Images use `object-fit: contain` with 16px padding, never cropped, never stretched.
- Lightbox: image on a white 6px panel, right column 320px with download PNG, download SVG, "Use in problem", and a collapsible "Properties (JSON)" for agents. Esc closes, arrows step.
- The scorecard does not belong here.

### 3.7 Library

- Title, search, tabs: Sources | Skills. Table (T3): name, kind tag, subject tag, used in (count link), added. Row opens a detail with "Problems that used this".
- Simple: no tiles, no hero. Empty: "No sources yet. Add a textbook or a reference pack." button "Add a source".

### 3.8 Settings

Template T4 (cobalt): tabs **Agents | Engines | Appearance | Data | About**, label column 4 / fields column 8, centred 960px.
- Agents: per agent a row (name, status tag, Connect or Disconnect), MCP config snippet in a mono inset with a 28px copy button.
- Engines: a table of SPICE, pandapower, python-control and others with version, availability tag (Available, Missing) and a "Check again" quiet button. This is where the old header chips live, as status.
- Appearance: Theme (Light, Dark, System) as a segmented control, Density (Comfortable, Compact), Symbol standard (IEEE or IEC, default IEEE).
- Data: runs folder path (mono), "Open folder".
- About: version, then the measured frontier scorecard (one table).
- Footer bar: Cancel (quiet) and Save (primary, disabled until changed). Changes that apply immediately (theme) do not need Save.

---

## 4. How engineering visuals sit in the UI

General rules for every figure, plot, schematic and diagram:
- **One palette, one type.** Figures read the same tokens as the UI (`--text-primary`, `--border`, `--accent-500`, `--cat-*`) at draw time and redraw on theme change. A figure is SVG (preferred) or a PNG rendered at 2x for display size. A white-background PNG inside a grey well in dark mode fails.
- **Render at display size.** The figure is produced at the size it is shown (for example 720 x 360 CSS px) so that text is never scaled down. Nothing below 11px at 100% zoom, tick labels 12px. If a diagram is wider than its container, scale it up to fill (never above 125%) or let the container scroll; never leave a small figure floating in a large empty card.
- **Container card.** A figure sits in one flat section: `--surface`, 1px `--border`, 6px radius, padding 16, no shadow, no nested border around the image. Header row (36px): human title in 14/22 600 on the left, tools on the right (zoom, download, expand, 28px quiet icon buttons). Caption under in 13/20 `--text-secondary`. The figure fills the container width.
- **Never auto-generated titles** like "Bode plot for sys[3]". Titles are human ("Open-loop Bode plot").
- **Provenance.** Each figure shows what produced it in the caption's `meta` line ("SPICE transient, 0 to 5 ms"). No ids.

### 4.1 Plots

| Property | Rule |
|---|---|
| Canvas | Transparent or `--surface`. No figure frame, no outer box, no black axes box (matplotlib default `axes.edgecolor` MUST be changed) |
| Axes | Left and bottom spines only, 1px `--border-strong`. Top and right spines off |
| Tick labels | 12px Geist, `--text-secondary`, tabular. 4 to 6 major ticks per axis. Minor ticks 3px on log axes, none on linear |
| Axis labels | 12px, 500, `--text-primary`, with units in parentheses and a real symbol: "Magnitude (dB)", "Phase (°)", "Frequency (rad/s)", "Time (s)", "Voltage (V)". Never "Output", never "x", never a bare unit missing |
| Gridlines | Horizontal 1px `--border` on linear axes. Add vertical decade lines on log axes (C13). Never both major and minor grids on both axes (the old Bode plots did) |
| Line weight | Subject 2px (2.25 at 2x export), other series 1.5px. Round joins. No markers on dense lines, 6px dots only for annotated points |
| Colour order | Series 1 `--accent-500`, 2 copper `#E07A3F`, 3 teal `#2A9D8F`, 4 ochre `#C99A2E`, 5 plum `#8E5B9A`, 6 olive `#7A8B3A`, then `--cat-other`. Maximum 4 series on one axis, otherwise small multiples |
| Stacked axes | Magnitude and phase of the **same system** use the **same colour** (cobalt on both). Use copper only when a second system is compared. Share the x-axis, label it only on the bottom plot, 16px gap between panels |
| Focus mode | When one series supports the answer: subject `--accent-500` 2px, others `#C4C4C2` 1.5px |
| Area fill | Optional on a single series: accent at 12% to 0% opacity, top to bottom, or flat `--accent-50`. The only gradient allowed |
| Annotations | Direct label at the line end (12px/500 in the line's colour at its `-700` text equivalent), not a legend. Legend only when labels collide, 6px dots plus 12px text, top-left inside the plot |
| Thresholds | 1px dashed `--warning` or `--critical`, label at the right end. Required for specs the student cares about: 0 dB line, -180° line, setpoint, voltage limit |
| Key points | Gain and phase margin, crossover, peak, settling band: a 6px dot on the data point, a 1px leader, and a 12px label with value and unit ("Phase margin 62°"). The same numbers also appear in the margin table |
| Step response | Setpoint dashed `--text-muted` line; ±2% band as a 1px dashed pair or a `--accent-50` band; label settling time and overshoot with units |
| Tooltip | `--surface`, 1px `--border`, 4px radius, `--elevation-1`, series dot, name, value with unit in 14/22 600, x value in `meta` |
| Dark theme | Same roles from cobalt section 16.1 (`--cat-*` lifted). Plots repaint on `data-theme` change |
| Size | Minimum 480 x 240 CSS px in a card. A thumbnail in a list or tile is a separate render, never a shrunken full plot |
| Accessibility | `<figure>` with `<figcaption>`, `aria-label` describing the finding in one sentence, and a "View data" table toggle |

### 4.2 Schematics (circuits)

- **One symbol standard.** Default IEEE/ANSI (zigzag resistor, coil inductor, parallel-plate capacitor, circle sources). IEC 60617 (rectangle resistor) is a setting, never mixed on one screen. A resistor drawn as a coil, or an inductor drawn as a zigzag, is a blocker.
- **Stroke.** Wires and symbols 1.5px, `--text-primary`, round caps, miter joins. Ground and reference symbols same stroke. Selection or highlight uses `--accent-500` 2px, never a glow.
- **Grid.** Symbols and wires snap to an 8px grid. A two-terminal part is 48 or 64px long between its terminals. Terminals sit on grid points.
- **Wires.** Orthogonal only. Junction dot (filled, 6px diameter) only where 3 or more wires meet. A crossing without a connection shows a 4px-radius hop or simply no dot, never a dot. No wire passes through a symbol or a label.
- **Labels.** Refdes (`R1`) in 12px/600 `--text-primary`, value (`10 kΩ`) in 12px `--text-secondary`, placed above or to the right of the part, 8px from the body, never rotated beyond 90 degrees, never overlapping a wire. Values carry units and real symbols (`kΩ`, `µF`, `mH`).
- **Nodes and results.** Node voltage labels are 12px in `--accent-700` on a 4px-radius `--accent-50` chip, with the unit. Currents use an arrow of 8px length next to the wire with its value. Only show them when the active tab is the result view.
- **Sources.** Voltage source circle 32px diameter with +/- or a sine symbol, DC value beside it. Ground symbol at the bottom, always connected.
- **Viewing.** Fit to container with 24px padding. Minimum rendered symbol length 40px. Pan and zoom as section 4.4.

### 4.3 Block diagrams (Simulink-style)

Rules come from Simulink's own modelling guidelines (see section 10): signals flow left to right, feedback may flow right to left, parallel blocks are stacked top to bottom, wires are horizontal or vertical segments only, wires do not overlap blocks, labels or each other, a line splits into at most two at a branch, crossings use line hops.

| Property | Rule |
|---|---|
| Layering (z-order) | Bottom to top: grid, wires, blocks, ports, selection outline, labels. **Blocks are drawn above wires** with an opaque `--surface` fill so a wire never shows through a block. Ports sit on top of the block edge |
| Block | Rectangle, 1px `--border-strong`, 4px radius, `--surface` fill. Default 96 x 56, always multiples of 8. Name centred 12px/600 `--text-primary`, key parameters under it in 12px `--text-secondary` (`Kp = 2`). A name is never truncated: grow the block in 8px steps or wrap to two lines. Never below 12px |
| Block variants | Sum block: circle, 24px diameter, signs `+` and `−` in 12px/600 placed outside the circle next to the relevant port. Gain: right-pointing triangle. Integrator and transfer function: rectangle with the typeset expression (`1/s`, `10/(s+1)`) in 14px |
| Ports | 8px circle centred exactly on the block edge, 1px `--border-strong` outline, `--surface` fill, filled `--accent-500` when connected or hovered. Inputs on the left edge, outputs on the right. Evenly spaced, on the 8px grid. Hit area 16px |
| Wires | 1.5px `--text-primary` at 100% (`--text-muted` for unselected in dim mode), orthogonal segments only, **no diagonals**, round line joins. Fewest bends: at most 2 per wire where possible. Wires leave a port horizontally by at least 16px before turning |
| Arrows | Filled triangle, 8px long, 6px wide, at every input port end. Outputs have no arrowhead |
| Routing | Forward path in a straight horizontal row. A feedback wire leaves the output, drops 32px below the lowest block in the row, runs left, and rises into the sum block's bottom port. Wires never pass under or through a block, a label or another wire along the same segment |
| Crossings | Line hop: a 4px-radius semicircular bump on the horizontal wire. A dot appears **only** where signals genuinely split |
| Branch | Filled 6px junction dot, at most two branches per point |
| Signal labels | Name above the wire, 12px `--text-secondary`, left-aligned to the first 8px after a port: `r`, `e`, `u`, `y`. A label never sits on a wire |
| Selection | 1px `--accent-500` outline offset 2px plus 6px square handles. Selected wire turns `--accent-500` 2px |
| States | Hover: block border `--border-strong` to `--accent-300`. Error (algebraic loop, unconnected port): 1px `--critical` outline, 16px alert icon at top-right of the block, and a banner text. An unconnected port stays hollow with a `--warning` ring |
| Auto-layout | "Tidy" action (Shift+Cmd/Ctrl+L) snaps blocks to the grid, re-routes orthogonally, and spaces 48px horizontally and 32px vertically between blocks |
| Scale | The diagram fits the canvas on open with 48px padding, up to 125%. A diagram that fills less than 50% of the canvas width when it has room to grow fails |
| Read-only (in a problem) | Same drawing, no handles, plus an "Open in Studio" quiet button |

### 4.4 Grid snapping, zoom and pan (Studio and Diagram tab)

- Grid: 8px dots in `--border`, every fourth dot (32px) in `--border-strong`. Dots fade out below 50% zoom. Snap on by default, hold Alt to place freely, toggle in the toolbar.
- Zoom range 25% to 400%, steps 25, 50, 75, 100, 125, 150, 200, 300, 400. Cmd/Ctrl + wheel or pinch zooms around the cursor. Plain wheel pans vertically, Shift+wheel horizontally, Space+drag or middle-drag pans. Double-click empty canvas: Fit.
- Keys: Cmd/Ctrl+0 is 100%, Shift+1 is Fit, Cmd/Ctrl + plus and minus step. The zoom level is shown as a number in the control and is a menu.
- Floating zoom control: bottom-left of the canvas, 32px high pill, `--surface`, 1px border, 6px radius, `--elevation-1`, containing minus, `100%`, plus, fit (all 16px icons, 32px targets). It never overlaps blocks that the user can no longer reach: when it would, it stays but the canvas pans to keep content clear.
- Minimap: optional, off by default, 160 x 100px, bottom-right, 16px inset, on its own layer. It MUST NOT overlap the inspector, the results drawer, or the zoom control (the old Studio did).
- Text stays 12px at any zoom below 100% only if clamped: below 60% zoom, hide parameter lines and show names only, rather than rendering sub-11px text.
- Undo and redo are keyed, listed in the toolbar, and every canvas change is attributed in the op log ("Agent changed Kp from 1 to 2", "You moved PID").

---

## 5. Rubric for round critiques

Score each criterion 1 to 5 (half points are not allowed). Screens are judged at 1280 x 800 unless stated. A criterion is scored across every screenshot in the round: take the weakest common pattern, not the best screen.

| # | Criterion | 1 (fails) | 3 (acceptable) | 5 (reference quality) |
|---|---|---|---|---|
| 1 | **Answer-first hierarchy** | The answer is hidden or mixed with logs and ids. No clear first thing to read. Several equal-weight elements compete | Answer is visible without scrolling, but status or engine evidence is weak, or work and answer have similar weight | Answer with units is the first and largest thing. Verified status and the engine and check are stated beside it. Work, plots and conversation are clearly secondary and tertiary. One primary action |
| 2 | **Layout, spacing and alignment** | Off-scale gaps, dead slabs, content pinned to one side, misaligned edges, page-level scroll bugs | Mostly on the scale and aligned, with a few cramped or loose areas and some unused space | Every gap on the 4 to 64 scale, edges align, content centred at the right max width, regions fill sensibly at 1280, 1440 and 1600 |
| 3 | **Typography** | Mixed fonts, many sizes, monospace labels, raw ids set as titles, numbers not tabular, sizes under 11px | Right family and a clear ramp but inconsistent weights, some long lines or poor unit setting | Geist ramp used exactly, tabular figures everywhere, real unit and subscript typography, at most 3 styles per section, readable at a glance |
| 4 | **Colour and accent discipline** | Accent fills or saturated blues scattered, status by colour alone, random hues, or all-grey with no identity | Cobalt used for the main action and nav, a few off-token colours or too much tint | Neutral-first, cobalt as trace everywhere and fill only on one action per region, status always with a word, categories in order |
| 5 | **Surfaces, borders, radii and elevation** | Big radii, soft shadows on content, nested boxes, double borders | Hairlines mostly used, one or two stray shadows or radii, some nesting | 1px hairlines drawn once, 4 and 6px radii only, shadow only on floating layers, at most two levels of box |
| 6 | **States and interaction** | Missing hover, focus, loading, empty or error states. Dev-text in empty states. Focus invisible | Hover and focus exist on most controls, empty and loading states exist but are generic | Every control has hover, focus-visible, active, disabled. Real skeletons, empty and error states with actions. Keyboard order sensible, shortcuts shown |
| 7 | **Plots** | Library defaults (black frame, dense grids, auto titles), missing units, tiny text, clipped, off-palette | Right palette and units, but small text, weak annotation, or poor sizing in the card | Section 4.1 followed: units on both axes, cobalt first, direct labels, thresholds, key points annotated, fills its card, matches theme |
| 8 | **Schematics and block diagrams** | Overlapping wires and blocks, diagonals, wrong symbols, truncated labels, tiny drawing in a big empty canvas | Orthogonal wires, readable labels, but ports or arrows inconsistent, drawing small, or one wrong symbol | Section 4.2 and 4.3 followed: blocks over wires, ports on edges, right-angle routing with hops or dots, correct symbols, fills the canvas, snap and zoom controls work |
| 9 | **Trust and copy** | Jargon, JSON and ids on surfaces. Unverified numbers look verified. Em dashes, exclamation marks, invented numbers | Mostly plain English, status clear, one or two jargon leaks or generic copy | Short, task-focused sentences. Engine and check stated in plain English. Estimates labelled. Units everywhere. No developer terms outside Diagnostics |
| 10 | **Shell, navigation and consistency** | Sidebar is a dump, header chips are noise, pages look like different products, no palette | Collapsible sidebar and top bar exist, some components inconsistent, Cmd+K limited | Sidebar and top bar match section 3.1, one component per job reused everywhere, Cmd+K works with actions and recents, motion and dark mode on-system |

Total /50. Ship bar: **40 or more with no criterion below 3.** 30 to 39: continue iterating. Below 30: structural problems, fix before polishing.

### Scoring template (paste per round)

```
ROUND n  |  build: <commit or date>  |  screens reviewed: <n> at 1280x800

 #  Criterion                         Score  One-line reason (cite screenshot filename)
 1  Answer-first hierarchy            /5
 2  Layout, spacing, alignment        /5
 3  Typography                        /5
 4  Colour and accent discipline      /5
 5  Surfaces, borders, elevation      /5
 6  States and interaction            /5
 7  Plots                             /5
 8  Schematics and block diagrams     /5
 9  Trust and copy                    /5
10  Shell, navigation, consistency    /5
                                     TOTAL  __/50   (previous: __/50, change: +/-__)

Blockers (any criterion at 1, or a section-4 symbol error): ...
Top 3 fixes (each with px values, tokens, copy):
 1. ...
 2. ...
 3. ...
Verified against the previous round's top 3: fixed / partly / not fixed
```

Critique conventions: name the screenshot file, say where on the screen ("top-left header", "right panel, second card"), name the rule (for example "2.4, shadow on section"), and give the exact change.

---

## 6. Build checklist (machine-checkable, run before every screenshot round)

- [ ] No `box-shadow` except on `.menu, .popover, .tooltip, .palette, .dialog, .toast, .zoom-pill, .drawer--overlay`
- [ ] No `border-radius` other than 0, 4px, 6px, 999px (dots, avatars, badges)
- [ ] No raw hex outside the token file. No `rgb()` literals in components
- [ ] No spacing value outside `4 8 12 16 24 32 48 64` (and 0), outside canvas geometry
- [ ] No `font-size` below 11px, 11px only with `text-transform: uppercase`, no weight above 600
- [ ] Every `button`, `a`, `[role=tab]`, `[tabindex]` has `:focus-visible { outline: 2px solid var(--accent-500); outline-offset: 2px; }`
- [ ] `background: var(--accent-500)` appears only on `.btn-primary`, the brand tile, checked controls, count badges, progress fill, and port fills
- [ ] At most one `.btn-primary` visible per region and one per page apart from dialogs
- [ ] `prefers-reduced-motion` media query present and tested
- [ ] `font-variant-numeric: tabular-nums` on numbers
- [ ] Lucide icons 16 or 18px (14 in dense rows) with rendered stroke 1.5px, no emoji, no text glyph icons
- [ ] No string matching `/[a-z]{4}-\d{8}T\d{6}Z/`, `"run_id"`, `recipe`, `run.start`, `node.start` rendered outside Diagnostics
- [ ] Window does not scroll, panels do. No horizontal scroll at 1280
- [ ] Screenshot at 1280x800 for each page, sidebar expanded and collapsed, plus Cmd+K open and dark mode Home

---

## 7. Top 10 things that make dev-built UIs look amateur, and the fix

| # | Tell | Fix (Arc rule) |
|---|---|---|
| 1 | **Raw data on the surface**: JSON, run ids as titles, file paths, `unchecked: false` | Human titles, plain-English status, everything technical behind a "Diagnostics" disclosure (3.4 Activity) |
| 2 | **Library-default charts**: black frame, double grids, "Bode plot for sys[3]", tiny text, white box in a grey well | Section 4.1: token palette, units, direct labels, rendered at display size, themed |
| 3 | **Big radii and soft shadows**: 12 to 16px corners, shadowed cards inside cards | 4 and 6px radii, 1px hairlines, shadow only on floating layers (2.4) |
| 4 | **Saturated blue everywhere**: filled pills for status, blue outlines on tabs, several primary buttons | Status = tinted tag + word. One filled cobalt button per region (2.5) |
| 5 | **Weak type hierarchy**: everything 14px regular, monospace metadata, no tabular numbers, unit glued to value wrong | Ramp in 2.2, tabular figures, `5.00 V` with real symbols, mono only for code |
| 6 | **Dead space and tiny content**: small diagram in a huge empty box, empty inspector, content pinned left | Fit content to its container (4.3 Scale), hide empty panels, centre at max width (3.1) |
| 7 | **Missing states**: no empty, loading, error, stale states, developer text like "Use the CLI" | State table in 2.7, copy with an action |
| 8 | **Off-grid spacing**: 10, 14, 18, 20px gaps, edges that almost align | Tokens only, checklist rule in 6, align edges on the 8px layout grid |
| 9 | **Inconsistent components**: three card styles, different thumbnails sizes, tabs that look like buttons | One component per job: tile, row, tag, tab. Same thumbnail size and style (3.2) |
| 10 | **Page-level scroll and layout shift**: a sidebar list that makes the page 16,000px tall, content that jumps on load | Panels scroll, window does not. Skeletons at final size. Reserve space for images (3.1, 2.7) |

Honourable mentions: letter glyphs as icons, chips of engine names in the header, inconsistent icon stroke weights, hover states that move things, tooltips on everything, and copy with exclamation marks or em dashes.

---

## 8. What to avoid, from the September UI (`round0/*.png`)

I opened all four captures. Reference only.

| File | What it shows | Avoid |
|---|---|---|
| `ui-checked-run.png` | A run page titled with an id (`brpx-20260911T080022Z`), then a pretty-printed JSON block, then an empty "Artifacts" box. Header says "127.0.0.1 · named runs · exact token unchecked". Sidebar lists three monospace ids. A card with a 16px corner radius | Ids as titles, JSON as content, localhost and jargon in the header, answer missing, mono as the default |
| `ui-empty.png` | One paragraph of developer copy ("Photo confirm never simulates by itself", "exact token") with a saturated blue "unchecked" pill inline. Sidebar says "No runs yet. Use the CLI." The panel is blank below | Copy that explains the implementation, no action, filled accent pill used as status, a blank screen |
| `ui-control-bode-full.png` | Header chips ("Numeric", "SPICE", "MATLAB via Arc", "Simulink via Arc"). Heavy pill tab buttons with a permanent blue outline. A shadowed 16px card containing a grey well containing a small unlabeled-looking diagram. Block diagram has an arrow entering the sum block from below overlapping the feedback line, the output label floating, and the feedback box drawn off the wire. Plots are matplotlib defaults inside another rounded card: black frame, major and minor gridlines, tiny text, cropped, auto title "Bode plot for sys[3]" | Chips as noise, nested cards, shadowed rounded containers, overlapping arrows, floating labels, default plots |
| `ui-block-diagram-full.png` | A 1280 x 15,954px full-page capture: the sidebar run list (ids, repeated "unchecked" tags) runs the page to 16,000px. The diagram area is a large empty rectangle | Unbounded lists in the page flow, no search or grouping, empty canvas |

Note: `design-loop/studio-r1/` also exists (two screenshots of the Control tab built on 13 Nov). I treated it as pre-round-1 evidence. It repeats the sidebar id dump and the header chips, shows block text at about 7px, a small diagram in a large canvas, four tall margin cards ("Infinite", "No crossover" with a paragraph each), an empty inspector card with a hint sentence, and a Bode image with white margins in a grey well. All of these are covered by sections 3.5 and 4.

---

## 9. Source gaps and open questions

1. **Cobalt focus ring fails contrast** (about 1.9:1). Fixed in C6.
2. **`--text-muted` fails AA** (3.47:1). Fixed in C7. Cobalt's own contrast table admits it.
3. **Input borders**: `--border` is 1.27:1 and `--border-strong` is 1.49:1 on white. WCAG 1.4.11 expects 3:1 for the boundary of a control unless other cues identify it. Arc keeps hairlines for calm density, with a filled label and 36px height as the cue. If accessibility is mandatory for coursework, add `data-contrast="strict"` that sets input borders to `#8A8A86` (3.47:1). Needs a decision from the owner.
4. **The spec never defines "Checked", "Unchecked", "Failed", "Running"**. I defined them in 3.4 and 2.5. Product needs to confirm: what tolerance, what counts as an independent check, and whether a human check can mark a problem Checked.
5. **Spec lists "agent conversation" nowhere on the problem page** (only Work and Activity tabs). I placed the thread in Activity and an ask bar pinned at the bottom (3.4). Confirm with product.
6. **Plot theming for dark mode**: the Visual Kit is matplotlib. Dark mode parity needs SVG output that reads CSS variables, or two renders. Not in the spec.
7. **Cobalt's chart rule "horizontal gridlines only"** conflicts with log-frequency plots. Resolved in C13.
8. **Symbol standard** (IEEE or IEC) is unspecified. IIT Roorkee material may use either. I defaulted to IEEE and made it a setting. Confirm with a student.
9. **Cobalt rail items are 40x40 and 20px icons**, the spec says 16 to 18px. Resolved in C3 and C4.
10. **Studio keyboard model, snap grid and zoom range** are not in the spec. Defined in 4.4. Studio canvas internals belong to the Control Studio agent, so the builder must coordinate.
11. **Responsive**: DESIGN.md is phone-first, spec says 1280 to 1600. Phone is out of scope (C17).
12. **Cobalt's `body` is 14/22**. 22px is not on the 4px scale. I kept it (it is Cobalt's value) but new line heights SHOULD prefer 20, 24, 28, 32.
13. **Lucide stroke ambiguity**: "1.5 stroke" can mean the prop or the rendered width. Resolved in C5 and needs an eye check in round 1.
14. **The spec says Recent items show a "subject dot and status"** but not which colours map to which subject. Defined in 2.5.

---

## 10. Evidence used (public sources, checked 13 Nov 2026)

These ground the rules. Where I paraphrase, I paraphrase; I do not quote beyond a few words.

- **Linear, "How we redesigned the Linear UI (part II)"** ([linear.app/now/how-we-redesigned-the-linear-ui](https://linear.app/now/how-we-redesigned-the-linear-ui)): the refresh set out to reduce visual noise, keep alignment, and raise hierarchy and density of navigation; themes are generated from three inputs (base colour, accent colour, contrast) in LCH instead of about 98 hand-set variables; Linear limited how much chrome colour (blue) went into its neutrals to look more neutral and timeless; text and neutral icons got darker in light mode; Inter Display for headings, Inter for the rest. Informs: neutral-first, one accent, hierarchy before decoration, dense navigation.
- **Vercel Geist, colours** ([vercel.com/geist/colors](https://vercel.com/geist/colors)): scale steps 100 to 1000 have fixed roles: 100 to 300 component backgrounds (default, hover, active), 400 to 600 borders (default, hover, active), 900 secondary text and icons, 1000 primary text and icons. Guidance to "draw each border once" and to keep shadows translucent. Informs: borders vs fills, hover and active steps, one border per edge (C9), and my state table.
- **Vercel Geist, typography** ([vercel.com/geist/typography](https://vercel.com/geist/typography)): Copy 14 is the most commonly used text style, Label 14 the most common label, Label 12 is for tertiary text in busy views, tabular numerals for numbers. A third-party snapshot of Geist's published recipes ([anglehq.com/brand/source/typography](https://www.anglehq.com/brand/source/typography), dated 8 Sep 2026) shows heading-16 at 16/24, weight 600, tracking -0.32px, heading-20 at 20/26, weight 600, tracking -0.4px, copy-14 at 14/20, button text 500. Informs: 14px default, 600 headings with negative tracking, 500 buttons. Arc follows the cobalt ramp, not Geist's, wherever they differ (for example 14/22 body, -0.01em at 20px).
- **Vercel Geist, materials** ([vercel.com/geist/materials](https://vercel.com/geist/materials)): surfaces ("on the page") use a 6px radius at base, floating layers (tooltip, menu, modal) are a separate lifted category. Informs: shadow only for floating layers. Arc keeps 6px for both (C16).
- **MathWorks Control Algorithm Modeling Guidelines (MAAB)**: jc_0903 ([page](https://www.mathworks.com/help/simulink/mdl_gd/maab/jc_0903prohibitionofoverlappingorcrossingofblocksandsignallines.html)): blocks, names and labels shall not overlap, signal lines shall not overlap blocks or each other, line crossing style set to Line Hop. db_0032 ([page](https://www.mathworks.com/help/simulink/mdl_gd/maab/db_0032signallineconnections.html) and [check](https://www.mathworks.com/help/slcheck/ref/check-signal-line-connections.html)): no more than two sub-lines at a branch, no unnecessary bends, no slanting lines. db_0141 ([page](https://www.mathworks.com/help/simulink/mdl_gd/maab/db_0141signalflowinsimulinkmodels.html)): signals flow left to right with feedback allowed right to left, parallel blocks arranged top to bottom. `Simulink.connectBlocks` documents orthogonal routing that avoids overlaps ([page](https://www.mathworks.com/help/simulink/slref/simulink.connectblocks.html)). Informs all of 4.3.
- **Lucide docs** ([sizing](https://lucide.dev/guide/react/basics/sizing), [stroke width](https://lucide.dev/guide/react/basics/stroke-width)): icons default to 24px and a 2px stroke, `strokeWidth` is a prop, `nonScalingStroke` keeps the on-screen stroke constant, and the component also exposes `absoluteStrokeWidth` ([source](https://github.com/lucide-icons/lucide/blob/main/packages/lucide-react/src/Icon.ts)). Informs: C5.
- **WCAG 2.2** ([What's new](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)): SC 2.5.8 Target Size (Minimum, AA) is 24 x 24 CSS px with exceptions. SC 2.4.13 Focus Appearance (AAA) asks for an indicator at least as large as a 2px perimeter with 3:1 contrast between focused and unfocused states. SC 2.4.11 Focus Not Obscured (AA). Informs: C3, C6, and the sticky ask bar and drawer rules.
- **Contrast figures** in C6 and C7 and section 2 were computed by me with the WCAG relative-luminance formula from the cobalt hex values.

Not verified from primary sources (these are Arc rules informed by general practice, not citations): the Cmd+K layout numbers, the shortcut map, the g-then-key navigation, zoom steps, the exact Studio panel widths, and the Notion, Figma and Hex behaviours. I did not fetch Notion, Figma or Hex design writing for this version. If a round needs it, add it to v1.1.
