# Implementation plan — Kernel harden (live pointer)

> **Live graph:** [`LOOP_GRAPH.md`](LOOP_GRAPH.md)  
> **Node plans:** [`plans/kernel-harden-loops/`](plans/kernel-harden-loops/)  
> **Gate 0:** [`docs/planning/GATE_0_KERNEL_HARDEN.md`](docs/planning/GATE_0_KERNEL_HARDEN.md)  
> **Product overlay:** [`docs/planning/PRODUCT_KERNEL_HARDEN.md`](docs/planning/PRODUCT_KERNEL_HARDEN.md)  
> **ADR:** [`docs/planning/ADR_TRACE_JSONL.md`](docs/planning/ADR_TRACE_JSONL.md)

Supersedes the previous live Simulink-agents pointer. Archived graph: [`docs/planning/LOOP_GRAPH_SIMULINK_AGENTS.md`](docs/planning/LOOP_GRAPH_SIMULINK_AGENTS.md).

## §0 Metadata

| Field | Value |
|-------|-------|
| Profile | project + graph-of-loops |
| Branch | `cursor/ee-kernel-harden-trace-8db3` |
| Commit budget | 40 (cap 42) |
| PRIORITY | QUALITY > CONSISTENCY > SPEED > AVAILABILITY > COST |

## §1 Objective

Stdlib JSONL tracing → ≥100 host-heavy UG EE trials → Unagent + Improveness critique → minimal kernel patches → UI surface → harden → docs-out case study.

## §18 / §19

Execute [`LOOP_GRAPH.md`](LOOP_GRAPH.md). Wave 0 is plans/docs only. §19 wins over linear protocol.
