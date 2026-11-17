import { test, expect } from "@playwright/test";
import { prepareTheme } from "./layout-helpers.js";

const BASE = process.env.STUDIO_URL || process.env.ARC_UI_URL || "http://127.0.0.1:8765";

test.describe("Collab RLC revision loop", () => {
  test("titles, stale answer, R20 settling, re-derive", async ({ page, request }) => {
    test.setTimeout(180_000);
    await page.setViewportSize({ width: 1440, height: 900 });
    await prepareTheme(page, "dark");

    const seed = await request.post(`${BASE}/api/examples/rlc-step/run`);
    test.skip(!seed.ok(), "series-rlc example API unavailable");
    const { run_id: runId } = await seed.json();
    expect(runId).toBeTruthy();

    await expect
      .poll(
        async () => {
          const res = await request.get(`${BASE}/api/runs/${runId}`);
          if (!res.ok()) return "";
          const b = await res.json();
          return b.circuit_derive?.value != null && b.rlc_transient?.Vc_peak_V != null ? "ready" : "";
        },
        { timeout: 120_000 },
      )
      .toBe("ready");

    await page.goto(`${BASE}/?problem=${runId}`);
    await expect(page.locator(".problem-display-title")).toHaveText("Series RLC step");
    await expect(page.getByRole("navigation").getByText("Series RLC step").first()).toBeVisible();
    await expect(page.locator(".answer-card .answer-line, .answer-card .answer-lines")).toContainText(
      /Vc,peak|No overshoot|11\.6/i,
      { timeout: 30000 },
    );

    const lab0 = await request.get(`${BASE}/api/runs/${runId}/lab`);
    expect(lab0.ok()).toBeTruthy();
    const labBody = await lab0.json();
    const graph = structuredClone(labBody.graph);
    for (const node of graph.nodes || []) {
      if (node.id === "r1") node.value = 20;
    }
    const put = await request.put(`${BASE}/api/runs/${runId}/graph`, { data: graph });
    expect(put.ok()).toBeTruthy();
    const verify = await request.post(`${BASE}/api/runs/${runId}/lab/verify`);
    expect(verify.ok()).toBeTruthy();

    await page.goto(`${BASE}/?problem=${runId}`);
    await expect(page.locator(".problem-display-title")).toHaveText("Series RLC step");
    await expect(page.locator(".is-derived-stale, .verification-strip.verification-stale")).toBeVisible({
      timeout: 20000,
    });
    await expect(page.locator(".answer-stale-rev, .verification-strip")).toContainText(/Out of date/i);
    await expect(page.getByText(/Needs review/i)).toHaveCount(0);

    await page.goto(`${BASE}/?view=studio&tab=circuits&run=${runId}`);
    await page.waitForSelector(".react-flow", { timeout: 45000 });
    await expect(page.locator(".lab-provenance-bar")).toContainText("Series RLC step");
    await expect(page.locator(".lab-verify-stack-metric")).toContainText("Final value");

    const rederive = await request.post(`${BASE}/api/runs/${runId}/lab/re-derive`);
    expect(rederive.ok()).toBeTruthy();
    const detail = await request.get(`${BASE}/api/runs/${runId}`);
    expect(detail.ok()).toBeTruthy();
    const body = await detail.json();
    expect(body.title).toBe("Series RLC step");
    expect(body.circuit_derive).toBeTruthy();
    expect(body.rlc_transient).toBeTruthy();

    await page.goto(`${BASE}/?problem=${runId}`);
    await expect(page.locator(".answer-line")).toContainText("5.83", { timeout: 15000 });
    await expect(page.locator(".answer-line")).toContainText(/Settling \(2%\)/i);
  });
});