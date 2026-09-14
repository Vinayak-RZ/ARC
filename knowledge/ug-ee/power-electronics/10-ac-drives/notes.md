# AC drives: V/f, CSI, and cycloconverter introduction

An AC drive supplies a variable-frequency, variable-voltage AC machine — almost always an induction motor at UG core, with a look at synchronous and CSI-fed machines. The converter is a VSI with PWM (units 05–07), a CSI, or a cycloconverter (unit 12). This unit is the electrical interface: why V/f is constant below base speed, how a CSI differs, and where a cycloconverter still appears (large low-speed mills). Vector control and FOC are named as the next course, not derived.

## Concepts

An induction motor’s air-gap flux is roughly \(V_1/(2\pi f)\) if stator resistance and leakage are neglected. Holding \(V/f\) constant holds flux, hence available torque, from near-zero speed up to base speed (rated \(V\) and \(f\)). Below a few hertz, \(IR\) drop is not negligible: a voltage boost (offset) is added so \(\Phi\) does not collapse at start. Above base speed, voltage is clamped at rated and frequency rises: flux falls, torque capability falls, power can stay near rated (field-weakening analog).

Implementation: a diode rectifier (or PWM rectifier) makes a DC bus; a three-phase IGBT VSI synthesizes \(V\) and \(f\) with SPWM/SVPWM. Slip is not commanded directly in open-loop V/f; load torque sets slip, and speed is \(n_s(1-s)\) with \(n_s=120f/P\). Open-loop V/f is cheap and works for fans and pumps. It struggles with fast torque steps, low-speed holding, and regeneration unless a brake chopper or active front end is present. Closed-loop slip compensation measures current or speed and bumps frequency.

Current-source inverter drives: a controlled rectifier plus a DC inductor feeds a CSI that impresses a six-step or PWM current on the machine. Commutation can be load-assisted (over-excited synchronous) or capacitor-assisted (induction). CSI drives handle regeneration naturally if the front-end rectifier can invert, and they have inherent current limit. They are bulky (DC inductor) and less common in new low-voltage products than VSI, but they remain on the UG list.

Cycloconverter drives: a direct AC–AC frequency changer (unit 12) feeding a low-frequency synchronous or induction machine, typically \(f_o\le f_i/3\). High power, low speed, no DC link. Harmonics and pf are poor compared with a PWM VSI. Rolling mills and cement kilns are the story problems.

Soft starters are AC voltage controllers at *fixed* frequency (unit 06). They limit inrush; they do not provide variable-speed torque like a V/f drive. Do not confuse a soft starter with a VFD.

Braking: a VSI with a diode front end cannot dump regenerated energy into the mains. The DC-link voltage rises; a brake chopper plus resistor, or an active front end (AFE), is required. CSI with a dual-converter DC front end can invert. Mechanical and DC-injection braking are named.

PWM-VSI harmonics: high-frequency switching is filtered by leakage inductance; low-frequency harmonics appear in overmodulation and with dead time. Long motor cables plus PWM \(dv/dt\) produce reflected-wave overvoltage at the terminals (a cable-and-filter issue, not a phasor issue).

Multi-level inverters and 400 V vs 690 V buses are industrial notes. UG analysis stays two-level unless a syllabus names NPC.

Open-loop V/f is a feedforward flux estimator that assumes the applied voltage minus a small \(IR\) is entirely back-emf. That is why boost exists and why a wrong boost saturates the machine (too much \(V\) at low \(f\), magnetizing current spikes) or starves it (too little \(V\), torque collapses). A current limit superimposed on the V/f ramp is the poor person’s vector control: if current exceeds a cap, frequency (and voltage) wait. Many cheap VFDs do exactly that. Slip compensation adds a term \(k I_q\) (or measured speed error) to \(f\) so that a loaded motor does not droop as much; it is still not field orientation.

The DC bus of a VSI drive is the energy buffer between line and machine. In motoring, the rectifier fills it and the inverter empties it. In braking, the machine fills it. Capacitor value sets the voltage rise \(\Delta V = \Delta E / (C V)\) for an energy dump \(\Delta E\). A brake resistor is sized from peak regenerative power and from RMS energy over a duty cycle (a hoist lowers often; a spindle decelerates rarely). Active front ends regulate \(V_{dc}\) and can meet harmonic limits on the line; they are PWM rectifiers from units 05–07 running as the drive’s first stage.

CSI drives couple torque to \(I_{dc}\) almost directly, which feels like a DC machine. The price is commutation at the machine terminals. An induction motor does not naturally supply leading current, so capacitors (or a PWM CSI) must. A synchronous motor with a field winding can. LCI starting of large synchronous machines is a standard industrial trick: start in CSI mode, then connect to the AC line. UG problems that give \(I_{dc}\) and ask for \(I_1\) are using the 120° block Fourier coefficient, not a VSI PWM formula.

Cycloconverter mill drives run at a few hertz and tens of megawatts. Torque quality is acceptable because the pulse number is high (36 thyristors) and the mechanical inertia is enormous. They regenerate through the same thyristors. A student who reaches for a 50 Hz cyclo to run a 4-pole 1500 r/min motor has missed the \(f_o\le f_i/3\) bound: that motor wants a VSI. Unit 12 does the thyristor arithmetic; this unit only places the cyclo in the drive taxonomy.

