# Equivalent circuit, torque-slip

The three-phase induction machine is the default industrial motor: cheap, rugged, no commutator. A stator winding produces a rotating MMF at synchronous speed \(n_s=120 f/P\). The rotor, squirrel-cage or wound, carries induced currents at slip frequency. Torque comes from the interaction of rotor current with the air-gap flux. The per-phase equivalent circuit — stator leakage and resistance, magnetizing branch, and rotor resistance divided by slip — is the analysis engine of this unit. Speed-torque shape, starting torque, breakdown torque, and the approximate Thevenin formulas are the UG staples. Starting methods and V/f control are the next unit.

Synchronous speed is the speed of the field, not of the rotor. The rotor of a motor runs slightly below \(n_s\); a generator (induction generator) runs slightly above. Slip \(s=(n_s-n)/n_s\) is positive motoring, negative generating, greater than 1 for plugging.

## Concepts

A balanced three-phase stator winding with \(p\) pole pairs, frequency \(f\), produces a travelling MMF at \(\omega_s=2\pi f / (p)\) mechanical rad/s. Amplitude is set by magnetizing current, as in a transformer. The air-gap flux wave induces stator EMF at \(f\) and rotor EMF at \(s f\). At \(s=0\) (synchronous speed) rotor induced voltage is zero, rotor current is zero, torque is zero. An induction motor cannot produce steady torque at \(s=0\) without a separate excitation; that is why it is asynchronous.

The per-phase exact equivalent circuit (IEEE-style, stator referred) has \(R_1+jX_1\) in series, then a shunt \(R_c\parallel jX_m\) (sometimes \(R_c\) omitted), then \(jX_2'\) and \(R_2'/s\). The rotor resistance referred to the stator is \(R_2'\); dividing by \(s\) accounts for both copper in the rotor and converted mechanical power. Split \(R_2'/s = R_2' + R_2'(1-s)/s\). The first term is rotor copper; the second is the mechanical load (including friction if not otherwise placed). Input to the air gap \(P_g = 3 I_2'^2 (R_2'/s)\). Rotor copper \(P_\mathrm{cu2}=s P_g\). Converted \(P_\mathrm{mech}=(1-s)P_g\). That split is exact in this model and is worth memorizing: \(P_\mathrm{cu2}:P_\mathrm{mech} = s:(1-s)\).

