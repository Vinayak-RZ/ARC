import { test, expect } from "@playwright/test";

const BASE = process.env.STUDIO_BASE ?? "http://127.0.0.1:8765";

async function studioUrl(request: import("@playwright/test").APIRequestContext) {
  if (process.env.STUDIO_URL) return process.env.STUDIO_URL;
  const res = await request.post(`${BASE}/api/control-studio/sessions`, {
    data: { title: "E2E step chart", golden: "pid_dc_motor" },
  });
  expect(res.ok()).toBeTruthy();
  const body = await res.json();
  return `${BASE}/?view=studio&session=${body.session_id}`;
}

test("Control Studio step chart visible and block labels not clipped", async ({ page, request }) => {
  test.setTimeout(180_000);
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto(`${await studioUrl(request)}&tab=control`);
  await page.locator(".studio-results").waitFor();
  await page.locator(".cs-simulate-btn").click();
  await page
    .locator(".studio-results-stage .studio-step-svg, .studio-results-stage img")
    .first()
    .waitFor({ timeout: 120000 });
  const stage = page.locator(".studio-results-stage").first();
  const plot = page.locator(".studio-results-stage .studio-step-svg, .studio-results-stage img").first();
  const plotBox = await plot.boundingBox();
  expect(plotBox?.height ?? 0).toBeGreaterThan(80);
  const stageBox = await stage.boundingBox();
  expect((stageBox?.height ?? 0) > 60).toBeTruthy();

  const clipped = await page.evaluate(() => {
    const sel = ".studio-block-body span, .plant-label, .studio-source span, .studio-block-kind";
    const nodes = document.querySelectorAll(sel);
    for (const node of nodes) {
      const el = node as HTMLElement;
      if (el.scrollHeight > el.clientHeight + 1) return el.textContent || "?";
    }
    return null;
  });
  expect(clipped, `label clipped: ${clipped}`).toBeNull();
});