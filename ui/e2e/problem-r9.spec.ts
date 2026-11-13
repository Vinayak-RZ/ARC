// Round 9: the Work tab shows the working by default, and the expander label tracks its state.
import { test, expect } from "@playwright/test";

const BASE = process.env.STUDIO_BASE ?? "http://127.0.0.1:8765";

test("step 2 is open by default and the expander label toggles", async ({ page, request }) => {
  const r = await request.post(`${BASE}/api/examples/divider/run`, { data: {} });
  const { run_id } = await r.json();
  await page.goto(`${BASE}/?problem=${run_id}`);
  await page.getByRole("tab", { name: "Work" }).click();
  const btn = page.locator(".step-expand").first();
  await expect(btn).toHaveAttribute("aria-expanded", "true");
  await expect(btn).toHaveAttribute("aria-label", "Hide working");
  await expect(page.locator(".step-detail")).toContainText("R");
  await btn.click();
  await expect(btn).toHaveAttribute("aria-expanded", "false");
  await expect(btn).toHaveAttribute("aria-label", "Show working");
  await expect(page.locator(".step-detail")).toHaveCount(0);
});
