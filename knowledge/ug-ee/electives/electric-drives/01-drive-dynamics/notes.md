# Drive dynamics: load torque and stability of equilibrium

An electric drive is a motor plus a mechanical load plus the power converter that feeds the motor. The core machines and power-electronics packs treat \(T(I,\phi)\) and the converter. This unit treats the shaft: equivalent inertia, load-torque types, multi-mass reduction, and whether an equilibrium \((\omega,T)\) is stable. Four-quadrant braking modes are the next unit. Time constants here are mechanical (\(J/B\) and \(J\omega/T\)) unless a problem couples the electrical transient.

## Concepts

Newton on the shaft:

\[
J\frac{\mathrm{d}\omega}{\mathrm{d}t}=T_m-T_\ell(\omega)-B\omega,
\]

with \(J\) the equivalent inertia at the motor shaft, \(T_m\) the electromagnetic motor torque, \(T_\ell\) the load torque referred to the same shaft, and \(B\) viscous friction if not already inside \(T_\ell\). Sign convention: motoring in the forward direction is \(T_m>0\), \(\omega>0\). A hoist lowering a mass may have \(T_\ell\) negative (overhauling). Equilibrium: \(\mathrm{d}\omega/\mathrm{d}t=0\) so \(T_m(\omega)=T_\ell(\omega)\) (including \(B\omega\)). Several intersections can exist; stability of each is a slope test.

Load-torque types (UG catalogue):

- Constant \(T_\ell\) (dry friction, crane holding, cutting at constant force, a hoist of a given mass at a given radius). Coulomb friction reverses with \(\mathrm{sign}(\omega)\).
- Linear viscous \(T_\ell=B\omega\) (some dampers, a crude generator on a fixed resistor if flux is fixed — actually \(T\propto\omega\) for a separately excited DC generator on \(R\)).
- Fan / pump (turbulent): \(T_\ell=k\omega^2\) in one direction; \(T_\ell=0\) or a small windage the other way. Power \(P=T\omega\propto\omega^3\).
- Constant power: \(T_\ell=P/\omega\) (some winding, a lathe in a constant-power region, a vehicle at constant power from the inverter).
- Hoist / elevator: \(T_\ell=T_{\mathrm{gravity}}\pm T_{\mathrm{friction}}\), gravity independent of speed; overhauling when lowering.
- Pulsating: compressor reciprocating, weaving — average plus a periodic component; \(J\) must be large enough that \(\Delta\omega\) is acceptable, or a flywheel is added.

Referring through gears: a load inertia \(J_L\) on a shaft with ratio \(n=\omega_m/\omega_L\) (motor faster for \(n>1\)) appears as \(J_L/n^2\) at the motor. Load torque \(T_L\) appears as \(T_L/n\) (ideal gears). Efficiency \(\eta\) of the gearbox: motoring, \(T_{\mathrm{motor}}=T_L/(n\eta)\); generating/overhauling, \(\eta\) moves to the other side so that losses are still dissipated. Leadscrews: rotary-to-linear \(T=F r\tan(\psi+\phi)\) or the problem’s \(F=T n/r\); UG usually gives an equivalent \(J\) and \(T_\ell\).

Equivalent \(J\) of a multi-motor or a train of inertias: sum \(J_i/n_i^2\). Translational mass \(m\) on a drum of radius \(r\): \(J=m r^2\). Always state which shaft.

Stability of equilibrium (steady operating point): linearize \(J\Delta\dot\omega=(\partial T_m/\partial\omega-\partial T_\ell/\partial\omega)\Delta\omega\). The point is attracting if

\[
\frac{\partial T_m}{\partial\omega}-\frac{\partial T_\ell}{\partial\omega}<0
\]

at the intersection, i.e. the load curve should cross the motor curve with \(T_\ell\) rising through \(T_m\) as \(\omega\) rises, or \(T_m\) falling through \(T_\ell\). Classic picture: a series DC motor (\(T\) high at low \(\omega\), falling) against a fan (\(T_\ell\propto\omega^2\)) is stable; a series motor against a hoist (constant \(T_\ell\)) can run away if the intersection is on the unstable branch or if field is too weak. A separately excited DC motor with a flat \(T_m\) (current-regulated) against a fan is stable. A DC motor with a drooping \(T_m(\omega)\) (armature voltage fixed, \(T=(V-k\omega)/R\cdot k\)) against constant \(T_\ell\) is stable if the droop exists (\(R>0\)). Synchronous motors lock at \(\omega_s\) or pull out — that is a different stability (power angle), not this slope test. Induction-motor steady curve \(T(s)\) against \(T_\ell(\omega)\): the intersection on the right of breakdown torque (low slip) is stable; the intersection on the left (high slip) is unstable for a usual fan or constant \(T_\ell\). Starting must therefore pass through the unstable region dynamically (the \(J\dot\omega\) term) — which it does if \(T_m>T_\ell\) at standstill.

