import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { voClosedForm } from "./rectifier.js";

describe("rectifier closed form", () => {
  it("full1 continuous alpha 30", () => {
    const Vo = voClosedForm({ topology: "full1", v_rms: 230, alpha_deg: 30, io_a: 0, ls_h: 0 });
    assert.ok(Math.abs(Vo - 179.33) < 0.5, String(Vo));
  });
  it("full3 alpha 45", () => {
    const Vo = voClosedForm({ topology: "full3", v_rms: 415, alpha_deg: 45, io_a: 0, ls_h: 0 });
    assert.ok(Math.abs(Vo - 396.3) < 0.5, String(Vo));
  });
  it("full3 with overlap", () => {
    const Vo = voClosedForm({
      topology: "full3",
      v_rms: 415,
      alpha_deg: 45,
      io_a: 20,
      ls_h: 0.002,
      f_hz: 50,
    });
    assert.ok(Math.abs(Vo - 384.3) < 1.0, String(Vo));
  });
});
