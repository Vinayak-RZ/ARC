# Ideal op-amp, linear circuits, and instrumentation amplifiers

The operational amplifier is the analog Lego brick of UG electronics. With a handful of resistors it realises inversion, scaling, summing, difference, integration, and a high-quality instrumentation front-end. This unit stays in the linear regime: the op-amp remains in the active region, negative feedback holds the differential input near zero, and the golden rules apply. Nonlinear uses (comparators, Schmitt, precision rectifiers) are the next unit.

## Concepts

An op-amp is a high-gain differential voltage amplifier. The output is \(v_o=A_{od}(v_+-v_-)\), with open-loop gain \(A_{od}\) typically \(10^4\)–\(10^6\) at DC, plus a high input impedance and a low output impedance. Power pins \(\pm V_{CC}\) (or a single supply with a mid-rail virtual ground) set the ceiling; the output cannot exceed the rails minus a dropout that depends on the process (rail-to-rail vs. the older \(\pm 2\,\mathrm{V}\) of a 741).

Ideal op-amp axioms used in almost every UG linear problem:

1. Infinite open-loop gain \(\Rightarrow\) with negative feedback, \(v_+=v_-\) (virtual short). No current is implied by that equality; it is a voltage constraint.
2. Infinite input impedance \(\Rightarrow\) \(i_+=i_-=0\).
3. Zero output impedance \(\Rightarrow\) \(v_o\) is an ideal voltage source (until current limit).
4. Infinite bandwidth and slew rate, zero offset, zero noise — unless the problem gives numbers.

The virtual short is *not* a wire. You may not short \(v_+\) to \(v_-\) in the schematic and then claim the output is zero. The output does whatever KCL at the inverting node requires to keep \(v_-\) equal to \(v_+\).

Inverting amplifier: input through \(R_1\) to the inverting node, feedback \(R_f\), noninverting input grounded. Virtual ground at the inverting node. \(i_{in}=v_{in}/R_1\) all flows through \(R_f\), so \(v_o=-(R_f/R_1)v_{in}\). Input resistance is \(R_1\), which is a real limitation: the source sees \(R_1\), not the op-amp's megaohm input.

Noninverting amplifier: input to \(+\), divider \(R_1,R_f\) on the output back to \(-\). Voltage-follower is the special case \(R_f=0\), \(R_1=\infty\). Gain \(1+R_f/R_1\), input resistance \(\approx\infty\), the configuration for buffers and sensor interfaces.

Summing amplifier: several inputs through resistors into the inverting node. Superposition: \(v_o=-R_f(v_1/R_1+v_2/R_2+\cdots)\). Weighted summer or averager (equal resistors plus a scale). A noninverting summer exists but needs a different algebra; exam default is inverting.

Difference amplifier (op-amp subtractor): four resistors. If \(R_2/R_1=R_4/R_3\) (standard labelling: \(R_1\) from \(v_1\) to \(-\), \(R_2\) feedback, \(R_3\) from \(v_2\) to \(+\), \(R_4\) from \(+\) to ground), then \(v_o=(R_2/R_1)(v_2-v_1)\). Common-mode gain is zero only if the ratios match. Source impedances unbalance the ratios; that is why a naked subtractor is a poor instrumentation front-end.

Instrumentation amplifier (in-amp): two buffers (or two noninverting stages sharing a gain resistor \(R_G\)) feeding a subtractor. The classic three-op-amp topology has differential gain \(A=1+2R/R_G\) set by one resistor, huge input impedance on both inputs, and excellent CMRR if the subtractor resistors match. Used for strain-gauge bridges, thermocouples with a series resistor, and any small differential signal sitting on a large common-mode voltage. Integrated in-amps (INA-style) are this circuit laser-trimmed.

Integrator: capacitor in feedback of an inverting op-amp, resistor at the input. \(v_o=-(1/RC)\int v_{in}\,dt\) plus the constant stored on \(C\). Practical integrators add a large \(R_f\) across \(C\) so DC offset does not ramp to the rail. Differentiator: \(C\) at the input, \(R\) in feedback; high-frequency noise and stability make it less popular than the integrator.

