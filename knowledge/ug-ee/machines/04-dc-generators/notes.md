# Generated emf, types, characteristics

A DC generator is a rotating armature of conductors in a magnetic field, with a commutator that converts the induced alternating coil voltages into a unidirectional brush voltage. The same machine run as a motor is the next unit; here the emphasis is generated emf, armature reaction, commutation, and the external characteristics of separately excited, shunt, series, and compound machines. The magnetic circuit of unit 01 supplies the field. Faraday supplies \(e=B\ell u\) in each conductor and \(E=k\phi\omega\) for the machine.

Undergraduate courses still teach DC machines because the algebra of \(E=V\pm I_a R_a\) and \(T=k\phi I_a\) is the cleanest electromechanical pair, and because DC motors remain in labs, traction heritage, and as the mental model of armature-controlled drives. Brushless DC is a permanent-magnet AC machine with an inverter; it is not this unit.

## Concepts

Generated emf in a simple lap-wound armature is \(E = \Phi Z N P / (60 A)\) with \(\Phi\) flux per pole (weber), \(Z\) number of armature conductors, \(N\) speed in r/min, \(P\) poles, and \(A\) parallel paths (\(A=P\) for lap, \(A=2\) for wave). Equivalently \(E = k\phi\omega\) in SI with \(\omega\) in rad/s and \(k = PZ/(2\pi A)\). The constant \(k\) is geometry. Flux \(\phi\) is set by field current through the saturation curve (OCC).

The open-circuit characteristic (OCC, magnetization curve) is \(E_0\) versus \(I_f\) at constant speed. It is the B-H curve of the machine’s magnetic circuit, scaled. Residual magnetism gives a small \(E\) at \(I_f=0\). The air-gap line is the tangent at the origin of the OCC if residual is ignored, or the linear gap-dominated slope. Saturation bends the OCC over.

Armature reaction is the MMF of armature current distorting and, with brush shift or interpoles aside, demagnetizing the main flux. In a generator at lagging “load” (DC has no PF, but the geometric cross-magnetizing field plus brush lead for commutation produces a demagnetizing component). Compensating windings in pole faces cancel armature MMF. Interpoles (commutating poles) in the interpolar axis provide a local flux that reverses coil current on time and also supply a compensating MMF in that axis.

Commutation is the reversal of current in a coil as it is shorted by a brush. Linear commutation is the ideal. Delayed commutation from inductance causes sparking. Interpoles, interpolar flux, and brush-neutral setting manage it. Poor commutation limits current, not just looks ugly.

Separately excited: field from an independent source. External characteristic \(V\) vs \(I_L\) droops from armature reaction and \(I_a R_a\) drop. Voltage is easily controlled by \(I_f\).

Shunt: field across the armature (through a field rheostat). Voltage builds by self-excitation if residual flux, correct field polarity, and field-circuit resistance below the critical resistance ( OCC and field-resistance line intersection). Critical speed is the dual: too slow, OCC too low, no intersection. Load characteristic droops more than separate excitation because \(I_f\) falls as \(V\) falls.

Series: field in series with the armature. Voltage rises with load in the unsaturated region (flux rises with \(I_a\)) then may droop with saturation and armature reaction. Unsuitable for a voltage supply without a load; used as a booster or historically as a traction motor (next unit).

Compound: series and shunt fields. Cumulative compounding can be flat or over-compounded (voltage rises with load to offset feeder drop). Differential compounding makes voltage fall steeply, used where current limit is desired. Long-shunt versus short-shunt changes whether the shunt sees terminal voltage or armature voltage; numerically they are close on large machines.

Armature resistance \(R_a\) includes interpoles and brushes as a first model. Brush drop is sometimes a constant 1–2 V total, not ohmic. Field resistance \(R_f\) is high (hundreds of ohms) on shunt machines.

Power flow: mechanical in, copper and core and friction out, electrical out. Generated power \(E I_a\). Terminal power \(V I_L\). The difference is armature copper and brush. Field copper is from the supply in separate excitation and from the armature in shunt.

Build-up of a shunt generator: residual \(E\) drives a small \(I_f\), which increases flux, which increases \(E\), until the OCC meets the field-resistance line. If the field is reversed relative to residual, the machine demagnetizes. If \(R_f\) is too large, the line misses the OCC except near the origin.

Voltage regulation of a DC generator is \((V_\mathrm{nl}-V_\mathrm{fl})/V_\mathrm{fl}\). Over-compounded machines can have negative regulation by that definition.

Parallel operation of DC shunt generators is common: they share load according to voltage droop. Series generators in parallel need equalizing connections because the series-field voltage rise is unstable without them.

Lap versus wave: lap for high current, many paths; wave for high voltage, two paths. Dummy coils and equalizer rings are winding details that appear in some syllabi; the emf equation still holds with the actual \(A\).

Saturation means you cannot use a single \(k\phi\) at all loads. For unsaturated separate excitation, superposition of armature reaction as a demagnetizing AT per pole on the OCC is the graphical method (ampere-turn method). UG numericals often give a constant flux or a linearized OCC.

## Equations

Emf:

\[
E = \frac{\Phi Z N P}{60 A} = k_n \Phi N = k_\omega \Phi \omega.
\]

Circuit (generator):

\[
E = V + I_a R_a + V_\mathrm{brush},\qquad I_a = I_L + I_f\ \text{(shunt)}.
\]

Separately excited: \(I_a=I_L\), \(I_f\) independent.

