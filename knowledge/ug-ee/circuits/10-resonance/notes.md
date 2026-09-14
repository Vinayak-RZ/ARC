# Series and parallel resonance, Q and bandwidth

Resonance in a lumped RLC network is the frequency where the input impedance is purely real, or equivalently where the imaginary part of the admittance is zero. Series and parallel (anti-)resonance are the two UG prototypes. Quality factor Q and half-power bandwidth B describe selectivity. Transformers, filters, and machine magnetizing branches all reuse these definitions.

## Concepts

Series RLC: \( Z = R + j\omega L + 1/(j\omega C) \). Resonance \( \omega_0 = 1/\sqrt{LC} \) when \( X_L + X_C = 0 \). Then \( Z = R \) is minimum, current is maximum for a voltage source, and voltage across L and C can each be Q times the source (voltage magnification). Dangerous for insulation if Q is large.

Parallel RLC: \( Y = 1/R + j\omega C + 1/(j\omega L) \). Resonance at the same \( \omega_0 \) for the ideal three-element tank. Then \( Z = R \) is maximum, current from a current source mostly circulates in the tank, and branch currents in L and C are Q times the source current (current magnification).

Practical coils have series r; a more accurate parallel coil is r in series with L, which shifts the admittance resonance slightly (maximum |Z| not exactly at \( 1/\sqrt{LC} \)). UG problems usually state which definition: \( X=0 \), max |Z|, or unity pf. They coincide for the ideal series RLC and the ideal parallel RLC with R in the resistive branch.

Q of a series circuit: \( Q = \omega_0 L / R = 1/(\omega_0 RC) \). Parallel (R across the tank): \( Q = R/(\omega_0 L) = \omega_0 RC \). Half-power frequencies: \( \omega_{1,2} = \omega_0 \pm \alpha \) for high Q, with bandwidth \( B = \omega_2 - \omega_1 = 2\alpha = \omega_0 / Q \) in rad/s. In hertz, \( f_0/Q \). High Q means a sharp peak and a slow time-domain ring (same Q as the transient unit).

Selectivity vs loss: increasing R in series lowers Q and widens B; increasing R in parallel raises Q. Loaded Q includes the source and load resistances. Unloaded Q is the tank alone. A generator with large Rs kills series Q.

Phasor diagrams at resonance: series voltages on L and C are equal, opposite, and large; the source matches the resistor. Parallel currents in L and C are equal, opposite, and large; the source matches the resistor.

A coil with series r and a parallel C is the realistic tank. The input impedance is Z(s) = (r + sL) ∥ 1/(sC). |Z| peaks near ω0 = 1/√(LC) but not exactly, and the frequency of unity power factor (Im Y = 0) is ω = √(1/LC − r²/L²), which is real only if r is not too large. UG problems that give r of a coil and a separate R should specify whether they want X=0, max |Z|, or zero phase. For high Q (Q > 10) all three sit within a percent of 1/√(LC) and the distinction is academic; for Q = 2 it is not.

Bandwidth definitions: half-power means |I| = Imax/√2 for series voltage-driven, or |V| = Vmax/√2 for parallel current-driven. Those are not always the −3 dB points of an arbitrary transfer H(jω) if the passband gain is not the peak of that same curve. For the standard prototypes they coincide. The exact half-power frequencies are geometrically symmetric about ω0: ω0² = ω1 ω2, while the arithmetic midpoint (ω1+ω2)/2 is slightly above ω0. High-Q lectures ignore the difference.

Universal resonance curve: plot |I/I0| versus normalized detuning 2Q Δω/ω0. For high Q the shape is the same for series and parallel. That is why one sketch serves many numerical problems. Off by one bandwidth, the response is down 3 dB; off by many Q, it is small.

Energy at resonance: average energy in L equals average energy in C in the ideal series or parallel tank, and Q = 2π (energy stored)/(energy dissipated per cycle). This energy definition of Q agrees with ω0 L/R for series. It remains the definition when the circuit is not a simple RLC. A cavity, a quartz crystal (modeled as a huge-Q series motional RLC with shunt C0), and a power-system LC filter all borrow it.

Design hazards: voltage magnification can produce hundreds of volts on a small-signal series tank; choose capacitor dielectric accordingly. Current magnification can overheat a coil in a parallel tank even when the source current is modest. A series resonant fault (a capacitor compensating a cable that resonates with transformer leakage) is a power-system cousin: same ω0, unwanted Q.

