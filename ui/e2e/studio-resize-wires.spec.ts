// Control Studio wires must survive viewport resize (1280×800 ↔ 1440×900).
import { test, expect } from "@playwright/test";

const BASE = process.env.STUDIO_BASE ?? "http://127.0.0.1:8765";

async function pidSession(request: import("@playwright/test").APIRequestContext) {
  const res = await request.post(`${BASE}/api/control-studio/sessions`, {
    data: { title: "E2E resize wires", golden: "pid_dc_motor" },
  });
  expect(res.ok()).toBeTruthy();
  const body = await res.json();
  return body.session_id as string;
}

async function wireStats(page: import("@playwright/test").Page) {
  return page.evaluate(() => {
    const paths = [...document.querySelectorAll(".studio-canvas .react-flow__edge-path")];
    return {
      n: paths.length,
      empty: paths.filter((p) => (p.getAttribute("d") || "").trim().length < 5).length,
      markers: paths.filter((p) => p.getAttribute("marker-end")).length,
    };
  });
}

async function expectStudioWires(page: import("@playwright/test").Page, label: string) {
  const deadline = Date.now() + 60_000;
  while (Date.now() < deadline) {
    const info = await wireStats(page);
    if (info.n >= 5 && info.empty === 0 && info.markers >= info.n) return;
    await page.waitForTimeout(250);
  }
  const info = await wireStats(page);
  expect(info, `${label}: studio wires`).toMatchObject({ n: expect.any(Number) });
  expect(info.n, `${label}: edge count`).toBeGreaterThanOrEqual(5);
  expect(info.empty, `${label}: empty paths`).toBe(0);
  expect(info.markers, `${label}: markers`).toBeGreaterThanOrEqual(info.n);
}

test("PID studio keeps signal wires after viewport resize down and back", async ({ page, request }) => {
  const sid = await pidSession(request);
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto(`${BASE}/?view=studio&tab=control&session=${sid}`, { waitUntil: "domcontentloaded" });
  await page.locator(".studio-canvas .react-flow").waitFor({ timeout: 30_000 });
  await expectStudioWires(page, "initial 1440");

  await page.setViewportSize({ width: 1280, height: 680 });
  await page.goto(`${BASE}/?view=studio&tab=control&session=${sid}`, { waitUntil: "domcontentloaded" });
  await page.locator(".studio-canvas .react-flow").waitFor({ timeout: 30_000 });
  await expectStudioWires(page, "narrow 1280 reload");

  await page.setViewportSize({ width: 1280, height: 800 });
  await expectStudioWires(page, "narrow 1280 after height bump");

  await page.setViewportSize({ width: 1440, height: 900 });
  await expectStudioWires(page, "restored 1440");
});