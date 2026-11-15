import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { niceTicks, logTicks } from "./ticks.js";

describe("ticks", () => {
  it("niceTicks covers range", () => {
    const t = niceTicks(0, 10, 5);
    assert.ok(t[0] <= 0 + 1e-9);
    assert.ok(t[t.length - 1] >= 10 - 1e-6);
  });
  it("logTicks decades", () => {
    assert.deepEqual(logTicks(1, 1000), [1, 10, 100, 1000]);
  });
});
