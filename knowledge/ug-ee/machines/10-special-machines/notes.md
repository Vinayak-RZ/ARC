# Stepper, BLDC, reluctance, servo intro

Special machines in a UG EE course are the ones that do not fit the transformer / DC / induction / wound-field synchronous quartet but appear in mechatronics, appliances, and servo drives. This unit is a first look at stepper motors, brushless DC (PM AC with electronic commutation), reluctance machines (switched and synchronous), and the idea of a servo loop around a motor. Equivalent circuits stay simple; the new ideas are discrete stepping, electronic commutation, reluctance torque from \(\mathrm{d}L/\mathrm{d}\theta\), and closed-loop position/speed.

Do not treat BLDC as a DC machine with the brushes hidden. The electromagnetic torque is synchronous, PM-excited; the inverter plus Hall (or encoder) sensors synthesizes the commutator. A stepper is a synchronous machine that is usually run open-loop in steps. A switched-reluctance motor (SRM) has no magnets and no rotor copper; torque is purely reluctance. A servo is a control architecture, not a winding.

## Concepts

Stepper motors: hybrid, variable-reluctance (VR), and PM steppers. A hybrid stepper (the usual NEMA 17/23) has a toothed PM rotor and two (or more) stator phases. Energizing phases in sequence moves the rotor by a fixed angle \(\theta_\mathrm{step}=360^\circ/(N_r N_\mathrm{ph} m)\) depending on full-step versus half-step versus microstep definitions; a common 1.8° hybrid has 200 full steps/rev. Full-step: one or two phases on. Half-step: alternate. Microstepping: sinusoidal currents in the two phases, approximating a rotating field; torque ripple falls, resolution rises, holding torque of a single full step is not simply divided by the microstep count because of the sine/cosine split.

Open-loop stepping assumes the rotor follows. If load torque plus inertia \(J\alpha\) exceeds available torque, the motor misses steps and the controller’s position count is a lie. Pull-in rate is the maximum stepping frequency at which the motor can start/stop without missing steps. Pull-out rate is higher: once running, it can follow faster, but it cannot start at that rate. Mid-frequency resonance (around 100–300 steps/s on small hybrids) can dump torque; microstepping and damping help. Holding torque is the static maximum with phases energized; detent torque is the PM cogging with phases off.

Drive electronics: unipolar (centre-tapped windings, simple transistors) versus bipolar (H-bridge, better copper use). Current chopping (PWM) holds rated current against the RL winding as speed (back-EMF) rises. L/R drives with a series resistor are obsolete thermally.

BLDC: trapezoidal back-EMF PM machine, typically three stator phases, surface magnets, electronic commutation every 60° electrical using Hall sensors. Two phases conduct at a time (120° conduction). Torque \(T=k_t I\) in the ideal trapezoidal overlap. PMSM (PM AC, sinusoidal back-EMF) is the sibling: three-phase sinusoidal currents, Park vector control, smoother torque. UG often says “BLDC” for both. Electrically, \(E=k_e\omega\), \(V=E+IR+L\mathrm{d}i/\mathrm{d}t\), same as DC but \(E\) is AC in each phase. Mechanical commutator is replaced by a six-step inverter. Regenerative braking is natural if the converter can return current.

Reluctance machines: torque \(T=\tfrac12 i^2 \mathrm{d}L/\mathrm{d}\theta\) per phase (singly excited). Switched-reluctance: sequential excitation of stator poles, rotor vanes align, then the next phase. Converter is typically an asymmetric H-bridge per phase (independent phases, fault tolerant). Highly nonlinear: saturation is required for decent torque density; inductance profiles \(L(\theta,i)\) are not a single sine. Noise and torque ripple are the reputation. Synchronous reluctance (SynRM): a rotating stator field like an induction motor, rotor with flux barriers (no cage, or a cage for start). Reluctance torque from \(X_d\neq X_q\). Efficiency can beat an induction motor (no rotor Cu) in some frames; power factor is worse. PM-assisted SynRM adds weak magnets.

