# Four-quadrant operation: plugging, regenerative, and dynamic braking

Unit 01 decided whether the load overhauls and which \((T,\omega)\) quadrants appear. This unit is how the drive produces a braking torque: regenerative (energy to the supply or DC bus), dynamic / rheostatic (energy to a resistor), and plugging / reverse-voltage (energy to heat plus supply). DC machines make the signs obvious; induction machines use the same names with slip \(s>1\) (plugging) or \(s<0\) (regeneration). Converter quadrant capability is the power-electronics cousin; here the machine and energy path are the core.

## Concepts

Quadrants again, machine convention: Q1 \(T>0,\omega>0\) forward motoring; Q2 \(T<0,\omega>0\) forward braking; Q3 \(T<0,\omega<0\) reverse motoring; Q4 \(T>0,\omega<0\) reverse braking. A braking mode is a way to get \(T\) opposite to \(\omega\).

Regenerative braking: the machine operates as a generator, \(E_a>V_t\) on a DC armature (or slip negative on an induction machine connected to a fixed-frequency supply, or a VSI that lets power reverse into the DC link). Energy \(\int T\omega\,\mathrm{d}t\) (minus losses) returns to the source. Requirements: a path for reversed current (dual converter, anti-parallel chopper, active front end, or a DC machine on a reverse-current converter), and a sink (the AC mains, a battery, or another motoring load on a DC bus). A diode-front-end VSI cannot regenerate to the AC line; the bus voltage rises and a brake chopper must dump energy unless an AFE is fitted. Speed must be high enough that generated voltage reaches the supply: a separately excited DC machine on a fixed \(V_t\) regenerates only above the no-load speed corresponding to that \(V_t\) (or you lower \(V_t\) first — field or armature control). Induction machine on a 50 Hz line regenerates only above synchronous speed (overhauling). A V/f inverter can regenerate at any speed if the bus can accept power, because synchronous speed is moved below \(\omega\).

Dynamic (rheostatic) braking: disconnect the AC or DC supply and dump generated energy into a resistor. DC machine: field remains excited, armature onto \(R_b\), \(I_a=E_a/(R_a+R_b)\), \(T=K\phi I_a\) braking. Induction machine: DC injection into the stator (DC dynamic braking) produces a stationary field; rotor currents at slip frequency \(\approx\omega\) heat the rotor. Or a chopper on the VSI DC link dumps into \(R_b\) while the inverter still controls torque — that is “dynamic” from the grid’s point of view even though the machine is in a generating quadrant relative to the inverter. Energy never returns to the AC mains. Resistor rating is energy \(\tfrac12 J\omega^2\) plus any gravitational energy on a descending hoist, with a duty cycle.

Plugging (reverse-current braking): reverse the supply polarity (DC armature or two stator leads of an induction machine) while the shaft still runs forward. DC: \(I_a=(-V_t-E_a)/R_a\) is huge; a limiter resistor is mandatory. Energy from the supply and from the inertia both heat \(R_a\) (and \(R_{\mathrm{ext}}\)). Induction: slip \(s=(n_s-(-\,n))/n_s=2-s_{\mathrm{old}}\approx 2\) at the instant of plugging from near \(n_s\); torque is the high-slip value, heating \(I^2R\) in the rotor is severe. Plugging is fast and brutal. It does not recover energy. A zero-speed detector must open the reverse contactors or the machine re-accelerates in reverse (plug-to-reverse, which may be intended on a reversing mill).

Comparison for a DC separately excited machine at speed \(\omega\), \(E_a=K\phi\omega\):

- Regen: \(I_a=(E_a-V_t)/R_a\) with \(V_t\) set below \(E_a\) (or current-regulated). Supply absorbs \(V_t I_a\).
- Dynamic: \(V_t=0\) effectively, \(I_a=E_a/(R_a+R_b)\). All electrical energy in the resistors.
- Plugging: \(I_a=(E_a+V_t)/(R_a+R_{\mathrm{st}})\). Supply still delivers \(V_t I_a\) into the resistors.

Mechanical power \(P_{\mathrm{mech}}=T\omega=E_a I_a\) (DC, generating sign). That identity picks the energy split.