Series: \(I_a=I_L=I_\mathrm{se}\), \(E=V+I_a(R_a+R_\mathrm{se})\).

Power:

\[
P_\mathrm{mech}\to E I_a,\qquad P_\mathrm{term}=V I_L.
\]

OCC at speed \(N_2\): \(E_2 = E_1 (N_2/N_1)\) if flux is unchanged (same \(I_f\), no extra saturation change from speed — frequency of tooth ripple is irrelevant to the DC OCC scaling).

Critical field resistance: slope of the air-gap line, \(R_{\mathrm{crit}} = E/I_f\) along that line. If the field-circuit resistance exceeds \(R_{\mathrm{crit}}\), no stable build-up.

Demagnetizing AT/pole (brushes shifted by \(\theta\) electrical from GNA), standard UG formula:

\[
\mathrm{AT}_d = \frac{I_a Z}{2A}\cdot\frac{\theta}{180^\circ}.
\]

Cross-magnetizing AT/pole:

\[
\mathrm{AT}_c = \frac{I_a Z}{2A}\left(\frac{1}{P}-\frac{\theta}{180^\circ}\right).
\]

(Use the problem’s angle convention; electrical versus geometrical degrees must not be mixed.)

## Methods

Given speed, flux, and winding data, compute \(E\) from the emf equation. Then apply KVL for the armature: generator \(E=V+I_a R_a\). Solve for the unknown (\(V\), \(I_a\), or \(R_a\)).

Shunt generator: \(I_a=I_L+I_f\), \(I_f=V/R_f\). If \(V\) is unknown, you may need the OCC: \(E(I_f)\) from the curve, \(E=V+I_a R_a\). Graphical: for a given \(I_L\), guess \(V\), get \(I_f\), read \(E\) from OCC, check KVL.

Build-up: plot OCC at the operating speed. Draw a straight line through the origin with slope \(R_f+R_\mathrm{rheostat}\). Intersection is the no-load voltage. If you only have OCC at another speed, scale all \(E\) values by \(N_\mathrm{new}/N_\mathrm{OCC}\).

External characteristic from OCC (ampere-turn method): for a load current, compute armature-reaction AT and \(I_a R_a\). Recede on the OCC by those AT, then drop \(I_a R_a\) vertically to get \(V\). This is a graphical staple.

Compounding: treat series-field AT as additional field AT on the OCC (cumulative) or opposite (differential). Flat compound: \(V_\mathrm{fl}=V_\mathrm{nl}\) at a specified current.

When residual voltage is given and \(I_f=0\), that is not zero flux; the OCC does not pass through the origin. Field-resistance lines still pass through the origin (no battery in the field). Intersection near residual is not a useful operating point if the OCC is only residual there.

Efficiency of a generator: \(\eta = P_\mathrm{out}/P_\mathrm{in} = V I_L / (V I_L + \text{losses})\). Losses: armature Cu, field Cu, core, friction and windage, stray. A UG “stray-loss 1% of output” is a given, not a law.

## Mistakes

Using motor KVL \(V=E+I_a R_a\) on a generator. The generated \(E\) is larger than terminal \(V\) in a generator.

Forgetting \(I_a \neq I_L\) on a shunt machine. Field current is not optional in the armature current.

Scaling OCC with field current instead of speed. OCC at a new speed scales \(E\), not \(I_f\).

Expecting a series generator to hold constant voltage. It does not.

Reversing the series field of a compound generator by accident and getting differential compounding (voltage collapse on load).

Using \(A=P\) on a wave winding. Wave: \(A=2\).

Treating brush drop as \(I_a R_\mathrm{brush}\) when the problem specified a constant voltage drop.

Computing \(E=\Phi Z N P/(60 A)\) with \(\Phi\) in mWb and forgetting \(10^{-3}\).

Ignoring residual magnetism in a self-excitation question, then claiming the machine cannot build up. Residual is required; too much \(R_f\) is the usual failure.

Paralleling series generators without an equalizer, then being surprised that one machine takes all the current.

Using power \(E I_L\) instead of \(E I_a\) for converted power.

Confusing GNA and MNA. Brushes sit on the MNA for sparkless commutation; armature reaction shifts MNA; interpoles restore a usable neutral.

A practical build-up checklist is worth running before blaming residual magnetism. Confirm rotation direction matches the residual polarity so that field current increases flux rather than opposing it. Confirm the field rheostat is at minimum resistance for first excitation. Confirm the voltmeter is on the armature, not across a blown field fuse. A reversed interpoles connection does not stop no-load build-up but it will spark as soon as load current flows; that is a commutation fault, not an OCC fault. Equalizer rings on lap windings keep the parallel paths from circulating on a slightly eccentric air gap; without them a heavily loaded generator can run hot in one path while the terminal voltage still looks normal. Wave windings need fewer equalizers because they already average the poles. Those winding notes do not change the emf equation, but they change whether the machine survives the load you computed.

Voltage drop along a feeder from a compound generator is why over-compounding exists: the series field is sized so that \(V_\mathrm{terminal}\) rises enough to cancel \(I R_\mathrm{feeder}\) at the load. Flat compound is defined at one current; at lighter load the machine is slightly over-compounded or under-compounded depending on saturation. Do not expect a straight external characteristic. Saturation of the series path and armature reaction both bend it. When a numerical gives a “linear OCC,” it is telling you to skip that bend, not that nature is linear.
