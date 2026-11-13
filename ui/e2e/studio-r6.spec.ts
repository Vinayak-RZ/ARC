import { test, expect, Page, APIRequestContext } from "@playwright/test";

const BASE = process.env.STUDIO_BASE ?? "http://127.0.0.1:8765";

async function open(page: Page, request: APIRequestContext, golden = "pid_dc_motor", title = "PID DC motor") {
  const r = await request.post(`${BASE}/api/control-studio/sessions`, { data: { title, golden } });
  const { session_id } = await r.json();
  const sess = await (await request.get(`${BASE}/api/control-studio/sessions/${session_id}`)).json();
  const want = Math.max(1, (sess.diagram?.wires ?? []).length as number);
  await page.goto(`${BASE}/?view=studio&session=${session_id}`);
  await expect(page.locator(".studio-canvas .react-flow__node").first()).toBeVisible();
  await assertEdgePaths(page, want);
  return { session_id, wires: want };
}

async function assertEdgePaths(page: Page, wires: number) {
  const paths = page.locator(".studio-canvas .react-flow__edge-path");
  await expect(paths).toHaveCount(wires, { timeout: 60_000 });
  await expect
    .poll(async () =>
      paths.evaluateAll(
        (els) => els.length > 0 && els.every((el) => (el.getAttribute("d") || "").trim().length > 4),
      ),
    )
    .toBe(true);
}

for (const width of [1280, 1440]) {
  test(`edge paths keep non-empty d before and after Simulate (${width})`, async ({ page, request }) => {
    await page.setViewportSize({ width, height: 900 });
    const errors: string[] = [];
    page.on("pageerror", (e) => errors.push(String(e)));
    page.on("console", (m) => m.type() === "error" && errors.push(m.text()));
    const { wires } = await open(page, request);
    await assertEdgePaths(page, wires);
    await page.getByRole("button", { name: "Simulate" }).click();
    await expect(page.locator(".studio-step-svg")).toBeVisible();
    await assertEdgePaths(page, wires);
    // wires must stay put: no flicker over a short idle window
    for (let i = 0; i < 6; i++) {
      await page.waitForTimeout(250);
      await assertEdgePaths(page, wires);
    }
    expect(errors, "console or page errors").toEqual([]);
  });
}

test("opening a session loads it once (no fetch/validate loop)", async ({ page, request }) => {
  const r = await request.post(`${BASE}/api/control-studio/sessions`, { data: { title: "loop", golden: "pid_dc_motor" } });
  const { session_id } = await r.json();
  let validates = 0;
  page.on("request", (q) => {
    if (q.url().includes(`/sessions/${session_id}/validate`)) validates += 1;
  });
  await page.goto(`${BASE}/?view=studio&session=${session_id}`);
  await expect(page.locator(".studio-canvas .react-flow__node").first()).toBeVisible();
  await page.waitForTimeout(3000);
  expect(validates, "validate calls in 3 s").toBeLessThanOrEqual(3);
});

for (const theme of ["light", "dark"]) {
  test(`arrowheads are visible (${theme})`, async ({ page, request }) => {
    await page.addInitScript((t) => localStorage.setItem("arc-theme", t), theme);
    await open(page, request);
    const res = await page.evaluate(() => {
      const canvas = document.querySelector(".studio-canvas") as HTMLElement;
      const bg = getComputedStyle(canvas).backgroundColor;
      const parse = (c: string) => c.match(/\d+(\.\d+)?/g)!.slice(0, 3).map(Number);
      const lum = ([r, g, b]: number[]) => {
        const f = (v: number) => {
          v /= 255;
          return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
        };
        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
      };
      const cr = (a: number[], b: number[]) => {
        const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p);
        return (x + 0.05) / (y + 0.05);
      };
      const paths = [...canvas.querySelectorAll(".react-flow__edge-path")];
      const withMarker = paths.filter((p) => p.getAttribute("marker-end")).length;
      const shapes = [...canvas.querySelectorAll(".react-flow__arrowhead polyline, marker polyline, marker polygon, marker path")];
      const sample = (el: Element) => {
        const st = getComputedStyle(el);
        const stroke = st.stroke && st.stroke !== "none" ? st.stroke : st.fill;
        return cr(parse(stroke), parse(bg));
      };
      const ratios = shapes.length ? shapes.map(sample) : paths.map((p) => cr(parse(getComputedStyle(p).stroke), parse(bg)));
      return { n: Math.max(withMarker, paths.length), min: ratios.length ? Math.min(...ratios) : 0 };
    });
    expect(res.n, "no arrowhead shapes found").toBeGreaterThanOrEqual(4);
    expect(res.min, "arrowhead contrast").toBeGreaterThanOrEqual(3);
  });
}

