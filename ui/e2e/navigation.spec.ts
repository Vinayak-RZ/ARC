import { test, expect } from "@playwright/test";

const BASE = process.env.ARC_UI_URL || "http://127.0.0.1:8765";

test.describe("product navigation", () => {
  test("Problems nav clears open problem", async ({ page }) => {
    await page.goto(`${BASE}/?view=home`);
    await page.evaluate(() => localStorage.setItem("arc-sidebar-collapsed", "0"));
    await page.reload();
    // Open first recent or skip if empty — use URL deep link if samples exist later
    const recent = page.locator(".sidebar-recent-item").first();
    if (await recent.count()) {
      await recent.click();
      await expect(page.locator(".product-topbar .breadcrumb")).toContainText("/");
      await page.getByRole("button", { name: "Problems", exact: true }).click();
      await expect(page.locator("main h1")).toHaveText("Problems");
      await expect(page).toHaveURL(/view=problems/);
      await expect(page).not.toHaveURL(/problem=/);
    } else {
      await page.getByRole("button", { name: "Problems", exact: true }).click();
      await expect(page).toHaveURL(/view=problems/);
    }
  });

  test("browser back returns to previous view", async ({ page }) => {
    await page.goto(`${BASE}/?view=home`);
    await page.getByRole("button", { name: "Gallery", exact: true }).click();
    await expect(page).toHaveURL(/view=gallery/);
    await page.getByRole("button", { name: "Library", exact: true }).click();
    await expect(page).toHaveURL(/view=library/);
    await page.goBack();
    await expect(page).toHaveURL(/view=gallery/);
  });

  test("sidebar collapsed by default on fresh profile", async ({ page }) => {
    await page.goto(`${BASE}/?view=home`);
    await page.evaluate(() => localStorage.removeItem("arc-sidebar-collapsed"));
    await page.reload();
    await expect(page.locator(".product-shell")).toHaveClass(/is-sidebar-collapsed/);
  });
});
