# RC and RL first-order transients

A first-order linear circuit has a single independent energy-storage element, or several that can be combined into one equivalent capacitor or inductor as seen by a Thévenin resistor. The natural response is a single exponential. Switching, initial conditions, and the forced DC (or sudden constant) source determine a unique \( v_C(t) \) or \( i_L(t) \). This is the core of UG transients before RLC.

## Concepts

A capacitor cannot change voltage instantly if the current is finite, because \( i = C dv/dt \). An inductor cannot change current instantly if the voltage is finite, because \( v = L di/dt \). Switching theorems: at \( t = 0^+ \), capacitor voltages and inductor currents equal their \( 0^- \) values unless an impulse of current or voltage is present (rare in UG resistive switching). Capacitor current and inductor voltage may jump.

The time constant \( \tau \) is \( RC \) for a capacitor looking into resistance \( R \) with independent sources deactivated, or \( L/R \) for an inductor. After a DC switch, the complete response of the capacitor voltage is \( v_C(t) = v(\infty) + [v(0^+) - v(\infty)] e^{-t/\tau} \) for \( t > 0 \). The inductor current has the same shape: \( i_L(t) = i(\infty) + [i(0^+) - i(\infty)] e^{-t/\tau} \). Other voltages and currents are linear combinations; they share the same \( \tau \) but not necessarily the same initial and final values, and they may include jumps.

Finding \( R \): remove the capacitor (open) or inductor (short for DC deactivation? No—for the Thévenin resistance seen by the storage element, deactivate independent sources, then \( R_\mathrm{eq} \) at the storage terminals). Do not include the load that is the capacitor itself.

Source-free (natural) response: \( v(\infty) = 0 \) or \( i(\infty) = 0 \). Step response: a constant source switched in. Sequence of switches: piece the solution on intervals, propagating \( v_C \) or \( i_L \) as the next initial condition. Continuity still holds at each switching instant for those state variables.

Physical meaning: RC discharge is charge leaking through R; energy \(\frac12 Cv^2\) ends up as heat in R. RL decay is magnetic energy \(\frac12 Li^2\) dissipated in R. Time to 1% remaining is about \( 4.6\tau \); five time constants is the lab rule of thumb for “settled.”

Impulse and unbounded derivatives appear if a charged capacitor is switched onto another capacitor with no series R (charge sharing with conservation of charge, voltage jump via an impulsive current) or if an inductor carrying current is opened (arc). UG courses mention these as illegal or special; include series R in any practical model.

Units: seconds for \( \tau \). Mixing µF with kΩ gives milliseconds: \( 1\,\mathrm{k}\Omega \times 1\,\mu\mathrm{F} = 1\,\mathrm{ms} \). Mixing H with Ω: \( 1\,\mathrm{H}/1\,\Omega = 1\,\mathrm{s} \).

The first-order story in words: the network has one degree of freedom. All voltages and currents are affine functions of that one state plus the instantaneous sources. After sources become constant, everything decays toward a unique DC operating point at the same τ. That is why you may be asked for iR(t) and you still only compute one exponential: find the state, then use algebra on the t>0 resistor network with the capacitor replaced by a known voltage source vC(t) (not a short, not an open, a time-varying but instantaneously defined voltage). Equivalently replace an inductor by a current source iL(t). This substitution is the fastest way to get a jump in a resistor voltage at t=0: the state is continuous, the sources may switch, so Ohm on the resistors can jump.

Piecewise constant sources, as in a square wave driving RC, are a sequence of first-order solutions. Match vC at each switching instant. If the square period is much longer than τ, you see nearly full charge and discharge (a good reset). If the period is much shorter than τ, vC hovers near the average (a smoothing filter). If they are comparable, you need the exact matching. The same remarks apply to PWM on an RL motor winding in a later drives course: the winding current is a first-order RL state.

Thevenin seen by C may include a dependent source. Then RTh is still v_test/i_test at the capacitor terminals with independent sources killed. If that RTh is negative, the exponential grows and the linearized model is unstable; the physical circuit saturates or oscillates, which a first-order linear model can only hint at. UG problems almost always have positive RTh.

