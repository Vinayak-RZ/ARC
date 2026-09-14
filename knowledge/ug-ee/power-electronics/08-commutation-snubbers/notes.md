# Commutation and snubbers: natural, forced, and protection networks

Commutation is the transfer of current from one switch (or diode) to another. Natural (line or load) commutation uses an AC voltage or a resonant load to bring device current to zero. Forced commutation uses an auxiliary circuit — historically capacitors and auxiliary thyristors — to impose a reverse voltage on an SCR. Snubbers are small R, C, and sometimes D networks that shape \(dv/dt\), \(di/dt\), and peak voltage so the device stays inside SOA (unit 01). UG courses still teach class A–E thyristor commutation because GATE and many Indian syllabi do; they also teach RCD turn-off snubbers on IGBTs and MOSFETs, which is what a modern lab actually solders.

## Concepts

Natural commutation (class F in some older lists, or simply “line commutation”): in a phase-controlled rectifier the incoming AC voltage reverse-biases the outgoing SCR after overlap, for a time long enough that \(t_q\) is satisfied. Load commutation: a resonant or over-excited synchronous machine presents a leading current so a CSI thyristor sees reverse voltage after current transfer. No extra capacitor is dedicated to killing the SCR; the power circuit itself does it. Failure mode: overlap too large, AC voltage too weak, or extinction angle too small — commutation failure, AC short through two bridges or two devices.

Forced commutation is required when the source is DC (choppers, inverters historically built with SCRs). A charged capacitor is switched across the conducting SCR so that current transfers into the capacitor path and the SCR is reverse-biased for \(t_q\). Textbook classes (a common UG list):

- Class A: resonant load commutation (series RLC, current rings through zero).
- Class B: resonant pulse commutation (an LC across the SCR rings a pulse that opposes load current).
- Class C: complementary commutation (two SCRs, capacitor commutates one when the other turns on — McMurray-Bedford family).
- Class D: auxiliary impulse commutation (auxiliary SCR dumps a capacitor into the main SCR).
- Class E: external pulse commutation (a pulse transformer or pulse network).

The student should sketch current paths and write \(v_C=V(1-\cos\omega_0 t)\) or \(i=V\sqrt{C/L}\sin\omega_0 t\) rather than memorize class letters without a circuit. Impulse value \(\int v\,dt\) must exceed \(L I\) to reverse the current, and the reverse-bias interval must exceed \(t_q\).

Modern converters commute by gate turn-off (MOSFET, IGBT, GTO). “Commutation” then means the overlap of voltage and current during switching, plus the diode reverse-recovery spike. Snubbers and layout inductance replace the thyristor capacitor networks.

Snubber roles:

1. \(dv/dt\) limit (turn-off of inductive current, or SCR false triggering). A capacitor across the device, often with a resistor, \(C_s\approx I_0 t_f/(2\Delta V)\) as a first cut, or from \((dv/dt)_{\mathrm{crit}}\).
2. Voltage clamp (energy stored in \(L_{\sigma}\) must not avalanche the die). RCD clamp: diode steers inductor energy into \(C\), resistor dumps it. Polarized (RCD) versus unpolarized (RC).
3. \(di/dt\) limit at turn-on (series saturable inductor or a small linear \(L\), plus gate-resistor control).
4. Lossy versus lossless: an RC snubber dissipates \(\tfrac12 C V^2 f_{sw}\) every cycle if it fully charges; at high \(f_{sw}\) this is intolerable, so low-loss snubbers or just better layout are used.

RC snubber across a TRIAC or SCR in an AC controller damps ringing with the line inductance. Damping factor \(\zeta=R/2\sqrt{C/L_{\sigma}}\) should not leave a high-Q ring that retriggers the device.

RCD turn-off snubber on an IGBT: at turn-off, load current charges \(C_s\) through the diode, so \(v_{CE}\) rises as \(i=C dv/dt\) instead of snapping to the bus plus spike. At turn-on, \(C_s\) discharges through \(R_s\) and the transistor; \(R_s\) must limit discharge current, and the time constant \(R_s C_s\) must finish before the next turn-off. Energy \(\tfrac12 C_s V_{dc}^2\) is lost each cycle in the resistor (plus a bit in the transistor).

Undeland and similar low-loss snubbers, and active clamps, are named in advanced notes. UG numericals stay with RC and RCD.

Gate-drive “snubber” is the gate resistor plus a clamp (TVS, miller clamp) to stop \(dv/dt\)-induced turn-on through \(C_{gd}\). That is still SOA protection.

Overlap in rectifiers (unit 02–03) is a commutation interval of duration \(u/\omega\). The same word “commutation” applies; the mechanism is AC voltage, not a snubber capacitor.

Forced-commutation classes are easier if you refuse to treat the letter as the concept. Ask four questions of any sketch: (1) what charges the commutating capacitor, (2) which switch dumps it into the main SCR, (3) where the load current goes during the reverse-bias window, and (4) how the capacitor is reset for the next cycle. Class C complementary commutation answers (2) with “the other main device of the pair.” Class D answers (2) with “an auxiliary SCR.” Class A answers (1)–(3) with “the load is an RLC that rings through zero without an auxiliary device.” If you can answer the four questions, the letter is optional.

McMurray and McMurray–Bedford inverter legs are the historical three-phase SCR inverter. Complementary capacitors on a centre-tapped DC link commute the two devices of a pole. They show up as figures that look busy; the UG task is to find \(\omega_0\), the peak capacitor current, and whether \(t_q\) fits in the reverse interval. Do not mix those capacitors with the DC-link energy-storage capacitor of a VSI — the latter is millifarads at line-frequency ripple, the former is microfarads at commutation-pulse frequency.

