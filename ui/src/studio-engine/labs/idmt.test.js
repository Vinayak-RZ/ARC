import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { idmtTime } from "./idmt.js";

describe("idmt", () => {
  it("standard PSM10 TMS1", () => {
    const t = idmtTime({ i_fault_a: 1000, ct_primary_a: 100, plug_setting: 1, tms: 1, curve: "standard" });
    assert.ok(Math.abs(t - 2.971) < 0.01, String(t));
  });
});
