# Cobalt UI — Design System v1.2

**Status:** v1.2 · 2026-10-13 · standalone (not tied to any one product)
**For:** people and coding agents building operational and technical software, such as dashboards, control-room consoles, monitoring tools, decision feeds, and technical reading tools.
**One-line brief:** a calm, high-density technical workstation for making decisions from complex information, with a cobalt accent that tells you where you are and what to do next.

This document is self-contained. An agent can build a compliant screen from this file alone. Product-specific rules (brand name, claims, domain policies) belong to the product that adopts this system.

---

## 00 — How to use this document (agents read first)

### Reading order

1. **§01 The defining rule** and **§02 Rules summary**. These are the non-negotiables.
2. **§05 Color** and **§06 Typography**. Copy the token block from §16 and the font link from §06 before writing any styles.
3. **§08 Page templates**. Pick the closest template and start from it.
4. **§09 Components**. Use the reference markup. Do not invent new component styles if one here fits.
5. **§15 Review checklist**. Run it before you call the work done.

### Rule language

- **MUST / MUST NOT**: a hard rule. Breaking it means the screen is not compliant.
- **SHOULD / SHOULD NOT**: the default. Deviate only with a stated reason.
- **MAY**: allowed, optional.

### Defaults you must not drop

- The accent is **cobalt (`#2F6FEB`) by default**. Do not swap it for gray, black, or another hue unless the product explicitly sets `data-accent`.
- Category 2 is **copper (`#E07A3F`)**, so data series never blend into the cobalt structural indicators.
- **Every screen MUST show the accent**, even a screen with nothing to decide. See §05.3 "Minimum presence".
- Use the supporting palettes (status, categories, chart colors). A screen with only grays and one button is under-designed, not "clean".

### Token discipline

- MUST use tokens (`var(--…)` or the Tailwind names in §16). MUST NOT hard-code hex values, pixel spacing, radii, or shadows in components.
- If a value you need is not a token, re-check the layout before adding one.

---

## 01 — The defining rule

> **Quiet neutral structure. A cobalt accent for intent. Full-strength color only where a decision lives.**

The workspace is built from calm warm-gray neutrals and thin lines. The accent (cobalt by default) is always present in small, precise amounts: it marks where you are, what is selected, and the main series in a chart. Its **filled, full-strength** form is saved for the one thing a person needs to do right now.

Supporting colors give data and status their meaning: categories, health, warnings. They are tinted and quiet, never loud. Warmth comes from the neutrals and the copper data color, not from the accent.

This makes the interface read as a professional, stable, technical workstation: alive, but never shouting.

---

## 02 — Rules summary

| # | Rule | Level |
|---|------|-------|
| R1 | The accent appears on every screen in its **trace** form: active navigation, focus, links, selected controls, primary chart series. | MUST |
| R2 | The accent **fill** (solid `--accent-500` background) is used only for the primary button, the brand mark, checked controls, and small count badges. | MUST |
| R3 | At most **one** filled primary button per region (one feed item, one panel, one dialog). | MUST |
| R4 | No accent-filled sections, banners, headers, or page backgrounds. Large accent areas use the tint (`--accent-50`) at most. | MUST |
| R5 | Sections have no shadow. Shadow only on menus, popovers, toasts, dialogs, and floating bars. | MUST |
| R6 | Borders are 1px. 2px only for focus rings and active indicators (nav, tabs). | MUST |
| R7 | Corner radius is 4px (controls) or 6px (sections). Pills only for status dots, avatars, and count badges. | MUST |
| R8 | Every gap is on the spacing scale `4 8 12 16 24 32 48 64`. | MUST |
| R9 | Color never carries meaning alone. Every colored state also has a word or an icon. | MUST |
| R10 | Accent text uses `--accent-700` (or `--accent-600` at 16px and up), never `--accent-500`. | MUST |
| R11 | Text is never smaller than 11px. Only uppercase labels use 11px. | MUST |
| R12 | No gradients, glassmorphism, glow, pulsing, or decorative illustration. | MUST NOT |
| R13 | Key figures in sentences are emphasised with weight (600), not color. | SHOULD |
| R14 | Content reads top to bottom as Observation → Context → Recommendation → Action → Outcome. | SHOULD |
| R15 | Charts use the categorical palette in order, accent first. Status colors appear in charts only to mark a breach or target. | SHOULD |

---

## 03 — Design philosophy

The interface should feel:

| Feel | Not |
|------|-----|
| Precise | Polished for its own sake |
| Quiet | Visually empty or bland |
| Warm (warm-gray neutrals, copper data) | Sterile |
| Dense | Cluttered |
| Operational | Consumer SaaS |
| Structured | Card-heavy |
| Confident | Loud, urgent, salesy |

It is **one continuous workspace**, not a collection of floating widgets. Someone with a shift to run should be able to open it, read two items, act on one, and leave in under a minute.

### Design targets

| Target | Meaning in practice |
|--------|---------------------|
| Time to first decision | The most urgent decision is visible without scrolling on a 1366×768 screen. |
| Scan speed | Each item can be understood from its first line plus its key figure. |
| Trust | Every recommendation shows its basis, its expected impact, and who acts. |
| Calm under load | Ten open items look as orderly as two. Density rises; loudness does not. |
| Identity | The accent is recognisable within a second of opening any screen. |

---

## 04 — Visual principles

### Surface

- Near-white canvas (`--canvas`), never pure white for the page.
- White (`--surface`) for content.
- Very light warm gray (`--surface-subtle`) for secondary areas: rails, input wells, table headers, inset context.
- Tints (`--accent-50`, status and category tints) for selected, recommended, or categorised things.
- Almost no shadows. Depth comes from surface steps, tints, and borders.

### Structure

- Thin 1px borders define structure.
- Minimal radius: 4px controls, 6px sections.
- Large, deliberate whitespace between major sections; tight spacing inside related groups.
- Cards behave as **sections of the workspace**, not floating objects.

### Information hierarchy

Every decision surface follows one sequence:

```
Observation → Context → Recommendation → Action → Outcome
```

| Step | Answers | Treatment |
|------|---------|-----------|
| Observation | What happened? | `--text-primary`, key figures at 600 |
| Context | Why does it matter here? | `--text-secondary`, or an inset `--surface-subtle` area, category tags |
| Recommendation | What should we do? | `--accent-500` border, `--accent-50` background, `--accent-700` label |
| Action | Who acts, and how? | One filled accent button, optional secondary and quiet actions |
| Outcome | Did it work? | Short sentence, result figure in a status color, muted timestamp |

---

## 05 — Color

Color has four jobs, and each job has its own palette:

| Palette | Job | Default |
|---------|-----|---------|
| **Neutrals** | Structure: page, surfaces, lines, text | Warm grays |
| **Accent** | Identity and intent: where you are, what's selected, what to do | Cobalt `#2F6FEB` (swappable) |
| **Status** | State: good, warning, critical, informational | Green, amber, red, blue |
| **Categories** | Data: series, groups, owners, areas | Six harmonised hues, accent first, copper second |

### 5.1 Neutrals

| Token | Value | Role |
|-------|-------|------|
| `--canvas` | `#FAFAF9` | Page background |
| `--surface` | `#FFFFFF` | Sections, cards, inputs |
| `--surface-subtle` | `#F5F5F4` | Rails, table headers, inset context, hovered rows |
| `--surface-sunken` | `#EFEFED` | Pressed states, track of progress bars and toggles |
| `--border` | `#E4E4E2` | All structural lines |
| `--border-strong` | `#D4D4D1` | Hovered controls, input hover |
| `--text-primary` | `#202020` | Primary content |
| `--text-secondary` | `#5F5F5C` | Supporting content |
| `--text-muted` | `#8A8A86` | Metadata, timestamps, placeholders |
| `--text-inverse` | `#FFFFFF` | Text on filled accent or dark surfaces |

### 5.2 Accent scale (default: cobalt)

The accent is a full scale, so it can be used at the right strength in each place. `--accent-500` is the signature color. Cobalt is the industry-standard accent for operational tools, monitoring panels, and developer consoles: it reads as stable and technical rather than as an alert.

| Token | Cobalt (default) | Use |
|-------|------------------|-----|
| `--accent-50` | `#EEF3FE` | Tints: recommendation background, selected rows, active nav background |
| `--accent-100` | `#DCE6FD` | Hovered tint, active category tag background, progress track highlight |
| `--accent-200` | `#B9CDFB` | Chart area fills, subtle accent borders |
| `--accent-300` | `#8AADF6` | Secondary chart series, disabled accent |
| `--accent-500` | `#2F6FEB` | **Signature.** Primary button fill, brand mark, focus rings, recommendation border, active indicator, main chart series, checked controls |
| `--accent-600` | `#2459C9` | Hover on solid buttons; accent text 16px and up; active nav icon |
| `--accent-700` | `#1D47A3` | Accent text of any size: labels, links, inline anchors, recommendation copy; pressed fill |
| `--accent-800` | `#173879` | Text on `--accent-100` tags |

Aliases kept for compatibility: `--action` = `--accent-500`, `--action-soft` = `--accent-50`, `--action-ink` = `--accent-700`.

#### Swapping the accent

The accent is a theme. Set `data-accent` on the root to change it. Everything that uses the accent changes with it; nothing else does.

| Preset | 50 | 100 | 500 | 600 | 700 | 800 | Category swap |
|--------|----|----|-----|-----|-----|-----|---------------|
| `cobalt` (default) | `#EEF3FE` | `#DCE6FD` | `#2F6FEB` | `#2459C9` | `#1D47A3` | `#173879` | — (category 2 is copper) |
| `orange` | `#FFF3F0` | `#FFE3DC` | `#F75440` | `#E23F2B` | `#C2361F` | `#962A18` | Category 2 back to slate blue, so copper doesn't clash with the orange accent |
| `teal` | `#E8F6F5` | `#CDEBE8` | `#0F8A84` | `#0C746F` | `#0A615C` | `#084A47` | Category 3 to slate blue |
| `graphite` | `#F2F2F1` | `#E4E4E2` | `#2A2A2A` | `#1F1F1F` | `#202020` | `#111111` | — |

