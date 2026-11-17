import { test, expect } from "@playwright/test";
import { prepareTheme } from "./layout-helpers.js";

const BASE = process.env.STUDIO_URL || process.env.ARC_UI_URL || "http://127.0.0.1:8765";

test.describe("Collab RLC revision loop", () => {
  test("derive r1 → edit r2 → re-derive → restore r3", async ({ page, request }) => {
    test.setTimeout(240_000);
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

    // r1 — agent derive
    await page.goto(`${BASE}/?problem=${runId}`);
    await expect(page.locator(".problem-display-title")).toHaveText("Series RLC step");
    await expect(page.getByRole("navigation").getByText("Series RLC step").first()).toBeVisible();
    await expect(page.locator(".answer-card")).toContainText("3.628", { timeout: 30000 });
    await expect(page.locator(".answer-card")).toContainText("11.630");

    const lab0 = await request.get(`${BASE}/api/runs/${runId}/lab`);
    expect(lab0.ok()).toBeTruthy();
    const rev1 = (await lab0.json()).lab_meta?.revision;
    expect(rev1).toBeGreaterThanOrEqual(1);

    // r2 — human R1 edit
    const labBody = await lab0.json();
    const graph = structuredClone(labBody.graph);
    for (const node of graph.nodes || []) {
      if (node.id === "r1") node.value = 20;
    }
    const put = await request.put(`${BASE}/api/runs/${runId}/graph`, { data: graph });
    expect(put.ok()).toBeTruthy();
    const verifyR2 = await request.post(`${BASE}/api/runs/${runId}/lab/verify`);
    expect(verifyR2.ok()).toBeTruthy();
    const lab2 = await request.get(`${BASE}/api/runs/${runId}/lab`);
    const rev2 = (await lab2.json()).lab_meta?.revision;
    expect(rev2).toBeGreaterThan(rev1);

    await page.goto(`${BASE}/?problem=${runId}`);
    await expect(page.locator(".problem-display-title")).toHaveText("Series RLC step");
    await expect(page.locator(".is-derived-stale, .verification-strip.verification-stale").first()).toBeVisible();
    await expect(page.locator(".answer-card, .verification-strip").first()).toContainText(/Out of date/i);
    await expect(page.getByText(/Needs review/i)).toHaveCount(0);

    await page.goto(`${BASE}/?view=studio&tab=circuits&run=${runId}`);
    await page.waitForSelector(".react-flow", { timeout: 45000 });
    await expect(page.locator(".lab-provenance-bar")).toContainText("Series RLC step");
    await expect(page.locator(".lab-provenance-rev")).toContainText(`r${rev2}`);

    // re-derive — agrees, no overshoot headline
    const rederive = await request.post(`${BASE}/api/runs/${runId}/lab/re-derive`);
    expect(rederive.ok()).toBeTruthy();

    await page.goto(`${BASE}/?problem=${runId}`);
    await expect(page.locator(".answer-card .answer-line")).toContainText("5.83", { timeout: 20000 });
    await expect(page.locator(".answer-card")).toContainText(/Settling \(2%\)/i);
    await expect(page.locator(".answer-card")).toContainText("10.00");

    await page.goto(`${BASE}/?view=studio&tab=circuits&run=${runId}&view=changes`);
    await page.waitForSelector(".react-flow", { timeout: 45000 });

    // restore — r3, original peak, no Changes chip
    const restore = await request.post(`${BASE}/api/runs/${runId}/lab/restore`);
    expect(restore.ok()).toBeTruthy();
    const lab3 = await request.get(`${BASE}/api/runs/${runId}/lab`);
    const rev3 = (await lab3.json()).lab_meta?.revision;
    expect(rev3).toBeGreaterThan(rev2);
    const r1node = (await lab3.json()).graph?.nodes?.find((n: { id: string }) => n.id === "r1");
    expect(Number(r1node?.value)).toBe(10);

    await page.goto(`${BASE}/?view=studio&tab=circuits&run=${runId}&view=changes`);
    await page.waitForSelector(".react-flow", { timeout: 45000 });
    await expect(page.locator(".lab-changes-chip-row")).toHaveCount(0);
    await expect(page.locator(".lab-provenance-rev")).toContainText(`r${rev3}`);
    await expect(page.locator(".studio-circuit-results .answer-line")).toContainText("11.630", {
      timeout: 60000,
    });
    await expect(page.locator(".studio-circuit-results .answer-line")).toContainText("3.628");
    await expect(page.locator(".lab-verify-badge.is-agrees")).toBeVisible();

    await page.goto(`${BASE}/?problem=${runId}`);
    await expect(page.locator(".problem-display-title")).toHaveText("Series RLC step");
    await expect(page.getByRole("navigation").getByText("Series RLC step").first()).toBeVisible();
    await expect(page.locator(".answer-card")).toContainText("3.628");
    await expect(page.locator(".answer-card")).toContainText("11.630");
    await expect(page.locator(".is-derived-stale")).toHaveCount(0);
  });
});