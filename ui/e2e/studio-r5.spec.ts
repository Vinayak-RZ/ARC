// Round 5/6 studio assertions (margins, inspector, preflight, dark arrowheads)
import { test, expect, Page } from "@playwright/test";

const BASE = process.env.STUDIO_BASE ?? "http://127.0.0.1:8765";

const box = async (page: Page, sel: string) =>
  page.locator(sel).evaluateAll((els) =>
    els.map((e) => {
      const r = e.getBoundingClientRect();
      return { x: r.x, y: r.y, w: r.width, h: r.height };
    }),
  );
const hit = (a: { x: number; y: number; w: number; h: number }, b: typeof a) =>
  a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;

async function openPid(page: Page, request: import("@playwright/test").APIRequestContext) {
  const r = await request.post(`${BASE}/api/control-studio/sessions`, {
    data: { title: "PID DC motor", golden: "pid_dc_motor" },
  });
  const { session_id } = await r.json();
  await page.goto(`${BASE}/?view=studio&session=${session_id}`);
  await page.waitForSelector(".studio-canvas .react-flow__node");
  return session_id;
}

test("preflight: backend matches the source", async ({ request }) => {
  const r = await request.post(`${BASE}/api/control-studio/sessions`, { data: { golden: "pid_dc_motor" } });
  const { session_id } = await r.json();
  const sess = await (await request.get(`${BASE}/api/control-studio/sessions/${session_id}`)).json();
  const pid = (sess.diagram?.blocks || []).find((b: { id: string }) => b.id === "pid1");
  expect(pid?.params?.kp, "PID kp must be 50 in served backend").toBe(50);
  const sim = await (await request.post(`${BASE}/api/control-studio/sessions/${session_id}/simulate`, { data: {} })).json();
  expect(sim.step_series, "backend is older than the UI").toBeTruthy();
  const tips = JSON.stringify(sim.analyze?.margin_tooltips ?? sim.analyze?.display ?? {});
  expect(tips).toContain("180");
  expect(tips).not.toContain("above 0 dB in the analyzed band");
});

test("margins never collide or clip", async ({ page, request }) => {
  await openPid(page, request);
  await page.getByRole("button", { name: "Simulate" }).click();
  await page.waitForSelector(".studio-margin");
  const clipped = await page.locator(".studio-margin .num, .studio-margin .is-textual").evaluateAll((els) =>
    els.filter((e) => e.scrollWidth > e.clientWidth + 1).map((e) => e.textContent),
  );
  expect(clipped).toEqual([]);
  const cells = await box(page, ".studio-margin");
  for (let i = 0; i < cells.length; i += 1) {
    for (let j = i + 1; j < cells.length; j += 1) expect(hit(cells[i], cells[j])).toBe(false);
  }
  const chart = (await box(page, ".studio-step-chart, .studio-results-stage"))[0];
  for (const c of cells) expect(hit(c, chart)).toBe(false);
});

for (const phase of ["before", "after"] as const) {
  test(`inspector never covers a block or wire (${phase} Simulate)`, async ({ page, request }) => {
    await openPid(page, request);
    if (phase === "after") await page.getByRole("button", { name: "Simulate" }).click();
    await page.locator(".react-flow__node", { hasText: "PID" }).click();
    await page.waitForTimeout(400);
    const insp = (await box(page, ".studio-inspector:not(.studio-inspector-float)"))[0];
    expect(insp).toBeTruthy();
    for (const n of await box(page, ".studio-canvas .react-flow__node")) expect(hit(insp, n)).toBe(false);
    for (const e of await box(page, ".studio-canvas .react-flow__edge-path")) expect(hit(insp, e)).toBe(false);
  });
}

test("arrowheads are visible in dark", async ({ page, request }) => {
  await page.addInitScript(() => localStorage.setItem("arc-theme", "dark"));
  await openPid(page, request);
  const res = await page.evaluate(() => {
    const canvas = document.querySelector(".studio-canvas") as HTMLElement;
    const paths = [...canvas.querySelectorAll(".react-flow__edge-path")];
    return paths.filter((p) => p.getAttribute("marker-end")).length;
  });
  expect(res).toBeGreaterThanOrEqual(4);
});