Rules for custom accents:

- `--accent-500` MUST give at least 3:1 against white; `--accent-700` MUST give at least 4.5:1.
- The accent SHOULD NOT be red or green, because those are the critical and success hues. If a brand needs one, shift the status hues away from it.
- When the accent changes, the first categorical chart color changes with it (§05.5), and any category close to the new accent is swapped (table above).
- Cobalt shares the blue family with the `info` status. Keep them apart: `info` is only ever a dot, icon, or tag with its word, never a fill or a large tint next to the accent.

### 5.3 Using the accent without looking like spam

Any accent reads as spam when it looks like a discount sticker or an alarm: big filled blocks, many shouting buttons, caps-lock badges, flashing. Cobalt is calmer than a warm accent, but the same rules hold. It reads as **confident and operational** when it is precise: thin, consistent, and always meaning "this is where you are" or "this is what to do".

The accent has three strengths:

| Strength | What it looks like | Where | How much |
|----------|--------------------|-------|----------|
| **Trace** | 1–2px lines, icons, small text, chart lines, focus rings, checkboxes | Active nav indicator, active tab underline, links, focus, selected checkbox and radio, toggle on, main chart series, progress bar, sparkline, brand mark | Always present on every screen |
| **Tint** | `--accent-50` / `--accent-100` backgrounds | Recommendation block, selected rows, active nav item background, accent tags, hovered accent items | A few areas per screen |
| **Fill** | Solid `--accent-500` with white text | Primary button, count badge, brand mark tile | One filled button per region |

**Minimum presence.** Every screen MUST show at least:

1. The brand mark or active nav item in the accent.
2. The active tab or page indicator in the accent, if there are tabs.
3. The accent on the main series of any chart.
4. The accent focus ring on keyboard focus.

**Ceiling.** Accent (all strengths combined) SHOULD stay under about 10% of visible pixels, and filled accent under about 2%.

**Never:**

- Fill a section, header, banner, sidebar, or page background with `--accent-500`.
- Put more than one filled accent button in a region.
- Write body paragraphs in accent text.
- Use accent uppercase badges like "NEW", "HOT", "URGENT".
- Animate, pulse, or blink the accent.
- Place the accent fill right next to `--critical` (two alarms competing).

### 5.4 Status

Each status has a solid tone (dots, icons, chart marks), a text tone (≥4.5:1 on white), and a tint (backgrounds).

| Status | Solid | Text | Tint | Meaning |
|--------|-------|------|------|---------|
| `success` | `#2F9E6A` | `#25774F` | `#E8F5EE` | Confirmed good outcome, healthy, live |
| `warning` | `#E0A526` | `#94600B` | `#FCF4E1` | Drifting, approaching a limit, needs a look soon |
| `critical` | `#D0312D` | `#B0241F` | `#FCECEB` | Breached, failed, stopped |
| `info` | `#3B79C4` | `#2C5E99` | `#EAF2FB` | Neutral notice, scheduled, in progress |

Tokens follow the pattern `--success`, `--success-text`, `--success-tint` (same for `warning`, `critical`, `info`).

- Status colors appear as dots, icons, text figures, tags, and thin chart marks. Tints MAY back a status tag or a banner.
- Warning amber is deliberately yellow-leaning so it does not get confused with the copper category color.
- MUST NOT use status colors decoratively, for example coloring section headers by status.

### 5.5 Categories (data and grouping)

Use these, in this order, for chart series, group tags, owners, areas, and avatars. They are tuned to sit together at the same visual weight.

| # | Name | Solid | Tint | Text on tint |
|---|------|-------|------|--------------|
| 1 | Accent | `var(--accent-500)` | `var(--accent-100)` | `var(--accent-800)` |
| 2 | Copper | `#E07A3F` | `#FCEEE5` | `#8F4519` |
| 3 | Teal | `#2A9D8F` | `#E3F4F1` | `#1C6B61` |
| 4 | Ochre | `#C99A2E` | `#F8F0DC` | `#7A5B12` |
| 5 | Plum | `#8E5B9A` | `#F3ECF5` | `#62386D` |
| 6 | Olive | `#7A8B3A` | `#F0F3E3` | `#4E5A20` |
| — | Other | `#A3A3A0` | `#F0F0EE` | `#5F5F5C` |

- Category 1 is always the accent, so the most important series carries the identity color.
- Category 2 is copper because it is the hue furthest from cobalt: the second series never blends into the layout's structural indicators. (Under the `orange` preset it reverts to slate blue `#4A6FA5` / `#E9EFF7` / `#2F4C77`.)
- Use category colors as tag tints, avatar backgrounds, chart lines, and 6px legend dots. MUST NOT use them as section backgrounds.
- After six categories, group the rest as "Other" instead of adding more hues.

### 5.6 Contrast reference (on white)

| Foreground | Ratio | Allowed for |
|------------|-------|-------------|
| `--text-primary` | ~16:1 | Everything |
| `--text-secondary` | ~6.4:1 | Everything |
| `--text-muted` | ~3.5:1 | Metadata and placeholders only; never decision-critical text |
| `--accent-500` | ~4.6:1 (4.1:1 on `--accent-50`) | Fills, borders, icons, chart lines, focus rings; not for text (R10) |
| `--accent-600` | ~6.3:1 | Icons, text 16px and up |
| `--accent-700` | ~8.5:1 (7.6:1 on `--accent-50`) | Accent text of any size |
| White on `--accent-500` | ~4.6:1 | Primary button label at 14px / 600 — meets WCAG AA with cobalt |
| White on `--accent-700` | ~8.5:1 | Primary button in strict-contrast mode |
| Status text tones | ≥4.5:1 | Text of any size |

**Strict-contrast mode.** Cobalt meets WCAG AA for the primary button by default. With a lighter custom accent (such as the `orange` preset, ~3.3:1), set `data-contrast="strict"` on the root where AA must be met everywhere: the primary button fill moves to `--accent-700` and everything else stays the same.

---

## 06 — Typography

### 6.1 Families

| Role | Family | Why |
|------|--------|-----|
| Interface, headings, labels, numbers | **Geist** | Compact, precise, neutral without being cold; excellent at small sizes; built-in tabular figures |
| Codes, IDs, raw readings | **Geist Mono** | Same design family; only where character alignment matters |

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
```

Next.js: `import { GeistSans } from "geist/font/sans"; import { GeistMono } from "geist/font/mono";`

Offline or static sites: bundle the variable fonts (`Geist-Variable.woff2`, `GeistMono-Variable.woff2` from the `geist` npm package, SIL Open Font License) and load them with `@font-face` instead of the Google Fonts link.

Approved alternatives, if Geist is unavailable (keep the pairing; do not mix):

| Sans | Mono |
|------|------|
| Inter (with `font-feature-settings: "cv11", "ss01"`) | JetBrains Mono |
| IBM Plex Sans | IBM Plex Mono |

Monospace is **not** used for labels, eyebrows, or general metadata. Use it only for IDs, codes, and raw readings such as `TAG-4471` or `0x3F`.

### 6.2 Scale

| Style | Size / line | Weight | Tracking | Use |
|-------|-------------|--------|----------|-----|
| `display` | 28 / 36 | 500 | -0.02em | Page title or greeting. One per screen. |
| `title` | 20 / 28 | 600 | -0.01em | Section titles, dialog titles |
| `heading` | 16 / 24 | 600 | -0.005em | Sub-section headings, item titles |
| `body-lg` | 16 / 26 | 400 | 0 | Observation and recommendation copy in feeds |
| `body` | 14 / 22 | 400 | 0 | Default UI text, table cells |
| `body-strong` | 14 / 22 | 600 | 0 | Key figures, names |
| `small` | 13 / 20 | 500 | 0 | Buttons, secondary lines, source names |
| `meta` | 12 / 16 | 400 | 0 | Metadata: mode, shift, time, counts |
| `label` | 11 / 16 | 600 | 0.06em, uppercase | Eyebrows, section labels, column headers, breadcrumbs |
| `kpi` | 28 / 32 | 500 | -0.02em, tabular | Metric values |

### 6.3 Rules

- Eyebrows and labels use **Geist 11px / 600 uppercase with 0.06em tracking** in `--text-secondary`, or `--accent-700` inside a recommendation. Never monospace, never below 11px, never lighter than `--text-secondary`.
- Metadata lines use **Geist 12px / 400** in `--text-muted`, separated by ` · `.
- MUST use `font-variant-numeric: tabular-nums` for numbers in tables, KPIs, and timestamps.
- SHOULD use at most three text styles in one section.
- MUST NOT use weights above 600, italics for emphasis, or text above 28px.
- Headings use slight negative tracking; body text uses none.

---

## 07 — Spacing, shape, depth, motion

### 7.1 Spacing

| Token | px | Typical use |
|-------|----|-------------|
| `--space-1` | 4 | Icon to label, dot to text |
| `--space-2` | 8 | Between metadata items, button groups, rail inset |
| `--space-3` | 12 | Label to content, header to body inside an item |
| `--space-4` | 16 | Compact section padding, gap between feed items, paragraph gap |
| `--space-5` | 24 | Default section padding, gap between regions in a panel |
| `--space-6` | 32 | Page gutter, gap between major regions |
| `--space-7` | 48 | Top margin above the page title |
| `--space-8` | 64 | Separation between unrelated areas |

Whitespace is part of the hierarchy: wide between sections, tight inside related information.

### 7.2 Shape, elevation, motion, layering

| Token | Value | Use |
|-------|-------|-----|
| `--radius-sm` | 4px | Buttons, inputs, tags, recommendation block, inset areas |
| `--radius-md` | 6px | Sections, workspace panel, dialogs, ask bar |
| `--radius-full` | 999px | Status dots, avatars, count badges only |
| `--elevation-1` | `0 1px 2px rgba(32,32,32,0.04), 0 4px 12px rgba(32,32,32,0.05)` | Menus, popovers, toasts, dialogs, floating bars |
| `--ease-out` | `cubic-bezier(0.22, 1, 0.36, 1)` | All transitions |
| `--duration-fast` | 120ms | Hover, press |
| `--duration` | 180ms | Appear, expand |
| `--z-rail` / `--z-sticky` / `--z-popover` / `--z-dialog` / `--z-toast` | 10 / 20 / 30 / 40 / 50 | Layering |

### 7.3 Icons

- Line icons, 1.5px stroke. Lucide, Phosphor (regular), or Tabler.
- Sizes: 16px inline, 20px in the rail, 14px in dense table controls.
- Default `--text-secondary`; `--text-primary` on hover; `--accent-600` when active or selected; status solid tones for status icons.

---

## 08 — Layout and page templates

### 8.1 Shell

```
┌──────┬────────────────────────────────────────────────────────────┐
│ rail │ breadcrumb bar                                   (44px)    │
│ 56px ├────────────────────────────────────────────────────────────┤
│ [■]  │                                                            │
│      │   EYEBROW                                                  │
│ ▣ ←  │   Page title                                    (display)  │
│ ◫    │                                                            │
│ ▤    │   ┌────────────────────────────────────────────────────┐   │
│ ⋮    │   │ section                                            │   │
│      │   └────────────────────────────────────────────────────┘   │
│      │   ┌────────────────────────────────────────────────────┐   │
│      │   │ section                                            │   │
│ ⟳    │   └────────────────────────────────────────────────────┘   │
│ (AB) │   ┌────────────────────────────────────────────────────┐   │
│ ⇥    │   │ ask bar / command bar (optional)          (56px)   │   │
└──────┴───┴────────────────────────────────────────────────────┴───┘
 [■] = brand mark tile in --accent-500
 ← = active item: --accent-50 background, --accent-600 icon, 2px --accent-500 indicator
