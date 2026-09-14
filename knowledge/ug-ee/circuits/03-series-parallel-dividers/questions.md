# Questions — Series-parallel reduction and dividers

Original pedagogical numbers.

## Q1

### Given

From a 24.0 V source, a 1.2 kΩ resistor is in series with the parallel of 3.6 kΩ and 1.8 kΩ.

### Find

Source current, voltage across the parallel pair, and current in the 1.8 kΩ.

### Solution

\( R_p = 3.6\parallel 1.8 = 1.2\,\mathrm{k}\Omega \). \( R_\mathrm{eq} = 1.2 + 1.2 = 2.4\,\mathrm{k}\Omega \). \( I_s = 24/2400 = 10.0\,\mathrm{mA} \). \( V_p = 10.0\,\mathrm{mA} \times 1.2\,\mathrm{k}\Omega = 12.0\,\mathrm{V} \). \( I_{1.8} = 12/1800 = 6.667\,\mathrm{mA} \). (The 3.6 kΩ takes 3.333 mA.)

### Answer

\( I_s = 10.0\,\mathrm{mA} \); \( V_p = 12.0\,\mathrm{V} \); \( I_{1.8} = 6.67\,\mathrm{mA} \).

## Q2

### Given

A two-resistor divider: \( R_1 \) from 9.0 V to output, \( R_2 \) from output to ground. Unloaded \( v_o = 2.5\,\mathrm{V} \).

### Find

Derive the required ratio \( R_1/R_2 \), and the loaded \( v_o \) if \( R_L = 3 R_2 \) is attached.

### Solution

Unloaded: \( 2.5 = 9 R_2/(R_1+R_2) \) ⇒ \( 2.5 R_1 + 2.5 R_2 = 9 R_2 \) ⇒ \( 2.5 R_1 = 6.5 R_2 \) ⇒ \( R_1/R_2 = 2.6 \). Loaded: bottom becomes \( R_2 \parallel 3R_2 = 0.75 R_2 \). \( v_o = 9 \cdot 0.75 R_2 / (2.6 R_2 + 0.75 R_2) = 6.75 / 3.35 = 2.015\,\mathrm{V} \).

### Answer

\( R_1/R_2 = 2.6 \); loaded \( v_o = 2.015\,\mathrm{V} \).

## Q3

### Given

Design a stiff unloaded divider from 12.0 V to 4.0 V using E12 resistors, standing current between 1 mA and 3 mA, no load specified yet.

### Find

A pair \( (R_1,R_2) \) from E12 (10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82 and decades) meeting the current window, and the actual open-circuit voltage.

### Solution

Need \( R_2/(R_1+R_2) = 1/3 \), so \( R_1 = 2 R_2 \). Standing current \( I = 12/(R_1+R_2) = 12/(3 R_2) \in [1,3]\,\mathrm{mA} \) ⇒ \( R_2 \in [1.333, 4]\,\mathrm{k}\Omega \). Pick \( R_2 = 1.8\,\mathrm{k}\Omega \), \( R_1 = 3.6\,\mathrm{k}\Omega \) (both E12). \( I = 12/5.4\mathrm{k} = 2.222\,\mathrm{mA} \). Actual ratio 1.8/5.4 = 1/3, \( v_o = 4.00\,\mathrm{V} \). Alternative 2.2 k and 4.7 k is not exactly 1:2.

### Answer

\( R_1 = 3.6\,\mathrm{k}\Omega \), \( R_2 = 1.8\,\mathrm{k}\Omega \); \( I = 2.22\,\mathrm{mA} \); \( v_o = 4.00\,\mathrm{V} \).

## Q4

### Given

A student reduces a Wheatstone bridge with arms 1.0 kΩ, 2.0 kΩ, 1.0 kΩ, 1.0 kΩ (one ratio pair unmatched) by calling the two 1.0 kΩ “in series” across the diagonal.

### Find

Explain why series-parallel reduction does not apply, and compute \( R_\mathrm{eq} \) seen by the source using a Y-Δ or mesh approach (source across one diagonal, detector open).

### Solution

The four arms form a cycle with both diagonals; the midpoints are not series because the bridge connection (even open detector) still ties two midpoints only through the fourth arm, not as a single shared current. Label: source on left-right, left-top 1 k, left-bottom 2 k, right-top 1 k, right-bottom 1 k, detector open so no fifth branch. Then left series of 1 k and 2 k is parallel to right series of 1 k and 1 k: this particular open-detector bridge IS series-parallel! \( R_\mathrm{left} = 3\,\mathrm{k}\Omega \), \( R_\mathrm{right} = 2\,\mathrm{k}\Omega \), \( R_\mathrm{eq} = 3\parallel 2 = 1.2\,\mathrm{k}\Omega \). The student's error was inventing a series path across the diagonal rather than two series strings in parallel. If the detector were a short, reduction would fail and mesh would be required.

### Answer

Open detector: two series strings in parallel, \( R_\mathrm{eq} = 1.2\,\mathrm{k}\Omega \). The “diagonal series” story is wrong; shorted detector would need mesh/Y-Δ.

## Q5

### Given

A 5.0 mA source feeds three parallel resistors 2.2 kΩ, 3.3 kΩ, and 6.8 kΩ.

### Find

Each branch current using current division.

### Solution

\( G_1 = 1/2200 = 4.545\times 10^{-4} \), \( G_2 = 3.030\times 10^{-4} \), \( G_3 = 1.471\times 10^{-4} \), \( \sum G = 9.046\times 10^{-4}\,\mathrm{S} \). \( i_k = 5.0\,\mathrm{mA} \cdot G_k/\sum G \): \( i_1 = 2.512\,\mathrm{mA} \), \( i_2 = 1.675\,\mathrm{mA} \), \( i_3 = 0.813\,\mathrm{mA} \). Check sum 5.000 mA. Equivalently \( R_p = 1/\sum G = 1.105\,\mathrm{k}\Omega \), \( V = 5.525\,\mathrm{V} \), then \( V/R_k \).

### Answer

2.51 mA, 1.68 mA, 0.813 mA in 2.2 k, 3.3 k, 6.8 k.
