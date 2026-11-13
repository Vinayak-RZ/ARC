// Round 7 additions. Run: STUDIO_BASE=http://127.0.0.1:8765 npx playwright test -c e2e/playwright.config.ts studio-r7
import { test, expect, Page } from "@playwright/test";

const BASE = process.env.STUDIO_BASE ?? "http://127.0.0.1:8765";

const parse = (c: string) => c.match(/[\d.]+/g)!.slice(0, 3).map(Number);
const lum = ([r, g, b]: number[]) => {
  const f = (v: number) => ((v /= 255) <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4);
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
};
const cr = (a: number[], b: number[]) => {
  const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p);
  return (x + 0.05) / (y + 0.05);
};

async function simulate(page: Page, request: any, theme: string) {
  await page.addInitScript((t) => localStorage.setItem("arc-theme", t), theme);
  const r = await request.post(`${BASE}/api/control-studio/sessions`, { data: { title: "PID DC motor", golden: "pid_dc_motor" } });
  const { session_id } = await r.json();
  await page.goto(`${BASE}/?view=studio&session=${session_id}`);
  await page.getByRole("button", { name: "Simulate" }).click();
  await page.waitForSelector(".studio-margin-meta");
}

for (const theme of ["light", "dark"]) {
  test(`margin captions are 12px and 4.5:1 (${theme})`, async ({ page, request }) => {
    await simulate(page, request, theme);
    const r = await page.evaluate(() => {
      const e = document.querySelector(".studio-margin-meta")!;
      const s = getComputedStyle(e);
      return { color: s.color, size: parseFloat(s.fontSize), bg: getComputedStyle(document.querySelector(".studio-results")!).backgroundColor };
    });
    expect(r.size).toBeGreaterThanOrEqual(12);
    expect(cr(parse(r.color), parse(r.bg))).toBeGreaterThanOrEqual(4.5);
  });

  test(`home thumbnail well is visible against its tile (${theme})`, async ({ page }) => {
    await page.addInitScript((t) => localStorage.setItem("arc-theme", t), theme);
    await page.goto(`${BASE}/`);
    await page.waitForSelector(".example-card .example-thumb-bg");
    const r = await page.evaluate(() => {
      const card = document.querySelector(".example-card")!;
      const well = document.querySelector(".example-card .example-thumb-bg")!;
      return { tile: getComputedStyle(card).backgroundColor, well: getComputedStyle(well).fill };
    });
    const ratio = cr(parse(r.tile), parse(r.well));
    expect(ratio, `tile ${r.tile} vs well ${r.well}`).toBeGreaterThanOrEqual(1.05);
    expect(ratio).toBeLessThanOrEqual(1.25); // a quiet step, not a second card
  });
}
