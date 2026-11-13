# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: studio-layout.spec.ts >> studio areas never intersect at 1280x800, before and after Simulate
- Location: e2e/studio-layout.spec.ts:70:3

# Error details

```
Error: before Simulate: canvas height

expect(received).toBeGreaterThanOrEqual(expected)

Expected: >= 280
Received:    272
```

# Page snapshot

```yaml
- generic [ref=e3]:
  - link "Skip to workspace" [ref=e4] [cursor=pointer]:
    - /url: "#workspace"
  - complementary "Main navigation" [ref=e5]:
    - generic [ref=e6]:
      - img "Arc" [ref=e7]
      - generic [ref=e8]:
        - strong [ref=e9]: Arc
        - generic [ref=e10]: EE coursework
      - button "Toggle sidebar (Ctrl+B)" [ref=e11] [cursor=pointer]
    - button "New problem" [ref=e15] [cursor=pointer]
    - navigation [ref=e18]:
      - button "Home" [ref=e19] [cursor=pointer]
      - button "Problems" [ref=e24] [cursor=pointer]
      - button "Studio" [ref=e29] [cursor=pointer]
      - button "Gallery" [ref=e35] [cursor=pointer]
      - button "Library" [ref=e42] [cursor=pointer]
    - generic [ref=e46]:
      - paragraph [ref=e47]: Recent
      - button "Voltage divider · Vout" [ref=e48] [cursor=pointer]
      - button "Wire test" [ref=e55] [cursor=pointer]
      - button "HW 3 · check" [ref=e62] [cursor=pointer]
      - button "Lab 4 · check" [ref=e69] [cursor=pointer]
      - button "Finite crossover" [ref=e76] [cursor=pointer]
    - generic [ref=e83]:
      - button "Agent connected" [ref=e84] [cursor=pointer]
      - button "Settings" [ref=e88] [cursor=pointer]
      - link "Help" [ref=e93] [cursor=pointer]:
        - /url: https://github.com/Vinayak-RZ/ARC
  - generic [ref=e102]:
    - banner [ref=e103]:
      - navigation "Breadcrumb" [ref=e104]:
        - generic [ref=e105]: Studio
    - main [ref=e106]:
      - generic [ref=e107]:
        - generic "Studio toolbar" [ref=e108]:
          - navigation "Breadcrumb" [ref=e109]:
            - generic [ref=e110]: Studio
            - generic [ref=e111]: /
            - generic [ref=e112]: E2E layout
          - group "Diagram mode" [ref=e113]:
            - button "Block diagram" [pressed] [ref=e114] [cursor=pointer]
            - button "Circuit" [disabled] [ref=e115] [cursor=pointer]
          - generic [ref=e116]:
            - button "Undo" [ref=e117] [cursor=pointer]
            - button "Redo" [disabled] [ref=e118] [cursor=pointer]
            - button "Fit" [ref=e119] [cursor=pointer]
            - generic [ref=e120]: 100%
            - button "Zoom out" [ref=e121] [cursor=pointer]: −
            - button "Zoom in" [ref=e122] [cursor=pointer]: +
            - button "Simulate" [ref=e123] [cursor=pointer]
        - complementary "Block palette" [ref=e124]:
          - searchbox "Search blocks" [ref=e125]
          - list [ref=e126]:
            - listitem [ref=e127]:
              - button "Step" [ref=e128]
            - listitem [ref=e133]:
              - button "Ramp" [ref=e134]
            - listitem [ref=e139]:
              - button "Sine" [ref=e140]
            - listitem [ref=e146]:
              - button "Gain" [ref=e147]
            - listitem [ref=e151]:
              - button "Sum" [ref=e152]
            - listitem [ref=e156]:
              - button "Transfer Fcn" [ref=e157]
            - listitem [ref=e161]:
              - button "PID" [ref=e162]
            - listitem [ref=e165]:
              - button "Integrator" [ref=e166]
            - listitem [ref=e170]:
              - button "Derivative" [ref=e171]
            - listitem [ref=e175]:
              - button "Saturation" [ref=e176]
            - listitem [ref=e181]:
              - button "Delay (Pade)" [ref=e182]
            - listitem [ref=e187]:
              - button "Scope" [ref=e188]
            - listitem [ref=e192]:
              - button "DC motor" [ref=e193]
            - listitem [ref=e198]:
              - button "1st-order plant" [ref=e199]
            - listitem [ref=e203]:
              - button "AGC area" [ref=e204]
        - application [ref=e211]:
          - generic [ref=e213]:
            - generic:
              - generic:
                - img:
                  - group "Edge from r to sum1"
                - img:
                  - group "Edge from sum1 to pid1"
                - img:
                  - group "Edge from pid1 to motor"
                - img:
                  - group "Edge from motor to y"
                - img:
                  - group "Edge from motor to sum1" [ref=e214] [cursor=pointer]
              - generic:
                - generic: r
                - generic: e
                - generic: u
                - generic: "y"
              - generic:
                - group [ref=e218]:
                  - generic [ref=e221]:
                    - generic [ref=e222]: ▸
                    - generic [ref=e223]: Step
                - group [ref=e224]:
                  - generic [ref=e227]:
                    - generic [aria-hidden] [ref=e228]: Σ
                    - generic [aria-hidden]: +
                    - generic [aria-hidden]: −
                - group [ref=e229]:
                  - generic [ref=e232]:
                    - generic [ref=e233]: PID
                    - generic [ref=e234]: Kp 50 · Ki 100 · Kd 5
                - group [ref=e235]:
                  - generic [ref=e239]:
                    - generic [ref=e240]: ⚙
                    - generic [ref=e241]: DC motor
                - group [ref=e242]:
                  - generic [ref=e244]:
                    - generic [aria-hidden] [ref=e245]: ◔
                    - generic [ref=e246]: Scope
        - generic "Results" [ref=e248]:
          - paragraph [ref=e252]: Run Simulate to see the step response and margins.
```

