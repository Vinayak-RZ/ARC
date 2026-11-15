import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { cAdd, cMul, cDiv, polyval } from "./complex.js";

describe("complex", () => {
  it("arith", () => {
    assert.deepEqual(cAdd([1, 2], [3, 4]), [4, 6]);
    assert.deepEqual(cMul([1, 1], [1, -1]), [2, 0]);
    const d = cDiv([1, 0], [0, 1]);
    assert.ok(Math.abs(d[0]) < 1e-12 && Math.abs(d[1] + 1) < 1e-12);
  });
  it("polyval s+1 at j", () => {
    const v = polyval([1, 1], [0, 1]);
    assert.ok(Math.abs(v[0] - 1) < 1e-12 && Math.abs(v[1] - 1) < 1e-12);
  });
});