Snubber placement is a layout drawing, not a schematic suggestion. An RCD clamp that is 5 cm from the IGBT module has 50 nH of extra loop and will not clamp the die voltage, only the far-end of the loop. The module’s Kelvin emitter and a laminated bus bar are how industrial inverters avoid heroic snubbers. UG numericals still compute \(C_s=I/(dv/dt)\) because that is examinable; the lab moral is “short loop first.”

Turn-on snubbers (\(di/dt\) inductors) conflict with turn-off snubbers (they store extra \(\tfrac12 L I^2\) that the turn-off network must then eat). Combined (loss-less) snubbers exist; they are over-scope except as a named sentence. Gate resistance is the cheap \(di/dt\) knob for MOSFETs and IGBTs: larger \(R_g\) slows the miller plateau, lowers \(dv/dt\) and \(di/dt\), and raises switching loss. That trade is how you stay inside RBSOA without a 20 W RCD resistor.

Failing a snubber design is often thermal, not dielectric. A 47 nF capacitor on a 600 V, 20 kHz inverter dumps about 170 W if it fully cycles — more than many IGBTs. If the calculation produces a resistor wattage that needs its own heatsink, the answer is not a bigger resistor, it is less capacitance, a clamp that does not discharge to zero, or a slower \(dv/dt\) spec that the device can already survive.

## Equations

Line commutation constraint:

\[
t_{\mathrm{reverse}}=\frac{\gamma}{\omega}>t_q,\qquad \gamma=180^\circ-\alpha-u.
\]

Resonant pulse (class B sketch), \(\omega_0=1/\sqrt{LC}\):

\[
i_C(t)=V\sqrt{\frac{C}{L}}\sin\omega_0 t,\qquad t_{\mathrm{pulse}}=\pi\sqrt{LC}.
\]

Need \(V\sqrt{C/L}>I_{\mathrm{load}}\) so the pulse can drive net SCR current through zero.

Capacitor voltage after a constant-current charge during turn-off (RCD, linearizing):

\[
v_C(t)=\frac{I_0}{C_s}t,\qquad t_v=\frac{C_s V_{dc}}{I_0}.
\]

RC snubber loss (full charge each cycle):

\[
P_{\mathrm{snub}}\approx \tfrac12 C_s V^2 f_{sw}.
\]

\(dv/dt\) from a capacitor and a current \(I\):

\[
\frac{dv}{dt}=\frac{I}{C_s}.
\]

Series \(di/dt\) inductor:

\[
\frac{di}{dt}=\frac{V}{L_{\mathrm{slew}}}.
\]

Damping of \(L_{\sigma}\)–\(C_s\):

\[
R_{\mathrm{damp}}=2\zeta\sqrt{\frac{L_{\sigma}}{C_s}},\qquad \zeta\sim 0.5\text{ to }1.
\]

## Methods

1. Decide natural vs forced. If an AC source or a leading load can reverse the device, size \(\gamma\) against \(t_q\). If the source is DC and the device is an SCR, draw the class A–E network and check pulse current and reverse time.
2. For IGBT/MOSFET, skip class B capacitors unless the question is historical. Design RCD from allowed \(dv/dt\) or from \(L_{\sigma}I^2/2\) energy dumped into \(C_s\), then size \(R_s\) from discharge current and from \(3R_s C_s < T_{\mathrm{on,min}}\).
3. Layout first: every centimetre of loop is nanohenries. Snubbers treat the leftover.
4. Check extra loss \(½CV^2 f\) against the thermal budget (unit 11). If it dominates, reduce \(C_s\) or move to a clamp that does not fully discharge, or to faster devices and tighter layout.
5. SCR \(dv/dt\): compute \(I/C_s\) or \(V/(R_s C_s)\) according to the network; compare with datasheet critical value.
6. Never snubber a dead short: the snubber is across the device, not in place of a fuse.

Worked pattern — RCD: \(I_0=20\,\mathrm{A}\), \(V_{dc}=300\,\mathrm{V}\), want \(dv/dt\le 500\,\mathrm{V/\mu s}\). \(C_s\ge I_0/(dv/dt)=20/5\times 10^8=40\,\mathrm{nF}\). Energy \(½C V^2=1.8\,\mathrm{mJ}\). At 20 kHz, \(P=36\,\mathrm{W}\) in the resistor — possibly more than the IGBT switching loss; redesign layout or accept a higher \(dv/dt\).

## Mistakes

- Using forced-commutation capacitor formulae on an IGBT inverter as if the IGBT needed \(t_q\) reverse bias. It needs a gate turn-off and a diode path.
- Sizing \(C_s\) for \(dv/dt\) and forgetting the \(½CV^2 f\) heater in \(R_s\).
- Placing the snubber capacitor with a long loop; the loop inductance is the original problem.
- Confusing class A (load rings) with class B (LC across the switch).
- Line commutation: measuring \(\gamma\) from the wrong zero (phase vs line).
- Assuming a polarised RCD snubber works in an AC TRIAC circuit (use RC or a bidirectional network).
- Setting \(R_s=0\) so \(C_s\) discharges in a spark through the transistor at turn-on.
- Treating overlap angle \(u\) as a snubber design variable; it is a source-inductance variable.

Commutation is how current changes path; snubbers are how voltage and current stay legal during that change. Drives (next units) assume this has been done so the converter can be treated as an average-voltage source.