Induction-motor map: motoring \(0<s\le 1\); generating \(s<0\); plugging \(s>1\). A VSI with field orientation can put the machine at any slip relative to the commanded vector; the *grid* still sees regen only if the DC bus exports. UG problems that say “AC supply plugging” mean two-lead reversal, not vector control.

Mechanical brake: at rest a hoist must hold without relying on \(T_m\). Electrical braking torque goes to zero as \(\omega\to 0\) for regen and dynamic on a DC machine (\(E_a\to 0\)) and for induction regen; plugging still produces torque at zero speed (it is actually starting torque in reverse) — which is why you must cut plugging at zero if you wanted a stop. DC injection still produces torque near zero. A shaft brake is the safety layer.

Energy accounting on a descending hoist: gravitational power \(mgv\) plus the change in \(\tfrac12 J\omega^2\). If regen, the converter exports most of \(mgv\). If dynamic, \(R_b\) absorbs it. If plugging, the supply may still *import* power while the mass descends — the least efficient stop.

Traction: regenerative on a receptive DC third rail; rheostatic when the line is non-receptive; blended. That is utilization unit 02 meeting this unit.

## Equations

DC armature, motoring: \(V_t=E_a+I_a R_a\), \(E_a=K\phi\omega\), \(T=K\phi I_a\).

Regenerative (current reversed, \(I_a>0\) generating):

\[
E_a=V_t+I_a R_a,\qquad T=K\phi I_a\ \text{(braking)}.
\]

Dynamic:

\[
I_a=\frac{E_a}{R_a+R_b},\qquad T=K\phi I_a.
\]

Plugging:

\[
I_a=\frac{V_t+E_a}{R_a+R_{\mathrm{ext}}}.
\]

Kinetic energy: \(W=\tfrac12 J\omega^2\). Power to a dynamic resistor: \(I_a^2(R_a+R_b)\) (includes armature copper). Mechanical power into the machine: \(E_a I_a\).

Induction slip:

\[
s=\frac{\omega_s-\omega}{\omega_s}.
\]

Plugging from speed \(\omega\) with reversed sequence: synchronous speed \(-\omega_s\), \(s=(\,-\omega_s-\omega)/(-\omega_s)=1+\omega/\omega_s\). Near full speed, \(s\approx 2\).

Regen on a fixed-frequency bus: \(\omega>\omega_s\), \(s<0\).

Brake chopper on a VSI bus (energy dump \(\Delta E\) into C):

\[
\Delta V\approx \frac{\Delta E}{C V_{\mathrm{dc}}}.
\]

If \(\Delta V\) would exceed the trip, \(R_b\) must take \(\Delta E\).

## Methods

1. Identify quadrant and whether the source can absorb power. Choose regen vs dynamic vs plugging.
2. DC: write \(E_a=K\phi\omega\), then the correct \(I_a\) equation for the mode. Limit \(|I_a|\) with \(R_{\mathrm{ext}}\) if needed. \(T=K\phi I_a\).
3. Energy: \(\tfrac12 J\omega^2\) plus \(mgh\) on a hoist. Assign it to supply, \(R_b\), or \(R_a\).
4. Induction: compute \(s\) after the switching event. Do not use the small-slip torque formula at \(s=2\).
5. Stop at zero: schedule a mechanical brake or DC injection; do not leave plugging contactors in.
6. Converter: diode rectifier + VSI ⇒ brake chopper for dynamic; AFE or thyristor dual converter ⇒ regen possible.
7. Plot \(T(\omega)\) in Q2 for each mode — plugging torque is large at high speed, dynamic falls with \(\omega\), regen exists only above a threshold on a fixed \(V_t\).

Worked pattern — dynamic: \(E_a=220\,\mathrm{V}\), \(R_a=0.50\,\Omega\), \(R_b=1.50\,\Omega\), \(K\phi=2.0\,\mathrm{V\cdot s/rad}\). \(I_a=220/2.00=110\,\mathrm{A}\), \(T=220\,\mathrm{N\cdot m}\), \(P_{\mathrm{mech}}=24.2\,\mathrm{kW}\).