Switch models: an ideal switch is an open or a short. At the closing instant onto a capacitor, no problem if a resistor is in series. At the opening instant of an inductor, insert a model of the arc or a diode path; otherwise vL is unbounded and the Laplace method will produce impulses. Many textbook figures sneak in a resistor across the inductor for t>0 for that reason.

How to report an answer: write the expression with t in seconds, state the interval t>0, and give a numerical τ. Sketch vC(0+), the asymptote, and the point at t=τ which is 63% of the way from start to finish (charging) or 37% remaining (discharge toward zero). Examiners look for that 63% literacy. Energy checks: the change in ½Cv² plus the integral of resistor power should match the source energy over the same interval. For a DC source charging C through R from 0 to Vs, source energy is C Vs², stored is ½C Vs², dissipated is ½C Vs², independent of R. That paradox (R does not appear) is a good oral-exam question; R changes the time scale, not the split.

## Equations

Capacitor: \( i_C = C \frac{dv_C}{dt} \), \( v_C(t) = v_C(0) + \frac1C \int_0^t i_C(\tau)\,d\tau \).

Inductor: \( v_L = L \frac{di_L}{dt} \), \( i_L(t) = i_L(0) + \frac1L \int_0^t v_L(\tau)\,d\tau \).

First-order DC-forced: \( x(t) = x(\infty) + [x(0^+) - x(\infty)] e^{-t/\tau} \), \( x = v_C \) or \( i_L \).

\( \tau = R_\mathrm{Th} C \) or \( \tau = L / R_\mathrm{Th} \).

RC source-free: \( v_C(t) = v_C(0) e^{-t/RC} \). RL source-free: \( i_L(t) = i_L(0) e^{-t R/L} \).

Energy: \( w_C = \frac12 C v_C^2 \), \( w_L = \frac12 L i_L^2 \). Dissipated energy is the drop in stored energy when the source-free network is passive.

## Methods

Draw the circuit for \( t < 0 \) (steady DC: capacitors open, inductors short). Find \( v_C(0^-) \) or \( i_L(0^-) \). Copy to \( 0^+ \). Draw the circuit for \( t > 0 \). Find \( x(\infty) \) from a new DC analysis. Find \( R_\mathrm{Th} \) seen by the storage element. Write the exponential. Then find any other requested variable from KCL/KVL/Ohm on the \( t>0 \) circuit, using the known state and the constitutive law if a derivative is needed.

If two capacitors share via resistors, the order is still first if they can be combined, otherwise second (next unit). If a switch reconfigures R, \( \tau \) changes at that instant but \( v_C \) does not.

Design: pick \( \tau \) for a desired 10–90% rise time \( t_r \approx 2.2 \tau \) of an RC step (low-pass). Watch the resistor's thermal energy \( \int i^2 R\,dt \) during the pulse.

A lab procedure: charge C from a DC supply through a known R, capture vC(t) on a DSO, fit an exponential, extract τ, compare with RC using the measured R and C (meter the parts; 20% capacitors lie). Repeat discharge with the source replaced by a short. The two τ values should match if the source impedance is low. If they do not, the supply current-limit or a remaining series R is in play. For RL, use a large R so τ is milliseconds, not microseconds of a shorted coil, and include a freewheel path when opening the switch. Write the predicted iL(t) before looking at the scope; confirmation is the point of the unit.

## Mistakes

Using \( v_C(0^+) \) as the voltage on a different node that jumped. Applying the exponential to a current through a capacitor as if it were continuous. Computing \( \tau = RC \) with a resistor that is not the Thévenin resistance (forgetting parallel paths). Treating the inductor as open at DC steady state (it is a short). Writing \( e^{+t/\tau} \) and watching the answer explode. Mixing \( t \) in milliseconds with \( \tau \) in seconds. Assuming every voltage in an RC circuit is continuous. Opening a current-carrying inductor in a simulation without a snubber and trusting the infinite spike. Using superposition of exponentials with different \( \tau \) from different intervals without resetting the time origin or matching the state. Forgetting that \( i_C = 0 \) at DC equilibrium even if \( v_C \ne 0 \). Calling the time constant “frequency” or writing τ = 1/RC for an RC circuit (that is ωc, not τ).
