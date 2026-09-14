# Questions — Network theorems

Original pedagogical numbers.

## Q1

### Given

A load \( R_L \) attaches to terminals a–b. Left of a: 36 V source in series with 2.7 kΩ to node n, then 4.7 kΩ from n to ground (b is ground). From n to a is 1.0 kΩ.

### Find

Thévenin equivalent at a–b and \( v_L \) if \( R_L = 3.3\,\mathrm{k}\Omega \).

### Solution

Open a–b: the 1.0 kΩ carries no current, so \( v_\mathrm{Th} = v_n = 36 \cdot 4.7/(2.7+4.7) = 169.2/7.4 = 22.86\,\mathrm{V} \). Deactivate 36 V (short): \( R_\mathrm{Th} = 1.0\mathrm{k} + (2.7\mathrm{k}\parallel 4.7\mathrm{k}) = 1.0 + 1.715 = 2.715\,\mathrm{k}\Omega \). Then \( v_L = 22.86 \cdot 3.3/(2.715+3.3) = 12.54\,\mathrm{V} \).

### Answer

\( v_\mathrm{Th} = 22.86\,\mathrm{V} \), \( R_\mathrm{Th} = 2.72\,\mathrm{k}\Omega \); \( v_L = 12.54\,\mathrm{V} \).

## Q2

### Given

Independent sources: 12 V and 3.0 mA in a linear resistive circuit. With only 12 V active, a marked voltage \( v = 4.2\,\mathrm{V} \). With only 3.0 mA active, the same \( v = -1.1\,\mathrm{V} \).

### Find

Derive \( v \) with both active, and the contribution if the current source is doubled.

### Solution

Superposition: \( v = 4.2 + (-1.1) = 3.1\,\mathrm{V} \). Doubling the current source doubles only its contribution: \( v = 4.2 + 2(-1.1) = 2.0\,\mathrm{V} \). Power cannot be scaled the same way.

### Answer

Both on: \( 3.1\,\mathrm{V} \). Doubled current source: \( 2.0\,\mathrm{V} \).

## Q3

### Given

A sensor Thévenin equivalent is \( 18.0\,\mathrm{mV} \) in series with \( 2.2\,\mathrm{k}\Omega \). Design \( R_L \) for maximum power, then a practical \( R_L \) that keeps efficiency \( P_L / P_\mathrm{source} \ge 0.80 \).

### Find

\( R_L \) for \( P_\mathrm{max} \), that \( P_\mathrm{max} \), and a value meeting the efficiency floor.

### Solution

Match: \( R_L = 2.2\,\mathrm{k}\Omega \), \( P_\mathrm{max} = (0.018)^2 / (4\times 2200) = 36.82\,\mathrm{nW} \). Efficiency \( \eta = R_L/(R_\mathrm{Th}+R_L) \). Need \( R_L/(2200+R_L) \ge 0.80 \) ⇒ \( R_L \ge 8.8\,\mathrm{k}\Omega \). Then \( P_L = (0.018)^2 \cdot 8800 / (11000)^2 = 13.11\,\mathrm{nW} \), less than \( P_\mathrm{max} \) but 80% of the power leaving the Thévenin voltage (which is \( v_\mathrm{Th}^2 R_L/(R_\mathrm{Th}+R_L)^2 \) over \( v_\mathrm{Th}^2 /(R_\mathrm{Th}+R_L) \) wait: source power is \( v_\mathrm{Th} i = v_\mathrm{Th}^2/(R_\mathrm{Th}+R_L) \), load power \( i^2 R_L \), so \( \eta = R_L/(R_\mathrm{Th}+R_L) \) yes.

### Answer

Match \( 2.2\,\mathrm{k}\Omega \), \( P_\mathrm{max} = 36.8\,\mathrm{nW} \); for \( \eta\ge 0.80 \) use \( R_L \ge 8.8\,\mathrm{k}\Omega \).

## Q4

### Given

Three parallel branches between a common pair of nodes: 5.0 V with 1.0 kΩ, 8.0 V with 2.2 kΩ, and 0 V (shorted source, i.e. only 3.3 kΩ).

### Find

The node-pair voltage by Millman, and explain the role of the third branch.

### Solution

\( v = \dfrac{5/1000 + 8/2200 + 0}{1/1000 + 1/2200 + 1/3300} = \dfrac{0.005 + 0.003636}{0.001 + 0.000455 + 0.000303} = 0.008636/0.001758 = 4.913\,\mathrm{V} \). The 3.3 kΩ contributes no numerator term but increases the denominator, pulling \( v \) down.

### Answer

\( v = 4.91\,\mathrm{V} \); the 3.3 kΩ only loads the node.

## Q5

### Given

A bilateral resistor grid has port 1 and port 2. A 2.0 mA source at port 1 produces 47 mV open at port 2. A student claims that 47 mV at port 1 would produce 2.0 mA at port 2.

### Find

Explain the correct reciprocity statement and the current at port 2 if 2.0 mA is instead applied at port 2 (port 1 open).

### Solution

Reciprocity equates transfer impedances, not a voltage at one port to a current at the other with swapped numbers. \( v_2 / i_1 = 47\,\mathrm{mV} / 2.0\,\mathrm{mA} = 23.5\,\Omega = v_1 / i_2 \) when the other port is open. Therefore 2.0 mA into port 2 yields \( v_1 = 47\,\mathrm{mV} \) open at port 1, not 2.0 mA out of port 1. The student's swapped voltage/current claim would require a transfer admittance identity with consistent port conditions, which they did not state.

### Answer

Open-circuit \( v_1 = 47\,\mathrm{mV} \) when 2.0 mA feeds port 2; the 47 mV → 2.0 mA claim is the wrong pair of port variables.