Linear applications that still obey the golden rules: voltage-to-current converter (Howland pump, or a simple inverting op-amp driving the grounded load in the feedback loop), current-to-voltage (transimpedance: photodiode into the inverting node, \(v_o=-i R_f\)), and DC-coupled first-order filters that are just the integrator/differentiator with finite poles.

Real-device corrections that UG exams actually ask:

- Finite \(A_{od}\): closed-loop gain is \(A_{cl}=A_{ideal}\times (A_{od}\beta)/(1+A_{od}\beta)\) with loop gain \(A_{od}\beta\). Error \(\approx 1/(A_{od}\beta)\).
- Input offset voltage \(V_{os}\): appears as a DC source at the input; output offset \(\approx V_{os}(1+R_f/R_1)\).
- Input bias currents: place a compensation resistor \(R_{comp}=R_1\parallel R_f\) in the \(+\) lead so \(I_B\) drops cancel; remaining error is \(I_{os} R_f\).
- CMRR: \(v_o\) includes \(A_{cm} v_{cm}\). Specified in dB as \(20\log(A_{dm}/A_{cm})\).
- Finite bandwidth: dominant-pole op-amps have constant gain-bandwidth product \(\mathrm{GBW}=A_{od} f_p\). Closed-loop bandwidth \(\approx\mathrm{GBW}/\text{noise gain}\). Unity-gain follower is the hardest for stability, not the easiest.
- Slew rate: \(\mathrm{SR}=dv_o/dt|_{\max}\), set by internal compensation current into \(C_c\). A sine of amplitude \(V_p\) distorts if \(2\pi f V_p>\mathrm{SR}\). Full-power bandwidth \(f_{fp}=\mathrm{SR}/(2\pi V_{o,\max})\).

Single-supply design: the golden rules still hold, but the output cannot go below the negative rail (ground). Bias the noninverting input to mid-rail, AC-couple, and remember that "ground" in the classic formulas is that mid-rail virtual ground.

## Equations

Ideal closed-loop gains:

\[
A_{\mathrm{inv}}=-\frac{R_f}{R_1},\qquad A_{\mathrm{ni}}=1+\frac{R_f}{R_1},\qquad A_{\mathrm{follower}}=1.
\]

Inverting summer:

\[
v_o=-R_f\sum_k \frac{v_k}{R_k}.
\]

Difference amplifier (matched ratios \(k=R_2/R_1=R_4/R_3\)):

\[
v_o=k(v_2-v_1).
\]

Three-op-amp instrumentation amplifier:

\[
v_o=\left(1+\frac{2R}{R_G}\right)\frac{R_F}{R_A}(v_2-v_1)
\]

(with the usual equal-resistor drawing; many sheets set \(R_F/R_A=1\)).

Integrator / differentiator (inverting):

\[
V_o(s)=-\frac{1}{sRC}V_{in}(s),\qquad V_o(s)=-sRC\, V_{in}(s).
\]

Finite-gain correction, noise gain \(G_n=1+R_f/R_1\) (same for inverting and noninverting):

\[
\frac{v_o}{v_{id,ideal}}=\frac{A_{od}}{1+A_{od}/G_n}.
\]

Loop gain \(L=A_{od}/G_n\).

Offset at output, bias-compensated:

\[
V_{o,\mathrm{err}}\approx V_{os} G_n + I_{os} R_f.
\]

Slew-rate limit for \(v_o=V_p\sin 2\pi f t\):

\[
2\pi f V_p \le \mathrm{SR}.
\]

## Methods