```

| Region | Spec |
|--------|------|
| Window | `--canvas` |
| Rail | 56px wide, `--surface`, 1px right `--border`. Brand mark tile (28px, `--accent-500`, `--radius-sm`, white mark) at top. Destinations, then account avatar and collapse at the bottom. |
| Workspace panel | One `--surface` panel, `--radius-md`, 1px `--border`, inset `--space-2` from the window. Everything lives inside it. |
| Breadcrumb bar | 44px, `label` style, 1px bottom `--border`. Past crumbs `--text-muted`; current crumb `--text-primary`. |
| Content column | **Centered** in the workspace, `--space-6` gutter. Max width 760px (`--reading-w`) for a reading column, 1280px for tables and boards, full width for control-room views. Never pin a narrow column to the left of a wide panel: the leftover space becomes one dead slab on the right. |
| Context column | Reading pages (feeds, articles, details) pair the reading column with a 264px (`--aside-w`) sticky context column, separated by `--space-7`. The two are centered as one group (8+4). It holds a page outline (§9.19) and at most one or two small context blocks. |
| Ask bar | Optional, pinned to the bottom of the workspace. |

### 8.2 Grid and responsive

- 12 columns, 24px gutters. Common splits: 12, 8+4, 6+6, 4+4+4. Top and left edges in a row MUST align.

| Width | Behavior |
|-------|----------|
| ≥ 1200 | Reading pages SHOULD show the right-hand context column (reading column + context column, centered together). |
| 768–1199 | The context column hides; the reading column stays centered at 760px. Other splits collapse to one column; tables scroll inside their section. |
| < 768 | Rail becomes a 56px bottom bar (max five icons). Panel loses inset and border. Section padding `--space-4`. |

### 8.3 Density

Set `data-density="compact"` on the root.

| Mode | Section padding | Row height | Feed text |
|------|-----------------|------------|-----------|
| Comfortable (default) | 24px | 40px | 16px |
| Compact | 16px | 32px | 14px |

### 8.4 Templates

**T1 Decision feed (home).**

```
eyebrow + display:  OVERVIEW · Good evening — two items need a decision.
KPI row (optional): 3–4 metrics in one section, sparklines in the accent
tabs:               Needs decision (2) | Watching (5) | Resolved      ← active tab underline in accent
feed:               [decision item: primary]    ← tint + filled button
                    [decision item: secondary]  ← accent border, outline button
                    [informational item]        ← category tag, status dot, no fill
                    [outcome item]              ← status figure
ask bar
```

Order by urgency, then time. Empty state: "Nothing needs a decision right now." plus the last check time.

**T2 Investigation (detail).**

```
breadcrumb:   OVERVIEW / LINE 3 / MOTOR 8
title row:    title + status tag + category tag                [secondary] [primary]
8 + 4 split:  [chart: subject series in accent, others gray/category] [context: facts, owner avatar, timeline]
section:      evidence table
section:      recommendation + actions, or outcome
```

**T3 Table workspace.**

```
title row:   title + count tag                       [filter] [secondary] [primary?]
toolbar:     search, filter chips (selected chips tinted accent), density toggle
section:     table with sticky header; selected rows tinted accent; status and category tags
selection:   sticky action bar at the bottom of the section
```

**T4 Settings / form.**

```
title + tabs (accent underline)
section per group: label column (4) + fields (8); toggles and checkboxes use the accent
footer bar:  [Cancel (quiet)] [Save (primary, disabled until changed)]
```

---

## 09 — Components

Class names use the `ops-` prefix; rename freely, keep the structure. CSS is in §16.2.

### 9.1 Navigation rail

- Brand mark tile at the top: 28px, `--accent-500` fill, white mark. This is the screen's guaranteed accent.
- Item: 40×40 hit area, `--radius-sm`, icon 20px in `--text-secondary`.
- Hover: `--surface-subtle` background, icon `--text-primary`.
- Active: `--accent-50` background, icon `--accent-600`, plus a 2px `--accent-500` indicator on the rail's left edge.
- Groups separated by a 1px `--border` line, 24px wide.
- Open-decision badge: 6px `--accent-500` dot at the icon's top-right, or a count badge (16px tall, `--accent-500`, white 11px/600 text).
- Tooltip on hover after 400ms with the destination name.

```html
<nav class="ops-rail" aria-label="Primary">
  <a class="ops-rail__brand" href="/" aria-label="Home"><svg aria-hidden="true">…</svg></a>
  <a class="ops-rail__item" href="/" aria-current="page" title="Overview"><svg aria-hidden="true">…</svg></a>
  <a class="ops-rail__item" href="/assets" title="Assets"><svg aria-hidden="true">…</svg></a>
  <hr class="ops-rail__sep">
  <a class="ops-rail__item" href="/alerts" title="Alerts">
    <svg aria-hidden="true">…</svg><span class="ops-badge" aria-label="2 open decisions">2</span>
  </a>
</nav>
```

### 9.2 Page header

```html
<header class="ops-page-header">
  <div class="ops-label">Overview · Shift 3</div>
  <h1 class="ops-display">Good evening — two items need a decision.</h1>
</header>
```

- Eyebrow 8px above the title, in `--text-secondary`. The eyebrow MAY use `--accent-700` when the page is about one open decision.

### 9.3 Tabs

- 40px tall, `small` text in `--text-secondary`, 1px bottom `--border` under the whole tab row.
- Active: `--text-primary`, 600, 2px `--accent-500` underline.
- Count: neutral tag next to the label; on the active tab, an accent tint tag (`--accent-100` / `--accent-800`).

### 9.4 Section

- `--surface`, 1px `--border`, `--radius-md`, padding `--section-pad`.
- Header: optional `label` eyebrow plus `title`, header actions right-aligned.
- MAY contain an inset: `--surface-subtle`, `--radius-sm`, padding `--space-3` `--space-4`.
- MUST NOT have a shadow, a colored header bar, a side stripe, or a hover lift.

### 9.5 Decision item (signature component)

Anatomy:

1. **Item header:** source avatar (20px, category tint), source name (`small` 600), metadata (`meta`, ` · ` separators), status dot or tag.
2. **Observation:** `body-lg`, key figures at 600.
3. **Context:** same paragraph or inset; category tags for line, area, or asset.
4. **Recommendation block.**
5. **Action row:** primary, secondary, quiet; owner avatar and name on the right.
6. **Outcome line** after acceptance.

Spacing: header → observation `--space-3`; observation → recommendation `--space-4`; recommendation → actions `--space-3`.

```html
<article class="ops-item" aria-labelledby="item-41-obs">
  <div class="ops-item__header">
    <span class="ops-avatar ops-cat-2" aria-hidden="true">M</span>
    <span class="ops-source">Monitoring agent</span>
    <span class="ops-meta">Watch · Threshold crossed this shift</span>
    <span class="ops-tag ops-tag--warning"><span class="ops-dot"></span>Drifting</span>
  </div>

  <p class="ops-item__obs" id="item-41-obs">
    Humidity climbed <strong>above 58%</strong> on the dehumidifier bypass, the same
    setup that preceded the last round of valve faults. Line 3 is already
    <strong>down 4.2%</strong> this shift.
  </p>

  <div class="ops-item__tags">
    <span class="ops-tag ops-cat-3">Line 3</span>
    <span class="ops-tag ops-cat-4">Filler</span>
  </div>

  <div class="ops-reco ops-reco--primary">
    <div class="ops-label ops-reco__label">Recommendation</div>
    <p class="ops-reco__action">Turn on the Line 3 zone dehumidifier to bring humidity below 58%.</p>
    <p class="ops-reco__impact">Projected about 40% fewer valve faults this week, based on the last three humidity events.</p>
  </div>

  <div class="ops-item__actions">
    <button class="ops-btn ops-btn--primary">Accept and assign</button>
    <button class="ops-btn ops-btn--secondary">View evidence</button>
    <button class="ops-btn ops-btn--quiet">Decline</button>
    <span class="ops-item__owner"><span class="ops-avatar ops-cat-5" aria-hidden="true">RM</span>Shift lead, Line 3</span>
  </div>
