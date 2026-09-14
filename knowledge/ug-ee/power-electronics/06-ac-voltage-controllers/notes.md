# AC voltage controllers: integral-cycle and phase AC control

An AC voltage controller (AC chopper, AC regulator) produces a variable RMS AC voltage at the same frequency as the source by switching thyristors (or TRIACs) in series with the load. No DC link. Two UG methods dominate: phase-angle control (delay \(\alpha\) every half-cycle) and integral-cycle (on–off whole cycles, burst firing). Applications: heater control, lighting (historically), soft-start of induction motors, transformer tap substitutes. This is not a cycloconverter (which changes frequency) and not an inverter.

## Concepts

Phase control with two anti-parallel SCRs (or one TRIAC) in series with a resistive load: each device fires at angle \(\alpha\) after the voltage zero. Load voltage is a sliced sinusoid. RMS load voltage is

\[
V_{L,\mathrm{rms}}=V_m\sqrt{\frac{1}{2\pi}\left(\pi-\alpha+\frac12\sin 2\alpha\right)}=V_s\sqrt{\frac{\pi-\alpha+\tfrac12\sin 2\alpha}{\pi}}
\]

with \(V_s=V_m/\sqrt{2}\) the source RMS and \(\alpha\) in radians. At \(\alpha=0\), full voltage. At \(\alpha=\pi\), zero. Harmonics: odd multiples of line frequency, plus a fundamental that lags. Power factor is poor at large \(\alpha\) because both distortion and displacement appear. For a purely resistive load the current copies the voltage; average power is \(V_{L,\mathrm{rms}}^2/R\).

Inductive load: current lags, so the device that was conducting continues past the voltage zero until current zero (extinction angle \(\beta>\pi\)). The next device cannot take over until it is forward-biased and gated. If \(\alpha\) is less than the load phase angle \(\phi=\arctan(\omega L/R)\), the controller may lose control (firing into a still-conducting complementary path, or the requested \(\alpha\) is before current zero). The practical lower bound is \(\alpha\ge\phi\). Extinction \(\beta\) solves a transcendental equation from the RL current expression. UG problems often give \(\alpha\) and \(\phi\) and ask whether conduction is possible, or they stay with resistive loads.

Extinction angle method and Fourier analysis of the chopped wave are exam staples. The fundamental current’s phase relative to voltage is not \(\phi\) of the load alone, because the waveform is not sinusoidal.

Integral-cycle (burst, cycle-selection, on–off control): the switch is on for \(n\) whole cycles and off for \(m\) whole cycles. RMS voltage is \(V_s\sqrt{n/(n+m)}\). Harmonics are subharmonics of the line frequency (flicker). Heaters with long thermal time constants tolerate this; incandescent lamps and motors generally do not (light flicker, torque pulsation). Zero-crossing switching reduces EMI compared with mid-cycle phase cuts. Duty of the burst \(D=n/(n+m)\) is not the same object as chopper \(D\), but the RMS scaling \(\sqrt{D}\) is analogous.

Sequence control and transformer tap changing: several phase-controlled stages in series with transformer sections can improve pf relative to a single large \(\alpha\). Named, not designed here.

Three-phase AC controllers: three pairs of anti-parallel devices in the three lines, or devices in a delta. Line-to-line chopped waveforms depend on whether two or three phases conduct. RMS formulae are messier; UG often asks conduction diagrams and the legal \(\alpha\) range (typically \(0\) to \(120^\circ\) or \(150^\circ\) depending on the connection). Never copy the single-phase RMS formula onto a three-phase controller without re-deriving.

Soft start of an induction motor: AC voltage controller ramps \(\alpha\) down so voltage rises, limiting inrush. Torque of a squirrel-cage motor at start scales roughly as \(V^2\), so this is a light-load starter, not a high-torque starter (contrast with V/f VSI drives).

TRIAC notes: quadrants I and III are common for AC regulators; gate sensitivity differs by quadrant. \(dv/dt\) false turn-on is a TRIAC specialty — snubbers (unit 08) appear across the device. An SCR pair can be more robust at high current.

Compared with a tap-changing autotransformer: the controller is smaller and faster but dirtier electrically (harmonics, EMI, pf). Compared with a DC chopper plus inverter: the AC controller cannot change frequency.

Two anti-parallel SCRs must be considered as a pair with a shared RC snubber and a gate-isolation transformer (or two optos). The device that has just turned off sees a \(dv/dt\) set by the other device’s turn-on into the line inductance; that is why unit 08 is not optional even for a “simple” heater controller. A TRIAC collapses the pair into one die and one gate, which is convenient at a few tens of amperes and inconvenient when \(dv/dt\) immunity and commutation of an inductive load (quadrant IV gating) become the story. For UG numericals, treat the pair as ideal switches that close at \(\alpha\) and open at current zero.

The RMS integral is worth doing once by hand so it is not magic. Load voltage is \(V_m\sin\theta\) from \(\alpha\) to \(\pi\) and again from \(\pi+\alpha\) to \(2\pi\) (resistive). Square, integrate, divide by \(2\pi\), square-root. The \(\sin 2\alpha\) term is the leftover of \(\sin^2\). If \(\alpha=0\), the formula must collapse to \(V_m/\sqrt{2}\). If \(\alpha=\pi/2\), it must collapse to \(V_m/2\) (which is \(V_s/\sqrt{2}\)). Those two checkpoints catch degree/radian errors. Power on a resistor is never the average of \(v\), which is zero over a cycle; it is \(V_{\mathrm{rms}}^2/R\).

