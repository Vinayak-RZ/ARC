# README cold read: IIT Roorkee UG EE (2nd/3rd year persona)

**Reader:** Second-year EE at IITR, just finished Network Analysis and starting Control Systems. Uses Cursor for labs, not a kernel hacker. Clone decision happens in one sitting after a friend shares the repo link.

## What feels useful

- **Try these prompts** now read like actual tutorial sheet lines (RLC step, Bode homework, LG fault, DC machine). I would paste one without rewriting.
- **Pip-first quick start** matches how we set up venv on the lab machine; I do not need uv to try it tonight.
- **Screenshots** (1280×900 window, Pillow ink gate) now show real ink: RLC series schematic (inspector as a bottom-right overlay, not a side split), control closed-loop blocks, and power/protection/drives one-lines. Plots sit below the diagram band.
- **Honest coursework spread:** circuits, control, power, protection, drives in one README table. Feels closer to our semester than “10 V divider only.”

## What felt fake or lab-toy before this pass

- Full-page scroll shots with twenty old runs in the sidebar looked like a dev dogfood dump, not a product I would show in a viva demo.
- Agent briefs that named internal recipes and `unchecked` policy read like operator docs, not student homework.
- Tiny 240px-wide Bode thumbnails and empty canvas on power/protection runs made the UI look like a CSV viewer with icons. **Fixed in PR #41:** static SVG study diagrams + mandatory capture ink check.

## What was still confusing (and README tweaks applied)

| Issue | Fix applied |
|-------|-------------|
| “Domain kernel” before I know what Arc does | Kept term in its section; prompts stand alone without kernel jargon |
| Unclear that numbers are checked locally | Quick start already says `127.0.0.1:8765`; screenshot caption now says one-run window |
| Too many screenshot files (duplicate control shots) | Single control shot: loop diagram + Bode/step |
| Drives missing from the visual tour | Added drives prompt + `ui-drives-full.png` |

## Would I clone it tonight?

**Yes, if** I already use Cursor for coding assignments. The prompts are copy-pasteable for EE302-style labs. **Maybe not** if I expected a MATLAB replacement on day one: README still assumes an agent in the loop, which is fair but should stay obvious (first paragraph already says agent-primary).

## Follow-ups (not blocking this PR)

- Hindi/regional unit hints in prompts (optional).
- Link one prompt to a gold eval folder so “expected answer shape” is visible without reading ARCHITECTURE.
- Motor diagram could show \( \omega \) arrow; cosmetic only.
