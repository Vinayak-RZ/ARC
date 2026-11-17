import path from "node:path";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { test } from "@playwright/test";
import {
  assertDarkPngCanvasNotLight,
  circuitCanvasLuminance,
  circuitLayoutProblem,
  prepareTheme,
  reinforceTheme,
  svgAxisOverlapProblem,
} from "./layout-helpers.js";
import { expect } from "@playwright/test";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(__dirname, "../../artifacts/ux-review/round-11-prep");

const BASE = process.env.ARC_UI_URL || "http://127.0.0.1:8765";

test.describe.configure({ mode: "serial" });

function sha256(file: string) {
  return createHash("sha256").update(readFileSync(file)).digest("hex");
}

async function shot(page: import("@playwright/test").Page, name: string) {
  await page.screenshot({ path: path.join(OUT, name), fullPage: false });
  if (name.startsWith("studio-circuit-") && name.includes("-dark.png")) {
    assertDarkPngCanvasNotLight(path.join(OUT, name));
  }
}

test("lab-rectifier-light", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await prepareTheme(page, "light");
  await page.goto(`${BASE}/?view=studio&tab=labs&lab=rectifier`);
  await reinforceTheme(page, "light");
  await page.waitForSelector(".lab-shell .se-waveform");
  expect(await svgAxisOverlapProblem(page, ".lab-shell .se-waveform")).toBeNull();
  await shot(page, "lab-rectifier-light.png");
});

test("lab-rectifier-dark", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await prepareTheme(page, "dark");
  await page.goto(`${BASE}/?view=studio&tab=labs&lab=rectifier`);
  await reinforceTheme(page, "dark");
  await page.waitForSelector(".lab-shell .se-waveform");
  await shot(page, "lab-rectifier-dark.png");
});

test("studio-circuit-series-rlc-after-simulate-light", async ({ page }) => {
  test.setTimeout(120_000);
  await page.setViewportSize({ width: 1440, height: 900 });
  await prepareTheme(page, "light");
  await page.goto(`${BASE}/?view=studio&tab=circuits`);
  await reinforceTheme(page, "light");
  await page.evaluate(() => localStorage.removeItem("arc-circuit-sandbox-v1"));
  await page.getByRole("button", { name: "Series RLC" }).click();
  expect(await circuitLayoutProblem(page)).toBeNull();
  await page.locator(".part-ref", { hasText: "V1" }).waitFor();
  await Promise.all([
    page.waitForResponse((r) => r.url().includes("/api/circuit-sandbox/simulate") && r.status() === 200),
    page.locator(".studio-circuit-app .cs-simulate-btn").click(),
  ]);
  await page.locator(".studio-circuit-results .se-waveform").waitFor({ timeout: 60000 });
  expect(await circuitLayoutProblem(page)).toBeNull();
  expect(await svgAxisOverlapProblem(page, ".studio-circuit-results .se-waveform")).toBeNull();
  expect(await circuitCanvasLuminance(page)).toBeGreaterThan(0.85);
  await shot(page, "studio-circuit-series-rlc-after-simulate-light.png");
});

test("studio-circuit-series-rlc-after-simulate-dark", async ({ page }) => {
  test.setTimeout(120_000);
  await page.setViewportSize({ width: 1440, height: 900 });
  await prepareTheme(page, "dark");
  await page.goto(`${BASE}/?view=studio&tab=circuits`);
  await reinforceTheme(page, "dark");
  await page.evaluate(() => localStorage.removeItem("arc-circuit-sandbox-v1"));
  await page.getByRole("button", { name: "Series RLC" }).click();
  await page.locator(".part-ref", { hasText: "V1" }).waitFor();
  await Promise.all([
    page.waitForResponse((r) => r.url().includes("/api/circuit-sandbox/simulate") && r.status() === 200),
    page.locator(".studio-circuit-app .cs-simulate-btn").click(),
  ]);
  await page.locator(".studio-circuit-results .se-waveform").waitFor({ timeout: 60000 });
  const lum = await circuitCanvasLuminance(page);
  expect(lum).toBeLessThan(0.2);
  expect(await circuitLayoutProblem(page)).toBeNull();
  await shot(page, "studio-circuit-series-rlc-after-simulate-dark.png");
  const lightHash = sha256(path.join(OUT, "studio-circuit-series-rlc-after-simulate-light.png"));
  const darkHash = sha256(path.join(OUT, "studio-circuit-series-rlc-after-simulate-dark.png"));
  expect(darkHash).not.toEqual(lightHash);
});

test("studio-control-after-simulate-light", async ({ page, request }) => {
  test.setTimeout(120_000);
  await page.setViewportSize({ width: 1440, height: 900 });
  await prepareTheme(page, "light");
  const res = await request.post(`${BASE}/api/control-studio/sessions`, {
    data: { title: "Spot control", golden: "pid_dc_motor" },
  });
  const { session_id } = await res.json();
  await page.goto(`${BASE}/?view=studio&session=${session_id}&tab=control`);
  await reinforceTheme(page, "light");
  await page.locator(".cs-simulate-btn").click();
  await page.locator(".studio-results-stage .studio-step-svg, .studio-results-stage img").first().waitFor({
    timeout: 120000,
  });
  await shot(page, "studio-control-after-simulate-light.png");
});

test("studio-control-after-simulate-dark", async ({ page, request }) => {
  test.setTimeout(180_000);
  await page.setViewportSize({ width: 1440, height: 900 });
  await prepareTheme(page, "dark");
  const res = await request.post(`${BASE}/api/control-studio/sessions`, {
    data: { title: "Spot control dark", golden: "pid_dc_motor" },
  });
  const { session_id } = await res.json();
  await page.goto(`${BASE}/?view=studio&session=${session_id}&tab=control`);
  await reinforceTheme(page, "dark");
  await page.locator(".cs-simulate-btn").click();
  await page.locator(".studio-results-stage .studio-step-svg, .studio-results-stage img").first().waitFor({
    timeout: 120000,
  });
  await shot(page, "studio-control-after-simulate-dark.png");
});

test("lab-idmt-light", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await prepareTheme(page, "light");
  await page.goto(`${BASE}/?view=studio&tab=labs&lab=idmt`);
  await reinforceTheme(page, "light");
  await page.waitForSelector(".lab-shell .se-waveform");
  expect(await svgAxisOverlapProblem(page, ".lab-shell .se-waveform")).toBeNull();
  await shot(page, "lab-idmt-light.png");
});

test("lab-idmt-dark", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await prepareTheme(page, "dark");
  await page.goto(`${BASE}/?view=studio&tab=labs&lab=idmt`);
  await reinforceTheme(page, "dark");
  await page.waitForSelector(".lab-shell .se-waveform");
  await shot(page, "lab-idmt-dark.png");
});