Servo intro: a servo motor is a motor plus a feedback device (encoder, resolver, tacho) plus a drive that closes current, speed, and often position loops. Bandwidth of the current loop is highest (kHz), speed loop middle, position loop slowest. Tuning (PI current, PI speed, P or PI position) is control-systems material; the machines point is that the plant is \(T=k t i\), \(J\dot{\omega}=T-T_L\), with electrical lag \(L/R\). AC servos are PMSMs; DC servos are PMDC; both exist. Stepper “servos” close the loop with an encoder to eliminate missed steps (closed-loop stepping).

Other cameo machines: hysteresis motors (smooth, low power, clocks), shaded-pole (cheap fans), universal motors (series wound, AC or DC, high speed appliances — commutation on AC is ugly but cheap), linear induction and linear PM motors (unrolled air gap). Universal motors are series DC machines on AC; torque is unidirectional because \(\phi\) and \(I_a\) reverse together.

Ratings: continuous torque from thermal limits, peak torque from magnetic saturation and inverter current. Servo catalogues list stall torque, rated torque at rated speed, and a speed-torque envelope. Do not size a stepper from holding torque alone if the move is fast; look at the torque-speed curve at the required step rate.

Encoders: incremental A/B/Z, absolute, resolvers (AM modulation, rugged). Hall sensors on BLDC give 60° resolution, enough for six-step, not for sinusoidal FOC (use encoder or observer).

## Equations

Stepper full-step angle (hybrid, typical):

\[
\theta_\mathrm{step}=\frac{90^\circ}{N_r}\quad\text{for two-phase with \(N_r\) rotor teeth in a common construction giving \(1.8^\circ\) when \(N_r=50\)}.
\]

Use the nameplate steps/rev when in doubt: \(\theta=360^\circ/N_\mathrm{steps}\).

Hybrid two-phase microstep currents:

\[
i_A=I_m\cos(k\pi/2N_\mu),\qquad i_B=I_m\sin(k\pi/2N_\mu).
\]

BLDC/PMDC-like averages (six-step):

\[
E=k_e\omega,\qquad T=k_t I,\qquad k_t=k_e\ \text{in SI}.
\]

Reluctance torque (one phase, linear):

\[
T=\frac12 i^2\frac{\mathrm{d}L}{\mathrm{d}\theta}.
\]

Synchronous reluctance power (steady, \(R_a=0\)):

\[
P=\frac{3 V^2}{2}\left(\frac{1}{X_q}-\frac{1}{X_d}\right)\sin 2\delta.
\]

Servo mechanics:

\[
J\frac{\mathrm{d}\omega}{\mathrm{d}t}+B\omega=T_e-T_L,\qquad \theta=\int\omega\,\mathrm{d}t.
\]

Electrical (phase):

\[
v=Ri+L\frac{\mathrm{d}i}{\mathrm{d}t}+e(\theta,\omega).
\]

## Methods

Stepper: convert required shaft resolution to steps, including gear ratio. Check torque at the stepping rate from the manufacturer curve, with a margin (1.5–2) for inertia. Accelerate with a ramp (not a step in frequency) so that \(T=J\alpha+T_L\) stays inside pull-in. If the load can back-drive, use holding current or a brake.

BLDC: read Halls, commutate the inverter (six states). Current control by chopping. For a numerical, treat it as \(V=k_e\omega + I R_\mathrm{eq}\) with \(R_\mathrm{eq}\) the two-phase-on resistance. Speed control is PWM duty on the DC link or on the chops.

Reluctance: integrate coenergy \(W'(i,\theta)=\int\lambda\,\mathrm{d}i\) if \(\lambda(\theta,i)\) is given; \(T=\partial W'/\partial\theta\). Linear \(L(\theta)\) is only a tutorial. For SynRM, use the salient-pole power formula with \(E_a=0\) (no magnets) or small \(E_a\) if PM-assisted.

