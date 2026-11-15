import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { partCount, splitEdgeAt } from "../slots/canvas/graph.js";

describe("splitEdgeAt", () => {
  it("replaces one wire with a junction and two wires", () => {
    const nodes = [
      { id: "a", data: { kind: "resistor" } },
      { id: "b", data: { kind: "resistor" } },
    ];
    const edges = [{ id: "e1", source: "a", target: "b", sourceHandle: "n2", targetHandle: "n1" }];
    const next = splitEdgeAt(nodes, edges, "e1", { x: 40, y: 20 });
    assert.equal(next.nodes.length, 3);
    assert.equal(next.edges.length, 2);
    assert.equal(next.nodes[2].data.kind, "junction");
    assert.equal(next.edges[0].target, next.nodes[2].id);
    assert.equal(next.edges[1].source, next.nodes[2].id);
    assert.equal(partCount(next.nodes), 2);
  });
});
