# Network frequency response and passive filters

Frequency response is H(jω), the sinusoidal steady-state transfer function obtained by setting s = jω in H(s) or by phasor analysis as a function of ω. Passive RLC filters—low-pass, high-pass, band-pass, band-stop—are the UG circuits realization. Bode plots (magnitude in dB, phase in degrees vs log ω) are the graphical language shared with control courses. Loaded vs unloaded response and source resistance are part of honest design.

## Concepts

H(jω) = |H| e^{jφ}. |H| is the amplitude ratio of output sinusoid to input sinusoid; φ is the phase lead of output over input. A low-pass RC: H = 1/(1+jωRC), |H| = 1/√(1+(ω/ωc)^2), ωc = 1/RC, −3 dB when |H| = 1/√2. High-pass CR: H = jωRC/(1+jωRC). Series RLC between source and load can be band-pass if output is taken on R, low-pass on C, high-pass on L. Parallel tanks make band-stop (notch) in series-arm use, or band-pass in shunt-arm use.

Bode: 20 log10 |H| versus log ω. First-order poles give −20 dB/decade after the break; zeros +20 dB/decade. Second-order complex poles with high Q peak near ω0 and then fall at −40 dB/decade. Phase of a first-order low-pass goes from 0 to −90° with −45° at ωc.

Decibels: 20 log |voltage ratio| when impedances match or when we simply mean a voltage transfer. Power dB is 10 log P2/P1. Mixing them is a classic mistake.

Loading: a filter designed for an open voltage ratio droops when R_L is comparable to the last resistor. Buffering (electronics) or absorbing RL into the design (this pack) are the two fixes. Source Rs is part of the first time constant.

Constant-k and m-derived image-parameter filters are historical UG topics in some Indian syllabi; modern courses emphasize first- and second-order sections and cascade. Either way, the frequency-response definitions do not change. Insertion loss is 10 log (P available / P load) and is not identical to −20 log |Vout/Vin| unless the port impedances are equal.

Resonance unit Q and this unit's band-pass Q are the same number: B = f0/Q at the half-power frequencies of |H|.

Bode plotting procedure that actually gets used: factor H(jω) into poles, zeros, and a constant K. Write 20 log|K| as the low-frequency floor if there is no pole at the origin. Each real zero at ωz: +20 dB/dec starting at ωz, +3 dB correction at ωz. Each real pole: −20 dB/dec, −3 dB at the break. A pole at the origin: already −20 dB/dec from the left of the paper. Complex pair: −40 dB/dec after ω0, peaking of about 20 log(Q) if Q>1, and a −90° phase jump smeared around ω0 (steeper if Q is high). Phase Bode: first-order pole contributes 0° a decade below, −45° at the break, −90° a decade above (asymptotic sketch). Adding these sketches is faster than computing |H| at twenty frequencies, and it catches a missing pole.

Passive limitations: a passive filter cannot have |H| > 1 at all frequencies for voltage if it is a ladder of positive R, L, C driven by a voltage source with resistive load in the usual sense—except that L and C can peak above 1 by resonance (energy stored, not power gain). There is no power gain; average P_out ≤ P_available. An LC ladder between 50 Ω and 50 Ω can have |S21| ≤ 1. A voltage divider of only R has |H| < 1 everywhere. If a homework |H| peaks at 8, look for a series-resonant voltage on C or L.

Prototype table (first and second order), voltage transfer, unloaded:

- LP RC: R series, C shunt, H = 1/(1+sRC).
- HP RC: C series, R shunt, H = sRC/(1+sRC).
- LP RL: L series, R shunt? Careful: RL low-pass is R series L shunt or L series R shunt depending on output; the common one is series L, output after L across R, which is LP with ωc = R/L.
- Series RLC, output on C: second-order LP.
- Series RLC, output on L: second-order HP.
- Series RLC, output on R: second-order BP.
- Parallel tank in series with the load as a notch, or across as a BP if driven by a current.

Choose impedance level so that C is tens of nF to µF in audio, tens of pF in RF, and R is kilohms on a breadboard or 50 Ω in RF. An audio LP with C = 10 pF and R = 1 MΩ is foolish because stray capacitance dominates.

