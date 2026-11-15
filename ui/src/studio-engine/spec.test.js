import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { validateDiagram, SCHEMA, MAX_POINTS } from "./spec.js";

describe("validateDiagram", () => {
  it("accepts minimal schematic", () => {
    const errs = validateDiagram({
      schema: SCHEMA,
      title: "t",
      panels: [
        {
          kind: "schematic",
          grid: 40,
          components: [{ id: "r1", type: "resistor", at: [0, 0], rot: 0 }],
          wires: [],
        },
      ],
    });
    assert.deepEqual(errs, []);
  });

  it("rejects point overflow", () => {
    const points = Array.from({ length: MAX_POINTS + 1 }, (_, i) => [i, 0]);
    const errs = validateDiagram({
      schema: SCHEMA,
      panels: [{ kind: "waveform", series: [{ id: "s", points, style: "primary" }] }],
    });
    assert.ok(errs.some((e) => e.includes("exceeds")));
  });
});
