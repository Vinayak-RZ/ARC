# BJT regions, biasing, and hybrid-π small-signal model

The bipolar junction transistor is still the device UG analog courses use to teach regions of operation, DC bias, and linearised amplifiers, even though CMOS dominates VLSI. A BJT is two pn junctions sharing a thin base. This unit treats NPN as the default (PNP is the polarity reverse), the four operating regions, the four common bias networks, the three amplifier configurations, and the hybrid-π model used for mid-band gain.

## Concepts

An NPN transistor has emitter (heavily doped n), base (thin p), and collector (lightly doped n). Forward-biasing the base–emitter junction injects electrons into the base; most are swept into the reverse-biased collector–base junction. Collector current is then \(\beta\) times the base current, or \(\alpha\) times the emitter current, with \(\alpha=\beta/(\beta+1)\) and \(I_E=I_C+I_B\). Typical discrete \(\beta\) is 50–300 and is poorly controlled; analog design therefore uses bias networks that make \(I_C\) depend on resistors and \(V_{BE}\), not on \(\beta\).

Regions of operation (NPN, voltages from the named terminal to the other):

- Cut-off: both junctions reverse (or BE not sufficiently forward). \(I_C\approx 0\). Used as an open switch.
- Forward-active (linear): BE forward, CB reverse. \(I_C=\beta I_B\) (simple model) and \(v_{CE}\) is free to sit between saturation and \(V_{CC}\). Used for amplification.
- Saturation: both junctions forward. \(v_{CE}\approx 0.2\,\mathrm{V}\) (silicon switching). Used as a closed switch. The forced \(\beta\) \(I_C/I_B\) is less than the active \(\beta\).
- Reverse-active: BE reverse, BC forward. \(\beta_R\) is small. Rarely used except in some TTL input structures and as a warning not to swap collector and emitter.

The large-signal Ebers–Moll view is two diodes plus current-controlled sources; UG courses mostly need the piecewise model: \(V_{BE}\approx 0.7\,\mathrm{V}\) in active and saturation, \(V_{CE,sat}\approx 0.2\,\mathrm{V}\), and \(I_C=\beta I_B\) only in forward-active.

Biasing sets a quiet operating point (Q-point) \(I_C,V_{CE}\) in the middle of the load line so that AC swings neither cut off nor saturate. The DC load line for a simple collector resistor \(R_C\) is \(V_{CE}=V_{CC}-I_C R_C\) (or \(V_{CC}-I_C(R_C+R_E)\) if an emitter resistor is present). Intersection with the device characteristic at the chosen \(I_B\) is the Q-point.

Four standard DC bias networks:

1. Fixed base bias: \(R_B\) from \(V_{CC}\) to base. \(I_B=(V_{CC}-V_{BE})/R_B\), \(I_C=\beta I_B\). Simple, hopelessly \(\beta\)-sensitive, used only in switching or throwaway examples.
2. Collector-to-base feedback bias: \(R_B\) from collector to base. Provides a little DC negative feedback: if \(I_C\) rises, \(V_C\) falls, \(I_B\) falls. Better than (1), still not the exam favourite.
3. Emitter bias with split supplies, or more commonly a single supply with \(R_E\): \(I_E\approx (V_B-V_{BE})/R_E\) if \(V_B\) is stiff. The key formula of analog courses.
4. Voltage-divider bias: \(R_1,R_2\) from \(V_{CC}\) to ground set \(V_{Th}=V_{CC}R_2/(R_1+R_2)\) and \(R_{Th}=R_1\parallel R_2\). Then \(I_E=(V_{Th}-V_{BE})/(R_E+R_{Th}/(\beta+1))\). If \(R_{Th}\ll(\beta+1)R_E\), \(\beta\) drops out. Design rule of thumb: divider current \(\approx 10 I_B\) (or 10 % of \(I_E\)).

Thermal stability: \(V_{BE}\) falls \(\approx 2\,\mathrm{mV/^\circ C}\), \(\beta\) rises with temperature, and \(I_{CBO}\) doubles every \(\approx 10^\circ\mathrm{C}\). Emitter degeneration \(R_E\) and voltage-divider bias reduce the sensitivity \(S=\partial I_C/\partial I_{CBO}\) and \(S_\beta\). Thermal runaway in power BJTs is the positive feedback of leakage and dissipation; a heatsink and emitter ballast resistors are the hardware answer.

AC coupling: coupling capacitors block DC so stages can be biased independently. Bypass capacitors short \(R_E\) (or part of it) at mid-band to raise gain while keeping DC degeneration. At mid-band those capacitors are treated as shorts.

Three configurations (signal ground on one terminal):

