import { test, expect, Page, APIRequestContext } from "@playwright/test";

const BASE = process.env.STUDIO_BASE ?? "http://127.0.0.1:8765";

async function open(page: Page, request: APIRequestContext, golden = "pid_dc_motor", title = "PID DC motor") {
  const r = await request.post(`${BASE}/api/control-studio/sessions`, { data: { title, golden } });
  const { session_id } = await r.json();
  const sess = await (await request.get(`${BASE}/api/control-studio/sessions/${session_id}`)).json();
  const want = Math.max(1, (sess.diagram?.wires ?? []).length as number);
  for (let attempt = 0; attempt < 3; attempt += 1) {
    await page.goto(`${BASE}/?view=studio&session=${session_id}`, { waitUntil: "domcontentloaded" });
    await page.waitForSelector(".studio-canvas .react-flow__node");
    try {
      await page.waitForFunction(
        (n) => document.querySelectorAll(".studio-canvas .react-flow__edge-path").length >= n,
        want,
        { timeout: 20000 },
      );
      break;
    } catch (err) {
      if (attempt === 2) throw err;
    }
  }
  return { session_id, wires: want };
}

for (const vp of [
  { width: 1280, height: 800 },
  { width: 1440, height: 900 },
]) {
  for (const phase of ["before", "after"] as const) {
    test(`every wire is drawn at ${vp.width}x${vp.height} (${phase} Simulate)`, async ({ browser, request }) => {
      const page = await browser.newPage({ viewport: vp });
      try {
        const errors: string[] = [];
        page.on("pageerror", (e) => errors.push(String(e)));
        page.on("console", (m) => m.type() === "error" && errors.push(m.text()));
        const { wires } = await open(page, request);
        if (phase === "after") {
          await page.getByRole("button", { name: "Simulate" }).click();
          await page.waitForSelector(".studio-step-svg");
          await page.waitForFunction(
            (n) => document.querySelectorAll(".studio-canvas .react-flow__edge-path").length >= n,
            wires,
            { timeout: 45000 },
          );
        }
        await expect(page.locator(".studio-canvas .react-flow__edge")).toHaveCount(wires);
        const sizes = await page.locator(".studio-canvas .react-flow__edge-path").evaluateAll((els) =>
          els.map((e) => {
            const r = e.getBoundingClientRect();
            return r.width + r.height;
          }),
        );
        expect(sizes.every((s) => s > 4), "an edge path has no size").toBe(true);
        expect(errors, "console or page errors").toEqual([]);
      } finally {
        await page.close();
      }
    });
  }
}

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
      return { n: withMarker, min: ratios.length ? Math.min(...ratios) : 0 };
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
