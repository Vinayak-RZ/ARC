# Comparators, Schmitt triggers, and precision rectifiers

When the feedback around an op-amp is positive, absent, or nonlinear, the golden-rule virtual short fails. The output slams to a rail or to a clamped voltage, and the circuit becomes a comparator, a Schmitt trigger, a window detector, or a precision rectifier that hides the 0.7 V diode drop inside a feedback loop. This unit is the nonlinear companion to linear op-amp circuits.

## Concepts

A comparator is an op-amp (or a dedicated comparator IC) used open-loop to tell which of two voltages is larger. \(v_o\) saturates high if \(v_+>v_-\) and low otherwise. Dedicated comparators (LM339-style) have open-collector outputs, unspecified linear-region behaviour, and are faster than compensated op-amps; they are not drop-in linear amplifiers. An op-amp can still be used as a slow comparator if you accept slew-rate-limited edges and possible phase inversion when inputs are overdriven (a 741 failure mode).

Threshold: a single reference \(V_{ref}\) on one input and the signal on the other. Inverting comparator: signal into \(-\), output high when \(v_{in}<V_{ref}\). Noninverting: the opposite. The threshold is infinitely sharp only in the idealisation; real devices have a millivolt-scale uncertainty from offset, noise, and finite gain. A slowly moving input therefore chatters — the output toggles on noise as \(v_{in}\) crawls through the threshold. That is the engineering reason for hysteresis.

Schmitt trigger: a comparator with positive feedback, which makes the threshold depend on the present output state. Two thresholds \(V_{T+}\) and \(V_{T-}\) (or \(UTP\), \(LTP\)) straddle the DC operating point. The transfer curve is a hysteresis loop. Once the output has gone high, the input must fall past the lower threshold to go low, and vice versa. Noise smaller than the hysteresis width cannot chatter. Inverting Schmitt: feedback to \(+\), signal into \(-\). Noninverting Schmitt: signal into the positive-feedback divider.

Design of an inverting Schmitt with output levels \(V_{OH},V_{OL}\) (often the rails, or \(\pm V_Z\) if a Zener clamp is used) and divider \(R_1\) from \(+\) to ground, \(R_2\) from output to \(+\):

The noninverting pin sits at a weighted average of the output and whatever DC is on \(R_1\). If \(R_1\) goes to ground, \(V_+=v_o R_1/(R_1+R_2)\), so \(V_{T+}=V_{OH} R_1/(R_1+R_2)\) and \(V_{T-}=V_{OL} R_1/(R_1+R_2)\). Shifting both thresholds up is done by tying \(R_1\) to a reference instead of ground, or by adding a third resistor.

Astable using a Schmitt plus an RC on the inverting input is a relaxation oscillator: the capacitor charges toward \(V_{OH}\) until \(V_{T+}\), then the output flips and the capacitor discharges toward \(V_{OL}\) until \(V_{T-}\). Period \(\approx 2RC\ln 2\) for a symmetric \(\pm\) rail Schmitt with thresholds at \(\pm V_{sat}/2\) wait — actually for the standard op-amp astable with \(\beta=R_1/(R_1+R_2)\), \(T=2RC\ln\frac{1+\beta}{1-\beta}\). That circuit is the cousin of unit 07 oscillators; mention it here because the Schmitt *is* the nonlinear element.

Window comparator: two thresholds, two comparators, outputs combined with AND/OR (open-collectors wired AND, or a logic gate). Output true when \(V_L<v_{in}<V_H\). Used as a go/no-go band detector.

Zero-crossing detector: comparator with \(V_{ref}=0\). Add hysteresis if the input is noisy. A diode bridge or a series resistor plus anti-parallel diodes at the input protects against voltages beyond the rails.

Precision rectifiers exist because a silicon diode does not conduct until 0.7 V, which is a disaster for millivolt signals. Superdiode: op-amp driving a diode, feedback from the diode cathode to the inverting input. As soon as the op-amp output exceeds one diode drop, the loop closes and the cathode follows the input (noninverting) or the usual inverting law. When the polarity reverses, the diode opens, the loop opens, and the op-amp slams to the opposite rail — that is the flaw of the half-wave superdiode: saturation recovery delay. The improved half-wave precision rectifier places the diode in the feedback path so that the op-amp never saturates; a second diode provides a path for the unused polarity. Full-wave precision rectifier (absolute-value circuit): two op-amps, or one op-amp plus a precision half-wave feeding a summing amplifier that computes \(v_{in}-2 v_{half}\). Peak detectors: superdiode into a capacitor; a buffer reads the capacitor; a reset switch dumps it. Analog sample-and-hold is the same idea with a switch instead of a diode.

Log and antilog amplifiers use the exponential diode (or \(V_{BE}\)) law inside the feedback loop: \(v_o\propto\log(v_{in}/V_{ref})\). Temperature compensation with matched pairs is required for anything better than a demo. Analog multipliers (Gilbert cell, or log-antilog) sit at the edge of this syllabus.

Clampers and clippers with op-amps: an op-amp plus diodes can make a precision clipper whose threshold is a clean DC, not \(V_B+0.7\). Bound to this unit, not to unit 01, because the 0.7 V is inside the loop.

Output clamping of comparators: a resistor from the op-amp output to a Zener pair, or a dedicated comparator with a pull-up to 5 V for TTL/CMOS compatibility (unit 12). Never assume a \(\pm 15\,\mathrm{V}\) op-amp output is a legal logic level.

