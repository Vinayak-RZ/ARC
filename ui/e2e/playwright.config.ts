import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: ".",
  testMatch:
    /(studio-(layout|wire-selection|step-results|resize-wires|r5|r6|r7|r8|r9)|circuit-sandbox|spot-round11-prep|problem-r9|navigation|learn|labs|home-packs|collab-lab|collab-rlc-revision|independent-full-collab-loop)\.spec\.ts/,
  retries: 0,
  workers: 1,
  timeout: 120_000,
  use: {
    headless: true,
    viewport: { width: 1280, height: 800 },
  },
});
