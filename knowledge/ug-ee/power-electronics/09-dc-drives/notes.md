# DC drives: one-quadrant through four-quadrant

A DC drive is a converter plus a DC machine. Undergraduate power electronics treats armature voltage control below base speed and field weakening above it, with the converter topology dictating which quadrants of the \(v\)–\(i\) plane are reachable. Choppers (unit 04) and phase-controlled rectifiers (unit 03) are the two UG power stages. Mechanical transients belong with the electric-drives elective; here the converter–machine electrical interface is the core.

## Concepts

The armature circuit in steady state is \(V_t=E_a+I_a R_a\) (motoring, generating sign of \(I_a\) flips). \(E_a=K\phi\omega\). Torque \(T=K\phi I_a\). Below base speed, flux is rated and \(V_t\) is varied: speed follows \(E_a=(V_t-I_a R_a)\). Above base speed, \(V_t\) is at the converter ceiling and \(\phi\) is reduced: speed rises, torque capability falls. A field converter is a low-power controlled rectifier or chopper; the armature converter is the high-power one.

Quadrants in the armature \(V_t\)–\(I_a\) plane (machine conventions: positive \(V\) and positive \(I\) = forward motoring):

- Q1: forward motoring. Unidirectional voltage and current. First-quadrant chopper (buck) or a single fully/half-controlled rectifier.
- Q2: forward braking (regeneration). Voltage still positive, current reversed. Needs a path for reversed \(I_a\) into the source: a second-quadrant chopper (boost from the armature into the DC bus) or inversion of a dual converter / anti-parallel thyristor bridge.
- Q3: reverse motoring. Negative voltage and negative current.
- Q4: reverse braking.

A one-quadrant drive cannot regenerate; stopping uses a mechanical brake or a dynamic-brake resistor (chopper dumps \(I_a\) into \(R_b\)). A two-quadrant drive is either reversible current at one voltage polarity (motoring + regen in one direction) or reversible voltage at one current polarity (not both useful for a DC machine without a field reverse). Four-quadrant: H-bridge chopper, or dual converter (circulating or non-circulating current, unit 12).

Single-phase versus three-phase armature converters: single-phase has 100 Hz (or 120 Hz) ripple and a lower voltage ceiling for a given RMS AC. Three-phase six-pulse is the industrial default above a few kilowatts. Discontinuous armature current at light load makes \(V_t(\alpha)\) differ from the continuous \(\cos\alpha\) formula; speed then droops less than the continuous model predicts (average \(E_a\) closer to the pulse peak). A smoothing choke reduces discontinuous operation.

Closed-loop: inner current loop, outer speed loop. The converter is modelled as a gain \(K_c\) with a small delay (half a thyristor period, or a PWM period). UG problems often stay open-loop: given \(\alpha\) or \(D\), find speed.

Braking modes:

- Regenerative: kinetic energy returns to the AC mains or DC bus. Needs Q2/Q4.
- Dynamic (rheostatic): armature or a resistor absorbs energy. A chopper with \(R_b\) across the DC link (VSI brake chopper) is the modern cousin; on a DC machine a switch can connect \(R_b\) across the armature.
- Plugging (reverse-voltage braking): \(V_t\) reversed while \(\omega\) is still forward, so \(I_a=(V_t+E_a)/R_a\) is large. A current limit or an extra resistor is mandatory. Energy is dissipated in \(R_a\) and the supply may still source power.

Ward-Leonard (motor-generator set) is the historical four-quadrant analog; the static Ward-Leonard is a dual converter.

Chopper drive specifics: buck motoring \(V_t=D V_{bus}\). Regeneration with a boost: the machine \(E_a\) is the boost input, the bus is the output, so \(V_{bus}=E_a/(1-D)\) in CCM if that topology is used — equivalently a second-quadrant chopper with duty defined on the switch that shorts the armature through \(L\). Always draw the current path.

Multi-motor and series/parallel: traction sometimes series-connects machines; UG mentions it. Field weakening must be coordinated so no machine runs away.

Converter selection is a quadrant table, not a brand name. Fan or pump, one direction, no overhauling load: first-quadrant chopper or a single controlled rectifier. Hoist that must hold and lower a mass: four-quadrant dual converter or H-bridge, plus a mechanical brake for zero-speed safety. Battery vehicle: H-bridge chopper, regeneration into the battery if the battery accepts current. Laboratory dynamometer: four-quadrant with circulating dual converter so torque crosses zero without a dead band.

Ripple torque at 2f (single-phase) or 6f (three-phase) is the mechanical cost of a thyristor armature supply. A large flywheel or a smoothing choke reduces speed ripple; the torque ripple is still in the air-gap. PWM choppers at a few kilohertz push the ripple above the mechanical bandwidth. That is why modern DC servo drives are choppers even when a rectifier could have made the same average voltage.

Current continuity deserves an explicit test in drive problems. The armature time constant \(L_a/R_a\) compared with the converter pulse width (10 ms for 50 Hz single-phase half-cycle, 3.3 ms for six-pulse, tens of microseconds for a chopper) tells you which average-voltage formula to trust. Discontinuous current in a thyristor drive makes speed regulation look “better” (higher \(V_t\) than \(\cos\alpha\) predicts) and current control harder (gain changes). Choppers with a few hundred microhenries of extra \(L\) almost always stay continuous at rated current; at no-load they may not.