Time to speed: if \(T_m-T_\ell\) is constant, \(\Delta\omega=(T_{\mathrm{net}}/J)t\). If \(T_m=a-b\omega\) and \(T_\ell=c+d\omega\), the equation is first-order linear, time constant \(J/(b+d)\). Fan \(T_\ell=k\omega^2\) against constant \(T_m\) integrates as a tanh or similar; UG often uses piecewise constant average torque or a graphical \(\int J\mathrm{d}\omega/(T_m-T_\ell)\).

Four-quadrant plane of \((T,\omega)\): Q1 forward motoring, Q2 forward braking, Q3 reverse motoring, Q4 reverse braking. A fan is Q1 only. A hoist needs Q1 and Q4 (or Q3 and Q2 depending on how you named “up”). A vehicle needs all four if it must reverse and regenerate. This unit decides which quadrants the *load* occupies; the next unit decides plugging versus regen versus dynamic brake.

Active loads (overhauling) can drive the motor above ideal no-load speed; a mechanical brake or a braking quadrant is mandatory. Passive loads cannot.

Thermal: RMS torque over a duty cycle \(T_{\mathrm{rms}}=\sqrt{(1/t_c)\int T^2\,dt}\) compared with rated torque. Inertia that looks “helpful” for a pulse still heats the motor if \(T\) is large.

## Equations

Shaft:

\[
J\dot\omega=T_m(\omega,u)-T_\ell(\omega),\qquad u=\text{voltage, current, or frequency command}.
\]

Gear reduction \(n=\omega_m/\omega_L\):

\[
J_{\mathrm{eq}}=J_m+\frac{J_L}{n^2},\qquad T_{\ell,\mathrm{eq}}=\frac{T_L}{n\eta}\quad(\mathrm{motoring}).
\]

Translational mass on drum radius \(r\):

\[
J=m r^2,\qquad T=F r.
\]

Fan: \(T_\ell=k\omega|\omega|\) (odd function if a reversible fan; usually one-sided). Power \(P=k\omega^3\).

Separately excited DC, armature voltage control:

\[
T_m=K\phi\frac{V_t-K\phi\omega}{R_a}.
\]

Slope \(\partial T_m/\partial\omega=-(K\phi)^2/R_a<0\).

Induction motor (approximate): stable region \(0<s<s_{\mathrm{bk}}\).

Stability:

\[
\left.\frac{\mathrm{d}T_m}{\mathrm{d}\omega}\right|_*<\left.\frac{\mathrm{d}T_\ell}{\mathrm{d}\omega}\right|_*.
\]

Constant net torque accel:

\[
t=\frac{J\Delta\omega}{T_{\mathrm{net}}}.
\]

Energy to speed: \(\tfrac12 J\omega^2=\int T_{\mathrm{net}}\omega\,\mathrm{d}t\).

Duty RMS:

\[
T_{\mathrm{rms}}=\sqrt{\frac{1}{t_c}\sum T_i^2 t_i}.
\]

## Methods

1. Draw \(T_m(\omega)\) and \(T_\ell(\omega)\) on the same axes. Mark intersections. Apply the slope test at each.
2. Refer all \(J\) and \(T\) to one shaft before writing \(J\dot\omega=\ldots\).
3. Classify the load (constant, viscous, fan, constant power, hoist, pulsating). Assign quadrants.
4. Time to speed: if \(T_{\mathrm{net}}\) is not constant, integrate \(\mathrm{d}t=J\mathrm{d}\omega/T_{\mathrm{net}}\) piecewise or use the closed form for linear droop.
5. Check adhesion / stall: at \(\omega=0\), is \(T_m(0)>T_\ell(0)\)? If not, the drive never starts (unless a clutch or a start winding).
6. RMS torque on a given cycle; compare with nameplate.
7. Overhauling: if \(T_\ell\) drives \(\omega\) above the motor no-load point, specify a brake (next unit).

Worked pattern — gear: motor \(J_m=0.4\,\mathrm{kg\cdot m}^2\), load \(J_L=16\,\mathrm{kg\cdot m}^2\), \(n=8\), \(\eta=1\). \(J_{\mathrm{eq}}=0.4+16/64=0.65\,\mathrm{kg\cdot m}^2\). A 80 N·m load torque is \(10\,\mathrm{N\cdot m}\) at the motor.

