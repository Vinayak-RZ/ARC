import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { converterMetrics } from "./converter.js";

describe("converter", () => {
  it("buck", () => {
    const r = converterMetrics({ topology: "buck", vin: 12, d: 0.5, l: 100e-6, c: 47e-6, fs: 100e3, r: 5 });
    assert.equal(r.Vo, 6);
  });
  it("boost", () => {
    const r = converterMetrics({ topology: "boost", vin: 12, d: 0.5, l: 100e-6, c: 47e-6, fs: 100e3, r: 10 });
    assert.equal(r.Vo, 24);
  });
  it("buck-boost", () => {
    const r = converterMetrics({ topology: "buck-boost", vin: 12, d: 0.6, l: 100e-6, c: 47e-6, fs: 100e3, r: 10 });
    assert.ok(Math.abs(r.Vo - -18) < 1e-9, String(r.Vo));
  });
});
