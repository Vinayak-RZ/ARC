import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { alphaFromPhi, findPhaseMargin } from "./lead.js";

describe("lead", () => {
  it("alpha at 40 deg", () => {
    const a = alphaFromPhi(40);
    assert.ok(Math.abs(a - 4.599) < 0.02, String(a));
  });

  it("PM unc for K=10 a=1 b=0 near 17.96", () => {
    const { pm } = findPhaseMargin(10, 1, 0);
    assert.ok(pm != null);
    assert.ok(Math.abs(pm - 17.96) < 0.5, String(pm));
  });
});
