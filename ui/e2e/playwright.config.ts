import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: ".",
  testMatch: /studio-(layout|wire-selection|r5|r6|r7)\.spec\.ts/,
  retries: 0,
  workers: 1,
  timeout: 120_000,
  use: {
    headless: true,
    viewport: { width: 1280, height: 800 },
  },
});