1. Draw the op-amp with both inputs, output, and feedback path. Confirm negative feedback exists at DC (resistive path from output to \(-\), or the integrator's capacitor with leakage). If the feedback is positive, this unit's golden rules do not apply.
2. Set \(v_+=v_-\) and \(i_+=i_-=0\). Write KCL at the inverting node (and at \(+\) if it is not a stiff divider). Solve for \(v_o\).
3. Superposition for multiple sources, including DC offsets: kill AC sources to find DC error, kill DC to find signal gain.
4. Instrumentation: first find the voltage across \(R_G\), which is \(v_2-v_1\). The currents through the two \(R\) resistors are \((v_2-v_1)/R_G\). Then the buffer outputs are \(v_2+IR\) and \(v_1-IR\). Feed those to the subtractor.
5. Finite \(A_{od}\): do not use \(v_+=v_-\). Use \(v_o=A_{od}(v_+-v_-)\) plus KCL. For a first-order estimate, use the loop-gain formula.
6. Always check the output against the rails. If \(|v_o|\) would be 18 V on a \(\pm 12\,\mathrm{V}\) amplifier, the answer is saturation, not 18 V.
7. Transimpedance: all photodiode current goes through \(R_f\). Sign: current into the inverting node produces a negative output.

## Mistakes

- Applying \(v_+=v_-\) to an open-loop comparator. Without negative feedback the differential input is *not* zero.
- Treating the virtual short as a physical short that steals signal current to ground in the inverting amplifier. The current goes through \(R_f\).
- Noninverting gain written as \(R_f/R_1\) (missing the 1). Follower gain written as 0 because "no resistors".
- Difference amplifier: mismatch of a fraction of a percent destroys CMRR. Quoting infinite CMRR after using 1 % resistors is dishonest.
- Connecting a sensor with 10 kΩ source impedance straight into a 10 kΩ subtractor and expecting the textbook gain.
- Integrator: omitting the minus sign, or forgetting the initial voltage on \(C\).
- Compensation resistor forgotten, then blaming \(V_{os}\) for a bias-current error of \(I_B R_f\) that can be hundreds of millivolts.
- Bandwidth: using GBW as the closed-loop bandwidth of a gain-of-100 stage. The closed-loop pole is about \(\mathrm{GBW}/100\).
- Slew rate vs small-signal bandwidth: a 1 MHz GBW part can still slew-limit a 10 kHz large sinusoid.
- Single-supply inverting amplifier with the \(+\) pin grounded: the output cannot produce the negative half of the waveform.

Frequency compensation is why a 741 has a 1 MHz GBW and a 0.5 V/µs slew, not a hundred megahertz. Internal Miller \(C_c\) (typically 30 pF) makes the open-loop response a dominant pole so that the loop is stable at unity-gain feedback. Decompensated op-amps (stable only for closed-loop gains above 5 or so) trade that capacitor for GBW; do not drop them into a follower. Capacitive load on the output adds a pole with \(R_{out}\); a series isolation resistor of 10–50 Ω is the field fix.

Common-mode input range is not the rails. On a 741 it is about \(\pm 12\,\mathrm{V}\) from \(\pm 15\,\mathrm{V}\) supplies; exceeding it can invert the output (phase reversal). Rail-to-rail input stages use complementary pairs and have their own crossover distortion in \(g_m\). Instrumentation work on a 5 V single supply needs a rail-to-rail in-amp, not a recycled 741 drawing.

The instrumentation amplifier CMRR is limited by subtractor resistor matching. 0.1 % resistors give a CMRR on the order of \(20\log(1+2R/R_G)-20\log(\epsilon)\) in a back-of-envelope sense; laser-trimmed integrated in-amps quote 80–110 dB. Guard the input cables, tie the cable shield to the common-mode voltage (driven guard) on microvolt sensors, and never share a long ground return with a motor.

Current-feedback op-amps (CFA) exist; their closed-loop bandwidth is less gain-dependent than a voltage-feedback part. UG default remains voltage-feedback with a constant GBW. If a problem does not say CFA, do not use CFA formulas.

Linear op-amp circuits are Kirchhoff plus one extra constraint. The skill is not memorising ten topologies; it is writing KCL at the inverting node without fear. The intern who can write that KCL on a whiteboard, then check the rails, then check GBW and slew, has finished this unit for analog coursework.