- Common-emitter (CE): input at base, output at collector, emitter AC-grounded. Voltage gain large and inverting, \(A_v\approx -g_m R_L'\), input resistance \(\approx r_\pi\parallel R_{bias}\), output resistance \(\approx R_C\parallel r_o\). The workhorse voltage amplifier.
- Common-collector (CC, emitter follower): input at base, output at emitter. \(A_v\approx 1\), high \(R_{in}\), low \(R_{out}\approx 1/g_m\). Buffer.
- Common-base (CB): input at emitter, output at collector. \(A_v\) noninverting and of order \(g_m R_L'\), low \(R_{in}\approx 1/g_m\), good high-frequency behaviour (no Miller on \(C_\mu\) at the input in the same way). Used in cascode and RF.

The hybrid-π model (forward-active, small signals) is a linear circuit valid for increments about the Q-point: \(g_m=I_C/V_T\), \(r_\pi=\beta/g_m=(\beta V_T)/I_C\), \(r_e=\alpha/g_m\approx 1/g_m\), and optionally \(r_o=|V_A|/I_C\) (Early effect). \(C_\pi\) and \(C_\mu\) matter for bandwidth (Miller theorem on CE). The older h-parameter model (\(h_{ie},h_{fe},h_{re},h_{oe}\)) is the same physics in two-port clothing; \(h_{fe}=\beta\), \(h_{ie}=r_\pi\).

Miller's theorem: a feedback impedance \(Z\) from output to input of an inverting gain \(A_v\) looks like \(Z/(1-A_v)\) at the input. \(C_\mu\) therefore appears as \(C_\mu(1+|A_v|)\) at the CE input and dominates the high-frequency pole. Cascode (CE+CB) kills Miller by presenting a low-resistance CB input at the CE collector.

Switching: to saturate, provide \(I_B>I_C/\beta_{\min}\) with a forced \(\beta\) of 10 often used in digital drive. Storage time in saturation is why Schottky-clamped transistors and ECL exist; analog amplifiers stay in forward-active on purpose.

## Equations

Current relations (forward-active):

\[
I_C=\beta I_B=\alpha I_E,\quad \alpha=\frac{\beta}{\beta+1},\quad I_E=I_C+I_B.
\]

Transconductance and hybrid-π resistances at the Q-point:

\[
g_m=\frac{I_C}{V_T},\quad r_\pi=\frac{\beta}{g_m},\quad r_e=\frac{V_T}{I_E},\quad r_o=\frac{|V_A|}{I_C}.
\]

Voltage-divider bias exact:

\[
V_{Th}=V_{CC}\frac{R_2}{R_1+R_2},\quad R_{Th}=R_1\parallel R_2,
\]

\[
I_E=\frac{V_{Th}-V_{BE}}{R_E+R_{Th}/(\beta+1)},\quad V_{CE}=V_{CC}-I_C(R_C+R_E)\ \ (I_C=\alpha I_E).
\]

CE mid-band voltage gain, \(R_E\) fully bypassed, \(R_L'=R_C\parallel R_L\parallel r_o\):

\[
A_v=-g_m R_L'.
\]

With unbypassed \(R_E\):

\[
A_v\approx -\frac{R_L'}{r_e+R_E}\approx -\frac{R_L'}{R_E}\quad (g_m R_E\gg 1).
\]

CE input resistance looking into the base:

\[
R_{ib}=r_\pi+(\beta+1)R_E
\]

(with \(R_E\) the unbypassed part).

CC voltage gain and output resistance:

\[
A_v=\frac{(\beta+1)(R_E\parallel R_L)}{r_\pi+(\beta+1)(R_E\parallel R_L)}\approx 1,\qquad R_{out}\approx\frac{r_\pi+R_{sig}'}{\beta+1}\parallel R_E.
\]

Stability factors (qualitative UG forms): \(S_{I_{CBO}}\approx (1+\beta)(1+R_B/R_E)/(1+\beta+R_B/R_E)\) for emitter-resistor bias; smaller \(R_B/R_E\) is more stable.

## Methods

1. DC first, capacitors open. Draw the bias network, find \(V_B\) or \(I_B\), then \(I_E\) or \(I_C\), then \(V_{CE}\). Compare \(V_{CE}\) with \(0.2\,\mathrm{V}\) and \(V_{CC}\) to confirm forward-active.
2. Never use \(\beta\) as if it were a 1 % resistor unless the problem gives a number and the topology is fixed-bias. In divider bias, keep the \(R_{Th}/(\beta+1)\) term unless the problem says to neglect base current.
3. For AC, capacitors short, DC sources AC-ground. Replace the BJT by hybrid-π. Compute \(g_m\) from the DC \(I_C\) you already found. Combine collector resistors into \(R_L'\).
4. Identify the configuration by which terminal is AC-grounded, not by which resistor is physically present. An emitter resistor that is fully bypassed still leaves a CE amplifier.
5. Saturation check for switching: compute \(I_{C,sat}=(V_{CC}-V_{CE,sat})/(R_C+R_E)\) and required \(I_B=I_{C,sat}/\beta\). If the actual \(I_B\) is larger, the device is in saturation and \(I_C\) is *not* \(\beta I_B\).
6. PNP: redraw with \(V_{EE}\) or negative rails, or mentally reverse all polarities. \(V_{EB}=0.7\,\mathrm{V}\), currents out of the collector in the arrow convention.
7. If Early voltage is given, include \(r_o\) in parallel with \(R_C\); if not given, omit it. Do not invent \(V_A\).

Design sketch: want \(I_C=2\,\mathrm{mA}\), \(V_{CC}=12\,\mathrm{V}\), \(V_{CE}=5\,\mathrm{V}\), \(R_E=1\,\mathrm{k}\Omega\). Then \(V_E=2\,\mathrm{V}\), \(V_B=2.7\,\mathrm{V}\), \(R_C=(12-5-2)/0.002=2.5\,\mathrm{k}\Omega\). Choose divider current 0.2 mA, so \(R_2=2.7/0.0002=13.5\,\mathrm{k}\Omega\), \(R_1=(12-2.7)/0.0002=46.5\,\mathrm{k}\Omega\). Then check the exact \(I_E\) formula with \(\beta=100\).

## Mistakes

- Using \(I_C=\beta I_B\) in saturation. Once both junctions are forward, collector current is set by the external resistors, not by \(\beta\).
- Forgetting \(V_{BE}\) in the emitter-bias KVL, or using 0.7 V on a problem that specifies 0.6 V or 0.65 V.
- Treating the voltage divider as unloaded when \(R_{Th}\) is comparable to \((\beta+1)R_E\). The base current pulls \(V_B\) down.
- AC analysis with coupling capacitors left open, or DC analysis with them shorted.
- Computing \(g_m=I_C/V_{BE}\) instead of \(I_C/V_T\). \(V_{BE}\) is a DC drop; \(V_T\) is the thermal voltage.
- CE gain sign: it is negative. A reported \(+g_m R_C\) is the magnitude, not the gain.
- Bypassing: if only part of \(R_E\) is bypassed, the unbypassed slice remains in the AC gain formula.
- Swapping CE and CC: seeing an emitter resistor and calling the circuit an emitter follower when the output is taken at the collector.
- \(\alpha\) versus \(\beta\): \(I_C=\alpha I_E\) is slightly less than \(I_E\); writing \(I_C=I_E\) is a 1 % error that some marking schemes still punish if \(\beta=50\).
- PNP current arrows: conventional current enters the emitter of a PNP. Mixing this with NPN KCL produces a sign error in \(I_E=I_C+I_B\).
- Early effect ignored when the question gives \(V_A\), or inserted when it does not.
- Miller: adding \(C_\mu\) only once at the input without the \((1+|A_v|)\) factor underestimates the CE dominant pole by an order of magnitude at high gain.

A laboratory measurement that belongs on this unit, not on a later instrumentation sheet, is the tracing of output characteristics on a curve tracer or a stepped-\(I_B\) DC sweep. The family of \(I_C\) vs \(V_{CE}\) curves at constant \(I_B\) is almost flat in the forward-active region; the slight upward slope is the Early effect. The crowding of curves toward \(V_{CE}=0\) is saturation. The spacing of the curves is \(\beta\), and it is visibly not constant: \(\beta\) peaks at an intermediate current and falls at both low current (recombination in the emitter-base space-charge layer) and high current (high-level injection, Kirk effect). That is why a bias point chosen at \(I_C=2\,\mathrm{mA}\) on a small-signal part is more honest than a bias at \(50\,\mu\mathrm{A}\) or at the edge of \(I_{C,\max}\).

Coupling-capacitor design is a first-order high-pass calculation. The input coupling capacitor sees \(R_{in}\) of the stage, so \(f_L=1/(2\pi R_{in} C_{in})\). The output coupling capacitor sees \(R_C+R_L\). The emitter bypass capacitor sees \(R_E\parallel(1/g_m)\) looking into the emitter, which is a small resistance, so \(C_E\) must be large if you want the bypass still to be a short at the lowest signal frequency. Exam problems that give all three capacitors ask you to find the dominant (highest) low-frequency pole, not to write a full transfer function.

h-parameter numbers on a datasheet are specified at a particular \(I_C\), \(V_{CE}\), and frequency (often \(1\,\mathrm{kHz}\)). They do not transfer unchanged to a different Q-point. Convert to hybrid-π at the datasheet point if you must, then recompute \(g_m=I_C/V_T\) at *your* \(I_C\). Treating \(h_{ie}\) as a constant like a 10 kΩ resistor is a beginner error this unit exists to kill.

Darlington pairs (\(\beta\approx\beta_1\beta_2\), \(V_{BE}\approx 1.4\,\mathrm{V}\)) and the Sziklai pair appear as "name this" extras. A current mirror (two matched BJTs, \(I_C\) copied) is the IC bias element that replaces the discrete voltage divider; the hybrid-π of each transistor is unchanged. If a question draws a mirror, write \(I_{C1}=I_{C2}\) only when the emitters are at the same potential and \(V_A\) is ignored.

The hybrid-π parameters are not optional decoration. Every later analog block — differential pair, current mirror, op-amp input stage — is this model drawn twice with a tail current source.
