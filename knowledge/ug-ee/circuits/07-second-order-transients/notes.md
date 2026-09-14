# RLC second-order transients

A second-order linear lumped circuit has two independent energy-storage states, typically one L and one C that cannot be merged, or two capacitors (or two inductors) coupled through resistors. The natural response is the solution of a characteristic quadratic: overdamped, critically damped, or underdamped. Series RLC and parallel RLC are the two canonical UG forms. Switching and DC sources add a particular solution; the complete response matches \( v_C(0^+) \) and \( i_L(0^+) \) (or two capacitor voltages).

## Concepts

The series RLC loop obeys \( L \ddot{i} + R \dot{i} + i/C = \dot{v}_s \) or, for source-free, \( \ddot{i} + (R/L)\dot{i} + (1/LC)i = 0 \). The parallel RLC node obeys \( C \ddot{v} + G \dot{v} + v/L = \dot{i}_s \). Both share the undamped natural frequency \( \omega_0 = 1/\sqrt{LC} \) and a damping coefficient \( \alpha \). For series, \( \alpha = R/(2L) \). For parallel, \( \alpha = 1/(2RC) \). The damping ratio \( \zeta = \alpha/\omega_0 \). Roots: \( s_{1,2} = -\alpha \pm \sqrt{\alpha^2 - \omega_0^2} \).

Overdamped \( \alpha > \omega_0 \): two distinct negative real roots (passive); \( x(t) = A_1 e^{s_1 t} + A_2 e^{s_2 t} \). Critically damped \( \alpha = \omega_0 \): \( x(t) = (A_1 + A_2 t) e^{-\alpha t} \). Underdamped \( \alpha < \omega_0 \): \( s = -\alpha \pm j\omega_d \) with \( \omega_d = \sqrt{\omega_0^2 - \alpha^2} \); \( x(t) = e^{-\alpha t}(B_1 \cos\omega_d t + B_2 \sin\omega_d t) \). Underdamped ringing is not “AC from nowhere”; it is energy sloshing between L and C while R dissipates.

Initial conditions: capacitor voltage and inductor current are the states. Their derivatives are not independent; they follow from KCL/KVL at \( t = 0^+ \). For series source-free, \( i(0^+) = i_L(0^+) \) and \( L di/dt|_{0^+} = -v_C(0^+) - R i(0^+) \). Wrongly setting both \( i(0) \) and \( v_C(0) \) as two constants in the same exponential without using the derivative constraint is the usual failed match.

DC forcing: add a constant particular solution (capacitor open, inductor short in the DC equivalent). The natural modes still use the same \( \alpha, \omega_0 \) computed from the \( t>0 \) network with independent sources deactivated. A step voltage in series RLC yields a transient current that starts at 0 if \( i_L(0)=0 \) and ends at 0, with a possible overshoot in \( v_C \) above the source (underdamped).

Quality factor: \( Q = \omega_0 / (2\alpha) \). High Q means slow decay of the envelope and a sharp frequency-domain resonance (later unit). Series RLC: \( Q = \omega_0 L / R = 1/(\omega_0 RC) \). Parallel: \( Q = R/(\omega_0 L) = \omega_0 RC \).

Repeated switching, piecewise sources, and op-amp RLC are still second order if two states remain. Three storage elements generally produce a cubic; UG stops at second order except for a comment.

The phase-plane view (optional but clarifying): plot vC versus iL. Source-free trajectories spiral into the origin if underdamped, or approach along eigendirections if overdamped. Stored energy is a positive-definite ellipse in that plane for uncoupled L and C; R makes the radius shrink. A DC source shifts the attractor to a new point (vC = Vs, iL = 0 for series RLC). Switching moves the attractor; the state cannot jump, so the trajectory starts from the old point and heads toward the new one. This picture prevents the mistake of giving vC a jump “because the source jumped.”

Matching constants without tears: write the general solution for the state you know best (usually vC or iL). Evaluate at t=0+ for one equation. For the second, either differentiate and use the known derivative from KCL/KVL, or evaluate a second variable if its general form is written with the same constants. Two linear equations, two unknowns. If the algebra produces huge cancelling exponentials in an overdamped case (s1 ≈ s2 ≈ −α), the problem is ill-conditioned because you are near critical; use the critical form or keep extra digits.

Laboratory: a series RLC with a square-wave source on a breadboard shows all three dampings by turning a pot for R. Critical is the fastest settling without a ring. Underdamped overshoot on vC can exceed the source; scope probes and capacitor voltage ratings must allow it. The measured ωd from the ring period and the envelope time constant 1/α should reconstruct L and C if R is known. That is a standard circuits-lab report and belongs in this unit's methods even if the numbers live in a notebook.

