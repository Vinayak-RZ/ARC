# V-curves, hunting, starting

A synchronous motor is an alternator with shaft power reversed: electrical power in, mechanical power out. It runs at locked synchronous speed. Torque is produced only at \(n_s\); starting therefore needs an auxiliary scheme (damper-winding induction start, pony motor, or a frequency converter). Once synchronized, the field current sets the power factor: overexcited motors draw leading current and are used as rotary capacitors (synchronous condensers). V-curves plot armature current versus field current at constant real power. Hunting is the oscillation of load angle \(\delta\) about the equilibrium, damped by damper windings. This unit is the UG motor and condenser.

The phasor is the generator phasor with current into the machine: \(\mathbf{E}_a=\mathbf{V}_\phi - \mathbf{I}_a R_a - j\mathbf{I}_a X_s\) if \(\mathbf{I}_a\) is motor (into positive terminal) and \(\mathbf{E}_a\) is still the excitation voltage. Many texts keep the generator current convention and flip the sign of \(P\). Pick one and stay with it. Here motor current is into the terminals, \(P>0\) motoring, \(Q>0\) supplying vars to the bus (overexcited, leading PF as seen by the supply — check the local sign of \(Q\)). The supply sees a leading PF when the motor is overexcited: the motor is a source of lagging VARs, i.e. a capacitor.

## Concepts

On an infinite bus, \(V\) and \(f\) are fixed. Mechanical load sets \(P\), hence \(\delta\) via \(P=3 V E_a\sin\delta/X_s\) (cylindrical, \(R_a=0\)). Field current sets \(E_a\), hence \(Q\). If the shaft load increases, \(\delta\) increases, more electrical power is drawn, and speed stays \(n_s\) unless the pull-out torque is exceeded. Pull-out is \(P_\mathrm{max}=3 V E_a/X_s\). A sudden overload that demands more than \(P_\mathrm{max}\) pulls the machine out of step: \(\delta\) slips, torque oscillates, stator current beats, and protection should trip.

V-curves: at fixed \(P\), as \(I_f\) (hence \(E_a\)) varies, \(I_a=\sqrt{P_\mathrm{component}^2+Q_\mathrm{component}^2}/(\sqrt{3}V_\mathrm{line})\) has a minimum at unity PF. That minimum \(I_a\) versus \(I_f\) is the bottom of the V. Family of V’s for different \(P\); inverted V-curves are PF versus \(I_f\). The unity-PF locus in the \(I_a\)–\(I_f\) plane is the line of minima. Underexcited: lagging PF, absorbs VARs (like an induction motor). Overexcited: leading PF, supplies VARs. A synchronous condenser is a motor with an unloaded (or lightly loaded) shaft, \(P\approx 0\), used only for \(Q\).

Hunting: a step in load or in bus angle makes \(\delta\) ring. The swing equation \( (2H/\omega_s)\mathrm{d}^2\delta/\mathrm{d}t^2 = P_m - P_e(\delta) \) is the power-system form; for a motor \(P_m\) is load. Small-signal synchronizing torque \(P_s=\mathrm{d}P_e/\mathrm{d}\delta = 3 V E_a\cos\delta / X_s\). Natural frequency \(\omega_n=\sqrt{\omega_s P_s/(2H)}\). Damper windings produce an asynchronous torque \(\propto s_\mathrm{transient}\) that adds damping \(D\). Without dampers, a turbo rotor still has eddy damping in the forging. Resonance with engine torque pulsations (2-stroke, 4-stroke harmonics) is a classical hunting cause; avoid matching \(\omega_n\) to those pulsations.

Starting:

1. Damper (amortisseur) winding: start as a squirrel-cage induction motor, field winding shorted through a resistor (to limit induced voltage and to add a little extra torque), then at near \(n_s\) apply DC field; the machine pulls into step. Field open at start would see a high AC voltage from transformer action at slip frequency.
2. Pony motor: an auxiliary motor brings the rotor to \(n_s\); then synchronize like a generator.
3. Variable-frequency start: inverter ramps \(f\) from a few hertz with the rotor already excited (true synchronous start). Used on large mills and on PM machines.

Excitation: brushless exciters or slip rings. Loss of excitation on a motor makes it an induction machine on the dampers, drawing heavy lagging VARs, overheating. Loss-of-field protection exists.

Efficiency: same loss inventory as a generator (stator Cu, field Cu, core, F&W, stray). No slip loss of the induction kind in steady synchronous running; damper currents are zero in the ideal steady state.

Salient-pole motors have reluctance torque even at \(E_a=0\) (if they can be started and locked). Reluctance motors as a class are the next unit. A lightly excited salient synchronous motor still has the \(\sin 2\delta\) term.

Power-factor correction: a plant with induction motors (lagging) plus one overexcited synchronous motor can present near-unity PF to the utility. Size the synchronous machine’s \(Q\) capability from its \(I_a\) and \(I_f\) limits, not from nameplate watts alone. The condenser rating is in MVAR.

Counter: a synchronous motor cannot run at a speed other than \(n_s\) in steady state. Speed control means changing frequency (V/f or vector, with a converter) or changing poles (not practical on the fly). It is not a slip machine.

## Equations

Cylindrical motor, \(R_a=0\), current into the motor, \(\mathbf{V}=V\angle 0\), \(\mathbf{E}_a=E_a\angle -\delta\) (\(\delta>0\) motoring):

\[
P=\frac{3 V E_a}{X_s}\sin\delta,\qquad Q=\frac{3}{X_s}(E_a\cos\delta - V)V
\]

with this \(Q>0\) when overexcited (\(E_a\cos\delta>V\)), motor supplying vars (leading PF at the terminals).

Armature current:

