import path from "node:path";
import { fileURLToPath } from "node:url";
import { test } from "@playwright/test";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(__dirname, "../../artifacts/ux-review/round-11-prep");

const BASE = process.env.ARC_UI_URL || "http://127.0.0.1:8765";

test.describe.configure({ mode: "serial" });

test("lab-rectifier-light", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto(`${BASE}/?view=studio&tab=labs&lab=rectifier`);
  await page.waitForSelector(".lab-shell");
  await page.screenshot({ path: path.join(OUT, "lab-rectifier-light.png") });
});

test("studio-circuit-series-rlc-after-simulate-light", async ({ page }) => {
  test.setTimeout(120_000);
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto(`${BASE}/?view=studio&tab=circuits`);
  await page.evaluate(() => localStorage.removeItem("arc-circuit-sandbox-v1"));
  await page.getByRole("button", { name: "Series RLC" }).click();
  await page.locator(".part-ref", { hasText: "V1" }).waitFor();
  await Promise.all([
    page.waitForResponse((r) => r.url().includes("/api/circuit-sandbox/simulate") && r.status() === 200),
    page.locator(".studio-circuit-sandbox .cs-simulate-btn").click(),
  ]);
  await page.locator(".studio-circuit-results .se-waveform").waitFor({ timeout: 60000 });
  await page.screenshot({ path: path.join(OUT, "studio-circuit-series-rlc-after-simulate-light.png") });
});

test("studio-control-after-simulate-light", async ({ page, request }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  const res = await request.post(`${BASE}/api/control-studio/sessions`, {
    data: { title: "Spot control", golden: "pid_dc_motor" },
  });
  const { session_id } = await res.json();
  await page.goto(`${BASE}/?view=studio&session=${session_id}&tab=control`);
  await page.locator(".cs-simulate-btn").click();
  await page.locator(".studio-results-stage .studio-step-svg, .studio-results-stage img").first().waitFor({
    timeout: 120000,
  });
  await page.screenshot({ path: path.join(OUT, "studio-control-after-simulate-light.png") });
});

test("lab-idmt-light", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto(`${BASE}/?view=studio&tab=labs&lab=idmt`);
  await page.waitForSelector(".lab-shell");
  await page.screenshot({ path: path.join(OUT, "lab-idmt-light.png") });
});