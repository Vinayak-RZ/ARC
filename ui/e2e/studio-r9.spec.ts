// Round 9 additions. Add studio-r9 to testMatch. Run: STUDIO_BASE=http://127.0.0.1:8765 npx playwright test -c e2e/playwright.config.ts studio-r9
import { test, expect, APIRequestContext } from "@playwright/test";

const BASE = process.env.STUDIO_BASE ?? "http://127.0.0.1:8765";

async function sim(request: APIRequestContext, golden: string, tFinal: string | number) {
  const r = await request.post(`${BASE}/api/control-studio/sessions`, { data: { title: "Lab 4 · check", golden } });
  const { session_id } = await r.json();
  const out = await (await request.post(`${BASE}/api/control-studio/sessions/${session_id}/simulate`, { data: { t_final: tFinal } })).json();
  return out.step_series.metrics;
}

// ts must not depend on the window button: K = 10 is ln(50)/11 = 0.3556 s whatever the grid.
for (const golden of ["unity_first_order", "pid_dc_motor"]) {
  test(`settling time does not depend on the window (${golden})`, async ({ request }) => {
    const auto = (await sim(request, golden, "auto")).t_settle_s as number;
    for (const w of [10, 30, 100]) {
      const ts = (await sim(request, golden, w)).t_settle_s as number;
      expect(Math.abs(ts - auto) / auto, `${w} s window vs Auto`).toBeLessThan(0.01);
    }
  });
}

test("K = 10 settling time matches theory on the default 10 s window", async ({ request }) => {
  const m = await sim(request, "unity_first_order", 10);
  expect(m.t_settle_s).toBeCloseTo(Math.log(50) / 11, 2); // 0.3556 +- 0.005
});

test("chart labels never overprint tick numbers or the setpoint line (PID and low gain)", async ({ page, request }) => {
  for (const golden of ["pid_dc_motor", "open_loop_low_gain"]) {
    const r = await request.post(`${BASE}/api/control-studio/sessions`, { data: { title: "HW 3 · check", golden } });
    const { session_id } = await r.json();
    await page.goto(`${BASE}/?view=studio&session=${session_id}`);
    await page.getByRole("button", { name: "Simulate" }).click();
    await page.waitForSelector(".studio-step-svg");
    const clashes = await page.evaluate(() => {
      const svg = document.querySelector(".studio-step-svg")!;
      const hit = (a: DOMRect, b: DOMRect) => a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;
      const labels = [...svg.querySelectorAll("text:not(.studio-step-tick):not(.studio-step-axis)")].map((n) => ({ n, r: n.getBoundingClientRect(), t: n.textContent }));
      const ticks = [...svg.querySelectorAll("text.studio-step-tick")].map((n) => n.getBoundingClientRect());
      const setpoint = svg.querySelector(".studio-step-setpoint")?.getBoundingClientRect();
      const out: string[] = [];
      for (const l of labels) {
        if (ticks.some((t) => hit(l.r, t))) out.push(`${l.t} overlaps a tick number`);
        if (setpoint && /%$/.test(l.t || "") && hit(l.r, setpoint)) out.push(`${l.t} crosses the setpoint line`);
      }
      return out;
    });
    expect(clashes, golden).toEqual([]);
  }
});
