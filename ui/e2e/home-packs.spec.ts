import { test, expect } from "@playwright/test";

const BASE = process.env.ARC_UI_URL || "http://127.0.0.1:8765";

test.describe("Home packs", () => {
  test("ten capability cards and power electronics example filter", async ({ page }) => {
    await page.goto(`${BASE}/?view=home`);
    await expect(page.getByRole("heading", { name: "What Arc can do" })).toBeVisible();
    await expect(page.locator(".capability-card")).toHaveCount(10);
    await page.getByRole("group", { name: "Filter examples by pack" }).getByRole("button", { name: "Power electronics" }).click();
    await expect(page.getByText(/rectifier/i).first()).toBeVisible();
  });
});