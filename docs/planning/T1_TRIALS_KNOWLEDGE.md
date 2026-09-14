# T1 — knowledge corpus trials

**Date:** 2026-09-14  
Queue from `plans/knowledge-loops/T1.md`.

| # | Trial | Pass means | Result | Evidence |
|---|-------|------------|--------|----------|
| 1 | Circuits Thévenin numerical recompute | Independent calc matches `questions.md` Q1 | pass | \(v_\mathrm{Th}=22.86\,\mathrm{V}\), \(R_\mathrm{Th}=2.715\,\mathrm{k}\Omega\), \(v_L=12.54\,\mathrm{V}\) vs [`knowledge/ug-ee/circuits/05-network-theorems/questions.md`](../../knowledge/ug-ee/circuits/05-network-theorems/questions.md) |
| 2 | Signals discrete convolution | Sequence matches Q2 | pass | \(y[n]=\{4,7,10,-3\}\) vs [`knowledge/ug-ee/signals/03-convolution/questions.md`](../../knowledge/ug-ee/signals/03-convolution/questions.md) |
| 3 | Control Routh \(K\) range | \(0<K<6\) for \(s^3+3s^2+2s+K\) | pass | [`knowledge/ug-ee/control/04-routh-hurwitz/questions.md`](../../knowledge/ug-ee/control/04-routh-hurwitz/questions.md) Q2 |
| 4 | Machines transformer OC | \(R_c=381\,\Omega\), \(X_m=74.1\,\Omega\), pf \(0.191\) | pass | [`knowledge/ug-ee/machines/03-transformer-tests-three-phase/questions.md`](../../knowledge/ug-ee/machines/03-transformer-tests-three-phase/questions.md) Q1 |
| 5 | PE buck chopper + elective headings | \(0.42\times 96=40.32\,\mathrm{V}\); microprocessors notes has Concepts/Equations/Methods/Mistakes | pass | [`knowledge/ug-ee/power-electronics/04-dc-dc-choppers/questions.md`](../../knowledge/ug-ee/power-electronics/04-dc-dc-choppers/questions.md) Q1; [`knowledge/ug-ee/electives/microprocessors/01-8085-architecture-timing/notes.md`](../../knowledge/ug-ee/electives/microprocessors/01-8085-architecture-timing/notes.md) 1843 words |

Independent Python used for rows 1, 4, 5 (arithmetic). Row 2 polynomial multiply. Row 3 Routh \(s^1\) entry \((6-K)/3\).