Worked pattern — plug current without \(R_{\mathrm{ext}}\): \(V_t=220\), \(E_a=200\), \(R_a=0.50\), \(I=(420)/0.50=840\,\mathrm{A}\) — why \(R_{\mathrm{ext}}\) exists.

## Mistakes

Calling plugging “regenerative” because the kinetic energy disappeared (it became heat). Regenerating into a diode front end with no chopper. Plugging without a current-limit resistor. Using motoring \(V=E+IR\) with the same signs in Q2. Induction regen below synchronous speed on a *fixed* 50 Hz bus. Leaving plugging on through zero speed when a stop was required. Dynamic braking with the field open on a DC machine (\(E_a=0\), no torque). Using \(s=2-s\) with \(s\) already the plugging slip (double count). Energy \(\tfrac12 J\omega^2\) with \(\omega\) in r/min. Assuming a series DC motor can dynamically brake easily (field is in series with the armature you just opened — you need a separate field supply or a reversed series connection). VSI “plugging” as two-lead reversal at PWM frequency — that is not how a VSI is operated; reverse the torque command instead.

Field weakening in braking: lowering \(\phi\) lowers \(E_a\) and can *prevent* regen into a high \(V_t\). Raise \(\phi\) (rated field) to regen from a given speed, or lower \(V_t\).

Thermal: plugging from full speed even once can exceed rotor thermal limits on a large induction machine. Dynamic-brake resistors have a peak energy and an RMS power. Regen is the only mode that does not heat a dedicated resistor — it heats the supply cables instead, which is usually fine.

Four-quadrant converters (H-bridge, dual converter, VSI+AFE) make regen the default. One-quadrant converters force dynamic or mechanical braking. Match the converter to the load quadrants from unit 01 before choosing a braking slogan.

Dynamic braking of a DC machine is first-order in \(\omega\) if \(\phi\) is fixed: \(T=K\phi E_a/(R_a+R_b)=(K\phi)^2\omega/(R_a+R_b)\), so \(J\dot\omega=-B_{\mathrm{eq}}\omega\) and \(\omega(t)=\omega_0 e^{-t/\tau}\) with \(\tau=J(R_a+R_b)/(K\phi)^2\). The constant-torque stopping time \(J\omega/T(0)\) underestimates the tail; it is a lower bound only if you take \(T(0)\) as the initial (largest) torque. Energy in the resistor is still \(\tfrac12 J\omega_0^2\) minus whatever friction ate, regardless of \(\tau\). Choosing \(R_b\) is a current-limit choice (\(I_a(0)=E_a/(R_a+R_b)\le I_{\max}\)) and an energy-rate choice (peak kW \(E_a I_a\)).

Induction DC-injection: a DC stator current makes a fixed mmf; rotor frequency is the mechanical frequency. Torque exists down to low speed and dies at rest except for a small reluctance/cogging leftover that you must not count on. Injection current is thermally limited in the stator. It is the usual “stop and hold almost” trick on a VSI that has no brake chopper and a diode front end — actually the VSI can still do vector braking into the bus until \(V_{\mathrm{dc}}\) trips, then DC injection or a mechanical brake.

Plugging energy on DC, from \(\omega_0\) to rest, with constant \(V_t\) and \(R_{\mathrm{tot}}\): both the supply and the inertia feed the resistor. Supply energy \(V_t\int I\mathrm{d}t\) is not small. That is why plugging a hoist on the way down can *increase* the substation kWh. Regen decreases it. If a numerical asks “energy taken from the supply during the stop,” plugging is the mode where that number is positive and large.

Zero-speed detection: a tachometer, a back-emf relay, or a frequency estimate on an encoder-less drive. Contactorship that waits a fixed 2 s will either clip a high-inertia train too early (still fast, mechanical brake slams) or too late (reverse acceleration). The method is “measure \(\omega\), then open.”

Two-quadrant chopper (motoring + regen in one direction) covers a hoist that never reverses rotation if the mechanical arrangement never needs Q3. A vehicle that must reverse needs four quadrants or a reversing contactor plus two. Draw the load’s \((T,\omega)\) orbit before shopping for converters.