Field circuit is not a footnote. \(T=K\phi I_a\) and \(E_a=K\phi\omega\) mean that a 10% field error is a 10% torque and speed-constant error. Field converters are often single-phase semi-converters (one-quadrant is enough if you never reverse flux electronically). If you reverse the field to reverse torque instead of reversing armature voltage, the field time constant (hundreds of milliseconds) makes a slow, ugly reverse — acceptable on some mills, unacceptable on a servo. Four-quadrant armature conversion is the default modern choice.

Protection: overcurrent from plugging or from a stalled armature at full \(V_t\) is a fuse or an electronic current limit, not a hope. Overvoltage on a regenerating bus is a brake chopper. Field-loss protection must trip the armature because \(E_a\) collapses and \(I_a\) flies. Those interlocks are UG-legitimate even if the numericals stop at \(D=V_t/V_{bus}\).

## Equations

Steady-state armature:

\[
V_t=E_a+I_a R_a,\qquad E_a=K\phi\omega,\qquad T=K\phi I_a.
\]

Controlled rectifier (three-phase, continuous \(I_a\)):

\[
V_t=1.35 V_{LL}\cos\alpha - I_a R_{\mathrm{eq}},
\]

where \(R_{\mathrm{eq}}\) includes \(R_a\) and overlap resistance \(3\omega L_s/\pi\).

Buck chopper motoring:

\[
V_t=D V_{bus}=E_a+I_a R_a,\qquad D=\frac{E_a+I_a R_a}{V_{bus}}.
\]

Speed below base:

\[
\omega=\frac{V_t-I_a R_a}{K\phi}.
\]

Field weakening (rated \(V_t\), reduced \(\phi\)):

\[
\omega=\frac{V_{t,\mathrm{rated}}-I_a R_a}{K\phi},\qquad T_{\max}\propto\phi.
\]

Plugging current (worst case, \(\omega\) still \(+\), \(V_t\) reversed to \(-V\)):

\[
I_a=\frac{-V-E_a}{R_a}\quad\text{(large negative)}.
\]

Dynamic brake, armature on \(R_b\), converter off:

\[
I_a=\frac{E_a}{R_a+R_b},\qquad T=K\phi I_a\ \text{(braking)}.
\]

Power: motoring \(P=V_t I_a\) into the armature, mechanical \(E_a I_a\), copper \(I_a^2 R_a\).

## Methods

1. Identify quadrants required by the application (hoist vs simple fan). Pick converter family.
2. Write \(V_t=E_a+I_a R_a\) with signs. Convert \(V_t\) to \(\alpha\) or \(D\).
3. Check continuous current if \(L_a\) and \(\alpha\) are given. If discontinuous, do not use the continuous \(\cos\alpha\) speed prediction blindly.
4. Current limit: solve \(I_a=(V_t-E_a)/R_a\) at start (\(E_a=0\)). If it exceeds rating, add a starter resistor or ramp \(V_t\) (chopper \(D\) ramp, or \(\alpha\) ramp).
5. Braking: choose regenerative vs dynamic vs plugging; compute energy path.
6. Field weakening: never reduce \(\phi\) until \(V_t\) is at ceiling, or the machine over-currents at modest speed.

Worked pattern — chopper: \(V_{bus}=220\,\mathrm{V}\), \(E_a=150\,\mathrm{V}\), \(R_a=0.8\,\Omega\), \(I_a=25\,\mathrm{A}\). \(V_t=170\,\mathrm{V}\), \(D=170/220=0.773\). That \(D\) is a PWM duty, not a thyristor \(\alpha\). If the same motor were on a three-phase rectifier, you would solve \(\cos\alpha=V_t/V_{do}\) instead. Mixing \(D\) and \(\alpha\) on the same line is a dimensional identity crisis: \(D\) is 0–1, \(\alpha\) is 0–180°.

## Mistakes

- Using \(N\propto V_t\) without the \(I_a R_a\) drop, then missing why speed sags with load.
- Regenerating into a diode rectifier DC bus with no brake chopper (capacitor over-voltage).
- Plugging without a current-limit resistor.
- Applying boost formulae to a first-quadrant buck drive.
- Field weakening below base speed (torque lost for no voltage headroom gained).
- Mixing motor conventions so Q2 is labelled “reverse motoring.”
- Single-phase converter: forgetting 2f torque ripple on a large machine.
- Using inverter six-step formulae on a DC drive.
- Treating chopper \(D\) as \(\alpha/180^\circ\) without converting through \(V_t\).

Closed-loop comments that stay inside this unit: a current loop treats the converter as a \(V_t\) actuator with a delay of half a pulse period (thyristor) or one PWM period (chopper). The plant is \(I_a(s)=(V_t-E_a)/(R_a+s L_a)\). \(E_a\) is a slow disturbance if inertia is large. Speed loop sits outside and commands \(I_a^*\). Anti-windup of the speed PI when \(I_a\) is limited is what makes a start-from-stall not overshoot violently. UG numericals rarely tune the PI; they do ask why a current limit is required at \(E_a=0\).

Dynamic braking energy is \(\tfrac12 J\omega^2\) dumped into \(R_a+R_b\) over the deceleration. If the question gives inertia and a time, you can size \(R_b\) from average power. Regenerative braking returns that energy to the bus; the bus must have a sink. Plugging returns little to the bus and a lot to heat. Those three sentences pick the resistor rating.

DC drives are the cleanest place to see quadrants. AC drives (next) hide the same energy story inside a VSI DC link. The chopper duty equation \(D=V_t/V_{bus}\) is the same \(D\) as unit 04; only the interpretation of \(V_t=E_a+I_a R_a\) is added. Keep that mapping explicit so a student does not invent a new conversion ratio for motors.
