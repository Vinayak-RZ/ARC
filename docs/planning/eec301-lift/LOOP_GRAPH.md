# LOOP_GRAPH — EEC-301 → Arc system lift (rev 2)

```mermaid
flowchart TB
  G0[GATE_0 system-first] --> W0[W0 contract docs]
  W0 --> L[Lab pack parallel]
  W0 --> W1[W1 SMIB engines]
  L -->|golden JSON| W1
  W1 --> W2[W2 SMIB skills/knowledge]
  W2 --> W3[W3 AGC system]
  L --> W3
  W3 --> W4[W4 ED system]
  L --> W4
  W0 --> W5[W5 diagrams]
  W4 --> W6[W6 host wiring]
  W5 --> W6
  W6 --> W7[W7 A/B proof]
  W7 --> W8[W8 CI + ≥30 attest]
  W8 --> MERGE[Landing PR only if commits ≥30]
```

## Wave exit gates

| Wave | Exit |
|------|------|
| W0 | GATE_0, LOOP_GRAPH, COMMIT_FLOOR, trap catalog on branch |
| W1 | SMIB engines + golden evals using lab truth |
| W2 | swing skill + T1–T3 knowledge |
| W3 | AGC engine/skill/knowledge/evals + parity notes |
| W4 | ED engine/skill/knowledge/evals + T10 validation |
| W5 | diagram research + ui-diagrams + T8 |
| W6 | host cards + T9 + lab→kernel doc |
| W7 | ablation harness + A/B docs + adversarial tests |
| W8 | CI green + commit-count attestation ≥30 |

## Loops

1. **Numeric:** lab solve ↔ PDF/hand check  
2. **Kernel:** failure → skill/knowledge/engine/eval  
3. **Diagram:** Claude patterns → skill → visual gate  
4. **Proof:** trap prompt → bare fail → Arc pass → document  
5. **Commit floor:** after each wave, `rev-list` vs plan; before merge, hard ≥30

## Stop

User stop; demand for licensed Simulink in CI; pressure to fabricate numbers; attempt to squash below floor → escalate, do not merge.
