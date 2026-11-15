import { test, expect } from "@playwright/test";

const BASE = process.env.ARC_UI_URL || "http://127.0.0.1:8765";

test.describe("Learn page", () => {
  test("S5 preselected, EEC-303 notes, topic done, practice recipe", async ({ page }) => {
    await page.goto(`${BASE}/?view=learn`);
    await expect(page.getByRole("heading", { name: "Learn" })).toBeVisible();
    const s5 = page.getByRole("tab", { name: /S5/ });
    await expect(s5).toHaveAttribute("aria-selected", "true");
    await page.getByRole("button", { name: /Power Electronics/i }).click();
    await expect(page.getByRole("heading", { name: "Power Electronics" })).toBeVisible();
    const frame = page.locator("iframe.learn-notes-frame");
    await expect(frame).toBeVisible();
    const done = page.locator(".learn-outline li").first().locator('input[type="checkbox"]');
    const before = await page.locator(".learn-subject-header .hint").innerText();
    await done.check();
    await expect(page.locator(".learn-subject-header .hint")).not.toHaveText(before, { timeout: 10000 });
    await page.getByRole("tab", { name: "Practice" }).click();
    await expect(page.getByText(/rectifier/i).first()).toBeVisible();
  });
});
