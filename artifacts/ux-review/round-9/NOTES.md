# Round 9 captures

Code commit and `preflight.json` `git_sha` are identical (`2297a66`), `git_dirty_lines` 0. Preflight now also probes Finite crossover (K = 10): status `settled_off_target`, final value 0.9091, settling time 0.355 s, overshoot 0.0%, e_ss 9.1%.

## Self-score against round 8 gating items

| Item | Self-score | Proof |
|---|---|---|
| R9-A captions never truncated, inspector open or closed | pass | Copy shortened ("No −180° crossing in 0.001 to 100,000 rad/s.", "Phase above −180° over ..."), clamp raised to 3 lines. `studio-r8.spec.ts` truncation tests (light, dark) and a new vertical-overflow check (`scrollHeight > clientHeight`) in `studio-r5.spec.ts` pass. Captures: `studio-block-selected-after-simulate-light.png`, `studio-step-unsettled-{light,dark}.png`, `studio-step-extended-{light,dark}.png` |
| R9-B settling against final value | pass | `_step_metrics`: y_ss is the tail mean, band 2% of abs(y_ss), settling time, overshoot and peak against y_ss, e_ss reported separately, all returned for on-target and off-target. Chart: setpoint line and dotted final-value line are separate, e_ss labelled, band centred on y_ss, no band or marker when unsettled, overshoot dot with percent. Header text now reads "Settling time 0.36 s · Final value 0.909 · 9.1% below setpoint" (units appended when the plant has them). Unit tests: K = 10 (theory ln 50 / 11 within 1%), K = 39 and K = 60 consistent, under-damped overshoot vs the textbook exp(-pi zeta / sqrt(1 - zeta^2)), unsettled has no band. `studio-r8.spec.ts` metric and chart tests pass |
| R9-C dark captures start clean | pass | `cmdk-open-dark.png` is on the Problems list, `sidebar-collapsed-dark.png` is on the Checked problem, each after a fresh page load and a focus blur |
| Student-style titles | pass | Sessions are "Lab 4 · DC motor PID", "HW 3 · Open-loop gain", "HW 3 · Unity feedback, K = 10". No "Control Studio", "Low gain" or "Finite crossover" in Recent |
| Settle wording (round 7 fix 6) | pass | see R9-B |
| Overshoot dot | pass | `studio-step-settled-{light,dark}.png` (1.6% at the peak) |
| Expander label and default-open | pass | label and aria-label flip "Show working" / "Hide working"; step 2 is open by default (`problem-r9.spec.ts`); `problem-work-dark.png`, `problem-work-tab-light.png` |

Known small gaps: the "1.6%" peak label sits close to the setpoint line; the settling-time summary is drawn inside the plot, with a visually hidden `role="status"` copy for screen readers; round 7 fixes 8 to 11 (drawer skeleton, palette fade, Problems list, Gallery and Library) are still not done.
