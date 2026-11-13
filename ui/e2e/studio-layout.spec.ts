// Run: STUDIO_URL=http://127.0.0.1:8765/?view=studio npx playwright test -c ui/e2e/playwright.config.ts
import { test, expect, Page } from "@playwright/test";

const BASE = process.env.STUDIO_BASE ?? "http://127.0.0.1:8765";

async function studioUrl(request: import("@playwright/test").APIRequestContext) {
  if (process.env.STUDIO_URL) return process.env.STUDIO_URL;
  const res = await request.post(`${BASE}/api/control-studio/sessions`, {
    data: { title: "E2E layout", golden: "pid_dc_motor" },
  });
  expect(res.ok()).toBeTruthy();
  const body = await res.json();
  return `${BASE}/?view=studio&session=${body.session_id}`;
}
const AREAS = {
  canvas: ".studio-canvas",
  palette: ".studio-palette-pane",
  inspector: ".studio-inspector",
  results: ".studio-results",
} as const;
type Box = { x: number; y: number; width: number; height: number };

const overlap = (a: Box, b: Box) => {
  const w = Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x);
  const h = Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y);
  return w > 0.5 && h > 0.5 ? { w, h } : null;
};

async function boxes(page: Page) {
  const out = {} as Record<keyof typeof AREAS, Box>;
  for (const [name, sel] of Object.entries(AREAS)) {
    const loc = page.locator(sel).first();
    const visible = await loc.isVisible().catch(() => false);
    if (!visible) continue;
    const b = await loc.boundingBox();
    expect(b, `${name} (${sel}) must be visible`).not.toBeNull();
    out[name as keyof typeof AREAS] = b!;
  }
  for (const required of ["canvas", "palette", "results"] as const) {
    expect(out[required], `${required} must be present`).toBeTruthy();
  }
  return out;
}

async function assertNoOverlap(page: Page, label: string) {
  const b = await boxes(page);
  const names = Object.keys(b) as (keyof typeof b)[];
  for (let i = 0; i < names.length; i++) {
    for (let j = i + 1; j < names.length; j++) {
      const hit = overlap(b[names[i]], b[names[j]]);
      expect(hit, `${label}: ${names[i]} overlaps ${names[j]} by ${JSON.stringify(hit)}\n${JSON.stringify(b)}`).toBeNull();
    }
  }
  const studio = (await page.locator(".studio").first().boundingBox())!;
  for (const n of names) {
    const r = b[n];
    expect(r.x, `${label}: ${n} left edge`).toBeGreaterThanOrEqual(studio.x - 0.5);
    expect(r.y, `${label}: ${n} top edge`).toBeGreaterThanOrEqual(studio.y - 0.5);
    expect(r.x + r.width, `${label}: ${n} right edge`).toBeLessThanOrEqual(studio.x + studio.width + 0.5);
    expect(r.y + r.height, `${label}: ${n} bottom edge`).toBeLessThanOrEqual(studio.y + studio.height + 0.5);
  }
  expect(b.canvas.height, `${label}: canvas height`).toBeGreaterThanOrEqual(280);
  expect(b.canvas.width, `${label}: canvas width`).toBeGreaterThanOrEqual(400);
}

for (const vp of [
  { width: 1280, height: 800 },
  { width: 1440, height: 900 },
]) {
  test(`studio areas never intersect at ${vp.width}x${vp.height}, before and after Simulate`, async ({ page, request }) => {
    await page.setViewportSize(vp);
    await page.goto(await studioUrl(request));
    await page.locator(AREAS.canvas).waitFor();
    await page.waitForTimeout(400);
    await assertNoOverlap(page, "before Simulate");

    if (process.env.NO_SIM) return;
    await page.locator(".cs-simulate-btn").click();
    await page.locator(".studio-results-stage .studio-step-svg, .studio-results-stage img").first().waitFor({ timeout: 120000 });
    await page.waitForFunction(() => {
      const svg = document.querySelector(".studio-results-stage .studio-step-svg");
      if (svg) return svg.getBoundingClientRect().height >= 120;
      const i = document.querySelector<HTMLImageElement>(".studio-results-stage img");
      return !!i && i.complete && i.naturalWidth > 0;
    });
    await page.waitForTimeout(250);
    await assertNoOverlap(page, "after Simulate");

    const r = (await page.locator(".studio-results").boundingBox())!;
    const stage = page.locator(".studio-results-stage .studio-step-svg, .studio-results-stage img").first();
    const plot = (await stage.boundingBox())!;
    expect(plot.y + plot.height).toBeLessThanOrEqual(r.y + r.height + 0.5);
    const th = page.locator(".studio-margin-table th");
    for (let i = 0; i < (await th.count()); i++) {
      const t = (await th.nth(i).boundingBox())!;
      expect(overlap(t, (await boxes(page)).canvas), `margin caption ${i} hidden`).toBeNull();
    }
  });
}

test("block text never renders below 11px on screen", async ({ page, request }) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto(await studioUrl(request));
  await page.locator(".studio-block").first().waitFor();
  await page.waitForTimeout(1600);
  const smallest = await page.evaluate(() => {
    const vp = document.querySelector(".react-flow__viewport") as HTMLElement | null;
    const zoom = vp ? new DOMMatrix(getComputedStyle(vp).transform).a : 1;
    let min = Infinity;
    let where = "";
    document.querySelectorAll(".studio-block *").forEach((el) => {
      const hasText = [...el.childNodes].some((n) => n.nodeType === 3 && (n.textContent || "").trim());
      if (!hasText) return;
      const px = parseFloat(getComputedStyle(el).fontSize) * zoom;
      if (px < min) {
        min = px;
        where = (el.textContent || "").trim().slice(0, 30);
      }
    });
    return { min, zoom, where };
  });
  expect(smallest.zoom, "fit zoom").toBeGreaterThanOrEqual(0.85);
  expect(smallest.min, `smallest block text ("${smallest.where}") at zoom ${smallest.zoom.toFixed(2)}`).toBeGreaterThanOrEqual(10.9);
});