Worked pattern — slope: DC motor \(T_m=40-0.80\omega\), fan \(T_\ell=0.020\omega^2\). Intersection: \(40-0.80\omega=0.020\omega^2\), \(\omega^2+40\omega-2000=0\), \(\omega=20\,\mathrm{rad/s}\) (positive). Slopes: \(\mathrm{d}T_m/\mathrm{d}\omega=-0.80\), \(\mathrm{d}T_\ell/\mathrm{d}\omega=0.040\omega=0.80\). \(-0.80<0.80\), stable.

## Mistakes

Adding \(J_L\) to \(J_m\) without \(1/n^2\). Using \(n\) as \(\omega_L/\omega_m\) in one equation and the reciprocal in the next. Stability test as “\(T_m>T_\ell\)” (that is acceleration, not linearized stability). Treating the high-slip induction intersection as a usable running point. Fan torque \(\propto\omega\) (that is viscous). Constant-power load \(T\propto\omega\). Forgetting that Coulomb friction flips sign at reversal (a dead band at \(\omega=0\)). Applying motoring gearbox \(\eta\) on an overhauling shaft without moving \(\eta\). Time to speed using \(J\omega/T_m\) while ignoring \(T_\ell\). RMS current from arithmetic mean torque. Synchronous-machine pull-out treated with the DC slope test. Reporting \(J\) in kg·m instead of kg·m².

A stable equilibrium is still unreachable if \(T_m(0)<T_\ell(0)\). The slope test is local; starting is global.

Current-regulated drives make \(T_m\) almost independent of \(\omega\) (flat). Stability then requires \(\mathrm{d}T_\ell/\mathrm{d}\omega>0\) (fan, viscous). A hoist with a flat \(T_m\) and constant \(T_\ell\) is neutrally sitting wherever you hold it — speed is an integrator; that is why hoists need a speed loop and a mechanical brake at rest, not an open-loop current.

Pulsating loads: the mean intersection can be stable while \(\omega\) still wobbles. Size \(J\) from \(\Delta\omega\approx (\Delta T)/ (J\Omega_{\mathrm{pulse}})\) or from a given flywheel coefficient. Do not call the wobble “instability” if it is a forced oscillation.

Closed-form accel for linear droop: \(T_{\mathrm{net}}=T_0-B_{\mathrm{eq}}\omega\) gives \(\omega(t)=(T_0/B_{\mathrm{eq}})(1-e^{-t/\tau})\) with \(\tau=J/B_{\mathrm{eq}}\). The initial slope is still \(T_0/J\). Students who report only the time constant and forget the final speed \(\omega_\infty=T_0/B_{\mathrm{eq}}\) have solved the homogeneous equation. Fan against constant \(T_m\): \(\mathrm{d}\omega/\mathrm{d}t=(T_m-k\omega^2)/J\), separate variables, \(t=(J/(2\sqrt{k T_m}))\ln|( \sqrt{T_m}+ \omega\sqrt{k})/(\sqrt{T_m}-\omega\sqrt{k})|\) toward \(\omega_\infty=\sqrt{T_m/k}\). That is the tanh story; a numerical midpoint \(T_{\mathrm{net,avg}}\) is accepted on a UG paper if the problem did not ask for the integral.

Multi-mass: two inertias and a shaft stiffness \(K_s\) have a torsional mode \(\omega_n=\sqrt{K_s(1/J_1+1/J_2)}\). If a step of motor torque rings that mode, the “equivalent single \(J\)” model is too crude for the first 50 ms but still right for the seconds-scale speed rise. This unit keeps the single-mass model unless \(K_s\) is given. Gear backlash is a dead-band in \(T\), not a second inertia.

Hoist numbers: mass \(m\), drum \(r\), counterweight \(m_c\). Net gravity torque \((m-m_c)gr\) plus friction. Raising \(m>m_c\) is Q1; lowering is overhauling Q4 if the net gravity exceeds friction. Counterweight sizing is a dynamics problem before it is a converter-quadrant problem. Elevator codes require a mechanical brake regardless of how pretty the electrical equilibrium is.

Temperature and altitude derate \(T_{\mathrm{rated}}\) on the nameplate; they do not change \(J\). A drive that was stable at rated flux can lose \(\partial T_m/\partial\omega\) if field weakening flattened the DC curve (smaller \(K\phi\), smaller droop \((K\phi)^2/R_a\)). Recheck the slope at the weak-field intersection; a fan that was fine at base speed can still be fine, a constant \(T_\ell\) hoist is more integrator-like.

When the problem gives a speed–torque table rather than a formula, graphical intersection plus a finite-difference slope is the method. Do not fit a high-order polynomial unless asked; two points around the crossing are enough for the sign of \(\mathrm{d}T_m/\mathrm{d}\omega-\mathrm{d}T_\ell/\mathrm{d}\omega\). If those two points give a positive net slope, the equilibrium is unstable and the plot needs another intersection or a start-up check.
