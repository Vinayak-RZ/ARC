// Round 8 additions. Run: STUDIO_BASE=http://127.0.0.1:8765 npx playwright test -c e2e/playwright.config.ts studio-r8
// Add studio-r8 to testMatch in playwright.config.ts.
import { test, expect, Page, APIRequestContext } from "@playwright/test";

const BASE = process.env.STUDIO_BASE ?? "http://127.0.0.1:8765";

async function session(request: APIRequestContext, golden: string, title: string) {
  const r = await request.post(`${BASE}/api/control-studio/sessions`, { data: { title, golden } });
  return (await r.json()).session_id as string;
}

for (const theme of ["light", "dark"]) {
  test(`margin captions are never truncated, inspector open (${theme})`, async ({ page, request }) => {
    await page.addInitScript((t) => localStorage.setItem("arc-theme", t), theme);
    const id = await session(request, "pid_dc_motor", "PID DC motor");
    await page.goto(`${BASE}/?view=studio&session=${id}`);
    await page.getByRole("button", { name: "Simulate" }).click();
    await page.waitForSelector(".studio-margin-meta");
    await page.locator(".react-flow__node", { hasText: "PID" }).click();
    await page.waitForTimeout(500);
    const cut = await page.locator(".studio-margin-meta").evaluateAll((els) =>
      els.filter((e) => e.scrollHeight > e.clientHeight + 1).map((e) => e.textContent),
    );
    expect(cut, "captions cut off by line-clamp").toEqual([]);
  });
}

// Settling is measured against the FINAL value, not the setpoint (Ogata, Nise, Franklin and Powell: 2% of final value).
test("off-target loop reports settling time and overshoot against its final value", async ({ request }) => {
  const id = await session(request, "unity_first_order", "Finite crossover"); // K = 10, y_ss = 10/11
  const sim = await (await request.post(`${BASE}/api/control-studio/sessions/${id}/simulate`, { data: {} })).json();
  const s = sim.step_series;
  const m = s.metrics;
  expect(m.status).toBe("settled_off_target");
  expect(m.final_value).toBeCloseTo(10 / 11, 3);
  expect(m.steady_state_error_pct).toBeCloseTo(9.1, 1);
  expect(m.t_settle_s, "settling time must exist for a flat, off-target response").not.toBeNull();
  // independent recomputation: last time |y - y_ss| > 2% of y_ss
  const yss = m.final_value as number;
  let idx = 0;
  for (let i = s.y.length - 1; i >= 0; i -= 1) if (Math.abs(s.y[i] - yss) > 0.02 * Math.abs(yss)) { idx = i; break; }
  expect(m.t_settle_s).toBeCloseTo(s.t[idx], 2);
  expect(m.t_settle_s).toBeLessThan(0.5); // ln(50)/11 = 0.36 s for this loop
  expect(m.overshoot_pct).toBeCloseTo(0, 1);
});

test("chart shows setpoint and final value separately when the loop settles off target", async ({ page, request }) => {
  const id = await session(request, "unity_first_order", "Finite crossover");
  await page.goto(`${BASE}/?view=studio&session=${id}`);
  await page.getByRole("button", { name: "Simulate" }).click();
  await page.waitForSelector(".studio-step-svg");
  await expect(page.locator(".studio-step-setpoint")).toHaveCount(1);
  await expect(page.locator(".studio-step-final"), "dotted final-value line").toHaveCount(1);
  await expect(page.locator(".studio-step-sse"), "steady-state error label").toContainText(/9\.1\s?%/);
  const { band, finalY } = await page.evaluate(() => {
    const b = document.querySelector(".studio-step-band")!.getBoundingClientRect();
    const f = document.querySelector(".studio-step-final")!.getBoundingClientRect();
    return { band: b.top + b.height / 2, finalY: f.top + f.height / 2 };
  });
  expect(Math.abs(band - finalY), "band is centred on the final value").toBeLessThan(1.5);
});
