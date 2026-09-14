# Questions — KCL, KVL, Ohm's law, independent sources

Original pedagogical numbers.

## Q1

### Given

A single loop contains a \( 28.8\,\mathrm{V} \) independent voltage source, then \( 4.7\,\mathrm{k}\Omega \), then \( 2.2\,\mathrm{k}\Omega \), then \( 1.5\,\mathrm{k}\Omega \), returning to the source minus. All polarities follow the loop current out of the source plus.

### Find

Loop current, voltage across the \( 2.2\,\mathrm{k}\Omega \) resistor (plus where current enters), and power delivered by the source.

### Solution

\( R_\mathrm{tot} = 4.7 + 2.2 + 1.5 = 8.4\,\mathrm{k}\Omega \). \( I = 28.8 / 8400 = 3.429\times 10^{-3}\,\mathrm{A} = 3.429\,\mathrm{mA} \). \( V_{2.2} = 3.429\times 10^{-3}\times 2200 = 7.543\,\mathrm{V} \). Source delivers \( P = 28.8 \times 3.429\times 10^{-3} = 98.74\,\mathrm{mW} \) (current leaves source plus, so the source is active).

### Answer

\( I = 3.429\,\mathrm{mA} \); \( V_{2.2} = 7.54\,\mathrm{V} \); \( P_\mathrm{del} = 98.7\,\mathrm{mW} \).

## Q2

### Given

A node has four leaving currents: \( i_1 = 2.6\,\mathrm{A} \), \( i_2 = -0.80\,\mathrm{A} \), \( i_3 \) unknown, and \( i_4 = 0.45\,\mathrm{A} \). No charge storage.

### Find

Derive \( i_3 \) from KCL and interpret the sign.

### Solution

KCL: \( i_1 + i_2 + i_3 + i_4 = 0 \) ⇒ \( 2.6 - 0.80 + i_3 + 0.45 = 0 \) ⇒ \( i_3 = -2.25\,\mathrm{A} \). The minus means 2.25 A actually enters the node along that branch, opposite the assigned leaving arrow.

### Answer

\( i_3 = -2.25\,\mathrm{A} \) (2.25 A entering).

## Q3

### Given

Design a series string from a \( 15.0\,\mathrm{V} \) regulated source that produces \( 3.3\,\mathrm{V} \) across a load resistor that may be \( 1.8\,\mathrm{k}\Omega \) or removed (open). You may use one series dropper resistor. Open-load voltage must not exceed \( 5.0\,\mathrm{V} \).

### Find

Explain why a single series resistor cannot meet both the 3.3 V loaded condition and the 5.0 V open limit, and propose a two-resistor divider that does.

### Solution

With only a series dropper \( R_s \) and load \( R_L = 1.8\,\mathrm{k}\Omega \), \( 3.3 = 15 \cdot R_L/(R_s+R_L) \) ⇒ \( R_s = 6.382\,\mathrm{k}\Omega \). With load removed, the open voltage is the full 15 V, which violates 5.0 V. A divider \( R_1 \) from source to output and \( R_2 \) from output to ground is required. Open-load: \( v = 15 R_2/(R_1+R_2) \le 5 \) ⇒ \( R_2/R_1 \le 1/2 \). Pick \( R_2 = 2.2\,\mathrm{k}\Omega \), \( R_1 = 4.7\,\mathrm{k}\Omega \): open \( v = 15\cdot 2.2/6.9 = 4.783\,\mathrm{V} \). Loaded: \( R_2\parallel 1.8\mathrm{k} = 0.990\,\mathrm{k}\Omega \), \( v = 15\cdot 0.990/(4.7+0.990) = 2.61\,\mathrm{V} \), below 3.3 V. Increase \( R_2 \) toward the open-voltage cap: \( R_1 = 3.3\,\mathrm{k}\Omega \), \( R_2 = 1.65\,\mathrm{k}\Omega \) gives open 5.0 V exactly; loaded \( R_2\parallel 1.8\mathrm{k} = 0.860\,\mathrm{k}\Omega \), \( v = 15\cdot 0.860/4.16 = 3.10\,\mathrm{V} \). A stiff divider (smaller \( R_1,R_2 \)) approaches 3.3 V loaded while keeping open ≤ 5 V; e.g. \( R_1 = 820\,\Omega \), \( R_2 = 410\,\Omega \) (open 5.0 V), loaded \( R_p = 334\,\Omega \), \( v = 15\cdot 334/1154 = 4.34\,\mathrm{V} \) which overshoots 3.3 V. So a linear divider cannot hit 3.3 V loaded and 5 V open unless the load is much larger than \( R_2 \). Honest design: use a 3.3 V regulator, not two resistors, if both specs are hard.