test("forward-path gaps and block labels", async ({ page, request }) => {
  await open(page, request);
  const zoom = await page.evaluate(() => {
    const t = getComputedStyle(document.querySelector(".react-flow__viewport")!).transform;
    return t === "none" ? 1 : new DOMMatrix(t).a;
  });
  const pid = await page.locator(".react-flow__node[data-id='pid1']").boundingBox();
  const motor = await page.locator(".react-flow__node[data-id='motor']").boundingBox();
  expect(pid && motor).toBeTruthy();
  expect((motor!.x - pid!.x - pid!.width) / zoom).toBeGreaterThanOrEqual(40);
  const overflowing = await page.locator(".studio-block-label, .studio-block-body").evaluateAll((els) =>
    els.filter((e) => e.scrollHeight > e.clientHeight + 1).map((e) => e.textContent),
  );
  expect(overflowing).toEqual([]);
});

test("step chart has ticks, size and one header row", async ({ page, request }) => {
  await open(page, request);
  await page.getByRole("button", { name: "Simulate" }).click();
  await page.waitForSelector(".studio-step-svg");
  const info = await page.evaluate(() => {
    const svg = document.querySelector(".studio-step-svg")!.getBoundingClientRect();
    const t = [...document.querySelectorAll(".studio-step-svg text.studio-step-tick")].map((n) => n.textContent ?? "");
    return { w: svg.width, h: svg.height, nums: t.filter((s) => /^-?\d+(\.\d+)?$/.test(s.trim())).length };
  });
  expect(info.w).toBeGreaterThanOrEqual(560);
  expect(info.h).toBeGreaterThanOrEqual(160);
  expect(info.nums, "tick labels").toBeGreaterThanOrEqual(6);
  const tabsTop = (await page.getByRole("tab", { name: "Step" }).boundingBox())!.y;
  const winTop = (await page.getByRole("button", { name: "Auto" }).boundingBox())!.y;
  expect(Math.abs(tabsTop - winTop), "tabs and window control share one row").toBeLessThan(12);
});

for (const theme of ["light", "dark"]) {
  test(`step chart header type and axis title (${theme})`, async ({ page, request }) => {
    await page.addInitScript((t) => localStorage.setItem("arc-theme", t), theme);
    await open(page, request);
    await page.getByRole("button", { name: "Simulate" }).click();
    await page.waitForSelector(".studio-step-svg");
    await page.getByRole("button", { name: "30 s" }).click();
    await expect(page.locator(".studio-step-axis").first()).toContainText("30 s window");
    const info = await page.evaluate(() => {
      const fs = (el: Element) => getComputedStyle(el).fontSize;
      const tab = document.querySelector(".studio-results-tabs button")!;
      const win = document.querySelector(".studio-window-segment button")!;
      const svg = document.querySelector(".studio-step-svg")!.getBoundingClientRect();
      const plot = document.querySelector(".studio-step-plot")!.getBoundingClientRect();
      const title = [...document.querySelectorAll(".studio-step-axis")].find((n) => /Time/.test(n.textContent || ""))!;
      const tb = title.getBoundingClientRect();
      const ticks = [...document.querySelectorAll("text.studio-step-tick")].map((n) => n.getBoundingClientRect());
      const tickBottom = Math.max(...ticks.map((r) => r.bottom));
      return {
        tabFs: fs(tab), winFs: fs(win),
        tabH: tab.getBoundingClientRect().height, winH: win.parentElement!.getBoundingClientRect().height,
        winColor: getComputedStyle(document.querySelector(".studio-window-segment button:not(.is-active)")!).color,
        titleBottomInSvg: svg.bottom - tb.bottom, titleBottomInPlot: plot.bottom - tb.bottom,
        titleAboveTicks: tb.top - tickBottom,
      };
    });
    expect(info.winFs).toBe(info.tabFs);
    expect(info.tabH).toBe(32);
    expect(info.winH).toBe(32);
    expect(info.titleBottomInSvg, "axis title inside svg").toBeGreaterThanOrEqual(2);
    expect(info.titleBottomInPlot, "axis title inside plot box").toBeGreaterThanOrEqual(0);
    expect(info.titleAboveTicks, "axis title does not touch tick numbers").toBeGreaterThanOrEqual(0);
  });
}

test("inspector controls stay visible after Simulate", async ({ page, request }) => {
  await open(page, request);
  await page.getByRole("button", { name: "Simulate" }).click();
  await page.waitForSelector(".studio-step-svg");
  await page.locator(".react-flow__node", { hasText: "PID" }).click();
  for (const name of ["Kp", "Ki", "Kd"]) await expect(page.getByLabel(name)).toBeInViewport();
  await expect(page.getByRole("button", { name: "Pin" })).toBeInViewport();
});

test("low gain: phase margin is not defined", async ({ page, request }) => {
  await open(page, request, "open_loop_low_gain", "Low gain");
  await page.getByRole("button", { name: "Simulate" }).click();
  await page.waitForSelector(".studio-margin");
  await expect(page.locator(".studio-margins")).toContainText("Not defined");
});
