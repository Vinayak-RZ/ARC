import { test, expect } from "@playwright/test";

const BASE = process.env.ARC_UI_URL || "http://127.0.0.1:8765";

test.describe("Learn page", () => {
  test("S5 preselected, EEC-303 notes, topic done, practice recipe", async ({ page }) => {
    await page.goto(`${BASE}/?view=learn`, { waitUntil: "networkidle" });
    await expect(page.getByRole("heading", { name: "Learn" })).toBeVisible({ timeout: 20000 });
    const s5 = page.getByRole("tab", { name: /S5/ });
    await expect(s5).toHaveAttribute("aria-selected", "true");
    await page.getByRole("button", { name: /Power Electronics/i }).click();
    await expect(page.locator(".learn-subject-header h1")).toHaveText("Power Electronics", { timeout: 20000 });
    const frame = page.locator("iframe.learn-notes-frame");
    await expect(frame).toBeVisible();
    const done = page.locator(".learn-outline li").first().locator('input[type="checkbox"]');
    const hint = page.locator(".learn-subject-header .hint");
    const before = await hint.innerText();
    await done.click();
    await expect(hint).not.toHaveText(before, { timeout: 10000 });
    await page.getByRole("tab", { name: "Practice" }).click();
    await expect(page.getByText(/rectifier/i).first()).toBeVisible();
  });
});
