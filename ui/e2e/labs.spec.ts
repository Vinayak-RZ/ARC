import { test, expect } from "@playwright/test";

const BASE = process.env.ARC_UI_URL || "http://127.0.0.1:8765";

test.describe("Studio labs", () => {
  test("rectifier lab Vo changes with alpha", async ({ page }) => {
    await page.goto(`${BASE}/?view=studio&tab=labs&lab=rectifier`);
    await expect(page.locator(".lab-shell h2").filter({ hasText: /Rectifier/i })).toBeVisible({ timeout: 15000 });
    const vo = page.locator(".lab-readouts .card").first().locator("strong");
    const before = await vo.innerText();
    await page.locator('input[type="range"]').nth(1).fill("90");
    await expect(vo).not.toHaveText(before);
  });
});