Approximate circuit: move the magnetizing branch to the terminals. Then \(I_2' \approx V_1 / (R_1+R_2'/s + j(X_1+X_2'))\). Thevenin equivalent looking into the network from the rotor (magnetizing included) is more accurate for torque: \(V_\mathrm{Th}=V_1 jX_m/(R_1+j(X_1+X_m))\), \(Z_\mathrm{Th}=R_\mathrm{Th}+jX_\mathrm{Th}\). Torque:

\[
T = \frac{3}{\omega_s} \frac{|V_\mathrm{Th}|^2 (R_2'/s)}{(R_\mathrm{Th}+R_2'/s)^2+(X_\mathrm{Th}+X_2')^2}.
\]

Breakdown (maximum) torque at \(s_m = R_2'/\sqrt{R_\mathrm{Th}^2+(X_\mathrm{Th}+X_2')^2}\). In the crude approximation \(R_\mathrm{Th}\approx 0\), \(s_m \approx R_2'/(X_1+X_2')\). Maximum torque is independent of \(R_2'\) in that approximation; \(R_2'\) only shifts the slip at which it occurs. That is why a wound-rotor motor can start with external \(R\) at high torque near \(s=1\) and then cut \(R\) out for efficient running at small \(s\).

Starting torque is \(T(s=1)\). It rises with \(R_2'\) until \(s_m=1\), then falls. Designers of cages use deep-bar or double-cage rotors to get high effective \(R_2\) at starting frequency (50 Hz in the rotor at s=1) and low \(R_2\) at slip frequency (1–3 Hz). That is a frequency-dependent \(R_2\), not a constant-parameter circuit, but UG still uses two lumped cages sometimes.

Classes (NEMA A, B, C, D) are torque-speed shapes. Class D is high \(R_2\), high starting torque, high slip. Class B is the general-purpose compromise.

Induction generator: driven above \(n_s\), \(s<0\), \(R_2'/s\) is negative, mechanical power in, electrical out, but it still needs reactive magnetizing VA from the grid or from capacitors (self-excitation). Voltage of a self-excited IG is a saturation intersection, analogous to a shunt DC generator OCC.

Power flow, motoring: stator input \(P_\mathrm{in}=3 V I \cos\phi\). Stator copper and core subtracted give air-gap power \(P_g\). Then the \(s:(1-s)\) split. Friction, windage, and stray subtracted from \(P_\mathrm{mech}\) give shaft output. Efficiency is shaft over stator input.

No-load and blocked-rotor tests play the transformer OC/SC roles: no-load at rated voltage gives magnetizing and rotational-loss information; blocked-rotor at reduced voltage and rated current gives \(R_1+R_2'\) and \(X_1+X_2'\). Frequency of the blocked-rotor test is sometimes reduced to 25 Hz to better match leakage at running slip; UG often uses line frequency. Stator resistance from a DC test splits \(R_1\) from \(R_2'\).

Circle diagram is a graphical phasor locus of stator current as slip varies, with \(R_2'/s\) changing. It is in some Indian UG syllabi. The equivalent-circuit formulas supersede it for numbers; the circle is a teaching picture of the current locus.

Single-phase induction motors (split-phase, capacitor-start, PSC, shaded-pole) use double-revolving-field or cross-field stories. Starting torque is zero for a single winding; an auxiliary winding in quadrature with a phase-shifted current produces a crude rotating field. They are mentioned here as a limit of the three-phase idea, not fully modelled.

Synchronous watt: torque in synchronous watts is \(P_g\) (three-phase). \(T=P_g/\omega_s\). That is why air-gap power is the first quantity to compute in a numerical.

## Equations

Synchronous speed:

\[
n_s=\frac{120 f}{P}\ \mathrm{r/min},\qquad \omega_s=\frac{4\pi f}{P}\ \mathrm{mech\ rad/s}.
\]

Slip:

\[
s=\frac{n_s-n}{n_s},\qquad f_2=s f,\qquad n=(1-s)n_s.
\]

Air-gap / rotor split:

\[
P_g=3 I_2'^2 \frac{R_2'}{s},\qquad P_\mathrm{cu2}=s P_g,\qquad P_\mathrm{mech}=(1-s)P_g,\qquad T=\frac{P_g}{\omega_s}.
\]

Approximate torque (magnetizing at terminals, \(X=X_1+X_2'\)):

\[
T=\frac{3}{\omega_s}\frac{V_1^2 (R_2'/s)}{(R_1+R_2'/s)^2+X^2}.
\]

Breakdown slip (approx.):

\[
s_m=\frac{R_2'}{\sqrt{R_1^2+X^2}}.
\]

Thevenin torque as in Concepts. Mechanical speed \(\omega_m=(1-s)\omega_s\). Shaft torque and \(P_\mathrm{mech}\) use \(\omega_m\): \(P_\mathrm{mech}=T\omega_m\) if \(T\) is electromagnetic torque and rotational losses are lumped elsewhere.

Input:

\[
P_\mathrm{in}=3 V_\mathrm{ph} I_1 \cos\phi.
\]

## Methods

Draw the per-phase circuit. Convert line voltage to phase voltage (Y: divide by \(\sqrt{3}\)). Compute \(Z_2 = R_2'/s + jX_2'\), combine with magnetizing if exact, get \(I_1\) and \(I_2'\). Then \(P_g\), \(T\), \(P_\mathrm{mech}\).

If only approximate circuit is justified (problem says neglect magnetizing, or gives only \(R_1,R_2,X\)), use the torque formula directly.

Blocked-rotor / no-load parameter extraction is unit 11 as a standard test, but the algebra is: no-load \(I_0,P_0,V\) → \(R_c,X_m\) after subtracting stator \(I_0^2 R_1\) if required; blocked \(V_\mathrm{br},I_\mathrm{br},P_\mathrm{br}\) → \(R_1+R_2'\) and \(X_1+X_2'\); DC stator resistance gives \(R_1\) (with a 1.2 AC factor sometimes). Split leakage 50/50 if Class A/B unknown.

For a given shaft power, work backwards: \(P_\mathrm{mech}=P_\mathrm{sh}+P_\mathrm{fw}\), \(P_g=P_\mathrm{mech}/(1-s)\), \(I_2'^2 = P_g/(3 R_2'/s)\). Then stator copper and input.

Torque-speed sketch: \(T=0\) at \(s=0\), \(T_\mathrm{st}\) at \(s=1\), peak at \(s_m\). Motoring \(0<s<1\), generating \(s<0\), plugging \(s>1\). Mark rated point at small slip (0.02–0.05 typical).

When \(R_2'\) changes (wound rotor), \(s_m\) proportional to \(R_2'\), \(T_\max\) almost constant. Starting torque follows the formula at \(s=1\).

Induction generator on the grid: same circuit, \(s\) negative, \(P_g\) negative (power toward the stator from the gap). Supply still feeds \(Q\) into \(X_m\).

## Mistakes

Using \(\omega_m\) instead of \(\omega_s\) in \(T=P_g/\omega\). Electromagnetic torque is air-gap power over synchronous speed.

Treating \(R_2'/s\) as only copper. The mechanical resistor \(R_2'(1-s)/s\) is not a physical resistor on the shaft; it is the converted power.

Using line voltage on a per-phase circuit that needs phase voltage.

Assuming \(T_\mathrm{max}\) increases with \(R_2'\). In the standard model it does not (approximately); only \(s_m\) moves.

Writing \(s=(n-n_s)/n_s\) with a sign error for motoring.

Forgetting the factor 3 in three-phase power. One phase’s \(I_2'^2 R_2'/s\) is not \(P_g\).

Using blocked-rotor \(X\) as \(X_m\). Blocked rotor sees leakage, not magnetizing.

Neglecting that \(I_1 \neq I_2'\) when the magnetizing branch is present, then computing stator copper from \(I_2'\).

Claiming an induction motor runs at \(n_s\) on no load. It runs just below, enough to cover rotational losses.

Using transformer 4.44 \(B_\mathrm{max}\) without remembering that pole flux and winding factors belong to the AC-winding unit (synchronous machines). For induction machines Faraday still holds per phase: \(E_1=4.44 f N_\mathrm{ph} k_w \Phi_p\).

Plugging \(s=2\) into efficiency formulas as if plugging were a steady efficient mode. Plugging dissipates \(|s|P_g\) in the rotor, large heat.

Single-phasing a three-phase motor (one line open): it may continue with reduced torque and overheating; it will not start from rest. Not a balanced equivalent-circuit case.

A clean numerical habit is to compute three powers and check that they add: stator copper \(3I_1^2 R_1\), core \(3E_1^2/R_c\) or the given \(P_\mathrm{core}\), and air-gap \(P_g\). Their sum is stator input in the standard model. Then \(s P_g\) and \((1-s)P_g\) must recover \(P_g\). If a spreadsheet does not close, the usual bug is using line current as phase current on a delta motor, or using \(R_2'\) without dividing by \(s\) in \(P_g\). Wound-rotor nameplates give rotor voltage and current at slip rings with the rotor open (standstill, stator rated). That open-circuit rotor voltage is \(E_2\), and \(R_2\) in actual rotor ohms is not \(R_2'\). Refer with \(R_2'=R_2/a_i^2\) where \(a_i\) is the effective current ratio, or equivalently \(a^2 R_2\) with the voltage ratio from \(E_1/E_2\). Mixing ring ohms with stator-referred ohms is the IM analogue of adding transformer \(R_1+R_2\) on opposite sides.

Deep-bar effect: at starting, rotor frequency is line frequency, current crowds to the top of a tall bar, effective \(R_2\) high, effective leakage a bit low. At running, slip frequency is a few hertz, current fills the bar, \(R_2\) low. Double-cage: an outer high-\(R\) cage for start, an inner low-\(R\) cage for run. UG lumped-parameter circuits with constant \(R_2'\) cannot capture that unless you use two parallel rotor branches with different \(X\). When a problem gives a single \(R_2'\), use it at the slip of the problem and do not invent a deep-bar correction.

No-load slip is not zero. It is \(P_\mathrm{fw}/P_g\) with \(P_g\) barely larger than rotational loss. Measuring speed with a stroboscope and computing \(s=(n_s-n)/n_s\) is more honest than writing \(s=0\) in the equivalent circuit; setting \(s=0\) makes \(R_2'/s\) infinite, \(I_2'=0\), which is the no-load model you already use by omitting the rotor branch. That is consistent. What is not consistent is claiming the shaft truly turns at \(n_s\).
