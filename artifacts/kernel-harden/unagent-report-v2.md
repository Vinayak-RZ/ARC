# Determinism Advisor report

> simulation != production; canary is confirmatory

| node | kind | class | action | n | p_mode | p_mode_lo | schema_ok | fail | tier | replay |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|
| check | deterministic_tool | deterministic | ABSTAIN | 1 | 1.00 | 0.21 | 1.00 | 1.00 | observational | diverged |
| confirm | deterministic_tool | deterministic | ABSTAIN | 1 | 1.00 | 0.21 | 1.00 | 1.00 | observational | diverged |
| ctrl | deterministic_tool | deterministic | ABSTAIN | 1 | 1.00 | 0.21 | 1.00 | 1.00 | observational | diverged |
| detect | deterministic_tool | deterministic | ABSTAIN | 1 | 1.00 | 0.21 | 1.00 | 1.00 | observational | diverged |
| draft | deterministic_tool | deterministic | ABSTAIN | 1 | 1.00 | 0.21 | 1.00 | 1.00 | observational | diverged |
| explain | deterministic_tool | deterministic | ABSTAIN | 1 | 1.00 | 0.21 | 1.00 | 1.00 | observational | diverged |
| label | deterministic_tool | deterministic | ABSTAIN | 1 | 1.00 | 0.21 | 1.00 | 1.00 | observational | diverged |
| load | deterministic_tool | deterministic | ABSTAIN | 1 | 1.00 | 0.21 | 1.00 | 0.00 | observational | diverged |
| retrieve | deterministic_tool | deterministic | ABSTAIN | 1 | 1.00 | 0.21 | 1.00 | 1.00 | observational | diverged |
| run.end | workflow | composite | ABSTAIN | 1 | 1.00 | 0.21 | 1.00 | 0.00 | observational | diverged |
| run.start | workflow | composite | ABSTAIN | 1 | 1.00 | 0.21 | 1.00 | 0.00 | cassette | tail_stable |
| solve | deterministic_tool | deterministic | ABSTAIN | 1 | 1.00 | 0.21 | 1.00 | 1.00 | observational | diverged |
| spice | deterministic_tool | deterministic | ABSTAIN | 1 | 1.00 | 0.21 | 1.00 | 1.00 | observational | diverged |
| summary | deterministic_tool | deterministic | ABSTAIN | 1 | 1.00 | 0.21 | 1.00 | 1.00 | observational | diverged |

## Reasons

### check — ABSTAIN
- DET node failure_rate=1.00 >= 0.30; FlipToNondet needs L1 evidence a policy swap recovers the tail

### confirm — ABSTAIN
- DET node failure_rate=1.00 >= 0.30; FlipToNondet needs L1 evidence a policy swap recovers the tail

### ctrl — ABSTAIN
- DET node failure_rate=1.00 >= 0.30; FlipToNondet needs L1 evidence a policy swap recovers the tail

### detect — ABSTAIN
- DET node failure_rate=1.00 >= 0.30; FlipToNondet needs L1 evidence a policy swap recovers the tail

### draft — ABSTAIN
- DET node failure_rate=1.00 >= 0.30; FlipToNondet needs L1 evidence a policy swap recovers the tail

### explain — ABSTAIN
- DET node failure_rate=1.00 >= 0.30; FlipToNondet needs L1 evidence a policy swap recovers the tail

### label — ABSTAIN
- DET node failure_rate=1.00 >= 0.30; FlipToNondet needs L1 evidence a policy swap recovers the tail

### load — ABSTAIN
- no rule fired with a CI that excludes the threshold

### retrieve — ABSTAIN
- DET node failure_rate=1.00 >= 0.30; FlipToNondet needs L1 evidence a policy swap recovers the tail

### run.end — ABSTAIN
- no rule fired with a CI that excludes the threshold

### run.start — ABSTAIN
- no rule fired with a CI that excludes the threshold

### solve — ABSTAIN
- DET node failure_rate=1.00 >= 0.30; FlipToNondet needs L1 evidence a policy swap recovers the tail

### spice — ABSTAIN
- DET node failure_rate=1.00 >= 0.30; FlipToNondet needs L1 evidence a policy swap recovers the tail

### summary — ABSTAIN
- DET node failure_rate=1.00 >= 0.30; FlipToNondet needs L1 evidence a policy swap recovers the tail

## Canary

- simulation != production; canary is confirmatory