</article>
```

Informational item: same header, observation, tags; **no** recommendation block; the button is `--secondary`; a status dot or tag shows its state.

### 9.6 Recommendation block

```
┌─────────────────────────────────────────┐
│ RECOMMENDATION                          │
│                                         │
│ Recommended action                      │
│                                         │
│ Expected impact                         │
└─────────────────────────────────────────┘
```

| Part | Primary (top decision) | Secondary (other open decisions) |
|------|------------------------|----------------------------------|
| Container | 1px `--accent-500` border, `--accent-50` background, `--radius-sm`, padding `--space-3` `--space-4` | 1px `--accent-200` border, `--surface` background |
| Label | `label`, `--accent-700` | `label`, `--accent-700` |
| Action sentence | `body-lg` 500, `--accent-700`, one sentence, verb first | `body-lg` 500, `--text-primary` |
| Expected impact | `body`, `--text-secondary`: estimate, basis, window | Same |
| Button | Filled primary | Outline accent (`--accent` variant) |

- One recommendation per block. Alternatives go behind "Other options (2)".
- Impact MUST be labelled as an estimate unless measured.

### 9.7 Buttons

| Variant | Fill | Border | Text | Use |
|---------|------|--------|------|-----|
| **Primary** | `--accent-fill` | none | white, 600 | The one decision action in a region |
| **Accent outline** | `--surface` | 1px `--accent-500` | `--accent-700`, 600 | Decision actions that are not the top one; "Create" actions in toolbars |
| **Secondary** | `--surface` | 1px `--border` | `--text-primary` | Navigation to detail, non-decision actions |
| **Quiet** | transparent | none | `--text-secondary` | Dismiss, snooze, details, cancel |
| **Destructive** | `--surface` | 1px `--border` | `--critical-text` | Delete, revoke. Always confirm. |

| Spec | Value |
|------|-------|
| Height | 32px default, 36px forms, 28px dense tables |
| Padding | 0 `--space-3` (0 `--space-4` at 36px) |
| Text | 14px / 600 for primary and accent outline, 14px / 500 otherwise |
| Radius | `--radius-sm` |
| Gap | `--space-2` |

States: hover (primary `--accent-600`; outline `--accent-50` fill; secondary `--border-strong`; quiet `--surface-subtle` fill), pressed (primary `--accent-700`), focus (2px accent ring, 2px offset), disabled (40% opacity), loading (14px spinner replaces the icon; width stays).

Labels are verbs that say what happens: "Accept and assign", "View the investigation", "Decline".

### 9.8 Links

- `--accent-700`, no underline at rest, underline on hover. In dense tables, `--text-primary` with an underline on hover.

### 9.9 Tags, status, badges, avatars

- **Tag:** 22px tall, `--radius-sm`, padding 0 `--space-2`, 12px / 500 text.
  - Neutral: `--surface-subtle` / `--text-secondary`.
  - Category: class `ops-cat-N`, category tint background with its text color.
  - Status: status tint background, status text color, leading 6px dot in the status solid tone.
  - Accent: `--accent-100` / `--accent-800`. For "selected" or "recommended" only.
- **Status dot:** 6px, `--radius-full`. Success, warning, critical, info solid tones; stale = hollow `--text-muted` ring. Never animated. Always paired with a word.
- **Count badge:** 16px tall, min-width 16px, `--radius-full`, 11px / 600 tabular. Neutral (`--surface-sunken` / `--text-secondary`) by default; `--accent-500` / white only for open decisions.
- **Avatar:** 20px (inline), 28px (lists), `--radius-full`, initials 11px / 600. Background and text from the category palette, assigned by a stable hash of the name.

### 9.10 Selection controls

- Checkbox and radio: 16px, 1px `--border-strong`, `--radius-sm` (checkbox). Checked: `--accent-500` fill, white check.
- Toggle: 32×18 track `--surface-sunken`; on = `--accent-500` track, white knob.
- Filter chip: neutral tag at rest; selected = `--accent-50` background, 1px `--accent-200` border, `--accent-700` text.

### 9.11 Table

| Part | Spec |
|------|------|
| Header | 36px, `--surface-subtle`, `label` style in `--text-secondary`, sticky |
| Rows | `--row-h`, 1px `--border` bottom, no zebra stripes |
| Cells | `body`; padding 0 `--space-4`; text left, numbers right with tabular figures |
| Hover | `--surface-subtle` |
| Selected | `--accent-50` background, checked accent checkbox |
| Status | Status tag in its own column |
| Category | Category tag or 6px category dot plus name |
| Inline bar | 4px bar in `--accent-500` on a `--surface-sunken` track for share or progress columns |

### 9.12 Charts

- **Series colors:** categorical palette in order. Series 1 (the subject) is the accent.
- **Focus mode:** when a chart supports a recommendation, the subject series is `--accent-500` at 2px and all others are `#C4C4C2` at 1.5px.
- **Area fill:** subject series MAY have an area fill from `--accent-500` at 12% to 0% opacity top to bottom (the only allowed gradient), or a flat `--accent-50`.
- **Gridlines:** horizontal only, 1px `--border`. No chart border.
- **Axes:** 12px `--text-muted`. Baseline only.
- **Thresholds and targets:** 1px dashed line in `--warning` or `--critical`, labelled at its right end.
- **Breach markers:** 6px dot in `--critical` on the data point.
- **Bars:** `--radius-sm` on the top corners only; 4px gaps between bars.
- **Tooltip:** `--surface`, 1px `--border`, `--radius-sm`, `--elevation-1`; series dot, name, value in `body-strong`.
- Direct labels at line ends; legend (6px dots + 12px text) only when labels collide.
- No 3D, no pie charts with more than three parts.

### 9.13 KPI row

```
LABEL                  ← label, --text-secondary
1,284 units            ← kpi style, --text-primary
▲ 4.2% vs last shift   ← 12px/600 in --success-text or --critical-text, with arrow icon
╱╲╱╲_╱‾               ← 24px sparkline in --accent-500
```

- KPIs sit in one section, divided by 1px vertical `--border` lines.
- MUST NOT build four separate colored KPI cards.

### 9.14 Progress

- Bar: 4px (inline) or 6px (standalone), `--radius-full`, track `--surface-sunken`, fill `--accent-500`. Complete = `--success`. Blocked = `--critical`.
- Steps: completed steps `--accent-500` dot plus `--text-primary` label; current step ring in `--accent-500`; future steps `--border-strong` ring.

### 9.15 Inputs

- Height 36px, `--surface`, 1px `--border`, `--radius-sm`, `body` text, padding 0 `--space-3`.
- Label above in `small` 500 `--text-primary` (forms) or `label` style (dense filters). Help text below in `meta`.
- Hover `--border-strong`; focus `--accent-500` border plus accent ring; error `--critical` border and `--critical-text` help with an icon.

### 9.16 Ask bar

- `--surface`, 1px `--border`, `--radius-md`, 56px, padding 0 `--space-4`.
- Leading icon `--text-muted`. Send button: 32px square, `--radius-sm`; neutral when empty; `--accent-500` fill with white icon once there is input.
- Focus: `--accent-500` border plus ring.

### 9.17 Dialog, popover, toast, banner

- **Dialog:** `--surface`, `--radius-md`, `--elevation-1`, max 480px, padding `--space-5`, `--overlay` backdrop. Title in `title`. Actions bottom-right, primary last.
- **Popover / menu:** items 36px, hover `--surface-subtle`, selected item has an accent check icon.
- **Toast:** bottom-left, `--surface`, `--elevation-1`, leading status dot, one line plus an optional quiet "Undo". Auto-dismiss after 6s unless it has an action.
- **Banner:** content-column width, `--radius-sm`, padding `--space-3` `--space-4`, leading 16px icon. Variants use status tints with 1px status-solid borders: `info`, `warning`, `critical`. No accent-filled banners.

### 9.18 Loading, empty, stale

- Skeletons: `--surface-subtle` blocks at content size, static or a 1.2s opacity fade.
- Spinner: 14px, `--accent-500` arc on a `--border` ring.
- Empty: one sentence in `--text-secondary`, last check time, at most one secondary action.
- Stale: hollow dot plus "Stale · last update 14 min ago". Stale data MUST be labelled before it supports a recommendation.

### 9.19 Page outline (context column)

The default occupant of the context column (§8.1): an "On this page" list that turns the spare width into wayfinding.

