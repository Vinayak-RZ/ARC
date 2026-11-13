import { test, expect, Page } from "@playwright/test";

const BASE = process.env.STUDIO_BASE ?? "http://127.0.0.1:8765";

async function studioUrl(request: import("@playwright/test").APIRequestContext) {
  const res = await request.post(`${BASE}/api/control-studio/sessions`, {
    data: { title: "Wire test", golden: "pid_dc_motor" },
  });
  expect(res.ok()).toBeTruthy();
  const body = await res.json();
  return `${BASE}/?view=studio&session=${body.session_id}`;
}

async function contentOutsideCanvas(page: Page, label: string) {
  const canvas = await page.locator(".studio-canvas").boundingBox();
  expect(canvas, `${label}: canvas`).not.toBeNull();
  const inset = 8;
  const box = {
    x: canvas!.x + inset,
    y: canvas!.y + inset,
    width: canvas!.width - 2 * inset,
    height: canvas!.height - 2 * inset,
  };
  const sel =
    ".react-flow__edge-path, .react-flow__arrowhead, .react-flow__edge circle, .studio-block";
  const rects = await page.locator(sel).evaluateAll((els) =>
    els.map((el) => {
      const r = el.getBoundingClientRect();
      return { x: r.x, y: r.y, width: r.width, height: r.height };
    }),
  );
  const bad: string[] = [];
  for (const r of rects) {
    if (r.width <= 0 && r.height <= 0) continue;
    if (
      r.x < box.x - 0.5 ||
      r.y < box.y - 0.5 ||
      r.x + r.width > box.x + box.width + 0.5 ||
      r.y + r.height > box.y + box.height + 0.5
    ) {
      bad.push(JSON.stringify(r));
    }
  }
  expect(bad, `${label}: drawn content outside canvas`).toEqual([]);
}

for (const vp of [
  { width: 1280, height: 800 },
  { width: 1440, height: 900 },
]) {
  test(`wires stay inside canvas at ${vp.width}x${vp.height}`, async ({ page, request }) => {
    await page.setViewportSize(vp);
    await page.goto(await studioUrl(request));
    await page.waitForSelector(".studio-canvas", { timeout: 15000 });
    await page.waitForTimeout(1200);
    await contentOutsideCanvas(page, "before simulate");
    await page.locator(".cs-simulate-btn").click();
    await page.waitForTimeout(1600);
    await contentOutsideCanvas(page, "after simulate");
    const pid = page.locator(".react-flow__node[data-id='pid1']");
    const b = await pid.boundingBox();
    if (b) await page.mouse.click(b.x + b.width / 2, b.y + b.height / 2);
    await page.waitForSelector(".studio-block.is-selected", { timeout: 5000 });
    await page.waitForTimeout(1200);
    await contentOutsideCanvas(page, "after select");
    await page.locator(".cs-simulate-btn").click();
    await page.waitForTimeout(2000);
    expect(await page.locator(".studio-block.is-selected").count()).toBe(1);
    await contentOutsideCanvas(page, "after simulate with selection");
  });
}
