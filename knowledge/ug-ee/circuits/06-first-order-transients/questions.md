# Questions — RC and RL first-order transients

Original pedagogical numbers.

## Q1

### Given

A 12.0 V source charges a 4.7 µF capacitor through 22 kΩ. The capacitor is initially 0 V. Switch closes at \( t = 0 \).

### Find

\( v_C(t) \), \( i_C(0^+) \), and the time when \( v_C = 8.0\,\mathrm{V} \).

### Solution

\( \tau = 22\times 10^3 \times 4.7\times 10^{-6} = 0.1034\,\mathrm{s} \). \( v_C(t) = 12(1-e^{-t/0.1034}) \). \( i_C(0^+) = 12/22000 = 0.545\,\mathrm{mA} \). \( 8 = 12(1-e^{-t/\tau}) \) ⇒ \( e^{-t/\tau} = 1/3 \) ⇒ \( t = 0.1034 \ln 3 = 0.1136\,\mathrm{s} \).

### Answer

\( v_C = 12(1-e^{-t/0.1034})\,\mathrm{V} \); \( i(0^+) = 0.545\,\mathrm{mA} \); \( t = 114\,\mathrm{ms} \) at 8 V.

## Q2

### Given

Inductor 0.80 H carries 0.25 A for \( t < 0 \) (steady). At \( t = 0 \) the source is switched out, leaving the inductor in a loop with 160 Ω only.

### Find

Derive \( i_L(t) \) and the energy dumped in the resistor.

### Solution

\( i_L(0^+) = 0.25\,\mathrm{A} \), \( i(\infty) = 0 \), \( \tau = L/R = 0.80/160 = 5.0\,\mathrm{ms} \). \( i_L(t) = 0.25 e^{-t/0.005}\,\mathrm{A} \). Stored energy \( \frac12 L i^2 = 0.5\times 0.80\times 0.0625 = 0.025\,\mathrm{J} \), all dissipated in 160 Ω as \( t\to\infty \).

### Answer

\( i_L(t) = 0.25 e^{-200 t}\,\mathrm{A} \); \( 0.025\,\mathrm{J} \) in the resistor.

## Q3

### Given

Design an RC blanking interval: after a 5.0 V step, a comparator should wait until the capacitor reaches 3.2 V at \( t = 40\,\mathrm{ms} \). Source is 5.0 V, \( C = 100\,\mathrm{nF} \), uncharged initially.

### Find

Required \( R \).

### Solution

\( 3.2 = 5(1-e^{-0.040/\tau}) \) ⇒ \( 0.64 = 1-e^{-0.040/\tau} \) ⇒ \( e^{-0.040/\tau} = 0.36 \) ⇒ \( 0.040/\tau = \ln(1/0.36) = 1.021 \) ⇒ \( \tau = 0.03918\,\mathrm{s} \). \( R = \tau/C = 0.03918 / 10^{-7} = 392\,\mathrm{k}\Omega \). Use 390 kΩ E12 and accept a slight time shift.

### Answer

\( R = 392\,\mathrm{k}\Omega \) (390 kΩ practical).

## Q4

### Given

A student writes \( v_C(t) = 10 e^{-t/RC} \) for a capacitor being charged from 0 toward 10 V.

### Find

Explain the error and write the correct function.

### Solution

That expression is a discharge from 10 V toward 0, the source-free response. Charging from 0 to 10 V is \( 10(1-e^{-t/RC}) \). At \( t=0^+ \) the student's formula is 10 V, contradicting an initially uncharged capacitor. The missing particular solution is the DC final value.

### Answer

Error: natural-only decay. Correct: \( v_C(t) = 10(1-e^{-t/RC})\,\mathrm{V} \).

## Q5

### Given

For \( t<0 \), a 24 V source, 6.0 kΩ, and 2.0 µF in series, capacitor voltage has reached steady state. At \( t=0 \) the source is shorted out (replaced by a wire), leaving 6.0 kΩ across the capacitor. A 3.0 kΩ was always in parallel with the capacitor.

### Find

\( v_C(0^+) \), \( \tau \) for \( t>0 \), and \( v_C(t) \).

### Solution

\( t<0 \) DC: capacitor open, so the 3.0 kΩ and 6.0 kΩ divide 24 V: \( v_C(0^-) = 24 \cdot 3/(6+3) = 8.0\,\mathrm{V} = v_C(0^+) \). For \( t>0 \) the 24 V is shorted, so both 6 kΩ and 3 kΩ remain across C: \( R_\mathrm{Th} = 6\parallel 3 = 2.0\,\mathrm{k}\Omega \). \( \tau = 2000 \times 2.0\times 10^{-6} = 4.0\,\mathrm{ms} \). \( v(\infty) = 0 \). \( v_C(t) = 8.0 e^{-t/0.004}\,\mathrm{V} \).

### Answer

\( v_C(0^+) = 8.0\,\mathrm{V} \); \( \tau = 4.0\,\mathrm{ms} \); \( v_C(t) = 8 e^{-250 t}\,\mathrm{V} \).
