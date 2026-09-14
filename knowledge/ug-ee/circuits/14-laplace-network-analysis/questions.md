# Questions — Laplace-domain networks and initial conditions

Original pedagogical numbers.

## Q1

### Given

Series R = 2 kΩ, C = 5 µF, VC(0−) = 8.0 V. For t>0 a 12 V DC source is switched in series, aiding the capacitor polarity as a charging source (source plus into R into capacitor plus).

### Find

VC(s) and vC(t).

### Solution

s-domain: 12/s in series with 2000, 1/(sC) = 2×10^5/s, and V0/s = 8/s with polarity opposing the source if V0 is already on the plus of C (the IC source is in series with C in the same polarity as vC). Loop current I(s) = (12/s − 8/s) / (2000 + 2e5/s) = (4/s) / ( (2000s + 2e5)/s ) = 4/(2000s+2e5) = 0.002/(s+100). Voltage on C: I(s)×1/(sC) + 8/s = 0.002/(s+100) × 2e5/s + 8/s = 400/(s(s+100)) + 8/s. 400/(s(s+100)) = 4/s − 4/(s+100). So VC = 12/s − 4/(s+100). vC(t) = 12 − 4 e^{-100 t} V. Check: 0+ is 8 V, ∞ is 12 V, τ = RC = 10 ms.

### Answer

\( V_C(s) = 12/s - 4/(s+100) \); \( v_C(t) = 12 - 4e^{-100t}\,\mathrm{V} \).

## Q2

### Given

Inductor 0.25 H, I(0−) = 0.40 A, switched at t=0 onto 50 Ω alone (source-free).

### Find

Derive I(s) using the L I0 voltage source and i(t).

### Solution

Series: voltage source L I0 = 0.10 V (impulse-free constant in s is 0.10/s? No: the IC source for the inductor is L I0, a constant voltage in the s-domain equal to the number L I0, i.e. 0.10 volts as a step-free algebraic source, modeled as 0.10 (not /s) because L di/dt ↔ sL I − L I0, the L I0 term is a constant voltage source of value L I0. Standard: series voltage source of value L i(0−), transform L I0 (a constant, Laplace L I0 / s? CONFLICT.

Standard textbook: inductor with initial current: impedance sL in series with a voltage source L I0 (the Laplace of an impulse? No).

From L{di/dt} = sI − i(0−), so V = L s I − L i(0−). The term L i(0−) is a constant in s, i.e. a voltage source whose transform is L I0 (not divided by s). That constant in s-domain is an impulse in time, which is wrong...

Careful: A constant in the s-domain F(s) = K means f(t) = K δ(t). That cannot be right for the IC source.

The correct model: V(s) = sL I(s) − L i(0−). The quantity L i(0−) is subtracted in the s-domain algebraic equation; it has the same units as V(s), so it is an s-domain voltage of value L I0 (a real number). Inverse of that bookkeeping is not a time-domain constant voltage. The s-domain circuit is algebraic, not a time circuit. So I(s) = L I0 / (sL + R) = 0.10 / (0.25s + 50) = 0.40 / (s + 200). i(t) = 0.40 e^{-200 t} A. Good.

### Answer

\( I(s) = 0.40/(s+200) \); \( i(t) = 0.40 e^{-200t}\,\mathrm{A} \).

## Q3

### Given

Design RC so H(s) = V_C/V_in = 1/(τs+1) has τ = 2.5 ms, C = 0.22 µF, zero IC, step input 5 V.

### Find

R and vC(t).

### Solution

τ = RC = 2.5e-3 ⇒ R = 2.5e-3 / 0.22e-6 = 11.36 kΩ. Vin = 5/s, VC = 5/(s(τs+1)) = 5(1/s − τ/(τs+1))/1 wait: 5/(s(τs+1)) = 5(1/s − 1/(s+1/τ)). vC = 5(1 − e^{-t/τ}) V = 5(1−e^{-400 t}) V.

### Answer

R = 11.4 kΩ; \( v_C(t) = 5(1-e^{-400t})\,\mathrm{V} \).

## Q4

### Given

A student applies the final-value theorem to I(s) = 3/(s^2 + 9) (undamped).

### Find

Explain why FVT fails and the true t→∞ behaviour.

### Solution

sI(s) = 3s/(s^2+9) has poles at ±j3 on the jω axis. FVT requires all poles of sF in the open left half-plane. The inverse is a cosine that never settles. lim s→0 sI(s) = 0, which is the average, not a final value.

### Answer

FVT does not apply; i(t) oscillates as (1/3) sin(3t) A (if I(s)=3/(s^2+9)).

## Q5

### Given

Parallel C = 1 µF with R = 10 kΩ, VC(0−) = 2 V, no independent source for t>0.

### Find

Use the parallel current source C V0 and find vC(t).

### Solution

C V0 = 2 µA? C V0 = 1e-6 × 2 = 2e-6 A as an s-domain current source of value C V0 (a number). Actually the parallel IC model is a current source of C v(0−), algebraic in s. Then V(s) = (C V0) × (R || 1/sC) wait easier: V(s) = v(0−)/(s + 1/RC) = 2/(s+100). vC = 2 e^{-100 t} V. τ = 10 k × 1 µF = 10 ms.

### Answer

\( v_C(t) = 2 e^{-100t}\,\mathrm{V} \).
