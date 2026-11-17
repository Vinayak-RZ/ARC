import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { circuitLayoutProblem, prepareTheme, reinforceTheme } from "./layout-helpers.js";

// STUDIO_URL may carry a path and query (?view=studio); API calls need the bare origin.
const BASE = new URL(process.env.STUDIO_URL || process.env.ARC_UI_URL || "http://127.0.0.1:8765").origin;

const BAD_TEXT = /(\bNaN\b|undefined|\[object Object\])/i;

const VIEWPORTS = [
  { theme: "light" as const, width: 1440, height: 900 },
  { theme: "dark" as const, width: 1440, height: 900 },
  { theme: "light" as const, width: 1024, height: 900 },
];

async function assertNoBadChrome(page: import("@playwright/test").Page) {
  const body = await page.locator("body").innerText();
  expect(BAD_TEXT.test(body)).toBeFalsy();
  expect(await circuitLayoutProblem(page)).toBeNull();
}

test.describe("Full collab loop (independent TE)", () => {
  for (const vp of VIEWPORTS) {
    test(`agent lab RLC collab at ${vp.width}x${vp.height} ${vp.theme}`, async ({ page, request }) => {
      test.setTimeout(120_000);
      await page.setViewportSize({ width: vp.width, height: vp.height });
      await prepareTheme(page, vp.theme);

      const seed = await request.post(`${BASE}/api/examples/rlc-step/run`);
      test.skip(!seed.ok(), "series-rlc example API unavailable");
      const { run_id: runId } = await seed.json();
      expect(runId).toBeTruthy();

      const lab0 = await request.get(`${BASE}/api/runs/${runId}/lab`);
      expect(lab0.ok()).toBeTruthy();
      const labBody = await lab0.json();
      expect((labBody.graph?.nodes || []).length).toBeGreaterThan(2);

      await page.goto(`${BASE}/?problem=${runId}`);
      await reinforceTheme(page, vp.theme);
      await page.getByRole("tab", { name: /Diagram/i }).click();
      await page.waitForSelector(".react-flow", { timeout: 45000 });

      await page.goto(`${BASE}/?view=studio&tab=circuits&run=${runId}`);
      await reinforceTheme(page, vp.theme);
      await page.locator(".studio-circuit-app .cs-simulate-btn").click();
      await expect(page.locator(".studio-circuit-results .answer-line").first()).toBeVisible({ timeout: 45000 });

      const r1 = page.locator(".studio-circuit-inspector input").first();
      if (await r1.isVisible()) {
        await r1.fill("20");
        await page.locator(".studio-circuit-app .cs-simulate-btn").click();
        await page.waitForTimeout(800);
      }

      await assertNoBadChrome(page);

      const accessibility = await new AxeBuilder({ page })
        .include(".studio-circuit-app")
        .withTags(["wcag2a", "wcag2aa"])
        .analyze();
      expect(accessibility.violations, JSON.stringify(accessibility.violations, null, 2)).toEqual([]);

      const restore = await request.post(`${BASE}/api/runs/${runId}/lab/restore`);
      if (restore.ok()) {
        const after = await request.get(`${BASE}/api/runs/${runId}/lab`);
        expect(after.ok()).toBeTruthy();
      }
    });
  }
});