- Sticky at `top: calc(--crumb-h + --space-5)`; scrolls on its own if taller than the window.
- `label` heading "ON THIS PAGE", then a list with a 1px `--border` left edge. Links are 13/20, `--text-secondary`, with `--space-1` vertical padding.
- The section in view gets `aria-current="location"`: `--text-primary`, weight 500, and a 2px `--accent-500` left indicator (the same trace as the rail's active item). Only one item is current at a time.
- Built from the page's section titles. Anchor jumps respect `scroll-padding-top` so headings land below the sticky breadcrumb bar.
- Below it, at most one or two small blocks (an `inset` with a secondary action, key facts). Never a primary button, never a second recommendation.

```html
<aside class="ops-aside" aria-label="Page outline">
  <nav aria-label="On this page">
    <div class="ops-label">On this page</div>
    <ol class="ops-toc">
      <li><a href="#overview" aria-current="location">Overview</a></li>
      <li><a href="#evidence">Evidence</a></li>
    </ol>
  </nav>
</aside>
```

---

## 10 — Visual behavior

Hierarchy comes from these tools, **in this order**:

```
Position → Whitespace → Typography → Borders → Density → Color
```

Color is still last for hierarchy. Color is used freely for **meaning**: identity (accent), state (status), and grouping (categories). Never use color just to make something look important.

### Motion

- Animate opacity and position only, with `--duration-fast` / `--duration` and `--ease-out`.
- A new feed item fades in and moves 4px down into place. Tab underline slides between tabs. Nothing bounces, pulses, or loops.
- MUST honor `prefers-reduced-motion: reduce`.

---

## 11 — The decision lifecycle

| State | Visual change |
|-------|---------------|
| **Open** | Recommendation block (primary or secondary treatment). |
| **Accepted** | Block border `--success`, background `--success-tint`, label "ACCEPTED" in `--success-text`. `meta`: `Accepted by R. Mehta · 11:48 PM`. Buttons removed. |
| **Declined** | Border `--border`, background `--surface`, label "DECLINED" in `--text-secondary`. `meta`: `Declined by … · reason`. |
| **Snoozed** | Collapses to the header line plus `Snoozed until 06:00`. |
| **Outcome pending** | `info` tag "Checking outcome", `meta`: next reading time. |
| **Outcome confirmed** | One `body` sentence; figure in `--success-text`; `success` tag. |
| **Outcome missed** | One `body` sentence; figure in `--critical-text`; `critical` tag. Neutral wording. |
| **Expired** | Label "EXPIRED" in `--text-muted`, text in `--text-secondary`, no actions. |

### Human-in-the-loop rules

- An action that changes something in the real world SHOULD name who accepts it ("Accept and send to Line 3 lead").
- The accepted state MUST show who acted and when.
- Actions that need an approver MUST NOT be a one-click primary button. Offer "Request approval" instead.
- Irreversible actions MUST use a confirmation dialog.

---

## 12 — Content and copy

- Lead with the observation, in the user's operating language: line, shift, asset, order, part.
- Two sentences maximum for an observation.
- Key numbers carry unit and comparison ("18% above baseline", "down 4.2% this shift").
- Estimates are labelled as estimates, with a basis and a window.
- Name people and roles. Avoid "the system", "AI", "smart", "magic", "insights".
- Sentence case everywhere except `label` style.
- No exclamation marks, no emoji, no urgency words like "Act now" or "Don't miss".

| Avoid | Prefer |
|-------|--------|
| "⚠️ Anomaly detected!" | "Motor 8 current is 18% above baseline." |
| "AI recommends optimizing humidity" | "Turn on the Line 3 dehumidifier to bring humidity below 58%." |
| "Saves 40%!" | "Projected about 40% fewer valve faults this week, based on three past events." |
| "Submit" | "Accept and assign" |

---

## 13 — Accessibility

- MUST meet WCAG 2.2 AA for text, except the documented primary-button default (use `data-contrast="strict"` where AA is mandatory).
- `--text-muted` MUST NOT carry decision-critical information.
- Accent text MUST use `--accent-700` (any size) or `--accent-600` (16px semibold and up).
- Focus MUST be visible: `outline: 2px solid var(--focus-ring); outline-offset: 2px`.
- Minimum target 24×24px; 32px for primary actions.
- Every status and category color MUST have a text equivalent.
- Decision items are `article` elements with `aria-labelledby`. The feed is a list or `role="feed"`.
- Live items SHOULD be announced through a polite `aria-live` region, at most once per 10 seconds.

---

## 14 — Anti-patterns

| Anti-pattern | Why it breaks the system | Do instead |
|--------------|--------------------------|------------|
| **No accent anywhere** (all gray) | Bland; no identity; no sense of where you are | Meet the minimum presence in §05.3 |
| Accent-filled header, sidebar, banner, or hero | Reads as spam, an alarm, or a generic SaaS template | Accent trace and tint; fill only on the primary button |
| Several filled accent buttons | No single next action; salesy | One primary per region; others outline or secondary |
| "NEW" / "HOT" / "URGENT" accent badges | Marketing urgency | Neutral tag or status tag with a plain word |
| Accent body text | Hard to read, shouty | `--text-primary`; accent only for labels and links |
| Cobalt accent next to `info` blue fills | Two blues that mean different things | `info` only as a dot, icon, or tag with its word |
| Slate blue as a data series beside cobalt | Data blends into navigation and focus indicators | Copper as category 2 (the default) |
| Monospace eyebrows at 10px | Cramped, hard to read | Geist 11px / 600 uppercase, 0.06em |
| Rainbow charts in random order | Color without system | Categorical palette, accent first, or focus mode |
| Floating cards with shadows and hover lift | Widget collection | Flat sections on the grid |
| Rounded 12–16px corners, pill buttons | Consumer-app feel | 4px / 6px |
| Four colored KPI cards | Dashboard cliché | One KPI row in one section, accent sparklines |
| Thick colored side stripes on cards | Decoration posing as status | Status tag, or recommendation border |
| Gradients, glass blur, glow | Generic SaaS look | Flat surfaces (one chart-area fade allowed) |
| Accent fill next to critical red | Two alarms competing | Critical tag; outline or primary button kept apart |

---

## 15 — Review checklist

Items marked ⚙ can be checked automatically.

**Accent and color**

- [ ] The accent is visible on first load (brand mark, active nav, active tab, main chart series).
- [ ] ⚙ At most one `.ops-btn--primary` per `.ops-item`, `.ops-section`, or dialog.
- [ ] ⚙ No `background` of `--accent-500` except on `.ops-btn--primary`, `.ops-rail__brand`, `.ops-badge--accent`, checked controls, and progress fills.
- [ ] ⚙ No text set in `--accent-500`.
- [ ] Status and category colors are used for meaning, with a word next to each.
- [ ] Squint test: calm neutral structure, cobalt accent clearly present, one obvious next action.
- [ ] Charts with two or more series: series 2 is copper, not another blue.

**Typography**

- [ ] ⚙ Fonts are Geist and Geist Mono (or one approved pair from §06.1).
- [ ] ⚙ No font size under 11px; 11px used only for uppercase labels.
- [ ] ⚙ No monospace on labels, eyebrows, or general metadata.
- [ ] ⚙ No font weight above 600; no size above 28px.

**Structure**

- [ ] ⚙ No `box-shadow` on sections or items.
- [ ] ⚙ Radii only 4px, 6px, or full (dots, avatars, badges).
- [ ] ⚙ Borders 1px, except 2px focus rings and active indicators.
- [ ] ⚙ No raw hex or pixel values outside the token block.
- [ ] Sections align to the grid.

**Content**

- [ ] Each decision item reads Observation → Context → Recommendation → Action → Outcome.
- [ ] Every recommendation has an estimated impact with basis and window.
- [ ] Every action label is a verb phrase.

**Accessibility**

- [ ] ⚙ Text contrast meets §05.6.
- [ ] Focus is visible everywhere; reduced motion works.

---

## 16 — Token and component export

### 16.1 CSS tokens

```css
:root {
  /* neutrals */
  --canvas: #FAFAF9;
  --surface: #FFFFFF;
  --surface-subtle: #F5F5F4;
  --surface-sunken: #EFEFED;
  --border: #E4E4E2;
  --border-strong: #D4D4D1;
  --text-primary: #202020;
  --text-secondary: #5F5F5C;
  --text-muted: #8A8A86;
  --text-inverse: #FFFFFF;

  /* accent: cobalt (default) */
  --accent-50: #EEF3FE;
  --accent-100: #DCE6FD;
  --accent-200: #B9CDFB;
  --accent-300: #8AADF6;
  --accent-500: #2F6FEB;
  --accent-600: #2459C9;
  --accent-700: #1D47A3;
  --accent-800: #173879;
  --accent-fill: var(--accent-500);
  --focus-ring: color-mix(in srgb, var(--accent-500) 45%, transparent);

  /* compatibility aliases */
  --action: var(--accent-500);
  --action-soft: var(--accent-50);
  --action-ink: var(--accent-700);

  /* status */
  --success: #2F9E6A;  --success-text: #25774F;  --success-tint: #E8F5EE;
  --warning: #E0A526;  --warning-text: #94600B;  --warning-tint: #FCF4E1;
  --critical: #D0312D; --critical-text: #B0241F; --critical-tint: #FCECEB;
  --info: #3B79C4;     --info-text: #2C5E99;     --info-tint: #EAF2FB;

  /* categories (1 = accent) */
  --cat-1: var(--accent-500); --cat-1-tint: var(--accent-100); --cat-1-text: var(--accent-800);
  --cat-2: #E07A3F; --cat-2-tint: #FCEEE5; --cat-2-text: #8F4519;
  --cat-3: #2A9D8F; --cat-3-tint: #E3F4F1; --cat-3-text: #1C6B61;
  --cat-4: #C99A2E; --cat-4-tint: #F8F0DC; --cat-4-text: #7A5B12;
  --cat-5: #8E5B9A; --cat-5-tint: #F3ECF5; --cat-5-text: #62386D;
  --cat-6: #7A8B3A; --cat-6-tint: #F0F3E3; --cat-6-text: #4E5A20;
  --cat-other: #A3A3A0; --chart-muted: #C4C4C2;

  /* type */
  --font-sans: "Geist", "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-mono: "Geist Mono", "JetBrains Mono", ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;

  /* space */
  --space-1: 4px;  --space-2: 8px;  --space-3: 12px; --space-4: 16px;
  --space-5: 24px; --space-6: 32px; --space-7: 48px; --space-8: 64px;

  /* shape, depth, motion, layers */
  --radius-sm: 4px; --radius-md: 6px; --radius-full: 999px;
  --elevation-1: 0 1px 2px rgba(32, 32, 32, 0.04), 0 4px 12px rgba(32, 32, 32, 0.05);
  --overlay: rgba(32, 32, 32, 0.28);
  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
  --duration-fast: 120ms; --duration: 180ms;
  --z-rail: 10; --z-sticky: 20; --z-popover: 30; --z-dialog: 40; --z-toast: 50;

  /* density */
  --section-pad: var(--space-5);
  --row-h: 40px;
  --feed-text: 16px;

  /* layout */
  --rail-w: 56px;
  --crumb-h: 44px;
  --reading-w: 760px;  /* reading column: ~75 characters at 16px */
  --aside-w: 264px;    /* context column */
}

[data-density="compact"] { --section-pad: var(--space-4); --row-h: 32px; --feed-text: 14px; }
[data-contrast="strict"] { --accent-fill: var(--accent-700); }

[data-accent="orange"] {
  --accent-50: #FFF3F0; --accent-100: #FFE3DC; --accent-200: #FFC6B8; --accent-300: #FDA08E;
  --accent-500: #F75440; --accent-600: #E23F2B; --accent-700: #C2361F; --accent-800: #962A18;
  --cat-2: #4A6FA5; --cat-2-tint: #E9EFF7; --cat-2-text: #2F4C77;
}
[data-accent="teal"] {
  --accent-50: #E8F6F5; --accent-100: #CDEBE8; --accent-200: #9DD6D0; --accent-300: #62BAB2;
  --accent-500: #0F8A84; --accent-600: #0C746F; --accent-700: #0A615C; --accent-800: #084A47;
  --cat-3: #4A6FA5; --cat-3-tint: #E9EFF7; --cat-3-text: #2F4C77;
}
[data-accent="graphite"] {
  --accent-50: #F2F2F1; --accent-100: #E4E4E2; --accent-200: #CFCFCC; --accent-300: #A3A3A0;
  --accent-500: #2A2A2A; --accent-600: #1F1F1F; --accent-700: #202020; --accent-800: #111111;
}
```

When an accent preset is close to a category hue, the preset replaces that category (as orange and teal do above) so no two series look alike.

### 16.2 Component CSS (reference)

```css
html { background: var(--canvas); color: var(--text-primary); font: 400 14px/22px var(--font-sans);
  -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility; }
:focus-visible { outline: 2px solid var(--focus-ring); outline-offset: 2px; }
.tnum { font-variant-numeric: tabular-nums; }

.ops-display { font: 500 28px/36px var(--font-sans); letter-spacing: -0.02em; margin: var(--space-2) 0 0; }
.ops-title   { font: 600 20px/28px var(--font-sans); letter-spacing: -0.01em; margin: 0; }
.ops-heading { font: 600 16px/24px var(--font-sans); letter-spacing: -0.005em; margin: 0; }
.ops-label   { font: 600 11px/16px var(--font-sans); letter-spacing: .06em; text-transform: uppercase; color: var(--text-secondary); }
.ops-meta    { font: 400 12px/16px var(--font-sans); color: var(--text-muted); font-variant-numeric: tabular-nums; }
.ops-source  { font: 600 13px/20px var(--font-sans); color: var(--text-primary); }
.ops-code    { font: 400 12px/16px var(--font-mono); }
.ops-sr      { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.ops-link    { color: var(--accent-700); text-decoration: none; } .ops-link:hover { text-decoration: underline; }

/* rail */
.ops-rail { width: 56px; display: flex; flex-direction: column; align-items: center; gap: var(--space-1);
  padding: var(--space-3) 0; background: var(--surface); border-right: 1px solid var(--border); z-index: var(--z-rail); }
.ops-rail__brand { width: 28px; height: 28px; display: grid; place-items: center; margin-bottom: var(--space-3);
  border-radius: var(--radius-sm); background: var(--accent-500); color: var(--text-inverse); }
.ops-rail__item { position: relative; width: 40px; height: 40px; display: grid; place-items: center;
  border-radius: var(--radius-sm); color: var(--text-secondary);
  transition: background-color var(--duration-fast) var(--ease-out), color var(--duration-fast) var(--ease-out); }
.ops-rail__item:hover { background: var(--surface-subtle); color: var(--text-primary); }
.ops-rail__item[aria-current="page"] { background: var(--accent-50); color: var(--accent-600); }
.ops-rail__item[aria-current="page"]::before { content: ""; position: absolute; left: -8px; top: 10px; bottom: 10px;
  width: 2px; border-radius: var(--radius-full); background: var(--accent-500); }
.ops-rail__sep { width: 24px; border: 0; border-top: 1px solid var(--border); margin: var(--space-2) 0; }
.ops-rail__item .ops-badge { position: absolute; top: 4px; right: 2px; }

/* tabs */
.ops-tabs { display: flex; gap: var(--space-5); border-bottom: 1px solid var(--border); }
.ops-tab { position: relative; height: 40px; display: inline-flex; align-items: center; gap: var(--space-2);
  font: 500 14px/20px var(--font-sans); color: var(--text-secondary); }
.ops-tab[aria-selected="true"] { color: var(--text-primary); font-weight: 600; }
.ops-tab[aria-selected="true"]::after { content: ""; position: absolute; left: 0; right: 0; bottom: -1px; height: 2px; background: var(--accent-500); }

/* section + feed */
.ops-section { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-md); padding: var(--section-pad); }
.ops-section__header { display: flex; align-items: baseline; justify-content: space-between; gap: var(--space-4); margin-bottom: var(--space-4); }
.ops-inset { background: var(--surface-subtle); border-radius: var(--radius-sm); padding: var(--space-3) var(--space-4); }
.ops-feed { display: flex; flex-direction: column; gap: var(--space-4); }

.ops-item { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-md); padding: var(--section-pad); }
.ops-item__header { display: flex; align-items: center; gap: var(--space-2); flex-wrap: wrap; }
.ops-item__header .ops-meta::before { content: "· "; }
.ops-item__obs { margin: var(--space-3) 0 0; font-size: var(--feed-text); line-height: 1.625; }
.ops-item__obs strong { font-weight: 600; }
.ops-item__tags { display: flex; gap: var(--space-2); margin-top: var(--space-3); }
.ops-item__actions { display: flex; align-items: center; gap: var(--space-2); margin-top: var(--space-3); }
.ops-item__owner { margin-left: auto; display: inline-flex; align-items: center; gap: var(--space-2); font: 400 12px/16px var(--font-sans); color: var(--text-secondary); }

/* recommendation */
.ops-reco { margin-top: var(--space-4); border: 1px solid var(--accent-200); border-radius: var(--radius-sm);
  padding: var(--space-3) var(--space-4); background: var(--surface); }
.ops-reco--primary { border-color: var(--accent-500); background: var(--accent-50); }
.ops-reco__label { color: var(--accent-700); }
.ops-reco__action { margin: var(--space-2) 0 0; font-size: var(--feed-text); font-weight: 500; line-height: 1.625; color: var(--text-primary); }
.ops-reco--primary .ops-reco__action { color: var(--accent-700); }
.ops-reco__impact { margin: var(--space-1) 0 0; color: var(--text-secondary); }
.ops-reco[data-state="accepted"] { border-color: var(--success); background: var(--success-tint); }
.ops-reco[data-state="accepted"] .ops-reco__label { color: var(--success-text); }
.ops-reco[data-state="declined"], .ops-reco[data-state="expired"] { border-color: var(--border); background: var(--surface); }
.ops-reco[data-state="declined"] :is(.ops-reco__label, .ops-reco__action),
.ops-reco[data-state="expired"] :is(.ops-reco__label, .ops-reco__action) { color: var(--text-secondary); }

/* buttons */
.ops-btn { height: 32px; padding: 0 var(--space-3); display: inline-flex; align-items: center; gap: var(--space-2);
  border-radius: var(--radius-sm); border: 1px solid transparent; font: 500 14px/20px var(--font-sans); cursor: pointer;
  transition: background-color var(--duration-fast) var(--ease-out), border-color var(--duration-fast) var(--ease-out); }
.ops-btn--primary { background: var(--accent-fill); color: var(--text-inverse); font-weight: 600; }
.ops-btn--primary:hover { background: var(--accent-600); }
.ops-btn--primary:active { background: var(--accent-700); }
.ops-btn--accent { background: var(--surface); border-color: var(--accent-500); color: var(--accent-700); font-weight: 600; }
.ops-btn--accent:hover { background: var(--accent-50); }
.ops-btn--secondary { background: var(--surface); border-color: var(--border); color: var(--text-primary); }
.ops-btn--secondary:hover { border-color: var(--border-strong); }
.ops-btn--quiet { background: transparent; color: var(--text-secondary); }
.ops-btn--quiet:hover { background: var(--surface-subtle); color: var(--text-primary); }
.ops-btn--destructive { background: var(--surface); border-color: var(--border); color: var(--critical-text); }
.ops-btn:disabled { opacity: .4; cursor: not-allowed; }

/* tags, dots, badges, avatars */
.ops-tag { height: 22px; padding: 0 var(--space-2); display: inline-flex; align-items: center; gap: 6px;
  border-radius: var(--radius-sm); font: 500 12px/16px var(--font-sans);
  background: var(--surface-subtle); color: var(--text-secondary); }
.ops-tag .ops-dot { background: currentColor; }
.ops-tag--accent   { background: var(--accent-100);    color: var(--accent-800); }
.ops-tag--success  { background: var(--success-tint);  color: var(--success-text); }
.ops-tag--warning  { background: var(--warning-tint);  color: var(--warning-text); }
.ops-tag--critical { background: var(--critical-tint); color: var(--critical-text); }
.ops-tag--info     { background: var(--info-tint);     color: var(--info-text); }
.ops-cat-1 { background: var(--cat-1-tint); color: var(--cat-1-text); }
.ops-cat-2 { background: var(--cat-2-tint); color: var(--cat-2-text); }
.ops-cat-3 { background: var(--cat-3-tint); color: var(--cat-3-text); }
.ops-cat-4 { background: var(--cat-4-tint); color: var(--cat-4-text); }
.ops-cat-5 { background: var(--cat-5-tint); color: var(--cat-5-text); }
.ops-cat-6 { background: var(--cat-6-tint); color: var(--cat-6-text); }

.ops-dot { width: 6px; height: 6px; border-radius: var(--radius-full); display: inline-block; flex: none; }
.ops-dot--success { background: var(--success); }
.ops-dot--warning { background: var(--warning); }
.ops-dot--critical { background: var(--critical); }
.ops-dot--info { background: var(--info); }
.ops-dot--stale { box-shadow: inset 0 0 0 1px var(--text-muted); }

.ops-badge { min-width: 16px; height: 16px; padding: 0 4px; display: inline-grid; place-items: center;
  border-radius: var(--radius-full); font: 600 11px/16px var(--font-sans); font-variant-numeric: tabular-nums;
  background: var(--accent-500); color: var(--text-inverse); }
.ops-badge--neutral { background: var(--surface-sunken); color: var(--text-secondary); }

.ops-avatar { width: 20px; height: 20px; display: inline-grid; place-items: center; flex: none;
  border-radius: var(--radius-full); font: 600 11px/1 var(--font-sans); }
.ops-item__owner .ops-avatar, .ops-avatar--lg { width: 28px; height: 28px; }

/* selection controls */
.ops-check { appearance: none; width: 16px; height: 16px; border: 1px solid var(--border-strong); border-radius: var(--radius-sm); background: var(--surface); }
.ops-check:checked { background: var(--accent-500) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='none' stroke='white' stroke-width='2'%3E%3Cpath d='M4 8.5l2.5 2.5L12 5.5'/%3E%3C/svg%3E") center/16px no-repeat; border-color: var(--accent-500); }
.ops-chip[aria-pressed="true"] { background: var(--accent-50); border: 1px solid var(--accent-200); color: var(--accent-700); }

/* table */
.ops-table { width: 100%; border-collapse: collapse; }
.ops-table th { position: sticky; top: 0; height: 36px; padding: 0 var(--space-4); text-align: left; background: var(--surface-subtle);
  font: 600 11px/16px var(--font-sans); letter-spacing: .06em; text-transform: uppercase; color: var(--text-secondary); }
.ops-table td { height: var(--row-h); padding: 0 var(--space-4); border-bottom: 1px solid var(--border); }
.ops-table .num { text-align: right; font-variant-numeric: tabular-nums; }
.ops-table tbody tr:hover { background: var(--surface-subtle); }
.ops-table tbody tr[aria-selected="true"] { background: var(--accent-50); }

/* progress */
.ops-progress { height: 4px; border-radius: var(--radius-full); background: var(--surface-sunken); overflow: hidden; }
.ops-progress > span { display: block; height: 100%; background: var(--accent-500); border-radius: inherit; }

/* inputs + ask bar */
.ops-input { height: 36px; padding: 0 var(--space-3); background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius-sm); font: inherit; color: var(--text-primary); }
.ops-input::placeholder { color: var(--text-muted); }
.ops-input:hover { border-color: var(--border-strong); }
.ops-input:focus { border-color: var(--accent-500); outline: 2px solid var(--focus-ring); outline-offset: 0; }
.ops-input[aria-invalid="true"] { border-color: var(--critical); }

.ops-ask { height: 56px; display: flex; align-items: center; gap: var(--space-3); padding: 0 var(--space-2) 0 var(--space-4);
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-md); z-index: var(--z-sticky); }
.ops-ask:focus-within { border-color: var(--accent-500); outline: 2px solid var(--focus-ring); outline-offset: 0; }
.ops-ask__send { width: 32px; height: 32px; display: grid; place-items: center; border-radius: var(--radius-sm);
  background: var(--surface-subtle); color: var(--text-muted); }
.ops-ask__send:not(:disabled) { background: var(--accent-500); color: var(--text-inverse); }

@media (prefers-reduced-motion: reduce) { * { transition-duration: 0ms !important; animation: none !important; } }
```

### 16.3 Tailwind (v3 `theme.extend`; map the same names to v4 `@theme`)

```js
// tailwind.config.js
const accent = (n) => `var(--accent-${n})`;
module.exports = {
  theme: {
    extend: {
      colors: {
        canvas: "var(--canvas)",
        surface: { DEFAULT: "var(--surface)", subtle: "var(--surface-subtle)", sunken: "var(--surface-sunken)" },
        line: { DEFAULT: "var(--border)", strong: "var(--border-strong)" },
        ink: { DEFAULT: "var(--text-primary)", secondary: "var(--text-secondary)", muted: "var(--text-muted)", inverse: "var(--text-inverse)" },
        accent: { 50: accent(50), 100: accent(100), 200: accent(200), 300: accent(300), 500: accent(500), 600: accent(600), 700: accent(700), 800: accent(800), DEFAULT: accent(500), fill: "var(--accent-fill)" },
        success: { DEFAULT: "var(--success)", text: "var(--success-text)", tint: "var(--success-tint)" },
        warning: { DEFAULT: "var(--warning)", text: "var(--warning-text)", tint: "var(--warning-tint)" },
        critical: { DEFAULT: "var(--critical)", text: "var(--critical-text)", tint: "var(--critical-tint)" },
        info: { DEFAULT: "var(--info)", text: "var(--info-text)", tint: "var(--info-tint)" },
        cat: {
          1: "var(--cat-1)", 2: "var(--cat-2)", 3: "var(--cat-3)", 4: "var(--cat-4)", 5: "var(--cat-5)", 6: "var(--cat-6)",
          other: "var(--cat-other)", muted: "var(--chart-muted)",
        },
      },
      fontFamily: { sans: ["var(--font-sans)"], mono: ["var(--font-mono)"] },
      fontSize: {
        display: ["28px", { lineHeight: "36px", letterSpacing: "-0.02em", fontWeight: "500" }],
        title: ["20px", { lineHeight: "28px", letterSpacing: "-0.01em", fontWeight: "600" }],
        heading: ["16px", { lineHeight: "24px", letterSpacing: "-0.005em", fontWeight: "600" }],
        "body-lg": ["16px", { lineHeight: "26px" }],
        body: ["14px", { lineHeight: "22px" }],
        small: ["13px", { lineHeight: "20px" }],
        meta: ["12px", { lineHeight: "16px" }],
        label: ["11px", { lineHeight: "16px", letterSpacing: "0.06em", fontWeight: "600" }],
        kpi: ["28px", { lineHeight: "32px", letterSpacing: "-0.02em", fontWeight: "500" }],
      },
      spacing: { 1: "4px", 2: "8px", 3: "12px", 4: "16px", 6: "24px", 8: "32px", 12: "48px", 16: "64px" },
      borderRadius: { sm: "4px", md: "6px", full: "999px" },
      boxShadow: { 1: "var(--elevation-1)" },
      transitionTimingFunction: { out: "var(--ease-out)" },
    },
  },
};
```

Tailwind spacing keys follow its 4px convention (`p-6` = 24px). Use only the keys listed. Use `label` text with the `uppercase` utility.

### 16.4 Design tokens (W3C DTCG JSON)

```json
{
  "color": {
    "neutral": {
      "canvas":         { "$type": "color", "$value": "#FAFAF9" },
      "surface":        { "$type": "color", "$value": "#FFFFFF" },
      "surface-subtle": { "$type": "color", "$value": "#F5F5F4" },
      "surface-sunken": { "$type": "color", "$value": "#EFEFED" },
      "border":         { "$type": "color", "$value": "#E4E4E2" },
      "border-strong":  { "$type": "color", "$value": "#D4D4D1" },
      "text-primary":   { "$type": "color", "$value": "#202020" },
      "text-secondary": { "$type": "color", "$value": "#5F5F5C" },
      "text-muted":     { "$type": "color", "$value": "#8A8A86" }
    },
    "accent": {
      "50":  { "$type": "color", "$value": "#EEF3FE" },
      "100": { "$type": "color", "$value": "#DCE6FD" },
      "200": { "$type": "color", "$value": "#B9CDFB" },
      "300": { "$type": "color", "$value": "#8AADF6" },
      "500": { "$type": "color", "$value": "#2F6FEB" },
      "600": { "$type": "color", "$value": "#2459C9" },
      "700": { "$type": "color", "$value": "#1D47A3" },
      "800": { "$type": "color", "$value": "#173879" }
    },
    "status": {
      "success":  { "solid": { "$type": "color", "$value": "#2F9E6A" }, "text": { "$type": "color", "$value": "#25774F" }, "tint": { "$type": "color", "$value": "#E8F5EE" } },
      "warning":  { "solid": { "$type": "color", "$value": "#E0A526" }, "text": { "$type": "color", "$value": "#94600B" }, "tint": { "$type": "color", "$value": "#FCF4E1" } },
      "critical": { "solid": { "$type": "color", "$value": "#D0312D" }, "text": { "$type": "color", "$value": "#B0241F" }, "tint": { "$type": "color", "$value": "#FCECEB" } },
      "info":     { "solid": { "$type": "color", "$value": "#3B79C4" }, "text": { "$type": "color", "$value": "#2C5E99" }, "tint": { "$type": "color", "$value": "#EAF2FB" } }
    },
    "category": {
      "1": { "$type": "color", "$value": "{color.accent.500}" },
      "2": { "$type": "color", "$value": "#E07A3F" },
      "3": { "$type": "color", "$value": "#2A9D8F" },
      "4": { "$type": "color", "$value": "#C99A2E" },
      "5": { "$type": "color", "$value": "#8E5B9A" },
      "6": { "$type": "color", "$value": "#7A8B3A" },
      "other": { "$type": "color", "$value": "#A3A3A0" }
    }
  },
  "font": {
    "sans": { "$type": "fontFamily", "$value": ["Geist", "Inter", "system-ui", "sans-serif"] },
    "mono": { "$type": "fontFamily", "$value": ["Geist Mono", "JetBrains Mono", "ui-monospace", "monospace"] }
  },
  "space": {
    "1": { "$type": "dimension", "$value": "4px" },  "2": { "$type": "dimension", "$value": "8px" },
    "3": { "$type": "dimension", "$value": "12px" }, "4": { "$type": "dimension", "$value": "16px" },
    "5": { "$type": "dimension", "$value": "24px" }, "6": { "$type": "dimension", "$value": "32px" },
    "7": { "$type": "dimension", "$value": "48px" }, "8": { "$type": "dimension", "$value": "64px" }
  },
  "radius": {
    "sm": { "$type": "dimension", "$value": "4px" },
    "md": { "$type": "dimension", "$value": "6px" },
    "full": { "$type": "dimension", "$value": "999px" }
  },
  "motion": {
    "ease-out":      { "$type": "cubicBezier", "$value": [0.22, 1, 0.36, 1] },
    "duration-fast": { "$type": "duration", "$value": "120ms" },
    "duration":      { "$type": "duration", "$value": "180ms" }
  }
}
```

---

### 16.1 — Dark theme

Dark is composed, not inverted. It is applied by `[data-theme="dark"]` on `<html>` (set before paint by an inline head script from `localStorage["learning.theme"]`, falling back to `prefers-color-scheme`), and duplicated under `@media (prefers-color-scheme: dark) :root:not([data-theme])` for the no-JS case. Tokens keep their semantic roles, so component CSS is unchanged: 50/100 accent and status tints become dark tinted fills, 700/800 become light text.

| Token | Dark | Why |
|---|---|---|
| `--canvas` / `--surface` / `--surface-subtle` / `--surface-sunken` | #111317 / #171A1F / #1E2127 / #0D0F12 | Cool-tinted near-black, never #000. Elevation goes up by getting lighter; sunken (code, formulas) sits below canvas. |
| `--border` / `--border-strong` | #2A2E35 / #3B4049 | Hairlines visible without glowing. |
| `--text-primary` / `-secondary` / `-muted` | #E9E9E7 / #B0B2B7 / #8D9097 | Off-white to stop halation; muted still 5.46:1 on surface. |
| `--text-inverse` | #0B1222 | Dark text on accent fills (6.79:1 on accent-500). |
| `--accent-50…300` | #141E33 #1B2A48 #24396A #3A5A9C | Navy fills for selected, tag and track states. |
| `--accent-500…800` | #6E9BF2 #86ACF5 #9EBDF8 #C3D6FB | Cobalt, lightened and slightly desaturated so it does not vibrate on dark. |
| success line / text / tint | #45B984 / #7AD3A6 / #15291F | |
| warning | #E3B341 / #EAC36A / #2C2310 | |
| critical | #EF6461 / #F59491 / #33191A | |
| info | #5E9BE0 / #93BDEE / #16243A | |
| `--cat-2…6` (line / tint / text) | #E8925E #4CBFB0 #D9B04F #B184BD #A3B55A, with matching dark tints and light text | Same hues, lifted for 3:1+ as chart lines. |
| `--chart-muted` / `--cat-other` | #4A4E56 / #8F918F | Background points and "other". |
| `--elevation` | 0 1px 2px rgba(0,0,0,.45), 0 6px 16px rgba(0,0,0,.35) | Shadows are weak on dark; lightness carries elevation. |

All dark pairs pass WCAG AA: text 4.5:1, UI lines, icons and focus 3:1. Sims read colours via `Learning.token()` at draw time and repaint on `learning:themechange`/`resize`; Mermaid re-renders from its stored source. The toggle (`.ops-theme-toggle`) is mounted by `Learning.mountThemeToggle()` at the end of `.ops-crumbs`, with `aria-pressed` reflecting dark.

## 17 — Agent prompt snippet

Paste this into a UI-building agent's instructions when the full document is too long for its context.

```text
Follow "Cobalt UI — Design System v1.2".
FEEL: calm, dense, technical workstation. One continuous workspace of flat sections on a grid. Professional and stable, not bland; confident, not salesy.
FONTS: Geist (UI, headings, labels, numbers) + Geist Mono (IDs/codes only). Scale 28/20/16/14/13/12/11px, weights 400/500/600.
  Eyebrows/labels: Geist 11px 600 UPPERCASE, letter-spacing .06em, #5F5F5C. Never monospace labels. Nothing under 11px. Tabular numbers.
NEUTRALS: canvas #FAFAF9, surface #FFFFFF, subtle #F5F5F4, border #E4E4E2 (1px), text #202020 / #5F5F5C / #8A8A86. Radius 4px controls, 6px sections. No shadows on sections.
ACCENT (default COBALT, swappable via data-accent): 50 #EEF3FE, 100 #DCE6FD, 200 #B9CDFB, 500 #2F6FEB, 600 #2459C9, 700 #1D47A3, 800 #173879.
  MUST appear on every screen: brand mark tile, active nav (50 bg + 600 icon + 2px 500 indicator), active tab underline, links (700), focus ring, checked controls, main chart series, progress, sparklines.
  Tint (50/100): recommendation background, selected rows, selected chips, accent tags.
  Fill (500 + white text): ONE primary button per region, brand mark, open-decision count badge. Never fill headers/banners/sidebars. Accent text = 700.
STATUS (solid/text/tint): success #2F9E6A/#25774F/#E8F5EE, warning #E0A526/#94600B/#FCF4E1, critical #D0312D/#B0241F/#FCECEB, info #3B79C4/#2C5E99/#EAF2FB. As dots, tags, figures; always with a word. Info never as a fill next to the cobalt accent.
CATEGORIES (charts, tags, avatars, in order): accent, copper #E07A3F, #2A9D8F, #C99A2E, #8E5B9A, #7A8B3A, other #A3A3A0. Tags = tint bg + dark text.
SPACING: 4/8/12/16/24/32/48/64 only.
DECISION ITEM: header (avatar, source, meta · separated, status tag) → observation (16px, key figures bold) → category tags → recommendation (accent border + tint, RECOMMENDATION label, verb-first action, estimated impact with basis and window) → actions (primary, secondary, quiet; owner on right) → outcome (who accepted, when, result in status color).
NEVER: gradients (except one faint chart-area fade), glass, glow, pulsing, emoji, pill buttons, thick side stripes, four colored KPI cards, "NEW/HOT/URGENT" badges, multiple filled accent buttons, accent body text, accent fill next to critical red.
RULE: quiet neutral structure, a cobalt accent for intent, full-strength color only where a decision lives.
```

---

## Appendix — Adoption: the learning library (this repo)

The learning website in `site/` is built on this system. Light mode only; fonts and Mermaid are bundled so it works offline from `file://`.

| File | Contains |
|------|----------|
| `site/assets/ui.css` | §16.1 tokens (cobalt default, copper `--cat-2`), the bundled Geist `@font-face`, and the `ops-*` components from §09 |
| `site/assets/lesson.css` | Lesson-only pieces (`lesson-*`): steps, diagram, interactive widget, think-it-through, go-deeper rows. Built only from tokens. |
| `site/assets/lesson.js` | Term popovers, click-through steps, think-it-through feedback, the "understood" marker, and Mermaid themed from the tokens |
| `site/assets/vendor/fonts/` | Geist and Geist Mono variable fonts (SIL OFL, see `OFL.txt`) |
| `.cursor/skills/learn-page/template.html` | Starting markup for every new lesson |

How the library maps onto this system:

- **Shell (§8.1):** the rail holds the brand tile and Library; the crumbs bar is Library / Area / Topic, with a 2px accent reading-progress line.
- **Library page (§8.4 T1 feed header + T3 table workspace):** KPI row (lessons, understood, areas, interactive), area tabs with counts, search input, `ops-table` of lessons. Status is a word tag: "Understood" (success) or "Not yet" (neutral).
- **Lesson page (a T2-style 8+4 split):** a centered 760px reading column plus a sticky context column with "On this page" (§9.19) and a "check me" prompt to copy. The one-sentence core idea is the page's single `ops-reco--primary`. The analogy, feedback and notes use `ops-inset`. "Where the picture breaks" is an `ops-banner--warning`. Simulation presets are `ops-chip`s, and the simulation result is a status tag plus a sentence. The glossary is an `ops-table`.
- **Areas → categories (§5.5):** tech areas get colour: electrical copper `cat-2`, software `cat-3`, manufacturing `cat-4`, AI `cat-5`. Psychology, economics and other stay neutral, since tech is the primary focus. Category 1 is skipped because it is the accent; `cat-6` is free for the next tech area.
- **Charts (§9.12):** the subject series is accent-500 2px with a 12% → 0 fill, gridlines use `--border`, and the target line is dashed `--warning` with a label at its right end.
- **Diagrams:** Mermaid `base` theme fed from tokens (white nodes, `--border-strong` outlines, no shadows). `class <node> accent` marks the one node that matters most.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-10-07 | First release (as "Operations UI", orange default accent). |
| 1.1 | 2026-10-13 | Renamed "Cobalt UI". Default accent is now cobalt (`#2F6FEB`); orange becomes a preset. Category 2 is now copper (`#E07A3F`) so data never blends into cobalt indicators; the orange preset restores slate blue, and the teal preset now swaps category 3 to slate blue. Contrast table updated: the cobalt primary button meets WCAG AA by default. Added offline font guidance, two anti-patterns, and an adoption appendix for the learning library. |
| 1.2 | 2026-10-13 | Content is centered instead of left-aligned. Reading column narrowed to 760px for a comfortable line length; reading pages pair it with a 264px sticky context column from 1200px wide (§8.1, §8.2). New §9.19 page outline. New layout tokens `--reading-w` and `--aside-w`. |
