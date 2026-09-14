# Oscillators: Barkhausen, RC, LC, and crystal

An oscillator is an amplifier that supplies its own input. UG courses treat sinusoidal oscillators through Barkhausen's criterion, then catalogue RC phase-shift and Wien-bridge circuits, LC (Hartley, Colpitts, Clapp), and the quartz crystal that actually keeps time. Relaxation oscillators (Schmitt + RC, 555, UJT) produce squares and triangles; they share this unit because the lab still asks for them.

## Concepts

Barkhausen (necessary condition for a *linear* sinusoidal oscillator at start-up, in the frequency-domain loop-gain picture): the loop gain \(L(j\omega)=A(j\omega)\beta(j\omega)\) satisfies \(|L|=1\) and \(\angle L=0^\circ\) (or an integer multiple of \(360^\circ\)) at one frequency \(\omega_0\). Equivalent: the closed-loop characteristic equation \(1-A\beta=0\) if the feedback sign convention takes positive feedback as \(+A\beta\). If \(|L|>1\) at that phase, amplitude grows until a nonlinearity (gain compression, lamp, diode AGC, supply clipping) reduces the effective \(|A|\) to 1. If \(|L|<1\), the transient dies — no oscillation. Real oscillators therefore start with \(|L|\) a few percent above 1 and let a deliberate AGC or the device's own saturation set amplitude. Barkhausen does not describe that amplitude; describing amplitude needs a describing function or an energy argument.

RC oscillators are the audio-frequency choice (no inductors). Wien-bridge: a noninverting op-amp with \(R_f,R_g\) setting \(A=1+R_f/R_g\), and a series-\(RC\) plus parallel-\(RC\) lead-lag network as \(\beta\). At \(\omega_0=1/RC\) (equal resistors and capacitors), \(\beta=1/3\) and the phase is \(0^\circ\), so the amplifier must provide \(A=3\), i.e. \(R_f=2 R_g\). Amplitude stabilisation: a lamp or a JFET or diodes in the \(R_f\) path so that gain falls as amplitude rises. Phase-shift oscillator: three cascaded RC high-pass (or low-pass) sections in the feedback of an inverting amplifier. Each section contributes up to \(90^\circ\) but not all at once; three sections can contribute \(180^\circ\) at one frequency, which plus the inverting amp's \(180^\circ\) satisfies Barkhausen. For three equal-\(R\), equal-\(C\) high-pass sections, \(\omega_0=1/(RC\sqrt{6})\) and the required \(|A|=29\). Twin-T and quadrature oscillators appear as extras.

LC oscillators use a tank. Frequency \(\omega_0\approx 1/\sqrt{L_T C_T}\) of the effective tank, with a small correction from device capacitances. Hartley: tap on the inductor (two inductors, or a tapped coil, plus one capacitor). Colpitts: tap on the capacitor (two capacitors, one inductor). Clapp: Colpitts with a series capacitor in the inductor branch, which improves frequency stability against device \(C_\pi\). Armstrong: transformer tickler. The active device can be a BJT, JFET, or op-amp; the small-signal picture is a negative resistance cancelling the tank loss, or an amplifier with \(\beta\) taken from the tank divider.

Crystal oscillators replace the tank's \(L\) with a quartz resonator. The electrical equivalent is a huge \(L_s\), tiny \(C_s\), small \(R_s\) (series arm, high \(Q\), often \(10^4\)–\(10^6\)) in parallel with holder capacitance \(C_p\). Two resonances: series \(f_s=1/(2\pi\sqrt{L_s C_s})\) (impedance minimum) and parallel \(f_p=f_s\sqrt{1+C_s/C_p}\) a few kilohertz above. Oscillator circuits (Pierce, Colpitts-style) operate the crystal in the inductive region between \(f_s\) and \(f_p\). Temperature stability of AT-cut crystals is why every microcontroller has one. Overtone crystals oscillate at odd multiples; the circuit must select the overtone with an LC.

Relaxation oscillators: no linear Barkhausen loop. A timing capacitor is charged and discharged between two thresholds. 555 astable: \(t_H=0.693(R_A+R_B)C\), \(t_L=0.693 R_B C\), \(f=1.44/((R_A+2R_B)C)\). Op-amp astable (unit 05) is the same idea. Monostable (one-shot) produces a single pulse of width \(1.1 R C\) (555). VCO: make the charging current a function of a control voltage (555 astable with a control pin, or a current-starved integrator plus Schmitt — the triangle-core VCO).

Design practicalities. Frequency stability: \(\mathrm{d}f/f = -\frac12\mathrm{d}C/C\) for an LC tank, so NP0 capacitors and a stable \(L\). Amplitude: never assume the output is \(V_{sat}\) in a Wien-bridge; with AGC it is a clean sine of a designed volt or two. Loading the tank or the Wien network shifts \(f_0\) and may kill start-up. Buffer the oscillator with an emitter follower. Distortion: more loop gain above 1 means more clipping and more harmonics. Crystal drive level is specified; overdrive ages the crystal and can crack the blank.

## Equations

Barkhausen:

\[
|A(j\omega_0)\beta(j\omega_0)|=1,\qquad \arg(A\beta)=2\pi n.
\]

Wien-bridge (equal \(R,C\)):

\[
f_0=\frac{1}{2\pi RC},\qquad A_{\min}=3.
\]

RC phase-shift (three equal high-pass sections, inverting amp):

\[
f_0=\frac{1}{2\pi RC\sqrt{6}},\qquad |A|_{\min}=29.
\]

Colpitts (caps \(C_1,C_2\) in the divider, inductor \(L\)):

\[
\omega_0=\frac{1}{\sqrt{L C_{eq}}},\qquad C_{eq}=\frac{C_1 C_2}{C_1+C_2},\qquad |A|\ge \frac{C_2}{C_1}
\]