When both C and L are present but one is in a branch that is a short at DC and open at the switching, still count two states unless a loop of capacitors or cut-set of inductors reduces the order (capacitor loop: voltages are not independent; inductor cut-set: currents are not independent). Order reduction is topological. A capacitor loop with a voltage source is a classic impulse case: voltages must satisfy KVL at 0+, so they jump, and an impulsive current redistributes charge. Laplace with 0− handles it; classical ODE with continuity does not without extra distribution theory.

Forcing functions other than DC: a ramp, an exponential, a sinusoid. The particular solution is a ramp, exponential, or sinusoid of the same frequency (undetermined coefficients). The homogeneous solution is still the same three cases. For a sinusoid that has been on forever, the homogeneous part is zero (phasors). For a sinusoid switched on at t=0, keep both. That last sentence is the bridge to the phasor unit: phasors are the particular solution after e^{st} transients are gone. When reporting an underdamped answer, give α, ωd, and the two constants with units; a plot without numbers is not a complete UG solution.

## Equations

Series: \( \alpha = R/(2L),\quad \omega_0 = 1/\sqrt{LC},\quad \zeta = R/2 \sqrt{C/L} \).

Parallel: \( \alpha = 1/(2RC),\quad \omega_0 = 1/\sqrt{LC},\quad \zeta = (1/(2R))\sqrt{L/C} \).

\( \omega_d = \sqrt{\omega_0^2 - \alpha^2} \) if underdamped.

Source-free series current: \( \frac{d^2 i}{dt^2} + \frac{R}{L}\frac{di}{dt} + \frac{1}{LC} i = 0 \).

Energy: \( w = \frac12 L i_L^2 + \frac12 C v_C^2 \), monotonically nonincreasing if only positive R is present.

Critical resistance series: \( R_\mathrm{crit} = 2\sqrt{L/C} \). Parallel: \( R_\mathrm{crit} = \frac12 \sqrt{L/C} \).

## Methods

Identify series vs parallel (or write the ODE from KVL/KCL if mixed). Compute \( \alpha, \omega_0 \). Classify damping. Write the general natural solution plus DC particular. Apply two initial conditions on the state and on the consistent derivative. Solve 2×2 for constants. Sketch: overdamped never crosses the final value more than once in the classic RC-like shape; underdamped oscillates about the final value inside a decaying envelope.

To find \( dv_C/dt \) at \( 0^+ \), use \( i_C = C dv_C/dt \) and KCL. To find \( di_L/dt \) at \( 0^+ \), use \( v_L = L di_L/dt \) and KVL. Do not differentiate the final formula until constants are known if you are checking.

Design a desired \( \omega_d \) and \( \zeta \) by choosing R, L, C subject to available parts. High L and small C at fixed \( \omega_0 \) changes impedance level. Damping resistor placement (series vs parallel) is a topology choice, not a free extra \( \alpha \) formula.

Worked classification drill: compute α and ω0 first, before writing any A1, A2. If they are close, keep extra digits; if α = 1.01 ω0 you are overdamped with two nearby real poles, and the t e^{−αt} critical formula is a better numerical approximation than subtracting two large exponentials. If a problem gives R, L, C that look “nice” (R² = 4L/C), it is probably critical on purpose. Underdamped constants B1, B2 are not “the peak and the phase” until you convert to D e^{−αt} cos(ωd t − φ); both forms are correct. Report SI units: α in s^−1, ω in rad/s, not hertz unless asked. Convert f = ωd/(2π) only for a scope time-base.

## Mistakes

Using series \( \alpha \) on a parallel circuit. Setting \( \omega_d = \omega_0 \) even when damping is not light. Matching two voltages that are not the two independent states. Forgetting the particular solution when a DC source remains. Claiming overdamped responses oscillate. Using \( Q \) from the wrong topology. Changing \( t \) origin without converting the constants. Treating critical damping as “the fastest without overshoot” in the wrong sense (it is the boundary; among overdamped, smaller \( \zeta \) toward 1 is faster). Writing \( e^{+\alpha t} \) with \( \alpha>0 \). Ignoring that \( v_C \) in series RLC can overshoot a DC step when underdamped, stressing a capacitor beyond the source rating. Using phasors for a transient problem that is not in sinusoidal steady state. Writing ωd in hertz inside a cosine that expects radians per second. Setting both undetermined coefficients from vC(0) alone and ignoring iL(0). Skipping the damping classification and writing a sine anyway. Keep α positive in the exponent.
