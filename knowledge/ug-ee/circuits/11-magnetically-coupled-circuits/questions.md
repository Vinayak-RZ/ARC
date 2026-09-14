# Questions — Mutual inductance and coupled coils

Original pedagogical numbers.

## Q1

### Given

L1 = 4.0 mH, L2 = 9.0 mH, k = 0.60. Currents both enter dotted terminals. i1 = 0.20 A DC, i2 = 0.10 A DC at an instant after a slow ramp (treat as instantaneous values for energy).

### Find

M and stored energy.

### Solution

\( M = 0.60\sqrt{4e-3\times 9e-3} = 0.60\times 6.0e-3 = 3.60\,\mathrm{mH} \). \( w = 0.5(0.004)(0.04) + 0.5(0.009)(0.01) + 0.0036(0.20)(0.10) = 80e-6 + 45e-6 + 72e-6 = 197\,\mu\mathrm{J} \).

### Answer

M = 3.60 mH; w = 197 µJ.

## Q2

### Given

Two coils in series: aiding inductance 28 mH, opposing 12 mH.

### Find

Derive L1+L2 and M.

### Solution

Aiding L1+L2+2M = 28, opposing L1+L2−2M = 12. Add: 2(L1+L2) = 40 ⇒ L1+L2 = 20 mH. Subtract: 4M = 16 ⇒ M = 4.0 mH.

### Answer

L1+L2 = 20 mH; M = 4.0 mH.

## Q3

### Given

Design coupling so that series opposing inductance is at least 2.0 mH given L1 = L2 = 8.0 mH.

### Find

Maximum allowed k.

### Solution

Lopp = 16 − 2M ≥ 2 ⇒ 2M ≤ 14 ⇒ M ≤ 7.0 mH. M = k×8 ⇒ k ≤ 0.875. A tighter coupling would make Lopp even smaller (even negative if k>1, forbidden).

### Answer

k ≤ 0.875.

## Q4

### Given

A student writes both mutual terms with plus signs while i1 enters a dot and i2 leaves a dot, PSC on both coils.

### Find

Explain the correct signs in the v = L di/dt ± M di_other/dt equations.

### Solution

Standard: plus M when both currents enter dotted ends. Here one enters and one leaves, so mutual terms are negative: v1 = L1 di1/dt − M di2/dt, v2 = L2 di2/dt − M di1/dt. The student's plus signs would describe the opposite dot placement.

### Answer

Mutual signs must both be minus for that current/dot combination.

## Q5

### Given

Phasors, ω = 1000 rad/s, L1 = 0.20 H, L2 = 0.05 H, M = 0.08 H, both currents into dots. I1 = 0.50∠0° A, coil 2 shorted so V2 = 0.

### Find

I2 and V1.

### Solution

V2 = jω L2 I2 + jω M I1 = 0 ⇒ I2 = −(M/L2) I1 = −(0.08/0.05)(0.50) = −0.80 A = 0.80∠180°. V1 = jω L1 I1 + jω M I2 = j1000[0.20(0.50) + 0.08(−0.80)] = j1000[0.100 − 0.064] = j36.0 V.

### Answer

I2 = 0.80∠180° A; V1 = 36∠90° V.
