import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { orthoPath, pinPosition, routeWire } from "./route.js";

describe("route", () => {
  it("ortho horizontal", () => {
    assert.equal(orthoPath(0, 0, 10, 0), "M 0 0 H 10");
  });
  it("pinPosition resistor", () => {
    const p = pinPosition({ type: "resistor", at: [2, 1], rot: 0 }, "a", 40);
    assert.deepEqual(p, { x: 40, y: 40 });
  });
  it("routeWire", () => {
    const d = routeWire({ x: 0, y: 0 }, { x: 10, y: 10 });
    assert.match(d, /^M /);
  });
});