Integral-cycle control is how a kiln or a water heater is actually run when flicker is acceptable. Subharmonics at \(f_i/(n+m)\) modulate the envelope. A 5-cycle period (as in a 2-on, 3-off example) puts energy at 10 Hz on a 50 Hz line, which lights hate and thermal masses ignore. Standards on flicker exist; UG problems instead ask you to convert a requested power fraction into \(n/(n+m)\) with small integers. Sequence control — several transformer taps each with their own pair of SCRs — reduces harmonic content relative to a single deep \(\alpha\) on the full voltage, at the cost of more devices. Named only.

Three-phase controllers in star with line devices have distinct \(\alpha\) regions because the number of conducting devices changes. For small \(\alpha\), three devices can conduct and the load sees nearly full line voltages with small slices missing. For large \(\alpha\), only two devices conduct at a time and the third load terminal floats. Writing a single RMS formula that pretends otherwise is the usual mistake. If an exam asks for a number, it will specify connection (star/delta, 3-wire/4-wire) and often restrict \(\alpha\) to one band.

Induction-motor soft start with an AC controller reduces voltage at slip = 1, so torque (which scales as \(V^2\) near start in the simple model) falls as well as current. A conveyor that needs breakaway torque may not move until \(\alpha\) is small, at which point the inrush is back. A V/f VSI (unit 10) is the tool that keeps flux (hence torque) while limiting current by ramping frequency. Use the AC controller when the load is a heater or a fan that may start unloaded.

## Equations

Resistive single-phase, source \(v=V_m\sin\omega t\), firing \(\alpha\):

\[
V_{L,\mathrm{rms}}=V_m\sqrt{\frac{\pi-\alpha+\tfrac12\sin 2\alpha}{2\pi}},\qquad P=\frac{V_{L,\mathrm{rms}}^2}{R}.
\]

Control range: \(0\le\alpha\le\pi\).

Input power factor (resistive, neglecting device drops):

\[
\mathrm{pf}=\frac{V_{L,\mathrm{rms}}}{V_s}=\sqrt{\frac{\pi-\alpha+\tfrac12\sin 2\alpha}{\pi}}.
\]

Integral-cycle, \(n\) on, \(m\) off, whole cycles:

\[
V_{L,\mathrm{rms}}=V_s\sqrt{\frac{n}{n+m}},\qquad P=P_{\mathrm{full}}\frac{n}{n+m}.
\]

RL load, \(\phi=\arctan(\omega L/R)\), \(\alpha\ge\phi\). Current for \(\omega t\in[\alpha,\beta]\):

\[
i(\theta)=\frac{V_m}{Z}\left[\sin(\theta-\phi)-\sin(\alpha-\phi)e^{-(\theta-\alpha)/\tau_\theta}\right],
\]

with \(Z=\sqrt{R^2+\omega^2 L^2}\), \(\tau_\theta=\omega L/R\), and \(\beta\) from \(i(\beta)=0\). Conduction angle \(\gamma=\beta-\alpha\).

Three-phase fully controlled AC controller (star load, devices in lines) — RMS line current expressions depend on \(\alpha\) bands \(0\)–\(60^\circ\), \(60^\circ\)–\(90^\circ\), \(90^\circ\)–\(150^\circ\). Use the piecewise conduction map rather than a single closed form unless the question specifies the band.

## Methods

1. Resistive vs RL: if \(L=0\), use the RMS integral of the sliced sine. If \(L\neq 0\), first compute \(\phi\), refuse \(\alpha<\phi\), then solve \(i(\beta)=0\) if a conduction angle is asked.
2. Power from RMS on resistors. Do not use \(V_m I_m/2\) on a chopped wave.
3. Integral-cycle: count whole cycles; RMS scales as square root of on-fraction; average power scales as on-fraction (for heaters).
4. Harmonic / flicker: phase control → odd harmonics of 50/60 Hz; integral-cycle → subharmonics. Pick the method to match the load’s thermal and visual time constants.
5. Three-phase: sketch which phases conduct. When a device in one line is off, the load star-point shifts. Compute line voltages from the conducting pair.
6. TRIAC/SCR rating: peak voltage \(\sqrt{2}V_s\), RMS current from the chopped waveform, \(dv/dt\) snubber.

Worked pattern — heater: 230 V, \(R=20\,\Omega\), \(\alpha=60^\circ=\pi/3\). \(\pi-\alpha+\tfrac12\sin 120^\circ=3.1416-1.0472+0.433=2.527\). \(V_{L,\mathrm{rms}}=230\sqrt{2.527/\pi}=206\,\mathrm{V}\). \(P=2120\,\mathrm{W}\) versus full \(2645\,\mathrm{W}\).

## Mistakes

- Using \(V_L=V_s(1-\alpha/\pi)\) (that is not the RMS of a sliced sine).
- Mixing degrees and radians inside \(\sin 2\alpha\).
- Phase-controlling an RL load with \(\alpha<\phi\) and still using the resistive formula.
- Treating integral-cycle RMS as \(V_s n/(n+m)\) instead of \(V_s\sqrt{n/(n+m)}\). Power *does* scale as \(n/(n+m)\) on a resistor; voltage RMS does not.
- Calling an AC voltage controller a cycloconverter. Frequency is unchanged.
- Copying single-phase RMS onto three-phase line quantities.
- Forgetting that a TRIAC must block in both polarities; PIV is the peak AC.
- Using average voltage of the sliced sine as if it fed a DC motor. This converter’s load is AC; average of a symmetric sliced sine is zero.

Gate isolation and zero-cross detection are the two extra circuit blocks a lab controller actually needs. Phase control fires mid-cycle, so the detector is a zero-voltage reference for \(\alpha\), not a command to switch at the zero. Integral-cycle uses the same detector as the switch command. Mixing the two in firmware is how you accidentally build a flicker machine while trying to build a heater.

AC voltage control is line-frequency chopping without a DC bus. Cycloconverters (unit 12) reuse thyristor phase control but synthesize a *lower* frequency.
