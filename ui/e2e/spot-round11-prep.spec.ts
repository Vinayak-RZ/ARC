import path from "node:path";
import { fileURLToPath } from "node:url";
import { test } from "@playwright/test";
import { circuitLayoutProblem, svgAxisOverlapProblem, setTheme } from "./layout-helpers.js";
import { expect } from "@playwright/test";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(__dirname, "../../artifacts/ux-review/round-11-prep");

const BASE = process.env.ARC_UI_URL || "http://127.0.0.1:8765";

test.describe.configure({ mode: "serial" });

async function shot(page: import("@playwright/test").Page, name: string) {
  await page.screenshot({ path: path.join(OUT, name), fullPage: false });
}

test("lab-rectifier-light", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await setTheme(page, "light");
  await page.goto(`${BASE}/?view=studio&tab=labs&lab=rectifier`);
  await page.waitForSelector(".lab-shell .se-waveform");
  expect(await svgAxisOverlapProblem(page, ".lab-shell .se-waveform")).toBeNull();
  await shot(page, "lab-rectifier-light.png");
});

test("lab-rectifier-dark", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await setTheme(page, "dark");
  await page.goto(`${BASE}/?view=studio&tab=labs&lab=rectifier`);
  await page.waitForSelector(".lab-shell .se-waveform");
  await shot(page, "lab-rectifier-dark.png");
});

test("studio-circuit-series-rlc-after-simulate-light", async ({ page }) => {
  test.setTimeout(120_000);
  await page.setViewportSize({ width: 1440, height: 900 });
  await setTheme(page, "light");
  await page.goto(`${BASE}/?view=studio&tab=circuits`);
  await page.evaluate(() => localStorage.removeItem("arc-circuit-sandbox-v1"));
  await page.getByRole("button", { name: "Series RLC" }).click();
  await page.locator(".part-ref", { hasText: "V1" }).waitFor();
  await Promise.all([
    page.waitForResponse((r) => r.url().includes("/api/circuit-sandbox/simulate") && r.status() === 200),
    page.locator(".studio-circuit-app .cs-simulate-btn").click(),
  ]);
  await page.locator(".studio-circuit-results .se-waveform").waitFor({ timeout: 60000 });
  expect(await circuitLayoutProblem(page)).toBeNull();
  expect(await svgAxisOverlapProblem(page, ".studio-circuit-results .se-waveform")).toBeNull();
  await shot(page, "studio-circuit-series-rlc-after-simulate-light.png");
});

test("studio-circuit-series-rlc-after-simulate-dark", async ({ page }) => {
  test.setTimeout(120_000);
  await page.setViewportSize({ width: 1440, height: 900 });
  await setTheme(page, "dark");
  await page.goto(`${BASE}/?view=studio&tab=circuits`);
  await page.evaluate(() => localStorage.removeItem("arc-circuit-sandbox-v1"));
  await page.getByRole("button", { name: "Series RLC" }).click();
  await page.locator(".part-ref", { hasText: "V1" }).waitFor();
  await Promise.all([
    page.waitForResponse((r) => r.url().includes("/api/circuit-sandbox/simulate") && r.status() === 200),
    page.locator(".studio-circuit-app .cs-simulate-btn").click(),
  ]);
  await page.locator(".studio-circuit-results .se-waveform").waitFor({ timeout: 60000 });
  expect(await circuitLayoutProblem(page)).toBeNull();
  await shot(page, "studio-circuit-series-rlc-after-simulate-dark.png");
});

test("studio-control-after-simulate-light", async ({ page, request }) => {
  test.setTimeout(120_000);
  await page.setViewportSize({ width: 1440, height: 900 });
  await setTheme(page, "light");
  const res = await request.post(`${BASE}/api/control-studio/sessions`, {
    data: { title: "Spot control", golden: "pid_dc_motor" },
  });
  const { session_id } = await res.json();
  await page.goto(`${BASE}/?view=studio&session=${session_id}&tab=control`);
  await page.locator(".cs-simulate-btn").click();
  await page.locator(".studio-results-stage .studio-step-svg, .studio-results-stage img").first().waitFor({
    timeout: 120000,
  });
  await shot(page, "studio-control-after-simulate-light.png");
});

test("studio-control-after-simulate-dark", async ({ page, request }) => {
  test.setTimeout(120_000);
  await page.setViewportSize({ width: 1440, height: 900 });
  await setTheme(page, "dark");
  const res = await request.post(`${BASE}/api/control-studio/sessions`, {
    data: { title: "Spot control dark", golden: "pid_dc_motor" },
  });
  const { session_id } = await res.json();
  await page.goto(`${BASE}/?view=studio&session=${session_id}&tab=control`);
  await page.locator(".cs-simulate-btn").click();
  await page.locator(".studio-results-stage .studio-step-svg, .studio-results-stage img").first().waitFor({
    timeout: 120000,
  });
  await shot(page, "studio-control-after-simulate-dark.png");
});

test("lab-idmt-light", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await setTheme(page, "light");
  await page.goto(`${BASE}/?view=studio&tab=labs&lab=idmt`);
  await page.waitForSelector(".lab-shell .se-waveform");
  expect(await svgAxisOverlapProblem(page, ".lab-shell .se-waveform")).toBeNull();
  await shot(page, "lab-idmt-light.png");
});

test("lab-idmt-dark", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await setTheme(page, "dark");
  await page.goto(`${BASE}/?view=studio&tab=labs&lab=idmt`);
  await page.waitForSelector(".lab-shell .se-waveform");
  await shot(page, "lab-idmt-dark.png");
});