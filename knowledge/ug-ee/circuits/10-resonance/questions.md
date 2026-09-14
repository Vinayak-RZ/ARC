# Questions — Series and parallel resonance, Q and bandwidth

Original pedagogical numbers.

## Q1

### Given

Series RLC: L = 12.0 mH, C = 47.0 nF, R = 8.2 Ω, voltage source 2.00 V RMS.

### Find

f0, Q, bandwidth (Hz), and RMS voltage across L at resonance.

### Solution

\( \omega_0 = 1/\sqrt{0.012\times 4.7e-8} = 4.211\times 10^4 \), \( f_0 = 6.702\,\mathrm{kHz} \). \( Q = \omega_0 L / R = 4.211e4 \times 0.012 / 8.2 = 61.62 \). \( B_f = f_0/Q = 108.8\,\mathrm{Hz} \). \( I = V/R = 0.2439\,\mathrm{A} \). \( V_L = I \omega_0 L = 0.2439 \times 505.3 = 123.2\,\mathrm{V} \) RMS, also \( Q V_s = 123.2\,\mathrm{V} \).

### Answer

6.70 kHz; Q = 61.6; B = 109 Hz; VL = 123 V RMS.

## Q2

### Given

Parallel tank, R = 22 kΩ across L = 330 µH and C unknown. Want f0 = 455 kHz (IF-style, original values not from a paper).

### Find

Derive C and Q, and the half-power frequencies.

### Solution

\( C = 1/(\omega_0^2 L) \), \( \omega_0 = 2\pi 455e3 = 2.859e6 \). \( C = 1/(8.173e12 \times 3.30e-4) = 371\,\mathrm{pF} \). \( Q = R/(\omega_0 L) = 22000 / (2.859e6 \times 3.30e-4) = 23.32 \). \( B = 455e3/23.32 = 19.51\,\mathrm{kHz} \). \( f_{1,2} = 455 \pm 9.76 \) kHz.

### Answer

C = 371 pF; Q = 23.3; 445 kHz and 465 kHz.

## Q3

### Given

Design a series RLC to pass 10.0 kHz with B = 400 Hz and L = 2.2 mH, driven by a 1.0 V RMS source with negligible Rs.

### Find

C, R, and I at resonance.

### Solution

Q = f0/B = 10000/400 = 25. \( \omega_0 = 2\pi 10^4 \). \( C = 1/(\omega_0^2 L) = 1/(3.948e9 \times 0.0022) = 115.1\,\mathrm{nF} \). \( R = \omega_0 L / Q = 138.2/25 = 5.53\,\Omega \). \( I = 1.0/5.53 = 181\,\mathrm{mA} \) RMS.

### Answer

C = 115 nF, R = 5.53 Ω, I = 181 mA RMS.

## Q4

### Given

A student says a parallel RLC with a voltage source has maximum source current at resonance.

### Find

Explain the correct source-current behaviour.

### Solution

At parallel resonance |Z| is maximum, so for a voltage source I_s = V/|Z| is minimum, not maximum. The large currents are internal to L and C. Maximum source current would occur at resonance for a series RLC voltage-driven circuit. The student mixed the two prototypes.

### Answer

Voltage-driven parallel tank: source current is minimum at resonance; tank currents are large.

## Q5

### Given

Series RLC, Q = 8.0, f0 = 2.50 kHz. Do not use the high-Q split blindly.

### Find

Exact f1, f2 from \( \omega_{1,2} = \alpha \pm \sqrt{\alpha^2+\omega_0^2} \) wait: series half-power \( \omega = \sqrt{\omega_0^2 + \alpha^2} \pm \alpha \) with \( \alpha = \omega_0/(2Q) \).

### Solution

\( \omega_0 = 1.571\times 10^4 \). \( \alpha = \omega_0/(2Q) = 982\,\mathrm{rad/s} \) because B = ω0/Q = 2α. Exact \( \omega_{1,2} = \sqrt{\omega_0^2+\alpha^2}\pm \alpha = 1.574e4 \pm 982 \). \( \omega_2 = 1.672e4 \), \( \omega_1 = 1.476e4 \). \( f_2 = 2.661\,\mathrm{kHz} \), \( f_1 = 2.349\,\mathrm{kHz} \). Approximate ±B/2 = ±156 Hz about 2.50 kHz gives 2.344 and 2.656 kHz, close even at Q = 8. Geometric mean \( \sqrt{f_1 f_2} = 2.500\,\mathrm{kHz} \).

### Answer

Exact 2.349 kHz and 2.661 kHz (geometric mean 2.50 kHz).
