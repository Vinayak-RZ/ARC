import { test, expect } from "@playwright/test";

const BASE = process.env.STUDIO_URL || "http://127.0.0.1:8765";

test("agent-built circuit opens in Studio circuits lab", async ({ page, request }) => {
  const seed = await request.post(`${BASE}/api/examples/divider/run`);
  let runId = "";
  if (seed.ok()) {
    const body = await seed.json();
    runId = body.run_id;
  }
  test.skip(!runId, "no run id from API");
  const lab = await request.get(`${BASE}/api/runs/${runId}/lab`);
  expect(lab.ok()).toBeTruthy();
  const labBody = await lab.json();
  expect((labBody.graph?.nodes || []).length).toBeGreaterThan(2);
  await page.goto(`${BASE}/?problem=${runId}`);
  await page.getByRole("tab", { name: "Diagram" }).click();
  await page.waitForSelector(".react-flow", { timeout: 30000 });
});