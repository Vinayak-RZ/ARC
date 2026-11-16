import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { answerPartsFromRow, buildAnswerRows, runHeadline } from "./formatAnswer.js";

describe("answerPartsFromRow", () => {
  it("formats Vo with volts", () => {
    const p = answerPartsFromRow("Vo", 396.3);
    assert.equal(p.name, "Vo");
    assert.equal(p.value, "396.30");
    assert.equal(p.unit, "V");
    assert.equal(p.display, "Vo = 396.30 V");
  });

  it("formats relay time with seconds", () => {
    const p = answerPartsFromRow("Relay time t", 2.971, 3);
    assert.equal(p.unit, "s");
    assert.equal(p.display, "Relay time t = 2.971 s");
  });
});

describe("runHeadline", () => {
  it("returns single-line headline for rectifier", () => {
    assert.strictEqual(
      runHeadline({ recipe_id: "rectifier-3ph-study", value: 396.3, title: "Rectifier" }, {}),
      "Vo = 396.30 V",
    );
  });
});

describe("buildAnswerRows", () => {
  it("uses recipe-specific quantity labels", () => {
    const { rows } = buildAnswerRows(
      { recipe_id: "rectifier-3ph-study", value: 396.29, unchecked: false },
      { title: "Three-phase rectifier" },
    );
    assert.equal(rows.length, 1);
    assert.equal(rows[0].name, "Vo");
    assert.equal(rows[0].unit, "V");
    assert.match(rows[0].display, /^Vo = /);
  });

  it("omits numeric row when lab needs review", () => {
    const { rows } = buildAnswerRows(
      { recipe_id: "simulate-circuit", value: 11.963, unchecked: false },
      { lab_verify: { needs_review: true, derived: 11.963, simulated: 11.63 } },
    );
    assert.equal(rows.length, 0);
  });

  it("formats IDMT headline", () => {
    const { rows } = buildAnswerRows(
      { recipe_id: "idmt-relay-study", value: 2.971, unchecked: false },
      { title: "IDMT relay time" },
    );
    assert.equal(rows[0].name, "Relay time t");
    assert.equal(rows[0].unit, "s");
  });
});