## Equations

Open-loop comparator (ideal):

\[
v_o=
\begin{cases}
V_{OH}, & v_+>v_-,\\
V_{OL}, & v_+<v_-.
\end{cases}
\]

Inverting Schmitt, \(R_1\) to ground, \(R_2\) feedback to \(+\), signal on \(-\):

\[
V_{T+}=V_{OH}\frac{R_1}{R_1+R_2},\qquad V_{T-}=V_{OL}\frac{R_1}{R_1+R_2},\qquad V_H=V_{T+}-V_{T-}.
\]

Noninverting Schmitt (signal through \(R_1\) into \(+\), \(R_2\) from output to \(+\), \(-\) at \(V_{ref}\)):

\[
V_{T}=V_{ref}\frac{R_1+R_2}{R_2}-v_o\frac{R_1}{R_2},
\]

evaluated at each \(v_o\in\{V_{OH},V_{OL}\}\).

Astable op-amp (Schmitt + RC on \(-\)):

\[
T=2RC\ln\frac{1+\beta}{1-\beta},\qquad \beta=\frac{R_1}{R_1+R_2}.
\]

Ideal precision full-wave (absolute value), inverting construction with matched resistors:

\[
v_o=-|v_{in}|\quad\text{or}\quad +|v_{in}|
\]

according to the summer signs. The diode drop does not appear in \(v_o\) while the loop is closed.

Log amp (diode in feedback, \(v_{in}\) through \(R\)):

\[
v_o=-n V_T \ln\frac{v_{in}}{I_S R}.
\]

## Methods

1. Comparator: identify which input is the signal and which is the reference. Sketch \(v_o(t)\) as a square-ish wave that flips at the crossings. If hysteresis is present, use two thresholds and remember the direction of approach.
2. Schmitt thresholds: write the voltage at the positive-feedback node as a function of \(v_o\). Set that equal to the voltage at the other input; solve for the input that causes switching. Do this twice, once per output state.
3. Hysteresis width is a design knob: more positive feedback \(\Rightarrow\) more noise immunity and more switching delay on slow ramps.
4. Precision rectifier: analyse each polarity separately. For the conducting polarity, the diode is a short in the idealisation *after* the loop has closed, so the usual op-amp gain formula applies at the load. For the blocking polarity, the diode is open; find the path that still gives the op-amp local feedback so it does not saturate (improved circuit).
5. Peak detector: capacitor KVL, diode on only while \(v_{in}>v_C+V_\gamma\) in a dumb diode circuit, or while \(v_{in}>v_C\) in a superdiode. Discharge path must be stated (resistor, reset switch, or leakage).
6. Logic interface: clamp or use an open-collector comparator plus pull-up to the logic rail. Then treat the output as a digital signal in unit 12.

## Mistakes

- Using \(v_+=v_-\) on a Schmitt or comparator. The whole point is that the differential input is *large* except during the nanoseconds of switching.
- Drawing an inverting Schmitt transfer curve with the wrong direction: inverting means a high input produces a low output; the hysteresis loop still has two thresholds.
- Computing a single threshold for a Schmitt as if it were an unbiased divider on a linear amplifier.
- Forgetting that \(V_{OL}\) of a \(\pm 15\,\mathrm{V}\) op-amp is about \(-15\,\mathrm{V}\), not 0. Thresholds are then symmetric about zero, not both positive.
- Open-collector comparator without a pull-up resistor: the output never goes high.
- Superdiode half-wave: ignoring the time the op-amp spends in saturation on the unused half-cycle. At a few kilohertz a 741 already distorts; use the non-saturating topology or a fast comparator-plus-switch.
- Precision rectifier resistor mismatch: the two half-cycles have different gains, so the output is not a true absolute value.
- Peak detector droop: treating \(C\) as holding forever when a 10 MΩ scope probe and diode leakage are present.
- Driving TTL with \(\pm 13\,\mathrm{V}\) swings. That is a fried input, not a logic 1.
- Log amp: using \(\log_{10}\) versus \(\ln\) inconsistently, and ignoring the \(I_S\) temperature dependence.

Lab practice: a comparator without hysteresis on a slowly ramped sensor will chatter at a few kilohertz and radiate. Add 20–50 mV of hysteresis (or more, if the noise is worse), then accept the extra switching delay. Debounce is the digital version of the same idea.

Monostable (one-shot) using a comparator or a 555: one input edge, one output pulse of width set by RC. Retriggerable vs non-retriggerable matters in pulse-stretching. The analog one-shot is being replaced by MCU timers; the exam still draws the 555.

PWM from a Schmitt (or a comparator) plus a triangle: the duty cycle is the fraction of time the triangle is below the control voltage. That is analog class-D at textbook level. Keep the triangle amplitude inside the comparator's common-mode range.

Diode-bounded integrators and analog computing: diodes around an integrator clamp the state. Analog computers are historical; the bounded integrator is still a PLL loop-filter trick.

Nonlinear op-amp circuits are piecewise-linear analysis plus an awareness of slew rate and saturation recovery. If the loop is closed through a diode, write the ON and OFF circuits separately, then keep the piece that is consistent. When the loop is *open* (comparator), do not write a virtual short; write a rail.