Group delay τg = −dφ/dω is flat in the passband of a Bessel filter (electronics/DSP) and peaks near the cutoff of a high-Q Chebyshev. UG circuits may only mention that phase is not linear, so a square wave rings. That ring is the same underdamped step response as unit 07.

When measuring, a scope FFT or a sweep generator traces |H|. Loading by the probe (10 MΩ ∥ 15 pF) is a high-pass zero and a low-pass pole on the node. At 10 kHz the 15 pF is 1 MΩ, already comparable to a 1 MΩ circuit. Use 10× probes and buffers. Write the load resistance on every Bode sketch, and mark the −3 dB frequency relative to the actual passband gain, not relative to 0 dB if the divider already sits at −6 dB.

## Equations

First-order LP: \( H(s) = \omega_c/(s+\omega_c) \), \( \omega_c = 1/RC \).

First-order HP: \( H(s) = s/(s+\omega_c) \).

Series RLC BP (output on R): \( H(s) = (s R/L) / (s^2 + s R/L + 1/LC) \), \( \omega_0 = 1/\sqrt{LC} \), \( Q = \omega_0 L/R \).

Notch (series L-C in the series arm, output after it): zero at ω0.

Bode dB: \( 20\log_{10}|H| \). −3 dB ⇔ |H| = 1/√2.

Cascade of isolated stages: H = H1 H2 (needs buffering or accounting for loading).

## Methods

Write H(s) from voltage division with Z(s). Set s=jω. Find |H| and φ. Break frequencies from poles/zeros. Sketch Bode asymptotes, then correct by ±3 dB at simple breaks and by a Q peak at complex poles. For design, pick topology from the need (LP/HP/BP/BS), pick ωc or ω0 and Q, solve R, L, C from impedance-level constraints (available C, reasonable R for op-amp later, or source 50 Ω).

Check DC: LP should pass, HP should block, series-C HP is 0 at DC. Check ω→∞: LP 0, HP constant, BP 0. Check phase sense: HP first-order leads toward +90° at low frequency.

A design sequence for a second-order audio low-pass: pick f0 (say 4 kHz), pick Q (0.707 Butterworth, no peak), pick C from a catalog (10 nF), then L = 1/(ω0² C), then R from Q for the chosen topology. If L comes out 2 H, the impedance level is too high or f0 too low for a practical inductor; raise C or use an active Sallen-Key (electronics pack). If L comes out 0.2 µH, you are in RF and stray L matters. Always compute |H| at f0 and at 10 f0. For a notch at 50 Hz hum, a high Q is tempting but component drift of 1% moves the zero off 50 Hz; a milder Q with some residual hum may be more reliable. Document loaded R_L in the Bode, not only the unloaded textbook curve.

## Mistakes

Using 10 log for a voltage ratio. Ignoring Rs and RL. Cascading two RC low-passes and using (1/(1+jωRC))^2 when they load each other. Taking output across L in series RLC and calling it band-pass (it is high-pass-ish with a peak). Confusing −3 dB bandwidth with 3 dB above the peak for a high-Q BP (half-power relative to the peak). Plotting Bode against f linearly. Using ωc = RC not 1/RC. Designing a notch with Q so high that component tolerance shifts the zero off the interferer. Reporting |H| in dB but then multiplying dB by a voltage. Treating a passive filter's |H|max as 1 when the divider already attenuates at the passband (series RLC BP on R has passband gain 1 only if that R is the entire resistive drop). Plotting 20 log(H) with H already in dB, doubling the dB. Using a linear f axis and calling it Bode. Cascading two second-order sections and adding Q (Q does not add). Taking a high-pass’s +20 dB/dec slope and expecting it to continue forever (it flattens after the break). Designing an LC filter into a 10 MΩ probe and then a 50 Ω cable without redesign. Confusing insertion loss with return loss. A first-order RC is never “Butterworth second-order”; name the order from the high-frequency slope, −20 dB/dec per order for a low-pass. If the measured slope is −35 dB/dec, a stray pole or the generator roll-off is in the picture, not a new topology. Document the load. If a lab Bode disagrees with the unloaded formula by several dB in the passband, the usual cause is Rs of the generator plus RL of the cable, not a wrong C. Recompute H with those two resistors in the divider before changing the topology.