(the gain inequality depends on which capacitor is which; the ratio is the tank divider \(\beta\)).

Hartley (inductors \(L_1,L_2\), mutual \(M\), capacitor \(C\)):

\[
\omega_0=\frac{1}{\sqrt{(L_1+L_2+2M)C}}.
\]

Crystal:

\[
f_s=\frac{1}{2\pi\sqrt{L_s C_s}},\qquad f_p=f_s\sqrt{1+\frac{C_s}{C_p}},\qquad Q=\frac{\omega L_s}{R_s}.
\]

555 astable:

\[
T_H=0.693(R_A+R_B)C,\quad T_L=0.693 R_B C,\quad f=\frac{1.44}{(R_A+2R_B)C}.
\]

555 monostable:

\[
T=1.10\, RC.
\]

## Methods

1. Write \(A(s)\) of the amplifier (loaded by the feedback network) and \(\beta(s)\) of the network. Set \(\operatorname{Im}\{A\beta\}=0\) to find \(\omega_0\), then \(|A\beta|=1\) to find the gain condition.
2. For op-amp RC oscillators, the amplifier phase is \(0^\circ\) (noninverting) or \(180^\circ\) (inverting). The network must supply the remaining phase.
3. For LC, compute the tank resonance first, then the divider ratio that \(\beta\) presents, then the transistor \(g_m R_L'\) needed. Check that the device still has that gain at \(f_0\) (BJT \(f_T\), Miller).
4. Crystal: identify series vs parallel mode from the circuit (Pierce uses the parallel mode, load capacitance specified, e.g. 18 pF). Do not treat the crystal as a ceramic capacitor.
5. 555: remember that the thresholds are \(V_{CC}/3\) and \(2V_{CC}/3\), charge through \(R_A+R_B\), discharge through \(R_B\) only (discharge pin). Duty cycle is always \(>50\,\%\) in the standard astable; a diode across \(R_B\) is the hack for \(<50\,\%\).
6. Start-up: verify \(|L|>1\) with small-signal (uncompressed) \(A\). Verify a nonlinearity exists to stop the growth.

## Mistakes

- Stating Barkhausen as \(|A\beta|>1\). That is the start-up inequality, not the steady-state criterion. Steady-state linear theory wants equality; practice wants slightly more, then compression.
- Wien-bridge gain set to 29 (the phase-shift number) or phase-shift gain set to 3.
- Using \(\omega=1/RC\) on a three-section phase-shift oscillator without \(\sqrt{6}\).
- Colpitts: adding \(C_1+C_2\) instead of the series combination for \(C_{eq}\).
- Hartley: forgetting mutual inductance, or treating two separate inductors as \(L_1+L_2\) when they are on one core.
- Crystal: oscillating at \(f_p\) when the circuit is a series-mode oscillator, or vice versa. Also ignoring specified load \(C_L\), which pulls \(f\) by tens of ppm.
- 555: using \(0.693(R_A+2R_B)C\) as a *high* time rather than the period pieces; swapping \(R_A\) and \(R_B\).
- Expecting a Wien-bridge to start when \(A=2.9\). Component tolerance needs a designed \(A\approx 3.1\) plus AGC back to 3.
- Loading the tank with a low-impedance next stage and wondering why \(f_0\) moved and the circuit died.
- Treating a relaxation oscillator with Barkhausen. There is no linear loop gain of 1; there are two thresholds and a ramp.

Amplitude control deserves a paragraph because Barkhausen does not give it. A Wien-bridge with \(R_f=2.2 R_g\) starts, then clips on the rails if nothing else happens; the output is a square-ish wave at \(f_0\), which is fine for a clock and terrible for audio. A small-signal tungsten lamp in the \(R_g\) path has a resistance that rises with RMS current, so the effective gain falls as amplitude rises, and the loop settles at a clean sine. FET AGC does the same with \(r_{DS}\) as \(R_g\). Diode-pair clippers across a portion of \(R_f\) are cruder and more distorting. Crystal oscillators usually run at a specified drive level in microwatts; overdrive looks like a healthy sine on a scope and ages the blank.

VFO vs VCO vs PLL. A Colpitts with a varactor in the tank is a VFO/VCO. Stability of a free LC VCO is parts-per-thousand; a crystal is parts-per-million; a GPS-disciplined oscillator is parts-per-billion and is not this course. A PLL locks a VCO to a reference with a loop filter; the oscillator *inside* the PLL is still this unit's VCO.

Quadrature oscillators (two integrators in a loop, or a Wien with a second path) produce sine and cosine. Analog I/Q modulators still use them; digital NCO has largely replaced the lab oscillator as a function-generator core.

Gunn and IMPATT oscillators, klystrons, and magnetrons are microwave devices named in EM/microwave electives, not in this analog unit. Here, if it is not RC, LC, crystal, or relaxation, say so and stop.

Oscillators are feedback with the sign flipped and the amplitude left to a nonlinearity. Compute the frequency from the network, the gain from Barkhausen, and the amplitude from whatever compresses \(A\). If the circuit will not start, raise unloaded \(|A|\) a few percent and check that the tank or Wien network is not loaded by the next stage. If it starts as a square wave, you have too much loop gain and no AGC. Pierce crystal circuits need the specified load capacitance (often 18 pF or 22 pF) from the combination of two capacitors to ground plus stray capacitance; missing \(C_L\) pulls frequency and can stop start-up. Ceramic resonators are cheaper, lower-Q cousins of quartz and belong on USB clocks, not on 1 ppm references. A lab oscillator that drifts with hand capacitance is under-buffered or has a tank sitting on a high-impedance node; add the follower. Hand capacitance is a diagnostic, not a tuning method.