### Answer

Single series resistor fails on open-load (15 V). A linear divider cannot simultaneously hold 3.3 V into 1.8 kΩ and ≤ 5 V open unless \( R_2 \ll 1.8\,\mathrm{k}\Omega \), which then violates the open cap or the loaded voltage; use a regulator for a hard spec.

## Q4

### Given

An independent 6.0 mA current source feeds a parallel combination of \( 3.3\,\mathrm{k}\Omega \) and \( 6.8\,\mathrm{k}\Omega \). A student writes \( V = IR = (6.0\,\mathrm{mA})(3.3\,\mathrm{k}\Omega) \).

### Find

Explain the error and compute the correct node voltage and branch currents.

### Solution

The 6.0 mA does not all flow through 3.3 kΩ; it splits. \( R_p = 3.3\parallel 6.8 = 2.228\,\mathrm{k}\Omega \). \( V = 6.0\times 10^{-3}\times 2228 = 13.37\,\mathrm{V} \). Then \( I_{3.3} = 13.37/3300 = 4.051\,\mathrm{mA} \), \( I_{6.8} = 13.37/6800 = 1.966\,\mathrm{mA} \), sum 6.017 mA (rounding). The student's 19.8 V would require the 6.8 kΩ to be absent.

### Answer

Error: used one branch resistance with the total current. \( V = 13.37\,\mathrm{V} \); 4.05 mA and 1.97 mA.

## Q5

### Given

Loop: 12.0 V source, 220 Ω, then a 15.0 V source opposing the first, then 180 Ω, back to the first source minus.

### Find

The current (out of the 12 V plus) and the power in each source (delivered or absorbed).

### Solution

KVL clockwise from 12 V plus: \( 12 - 220I - 15 - 180I = 0 \) ⇒ \( -3 = 400 I \) ⇒ \( I = -7.5\,\mathrm{mA} \). Physical current is 7.5 mA out of the 15 V plus. Power: 12 V source with assigned \( I \) leaving its plus: \( P_{12} = 12 I = -90\,\mathrm{mW} \) (absorbs 90 mW). 15 V source: traversing, current assigned \( I \) enters its plus, so PSC power \( 15 I = -112.5\,\mathrm{mW} \) wait — assigned I is clockwise; 15 V plus is met going clockwise so clockwise current leaves the 15 V plus? Layout: 12V plus → 220 → 15V plus? Problem says 15 V opposing, so 12V plus → R220 → 15V minus → 15V plus → R180 → 12V minus. Then clockwise I leaves 12V plus and enters 15V plus. PSC on 15 V: current into plus, \( p = 15 I \). \( I = -7.5\,\mathrm{mA} \), \( p_{15} = 15(-0.0075) = -0.1125\,\mathrm{W} \) meaning 15 V delivers 112.5 mW. 12 V: current assigned leaving plus equals I, source-delivered power \( 12 I = -90\,\mathrm{mW} \) meaning 12 V absorbs 90 mW. Resistors absorb \( (0.0075)^2 (400) = 22.5\,\mathrm{mW} \). Check: 112.5 delivered = 90 + 22.5 absorbed.

### Answer

\( I = -7.5\,\mathrm{mA} \) (7.5 mA counterclockwise); 12 V absorbs 90 mW; 15 V delivers 112.5 mW.
