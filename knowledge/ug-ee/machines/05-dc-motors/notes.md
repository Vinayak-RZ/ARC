# Torque, speed control, starters

A DC motor is the same electromagnetic machine as a DC generator with power reversed: electrical power in at the terminals, mechanical power out at the shaft. Terminal voltage \(V\) exceeds generated (back) emf \(E\) by the armature drop. Torque is \(T=k\phi I_a\). Speed is whatever makes \(E=k\phi\omega\) satisfy KVL. That one sentence is speed control: change \(V\), \(R\) in the armature circuit, or \(\phi\). Starters limit \(I_a=(V-E)/R_a\) at standstill when \(E=0\).

This unit is shunt, series, and compound motors, their characteristics, Ward–Leonard and chopper/armature-voltage control, field weakening, and classical three-point/four-point starters. Regenerative, dynamic, and plugging braking belong with drives electives; the KVL still holds.

## Concepts

Back emf \(E=k\phi\omega\) is not a battery. It is Faraday’s voltage from rotation. At start, \(\omega=0\), \(E=0\), so \(I_a=V/R_a\) is huge (ten to twenty times rated on a shunt motor). A starter inserts resistance in series with the armature and cuts it out as \(E\) builds. Running, \(I_a=(V-E)/R_a\) is modest because \(E\) is 90-plus percent of \(V\).

Torque: converted power \(E I_a = T\omega\), so \(T=E I_a/\omega = k\phi I_a\). Direction: reverse either field or armature current, not both, to reverse rotation. Series motors reverse by reversing field or armature.

Shunt motor: flux approximately constant if \(V\) and \(R_f\) are constant (armature reaction aside). Speed is nearly constant with load: a small drop in \(\omega\) reduces \(E\), which allows more \(I_a\), which supplies more torque. The shunt motor is the classical “constant speed” DC machine. Speed regulation \((n_\mathrm{nl}-n_\mathrm{fl})/n_\mathrm{fl}\) is a few percent.

Series motor: flux rises with \(I_a\) until saturation. Torque is roughly \(I_a^2\) unsaturated, then linear with \(I_a\) when saturated. Speed is high at light load (flux small, \(\omega \approx V/(k\phi)\)) and low at heavy load. Never run a series motor without a load on the shaft in the lab: it can overspeed. Traction likes the high starting torque.

Compound motor: cumulative compound has a definite no-load speed (shunt field) and a series-field torque boost. Differential compound can be unstable (speed rises with load) and is rarely used as a drive.

Speed control methods:

1. Armature voltage: \(V_a\) variable, field full. Speed from near zero to base speed at full torque (torque limited by \(I_a\) and heating). Ward–Leonard: a DC generator with controlled field supplies the motor armature. Modern: controlled rectifier or DC–DC chopper.
2. Armature series resistance: cheap, dissipative, poor speed regulation, used historically and for starting.
3. Field weakening: reduce \(I_f\) below rated, \(\phi\) falls, speed rises above base speed, torque capability falls as \(1/\phi\) for a given \(I_a\). Limited by commutation, stability, and maximum speed.
4. Combined: constant torque below base (armature control), constant power above base (field weakening), the DC analogue of induction-motor V/f plus weakening.

Power and torque limits: armature copper \(I_a^2 R_a\), commutator sparking, and cooling set \(I_{a,\max}\). Field heating sets \(I_{f,\max}\). Mechanical speed sets \(n_{\max}\).

Starters: three-point starter for shunt motors puts the holding coil in series with the field so that field failure releases the handle (no-volt release). Four-point starter puts the holding coil across the supply so that field weakening (large rheostat) does not drop out the hold. Overload release is a series coil that trips on overcurrent. Face-plate starters are being replaced by electronic ramps; the electrical necessity — limit \(I_a\) until \(E\) exists — remains.

Braking (overview): dynamic braking connects the armature to a resistor with the field excited, motor as generator. Plugging reverses armature voltage, \(E\) and \(V\) add, current is \((V+E)/R\), very harsh. Regenerative braking returns power when \(E>V\) (overhauling load or field strengthening). Series motors need a reversed field connection to regenerate.

Armature reaction in a motor distorts flux and can cause commutation trouble at heavy load; interpoles are standard. In a motor the interpoles have the same polarity as the following main pole (opposite to generator rule) because current direction versus rotation differs.

Stability: a shunt motor with too-weak field can run away (same as series at no load). Differential compound can have a rising speed-torque curve that is unstable against a constant-torque load. Cumulative compound and series (with load) are stable in the usual UG sense \(\mathrm{d}T/\mathrm{d}\omega < 0\) intersecting a load curve.

Efficiency: \(\eta = P_\mathrm{shaft}/(V I_L)\). Converted power \(E I_a\) minus rotational losses is shaft power. Rotational losses (core, friction, windage) are often taken as constant near rated speed.

Permanent-magnet DC motors have \(\phi\) fixed (almost). Speed control is armature voltage. No field weakening except by demagnetizing, which is a failure mode. They still need current limiting at start.

## Equations

KVL (motor):

\[
V = E + I_a R_a + V_\mathrm{brush},\qquad E = k\phi\omega.
\]

Torque and power:

\[
T = k\phi I_a,\qquad P_\mathrm{conv}=E I_a=T\omega.
\]

Shunt: \(I_L=I_a+I_f\), \(I_f=V/R_f\) if field is across the supply.

Series: \(I_L=I_a\), \(E=V-I_a(R_a+R_\mathrm{se})\), \(T\propto \phi(I_a) I_a\).

