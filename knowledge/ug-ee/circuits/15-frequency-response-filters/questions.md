# Questions — Network frequency response and passive filters

Original pedagogical numbers.

## Q1

### Given

RC low-pass: R = 4.7 kΩ from input to output node, C = 22 nF from output to ground. Source Rs = 0.

### Find

fc, |H| at 2 kHz, and phase at fc.

### Solution

ωc = 1/RC = 1/(4700×22e-9) = 9671 rad/s, fc = 1.539 kHz. At 2 kHz, ω/ωc = 1.300, |H| = 1/√(1+1.69) = 0.610. Phase at fc is −45°.

### Answer

fc = 1.54 kHz; |H(2 kHz)| = 0.610; φ(fc) = −45°.

## Q2

### Given

Series RLC, output on R, L = 1.5 mH, C = 6.8 nF, R = 12 Ω.

### Find

Derive f0, Q, and B in hertz.

### Solution

f0 = 1/(2π√(LC)) = 1/(2π√(1.5e-3×6.8e-9)) = 49.85 kHz. Q = ω0 L / R = 2π×49850×0.0015 / 12 = 39.15. B = f0/Q = 1.273 kHz.

### Answer

f0 = 49.9 kHz; Q = 39.2; B = 1.27 kHz.

## Q3

### Given

Design a first-order high-pass with fc = 80 Hz for a line-level block of DC, C = 1.0 µF, unloaded.

### Find

R to ground after the series C, and |H| at 20 Hz.

### Solution

ωc = 2π×80 = 503. Series C, R to ground: ωc = 1/RC ⇒ R = 1/(ωc C) = 1.99 kΩ. Use 2.0 kΩ. At 20 Hz, ω/ωc = 0.25, |H| = (ω/ωc)/√(1+(ω/ωc)^2) = 0.25/√1.0625 = 0.243 (−12.3 dB).

### Answer

R = 1.99 kΩ; |H(20 Hz)| = 0.243.

## Q4

### Given

Two identical RC low-passes cascaded without a buffer, each R = 10 kΩ, C = 10 nF. A student uses [1/(1+jωRC)]^2.

### Find

Explain the loading error and the correct H(s).

### Solution

The second stage's 10 kΩ loads the first capacitor. Nodal: H(s) = 1 / ( (sRC)^2 + 3 sRC + 1 ), not 1/(sRC+1)^2. The 3 comes from extra current into the second R. Isolated cascade would need a buffer. Numerical: RC = 100 µs, ωc isolated would be 1.59 kHz, but the loaded pair has different poles.

### Answer

Loading makes H = 1/(s²τ² + 3sτ + 1), τ=RC; the squared first-order form is wrong without isolation.

## Q5

### Given

Unloaded RC low-pass, |Vin| = 2.0 V peak. At a frequency where |H| = 0.50, a student says the output is −6 dB and therefore 1.0 V peak, then also writes 20 log(0.5) = −3 dB.

### Find

Correct dB and peak voltage.

### Solution

20 log10(0.50) = −6.02 dB. The −3 dB point is |H| = 0.707, not 0.5. Vout peak = 1.0 V is correct for |H|=0.5; the dB number is −6 dB, not −3 dB.

### Answer

−6.0 dB; 1.0 V peak. (−3 dB is half-power, not half-voltage.)