When R, L, C are all series but the output is taken on C, the voltage transfer is low-pass with a possible Q peak (second-order low-pass), not the band-pass of the current. Always name the output port before saying “the circuit is band-pass.” Resonance of Z_in is not the same sentence as resonance of H(jω). In a lab book, write f0, Q, B, and the drive type (voltage or current) on the same line so the next engineer does not reuse a series plot on a parallel tank.

## Equations

\( \omega_0 = 1/\sqrt{LC} \). Series \( Q_s = \omega_0 L/R \). Parallel \( Q_p = R/(\omega_0 L) \).

\( B_\mathrm{rad/s} = \omega_0 / Q \), \( f_{1,2} = f_0 \pm B_f/2 \) (high-Q approximation, geometric mean exactly \( \omega_0 = \sqrt{\omega_1\omega_2} \)).

Exact half-power series: \( \omega_{1,2} = \pm R/(2L) + \sqrt{(R/2L)^2 + 1/LC} \).

Voltage magnification series: \( |V_L|/|V_s| = Q \) at \( \omega_0 \). Current magnification parallel: \( |I_L|/|I_s| = Q \).

Damping: \( \alpha = R/(2L) \) series = \( B/2 \).

## Methods

Write Z(jω) or Y(jω). Set Im = 0 or d|Z|/dω = 0 as required. Compute Q from energy or from element formulas. Bandwidth from Q if Q ≳ 10; otherwise use the exact quadratic. For loaded circuits, absorb source and load into an effective R before using the formulas.

Design a series trap: choose \( \omega_0 \), pick C from voltage rating and available parts, then L, then R from desired Q. Check inductor current at resonance \( V_s/R \). Design a parallel tank for a current-driven crystal replacement: pick L, C, then R from Q.

When sketching |I(ω)| for series, peak at ω0, half-power at ω0±B/2. Do not sketch a high-Q curve for Q = 1.

A measurement recipe: drive a series RLC with a function generator of low Rs, measure I by the voltage on R, sweep f, find f0 at Imax, find f1 and f2 at Imax/√2, then Q = f0/(f2−f1). Compare with ω0 L/R using LCR-meter values. Discrepancy is usually generator Rs adding to R (loaded Q) or capacitor ESR. For a parallel tank, use a series dropper resistor from the generator so the tank sees an approximate current source; then V(f) peaks at resonance. Plotting 1/|Z| by mistake will invert the story. Record whether the generator voltage was held constant (voltage drive) or not; many generators sag, which distorts the measured Q.

## Mistakes

Using series Q on a parallel tank. Setting bandwidth in hertz equal to ω0/Q without dividing by 2π. Claiming resonance when |Z| is min for a parallel circuit. Ignoring source resistance in loaded Q. Computing VL = Q Vs and forgetting it is at ω0 only. Using DC resistance of a coil as the only R at RF (skin effect). Applying the high-Q half-power split when Q = 2. Adding L and C voltages as RMS scalars at resonance (they cancel). Designing C from ω0 with L in mH and ω in Hz mixed. Treating a series RLC fed by a current source as having a current peak at resonance (current is imposed; voltage peaks instead). Using f0 = 1/√(LC) with LC in mixed prefixes and missing 2π when the answer was asked in hertz. Stating Q = R/ωL for a series circuit (that is the parallel formula). Designing a tank with Q = 200 on a breadboard and expecting it to hold: stray C, ESR, and generator Rs will load it. Measuring bandwidth with a linear frequency sweep plotted on a scope time base instead of a frequency axis. Confusing the −3 dB points of |Z(jω)| with those of a voltage transfer taken on C. Forgetting geometric symmetry ω0 = √(ω1 ω2) and averaging f1 and f2 arithmetically as f0 when Q is low. Claiming energy is destroyed at resonance; it is stored and returned twice per cycle while R dissipates the average P. A series resonant capacitor voltage of Q Vs can puncture a part rated only for Vs; that is a design mistake, not a formula mistake, and it belongs in this unit because voltage magnification is the whole point of series Q. Write whether Q is loaded or unloaded next to every bandwidth number. Loaded Q is always lower than unloaded Q when extra positive R appears. Generator Rs in series with a series tank is the usual hidden extra R.