Servo sizing: worst-case torque = load + \(J_\mathrm{total}\alpha_\mathrm{max}\) + friction. Inertia mismatch \(J_\mathrm{load}/J_\mathrm{motor}\) affects tuning; gearboxes trade torque and inertia reflected as \(J/n^2\). Current loop first (plant \(L,R\)), then speed (\(J,B,k_t\)), then position.

When comparing a stepper and a servo for the same axis: stepper is cheaper and holds with power on without a loop; servo is quieter, faster, and knows if it lost position. Closed-loop stepper sits between them.

## Mistakes

Treating holding torque as available at 2000 steps/s. Torque collapses with speed (back-EMF and inductance).

Open-loop stepping a high-inertia load without an acceleration ramp, then blaming the motor for “lost steps.”

Calling BLDC a DC machine in an equivalent-circuit exam and writing a commutator. Write three AC phases plus an inverter.

Using \(k_t\) in N·m/A with \(k_e\) in V/kRPM without converting; in SI they are equal.

Exciting two SRM phases with a topology that cannot freewheel or PWM, then over-voltaging the DC link at commutation (energy in \(L\) has to go somewhere).

Expecting SynRM to have induction-motor PF. Reluctance machines are thirsty for VARs.

Closing a position loop around a stepper without an encoder and calling it a servo. Open-loop is not a servo.

Reversing only one Hall sensor on a BLDC and expecting smooth rotation. Commutation maps are a cyclic permutation; a single swapped Hall jitters.

Sizing from peak torque as if it were continuous. Thermal time constants of small motors are seconds, not minutes.

Using \(T=\tfrac12 i^2 \mathrm{d}L/\mathrm{d}\theta\) with \(L\) in millihenries and \(\theta\) in degrees, then missing \(\pi/180\). Use radians in SI.

Universal motor on DC versus AC: same series connection, but AC has reactance drop and more sparking; speed on AC is a bit lower for the same RMS voltage.

Ignoring cogging in a PM servo at very low speed. Slot/pole combinations and skew are design, but UG should know cogging is a real torque ripple at the slot frequency.

A stepper current chopper is a small DC–DC story: the winding is \(R,L,E\), the supply is \(V_\mathrm{bus}\) (often 24–70 V, much larger than \(I R\)), and a comparator keeps \(i\) near \(I_\mathrm{set}\). The high bus is what forces current into an inductive winding against back-EMF as speed rises. An L/R drive that uses 5 V on a 5 Ω winding cannot do that. When the chopper saturates (duty 100%) the current falls with speed and torque falls; that is the knee of the torque-speed curve. Microstepping tables that assume the current vector is still at \(I_m\) are then false. Thermal: RMS of a two-phase microstep sinusoid at amplitude \(I_m\) is \(I_m/\sqrt{2}\) per phase if you scale like AC; if you hold the vector at \(I_m\sqrt{2}\) to keep full-step holding, heating is the two-phase-on heating. Read the drive manual before promising 0.8 N·m at 16 microsteps.

BLDC Hall commutation is a state machine of six states. Advance angle (commutating early) can raise high-speed torque a little, like brushes shifted on a DC machine, at the cost of ripple. Sensorless control estimates zero crossings of the silent phase’s back-EMF; it fails at standstill, so a start open-loop or with a pulse injection is required. That is why cheap fans jerk at start. PMSM field-oriented control is smoother but needs a transform (Park) and an angle; it is the servo default.

Switched-reluctance firing: turn on a phase while \(L\) is rising (\(\mathrm{d}L/\mathrm{d}\theta>0\)) for motoring, while \(L\) is falling for generating. Dwell angle and advance are the control knobs, analogous to ignition timing. Saturation makes \(\lambda(\theta,i)\) a family of curves; coenergy differences on that family are the honest torque. Linear \(L(\theta)\) overpredicts at high current because incremental \(L\) falls. Acoustic noise is radial force on the stator yoke at twice electrical frequency; it is not a sign that the torque formula is wrong.
