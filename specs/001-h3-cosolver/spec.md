# Feature Specification: H3 UG EE co-solver

> **Historical.** Spec Kit artifact for the H1 execution graph. Live contract: [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md), [`docs/UI.md`](../../docs/UI.md), [`docs/PRD.md`](../../docs/PRD.md).

**Feature Branch**: `cursor/ee-product-execution-9e9d`  
**Created**: 2026-09-10  
**Status**: Specified (D0)  
**Input**: Ship Electrical Engineer end-to-end: named workflows, localhost UI, stdio MCP, checked numbers or exact token `unchecked`.

## User Scenarios & Testing

### User Story 1 — Solve a circuit homework (Priority: P1)

A UG student runs a named circuit workflow from the CLI, gets a working plus
answer, and sees either a tool-checked number or the exact token `unchecked`.

**Why this priority**: Core co-solver promise.

**Independent Test**: Run `solve-circuit-problem` on a licence-clean gold item;
`summary.json` contains `recipe_id` and either a checked value or `unchecked`.

**Acceptance Scenarios**:

1. **Given** a named circuit recipe and a numeric homework prompt, **When** the student runs it, **Then** the run directory contains `summary.json` with `recipe_id` and never presents an unverified number as simulation.
2. **Given** no verifier can check the number, **When** the run finishes, **Then** both the answer and `summary.json` contain the exact token `unchecked`.

### User Story 2 — See the work in a local UI (Priority: P1)

The student opens a persistent local workspace, inspects a run, and confirms a
photo-derived netlist without the product simulating it.

**Why this priority**: Persistent UI is a critical surface.

**Independent Test**: UI serves only on `127.0.0.1`; confirm action does not start SPICE.

**Acceptance Scenarios**:

1. **Given** the UI command, **When** the workspace starts, **Then** it binds `127.0.0.1` and stays up across the session.
2. **Given** a photo stub draft, **When** the student confirms topology, **Then** the product stops (no silent simulate).

### User Story 3 — Hosts run the same recipes (Priority: P2)

Cursor/Claude/OpenAI list and run workflows through stdio MCP without waiting
on a human in the MCP call.

**Why this priority**: H3 portable core.

**Independent Test**: `run_workflow` returns fail-closed JSON with `ui_url` or a CLI hint when a human would be required.

**Acceptance Scenarios**:

1. **Given** stdio MCP, **When** a client lists workflows, **Then** catalog ids from the public catalog appear.
2. **Given** a run that would need a human interrupt, **When** MCP `run_workflow` is called, **Then** it does not block; it fails closed.

### Edge Cases

- Unmatched prompt uses `unmatched-cosolver` and never auto-simulates.
- Classifier top-1 and top-2 within 0.15 asks the student (CLI/UI), not MCP wait.
- BYO PDF or memory file cannot flip gates or `unchecked`.
- Compose-from-parts rejects more than 16 nodes or 24 edges.
- Local LLM missing: skip-if-missing; deterministic nodes still run.

## Requirements

### Functional Requirements

- **FR-001**: Students MUST be able to run named catalog workflows from a local CLI without a coding host.
- **FR-002**: Unverified numbers MUST use the exact token `unchecked` in the answer and the run summary.
- **FR-003**: A persistent local workspace MUST bind only to loopback.
- **FR-004**: Photo and control-diagram stubs MUST confirm in the UI and MUST NOT simulate without that confirm.
- **FR-005**: Stdio MCP MUST expose list and run tools and MUST NOT wait on humans.
- **FR-006**: Every curriculum pack MUST have solve and explain recipes or an honest cannot-do row.
- **FR-007**: Eval gold items MUST name a recipe id; injection MUST NOT disable `unchecked` or gates.
- **FR-008**: Memory files MUST be explicit, capped, and untrusted.
- **FR-009**: Gates MUST apply most-restrictive wins, at most two human interrupts per root run.

### Key Entities

- **Workflow recipe**: catalog id, pack, YAML DAG of registered activity nodes.
- **Run**: isolated directory, `summary.json`, artifacts, optional child runs.
- **Gold item**: licence-clean prompt + expect, including injection cases.

## Success Criteria

### Measurable Outcomes

- **SC-001**: A student can obtain a checked number or exact `unchecked` for a named circuit task in one local command.
- **SC-002**: The local workspace is reachable only on loopback for the session.
- **SC-003**: MCP run never blocks a host on a human prompt.
- **SC-004**: Injection gold cannot make the product omit `unchecked` or skip gates.
- **SC-005**: Each of the ten UG packs has a solve recipe and an explain recipe, or a documented cannot-do row.

## Assumptions

- Owner start/execute of the product graph counts as PRD acceptance for this scope.
- OSS verifiers are first-class; MATLAB is optional.
- Workflow ids remain renamable until the first CLI ships, then freeze in git.
