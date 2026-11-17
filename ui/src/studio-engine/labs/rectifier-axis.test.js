import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { fixedYAxisFromSearch } from "./rectifier-axis.js";
import { waveformBounds } from "../renderers/waveformBounds.js";

describe("fixed y axis for the rectifier lab", () => {
  it("parses ?ymax= with ymin defaulting to 0", () => {
    assert.deepEqual(fixedYAxisFromSearch("?view=studio&lab=rectifier&ymax=600"), { min: 0, max: 600 });
    assert.deepEqual(fixedYAxisFromSearch("?ymin=-100&ymax=600"), { min: -100, max: 600 });
  });

  it("ignores absent or invalid values so the plot keeps autoscaling", () => {
    assert.equal(fixedYAxisFromSearch(""), null);
    assert.equal(fixedYAxisFromSearch("?ymax=abc"), null);
    assert.equal(fixedYAxisFromSearch("?ymax=0"), null);
    assert.equal(fixedYAxisFromSearch("?ymin=700&ymax=600"), null);
  });
});

describe("waveformBounds", () => {
  const series = [{ points: [[0, 10], [180, 110]] }];

  it("autoscales with padding when no fixed range is given", () => {
    const b = waveformBounds(series, { y: { scale: "linear" } });
    assert.equal(b.yMin, 0);
    assert.equal(b.yMax, 120);
  });

  it("holds the y axis exactly at a fixed range and leaves x untouched", () => {
    const auto = waveformBounds(series, {});
    const b = waveformBounds(series, { y: { min: 0, max: 600 } });
    assert.equal(b.yMin, 0);
    assert.equal(b.yMax, 600);
    assert.equal(b.xMin, auto.xMin);
    assert.equal(b.xMax, auto.xMax);
  });
});
