# Prototype decision

## Directions explored

1. **A — Notebook shell** (`shell-direction-a-notebook.html`): Left nav on warm gray, white main, home with one primary CTA and recent runs section. Matches `docs/design/DESIGN.md` ("shift notebook"): sections not floating marketing cards, cobalt only on selection and primary action.
2. **B — Studio top nav** (`shell-direction-b-studio.html`): Horizontal tabs in header. Familiar but steals vertical space and duplicates nav with run list.
3. **C — Answer-first run** (`run-result-direction-c-split.html`): Verification card then large plot grid. Applies regardless of shell.

## Chosen direction

**Ship A + C together.**

Rationale (judgement): Arc is a dense technical tool used for long sessions. A persistent left rail matches Runs/Books/Visuals/Control switching without crowding the header. Removing engine chips and using the Learning Lab palette directly supports trust and calm. Answer-first layout addresses the core loop step where students decide whether to trust the run before diving into diagrams.

**Not chosen:** B adds a second navigation language (top tabs plus sidebar runs) and reads closer to a generic SaaS dashboard than the design north star.
