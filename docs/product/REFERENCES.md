# Product references (Nov 2026)

Study notes for Arc v1 shell. Judgement sections labeled. Sources: public marketing sites, changelogs, and help docs (accessed Nov 2026).

## Linear

**Borrow**
- Collapsible sidebar with keyboard shortcut (`[` / Cmd+B style) and persisted width.
- Command menu for navigation without hunting sidebar items.
- Dense list views: status, owner, and relative time in one scannable row.
- Subtle borders and low visual noise; one cobalt primary per region.

**Arc improvement**
- EE subjects (Circuits, Control, Power) instead of team/project hierarchy.
- Verification status (Checked / Unchecked) is first-class on every problem row, not optional metadata.

## Vercel dashboard

**Borrow**
- Top bar with environment/project context left and actions right.
- Skeleton loaders and toasts for deploy-style async actions (we use the same for Solve / Run again).
- Settings separated from daily workflow (integrations, appearance).

**Arc improvement**
- Breadcrumbs name the **problem** (human title), not repository ids.
- Engine availability lives in Settings, not the main header.

## Notion

**Borrow**
- Sidebar sections (workspace, favorites/recents, settings at bottom).
- Collapsed icon rail with tooltips on hover.
- "Continue where you left off" on home via recent pages.

**Arc improvement**
- Recents are **problems with answers**, not unstructured pages.
- Home is action-oriented (Ask / Try example), not an empty doc tree.

## Figma

**Borrow**
- Persistent tool rail; canvas is full-bleed in Studio.
- Zoom/fit and selection inspector on the right.
- Files organized by recency and explicit open-in-editor flow.

**Arc improvement**
- Studio opens from a problem with context (diagram tied to verified answer).
- Collaboration badges (agent vs human) on edits, not just avatars.

## Hex / Observable

**Borrow**
- Figure-first presentation: plots large, code/parameters secondary.
- Gallery of reusable visuals with plain-language captions.
- Parameters tweak then re-run loop surfaced in the UI.

**Arc improvement**
- Figures are engine-bound (Visual Kit), not notebook cells.
- Parameters drawer ties directly to stale state and Run again on the same problem.

## Summary table

| Pattern | From | Arc use |
|---------|------|---------|
| Collapsible sidebar + shortcut | Linear, Notion | App shell |
| Command palette | Linear | Cmd/Ctrl+K |
| Breadcrumb + page actions | Vercel | Top bar |
| Recent items block | Notion | Sidebar + Home Continue |
| Full-bleed editor | Figma | Studio |
| Large figures + captions | Hex | Gallery + Problem Figures tab |
| Settings for integrations | Vercel | Agents, Engines, scorecard |
