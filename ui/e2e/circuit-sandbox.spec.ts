import { test, expect } from "@playwright/test";
import { circuitLayoutProblem, prepareTheme, reinforceTheme, svgAxisOverlapProblem } from "./layout-helpers.js";

const BASE = process.env.ARC_UI_URL || "http://127.0.0.1:8765";

test.describe("Circuit sandbox", () => {
  test("Series RLC simulate reports Vc,peak near 11.630 V with unit", async ({ page }) => {
    test.setTimeout(90_000);
    await page.setViewportSize({ width: 1440, height: 900 });
    await prepareTheme(page, "light");
    await page.goto(`${BASE}/?view=studio&tab=circuits`);
    await reinforceTheme(page, "light");
    await page.evaluate(() => localStorage.removeItem("arc-circuit-sandbox-v1"));
    await page.getByRole("button", { name: "Series RLC" }).click();
    await page.locator(".part-ref", { hasText: "V1" }).waitFor();
    const simBtn = page.locator(".studio-circuit-app .cs-simulate-btn");
    await Promise.all([
      page.waitForResponse((r) => r.url().includes("/api/circuit-sandbox/simulate") && r.status() === 200),
      simBtn.click(),
    ]);
    await expect(page.locator(".studio-circuit-results .se-waveform")).toBeVisible({ timeout: 30000 });
    const num = page.locator(".studio-circuit-results .answer-num");
    await expect(num).toBeVisible();
    await expect(page.locator(".studio-circuit-results .answer-unit")).toHaveText(/V/);
    const v = parseFloat(await num.innerText());
    expect(Number.isFinite(v)).toBeTruthy();
    expect(Math.abs(v - 11.63) / 11.63).toBeLessThan(0.005);
    await expect(page.locator(".studio-circuit-probes")).toBeVisible();
    expect(await circuitLayoutProblem(page)).toBeNull();
    expect(await svgAxisOverlapProblem(page, ".studio-circuit-results .se-waveform")).toBeNull();
  });
});