# Test source

```ts
  1   | // Run: STUDIO_URL=http://127.0.0.1:8765/?view=studio npx playwright test -c ui/e2e/playwright.config.ts
  2   | import { test, expect, Page } from "@playwright/test";
  3   | 
  4   | const BASE = process.env.STUDIO_BASE ?? "http://127.0.0.1:8765";
  5   | 
  6   | async function studioUrl(request: import("@playwright/test").APIRequestContext) {
  7   |   if (process.env.STUDIO_URL) return process.env.STUDIO_URL;
  8   |   const res = await request.post(`${BASE}/api/control-studio/sessions`, {
  9   |     data: { title: "E2E layout", golden: "pid_dc_motor" },
  10  |   });
  11  |   expect(res.ok()).toBeTruthy();
  12  |   const body = await res.json();
  13  |   return `${BASE}/?view=studio&session=${body.session_id}`;
  14  | }
  15  | const AREAS = {
  16  |   canvas: ".studio-canvas",
  17  |   palette: ".studio-palette-pane",
  18  |   inspector: ".studio-inspector",
  19  |   results: ".studio-results",
  20  | } as const;
  21  | type Box = { x: number; y: number; width: number; height: number };
  22  | 
  23  | const overlap = (a: Box, b: Box) => {
  24  |   const w = Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x);
  25  |   const h = Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y);
  26  |   return w > 0.5 && h > 0.5 ? { w, h } : null;
  27  | };
  28  | 
  29  | async function boxes(page: Page) {
  30  |   const out = {} as Record<keyof typeof AREAS, Box>;
  31  |   for (const [name, sel] of Object.entries(AREAS)) {
  32  |     const loc = page.locator(sel).first();
  33  |     const visible = await loc.isVisible().catch(() => false);
  34  |     if (!visible) continue;
  35  |     const b = await loc.boundingBox();
  36  |     expect(b, `${name} (${sel}) must be visible`).not.toBeNull();
  37  |     out[name as keyof typeof AREAS] = b!;
  38  |   }
  39  |   for (const required of ["canvas", "palette", "results"] as const) {
  40  |     expect(out[required], `${required} must be present`).toBeTruthy();
  41  |   }
  42  |   return out;
  43  | }
  44  | 
  45  | async function assertNoOverlap(page: Page, label: string) {
  46  |   const b = await boxes(page);
  47  |   const names = Object.keys(b) as (keyof typeof b)[];
  48  |   for (let i = 0; i < names.length; i++) {
  49  |     for (let j = i + 1; j < names.length; j++) {
  50  |       const hit = overlap(b[names[i]], b[names[j]]);
  51  |       expect(hit, `${label}: ${names[i]} overlaps ${names[j]} by ${JSON.stringify(hit)}\n${JSON.stringify(b)}`).toBeNull();
  52  |     }
  53  |   }
  54  |   const studio = (await page.locator(".studio").first().boundingBox())!;
  55  |   for (const n of names) {
  56  |     const r = b[n];
  57  |     expect(r.x, `${label}: ${n} left edge`).toBeGreaterThanOrEqual(studio.x - 0.5);
  58  |     expect(r.y, `${label}: ${n} top edge`).toBeGreaterThanOrEqual(studio.y - 0.5);
  59  |     expect(r.x + r.width, `${label}: ${n} right edge`).toBeLessThanOrEqual(studio.x + studio.width + 0.5);
  60  |     expect(r.y + r.height, `${label}: ${n} bottom edge`).toBeLessThanOrEqual(studio.y + studio.height + 0.5);
  61  |   }
> 62  |   expect(b.canvas.height, `${label}: canvas height`).toBeGreaterThanOrEqual(280);
      |                                                      ^ Error: before Simulate: canvas height
  63  |   expect(b.canvas.width, `${label}: canvas width`).toBeGreaterThanOrEqual(400);
  64  | }
  65  | 
  66  | for (const vp of [
  67  |   { width: 1280, height: 800 },
  68  |   { width: 1440, height: 900 },
  69  | ]) {
  70  |   test(`studio areas never intersect at ${vp.width}x${vp.height}, before and after Simulate`, async ({ page, request }) => {
  71  |     await page.setViewportSize(vp);
  72  |     await page.goto(await studioUrl(request));
  73  |     await page.locator(AREAS.canvas).waitFor();
  74  |     await page.waitForTimeout(400);
  75  |     await assertNoOverlap(page, "before Simulate");
  76  | 
  77  |     if (process.env.NO_SIM) return;
  78  |     await page.locator(".cs-simulate-btn").click();
  79  |     await page.locator(".studio-results-stage .studio-step-svg, .studio-results-stage img").first().waitFor({ timeout: 120000 });
  80  |     await page.waitForFunction(() => {
  81  |       const svg = document.querySelector(".studio-results-stage .studio-step-svg");
  82  |       if (svg) return svg.getBoundingClientRect().height >= 120;
  83  |       const i = document.querySelector<HTMLImageElement>(".studio-results-stage img");
  84  |       return !!i && i.complete && i.naturalWidth > 0;
  85  |     });
  86  |     await page.waitForTimeout(250);
  87  |     await assertNoOverlap(page, "after Simulate");
  88  | 
  89  |     const stageBox = (await page.locator(".studio-results-stage").boundingBox())!;
  90  |     const stage = page.locator(".studio-results-stage .studio-step-svg, .studio-results-stage img").first();
  91  |     const plot = (await stage.boundingBox())!;
  92  |     expect(plot.y + plot.height).toBeLessThanOrEqual(stageBox.y + stageBox.height + 2);
  93  |     const dt = page.locator(".studio-margin dt");
  94  |     for (let i = 0; i < (await dt.count()); i++) {
  95  |       const t = (await dt.nth(i).boundingBox())!;
  96  |       expect(overlap(t, (await boxes(page)).canvas), `margin caption ${i} hidden`).toBeNull();
  97  |     }
  98  |   });
  99  | }
  100 | 
  101 | test("block text never renders below 11px on screen", async ({ page, request }) => {
  102 |   await page.setViewportSize({ width: 1280, height: 800 });
  103 |   await page.goto(await studioUrl(request));
  104 |   await page.locator(".studio-block").first().waitFor();
  105 |   await page.waitForTimeout(1600);
  106 |   const smallest = await page.evaluate(() => {
  107 |     const vp = document.querySelector(".react-flow__viewport") as HTMLElement | null;
  108 |     const zoom = vp ? new DOMMatrix(getComputedStyle(vp).transform).a : 1;
  109 |     let min = Infinity;
  110 |     let where = "";
  111 |     document.querySelectorAll(".studio-block *").forEach((el) => {
  112 |       const hasText = [...el.childNodes].some((n) => n.nodeType === 3 && (n.textContent || "").trim());
  113 |       if (!hasText) return;
  114 |       const px = parseFloat(getComputedStyle(el).fontSize) * zoom;
  115 |       if (px < min) {
  116 |         min = px;
  117 |         where = (el.textContent || "").trim().slice(0, 30);
  118 |       }
  119 |     });
  120 |     return { min, zoom, where };
  121 |   });
  122 |   expect(smallest.zoom, "fit zoom").toBeGreaterThanOrEqual(0.85);
  123 |   expect(smallest.min, `smallest block text ("${smallest.where}") at zoom ${smallest.zoom.toFixed(2)}`).toBeGreaterThanOrEqual(10.9);
  124 | });
  125 | 
```