Speed from KVL:

\[
\omega = \frac{V - I_a R_a}{k\phi}.
\]

Starter first-notch current (standstill): \(I_{a,\mathrm{st}}=(V)/ (R_a+R_\mathrm{st})\). Design often allows \(I_\mathrm{st}=1.5\)–\(2\) times rated.

Speed ratio, field weakening, same \(V\) and neglecting \(I_a R_a\): \(\omega_2/\omega_1 \approx \phi_1/\phi_2\).

Ward–Leonard: motor \(V_a = E_g\) of the generator, \(E_g=k_g \phi_g \omega_g\) with \(\omega_g\) of a constant-speed prime mover, so \(V_a\) follows generator field.

## Methods

Always write KVL and the emf equation before inventing a “rule of thumb.” Identify shunt versus series versus compound so that \(I_a\) versus \(I_L\) is correct.

Speed at a given load: from shaft torque (or power) get \(I_a\) via \(T=k\phi I_a\) if \(\phi\) is known, or via \(P_\mathrm{conv}=E I_a\) with \(E=V-I_a R_a\). That last pair is a quadratic in \(I_a\) when power is given: \(E I_a = (V-I_a R_a)I_a = P_\mathrm{conv}\).

Field-weakening numerical: if \(\phi\) is reduced to 80% and \(T\) is unchanged, \(I_a\) must rise 1/0.8. Check \(I_a\) against rated. Speed rises about 1/0.8 if \(IR\) drop is neglected; include \(IR\) for accuracy.

Starter design (equalizer resistance steps, UG version): specify max and min current during start, \(I_1\) and \(I_2\). Ratio \(\gamma = I_1/I_2\). Total resistance at first notch \(R_1=V/I_1\). Subsequent \(R_{k+1}=R_k/\gamma\) until \(R_a\) remains. Number of sections from \(\gamma^{n}=R_1/R_a\).

Characteristic sketches: shunt \(n\) vs \(T\) almost flat, slightly drooping. Series \(n\) vs \(T\) hyperbolic-ish. Cumulative compound between them, with finite no-load speed.

To reverse a DC motor from a diagram: reverse armature leads (preferred, interpoles stay correct with the armature) or reverse field leads (then interpoles may need to stay with the armature). Reversing the supply reverses both and does not reverse rotation.

When rotational losses are given, \(P_\mathrm{shaft}=E I_a - P_\mathrm{rot}\). When they are not, some problems treat \(E I_a\) as shaft power; that is an approximation.

For chopper control, average armature voltage \(V_a = \delta V_\mathrm{dc}\) in CCM for a buck chopper, then the same KVL. Current ripple depends on \(L_a\) and chopping frequency; UG often uses averages only.

## Mistakes

Using generator KVL \(E=V+I_a R_a\) on a motoring machine.

Starting a shunt motor without a starter (or a current-limited supply). \(R_a\) of 0.3 Ω on 220 V is 700 A.

Running a series motor at no load.

Field weakening below the point of commutation or mechanical limit, treating it as unbounded speed control.

Reducing armature voltage and expecting constant power. Below base speed, rated \(I_a\) gives roughly constant torque, so power falls with speed.

Putting the starter resistance in the field circuit of a shunt motor. That weakens flux at start, which increases starting current and wrecks torque. Starter resistance belongs in the armature path; the field should be fully excited at start.

Three-point starter with a large field rheostat: the hold coil drops out. Use four-point.

Reversing both field and armature and expecting reversal.

Using \(T\propto I_a^2\) for a shunt motor. Shunt \(\phi\) is not proportional to \(I_a\).

Forgetting that \(E I_a\) is converted power, not shaft power, when rotational losses are listed.

Computing speed from \(E=k\phi N\) with \(k\) in mixed units (r/min versus rad/s) without converting.

Ignoring armature reaction at heavy load: actual flux is less than no-load \(\phi\), so speed is a little higher than the constant-\(\phi\) prediction (shunt motor).

A laboratory speed-control write-up should state which quantity is held constant. Armature control at full field: plot \(n\) versus \(V_a\) at a stated \(T\) or \(I_a\). Field control at full \(V_a\): plot \(n\) versus \(I_f\) and stop when sparking or the speed limit appears. Combined control: mark base speed. Below base, the torque limit is heating of the armature (and interpoles). Above base, the torque limit falls and the commutator voltage between bars rises; that, not the algebra of \(E=k\phi\omega\), is what caps field weakening. Ward–Leonard sets still appear in mines and mills because four-quadrant torque is natural: reverse generator field, reverse motor \(V_a\), reverse torque, regenerate into the AC machine that drives the MG set. A thyristor dual converter does the same with less rotating plant. For UG numbers, replace the generator with a controlled \(V_a\) and keep KVL.

Series-motor starters must not open the field. A diverter across the series field weakens flux for speed-up under load; a diverter that opens is a runaway. When plugging a shunt motor, the starter resistance (or a plugging resistor) must be back in because \(V+E\approx 2V\). Compute \(I=(V+E)/(R_a+R_\mathrm{plug})\) and compare with commutation limits. Dynamic braking: switch the armature onto \(R_b\) with field excited; \(I_a=E/(R_a+R_b)\), \(T=k\phi I_a\) retards the shaft. As speed falls, \(E\) falls, torque fades; a mechanical brake finishes the stop. That fade is why dynamic braking is poor at crawl and why servos use four-quadrant drives instead.