\[
\mathbf{I}=\frac{\mathbf{V}-\mathbf{E}_a}{j X_s}\quad (R_a=0).
\]

Pull-out torque \(T_\mathrm{max}=P_\mathrm{max}/\omega_s\).

Swing (per-unit \(H\)):

\[
\frac{2H}{\omega_s}\frac{\mathrm{d}^2\delta}{\mathrm{d}t^2}=P_m-P_e-D\frac{\mathrm{d}\delta}{\mathrm{d}t}.
\]

Synchronizing power coefficient \(P_\mathrm{syn}= \mathrm{d}P/\mathrm{d}\delta\).

Starting as induction: use the cage equivalent of the damper, slip \(s\approx 1\) at start, then \(s\) small at pull-in. Pull-in torque must exceed load torque at the slip where the field is applied.

## Methods

For a specified \(P\) and PF, reconstruct \(\mathbf{I}\) from \(S=P+jQ\) (watch \(Q\) sign), then \(\mathbf{E}_a=\mathbf{V}-\mathbf{I}R_a-j\mathbf{I}X_s\) (motor). Compare \(|E_a|\) to the open-circuit curve to get \(I_f\).

V-curve construction: fix \(P\), vary \(E_a\), compute \(\delta=\arcsin(P X_s/(3 V E_a))\), then \(Q\) and \(I=S/(\sqrt{3}V_L)\). Minimum \(I\) at \(Q=0\). If \(E_a\) is too small for the required \(P\), \(\arcsin\) argument exceeds 1: pull-out, no operating point.

Condenser: \(P=0\), \(\delta=0\) in the lossless model, \(I=(V-E_a)/X_s\) purely reactive. \(E_a>V\) overexcited, leading.

Starting check: induced field voltage at start \(\approx s E_\mathrm{open,rated}\) with \(s=1\), so about the OC voltage at that speed if the field were spinning at \(n_s\) with the same flux — actually the stator flux at line frequency induces a high voltage in an open field. Always close the field through a discharge resistor during induction start.

Hunting estimate: compute \(P_\mathrm{syn}\) at the operating \(\delta\), then \(f_n\). If a diesel generator set has torque pulses at firing frequency, compare.

To reverse a synchronous motor: reverse two stator phases (rotation of the field), with the rotor allowed to re-synchronize. Do not reverse field polarity alone and expect a reversal of shaft rotation; that only flips \(\delta\) sign relative to the same rotating field, i.e. generator versus motor on the same direction if the prime mover allows.

## Mistakes

Using generator KVL with motor current without flipping. Draw the phasor.

Calling overexcited operation lagging. The motor PF is leading when overexcited.

Claiming a synchronous motor’s speed falls with load like a shunt DC motor. It does not, until pull-out.

Starting with the field open. Dangerous induced voltage, weak damper torque.

Applying DC field at large slip. The torque pulsates at slip frequency and may not pull in; the field winding overheats.

Using \(Q=3(E_a-V)V/X_s\) at finite \(\delta\) without the \(\cos\delta\). That formula is only for \(\delta=0\) (condenser).

Treating V-curve minimum as zero current. Minimum is the real-power current, \(I=P/(\sqrt{3}V_L)\) at unity PF, not zero unless \(P=0\).

Ignoring reluctance torque on a salient motor, then being unable to explain a small \(P\) at low excitation.

Sizing a condenser from kW nameplate of a sister motor. MVAR capability depends on \(X_s\), field heating, and stator current, not on a shaft that is not loaded.

Using induction-motor slip formulas for steady synchronous running. Slip is zero in the mean; damper currents are for transients.

Hunting: increasing \(H\) always “helps.” It lowers \(\omega_n\) but also slows the response; damping \(D\) is what kills the ring. Adding \(H\) without \(D\) can move \(\omega_n\) onto a bad resonance.

V-curves in the lab are measured at constant shaft load (a DC generator on the same shaft with a fixed resistor, or a dynamometer) while \(I_f\) is swept. Plot \(I_a\) and PF. The minimum \(I_a\) should sit near unity PF if \(R_a\) is small; a slight offset remains because of resistance and because of core loss. If the V is lopsided, residual instrumentation error or a drifting load is more likely than a new theory. Inverted-V (PF versus \(I_f\)) peaks at 1.0 and falls to leading on the overexcited side and lagging on the underexcited side. Crossing into the underexcited region too far at high \(P\) is how you hit pull-out: the \(\arcsin\) argument \(P X_s/(3 V E_a)\) reaches 1.

Synchronous condenser siting: voltage control on a long feeder or at a bus with many induction motors. The condenser’s \(Q\) is nearly \(3V(E_a-V)/X_s\) at \(\delta=0\). Raising \(E_a\) boosts bus voltage on a weak grid because the exported VARs reduce \(I X\) drop. Unlike a shunt capacitor bank, the condenser can absorb VARs (underexcited) to buck voltage, and it has a transient contribution from the rotating inertia and damper. Unlike a STATCOM, it is a rotating machine with maintenance. UG should be able to compute the current at a stated \(E_a\) and to say which side of \(V\) is leading.

Pull-in versus pull-out: pull-out is the steady synchronous \(P_\mathrm{max}\). Pull-in is the induction-start problem of synchronizing against load torque and inertia when DC excitation is applied. A motor that can pull out at 2 pu torque might still fail to pull in on a high-inertia fan if the damper torque at 5% slip is tiny. Field application too early (large slip) makes \(P\) pulsate at slip frequency with amplitude \(3 V E_a / X_s\); that pulsation can pound a coupling. Relays and auto-synchronizers exist on large motors for a reason. Small lab machines are synchronized by a switch and a hope; still short the field through a resistor until the last moment.