Thermal and cable notes that belong with drives rather than with devices: inverter-grade magnet wire, dV/dt filters on long leads, bearing currents from common-mode PWM voltage. They are named so a lab motor does not get a surprise fluted bearing. They do not change the V/f arithmetic.

## Equations

Synchronous speed:

\[
n_s=\frac{120 f}{P}\ \text{(r/min)},\qquad \omega_s=\frac{4\pi f}{P}\ \text{(mech rad/s)}.
\]

Constant flux (ideal):

\[
\frac{V}{f}=\text{const}=\frac{V_{\mathrm{rated}}}{f_{\mathrm{rated}}}.
\]

Low-frequency boost (first-cut):

\[
V(f)=V_0 + k f,\qquad k=\frac{V_{\mathrm{rated}}-V_0}{f_{\mathrm{rated}}}.
\]

Linear SPWM voltage (from unit 07):

\[
V_{LL,1}=0.612\, m_a V_{dc}.
\]

For a diode rectifier front end, \(V_{dc}\approx 1.35 V_{LL,\mathrm{ac}}\) no-load, sagging with overlap.

Slip and torque (per-phase approximate, Thevenin neglected):

\[
s=\frac{n_s-n}{n_s},\qquad T\approx \frac{3}{\omega_s}\frac{V_s^2 (R_2/s)}{(R_{\mathrm{th}}+R_2/s)^2+(X_{\mathrm{th}}+X_2)^2}.
\]

At constant flux, breakdown torque is roughly constant below base speed. At reduced flux (high \(f\), clamped \(V\)), \(T_{\mathrm{max}}\) falls about as \(1/f^2\) in the simplest model.

CSI fundamental current:

\[
I_{1,\mathrm{rms}}\propto I_{dc}.
\]

Cycloconverter output frequency (three-phase six-pulse family, rule of thumb):

\[
f_o \lesssim \frac{f_i}{3}.
\]

## Methods

1. Below base speed: pick \(f\) from desired \(n_s\), set \(V=(V_{\mathrm{rated}}/f_{\mathrm{rated}})f\) plus boost if \(f\) is small. Check that the VSI can make that \(V\) from the available \(V_{dc}\) (SPWM 0.612, SVPWM 0.707, six-step 0.780).
2. Above base speed: \(V=V_{\mathrm{rated}}\), raise \(f\), accept flux drop. Check maximum inverter frequency and mechanical limits.
3. Start: either V/f ramp (current limited by ramp rate and boost) or a current-regulated start. Compare with a soft starter (fixed \(f\), reduced \(V\)).
4. Regeneration: if the load can overhaul, specify brake chopper energy or an AFE.
5. CSI: size \(I_{dc}\) from torque (current) demand; commutation capacitors or machine excitation must be in the problem or assumed.
6. Cyclo: confirm \(f_o\) is a fraction of line frequency; do not promise 50 Hz out of a 50 Hz cyclo without circulating-current tricks (and even then UG says no).

Worked pattern — V/f: 415 V, 50 Hz, 4-pole. Want 900 r/min. \(n_s\) at 50 Hz is 1500 r/min, so \(f=30\,\mathrm{Hz}\) for 900 r/min synchronous (actual speed a bit less). \(V=415\times 30/50=249\,\mathrm{V}\). Bus from 415 V AC is \(\approx 560\,\mathrm{V}\); SPWM can make \(0.612\times 560=343\,\mathrm{V}>249\,\mathrm{V}\). OK. If the requested speed were 1500 r/min on a 330 V SPWM ceiling, you would be forced into SVPWM, overmodulation, or a higher bus — that check is part of the same method, not a later unit.

## Mistakes

- Changing frequency without changing voltage (saturation at low \(f\), or weak flux at high \(f\) if \(V\) is also reduced).
- Treating a soft starter as a variable-speed drive.
- Using \(V_{LL}=m_a V_{dc}\) without the 0.612 factor.
- Forgetting boost at 2–5 Hz and wondering why the motor will not start.
- Regenerating into a diode bridge with no brake path.
- Setting cyclo \(f_o=50\,\mathrm{Hz}\) from a 50 Hz supply as if it were a VSI.
- Applying DC-machine \(E=V-IR\) directly to an induction motor without a phasor model.
- CSI: opening the DC inductor path during a commutation glitch (huge voltage).

Rated-slip arithmetic: a 4-pole 50 Hz motor with 3% rated slip runs at 1455 r/min at 50 Hz. At 25 Hz with constant flux, rated-slip speed is about 727 r/min, not 750 minus a 50 Hz slip in r/min. Slip is a frequency (rotor current frequency \(s f\)), so the slip *speed* in r/min scales with the actual \(n_s\). Using 45 r/min slip at every stator frequency is a common numerical error.

V/f is the UG default AC drive. CSI and cyclo are the two named alternatives that still appear on papers. Magnetics and thermal (next) decide whether the inverter actually survives the current those drives command. When a problem gives \(V_{dc}\) and a motor voltage, always convert through the PWM law of unit 07 before claiming the drive is “at rated flux.”
