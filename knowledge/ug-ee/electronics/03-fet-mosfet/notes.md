# JFET and MOSFET characteristics and bias

Field-effect transistors are voltage-controlled majority-carrier devices. UG EE courses treat the JFET as a teaching analog of a voltage-controlled current source, then spend the rest of the term on the enhancement MOSFET that actually ships in CMOS. This unit covers symbols and regions, Shockley (JFET) and square-law (MOSFET) equations, DC bias, small-signal \(g_m\) and \(r_o\), body effect, and the CMOS inverter as a pair of complementary MOSFETs (timing is unit 14).

## Concepts

A FET has a channel whose conductivity is modulated by an electric field from the gate. In a JFET the gate is a reverse-biased pn junction; gate current is leakage. In a MOSFET the gate is insulated by oxide; DC gate current is essentially zero. Both present a huge DC input resistance, which is why they appear as analog switches, input stages, and digital logic.

JFET (n-channel default). With \(v_{GS}=0\) the n-channel between source and drain conducts; this is a depletion-mode device, normally on. Reverse-biasing the gate-channel junction (\(v_{GS}\) negative for n-channel) pinches the channel. At \(v_{GS}=V_P=V_{GS(off)}\) (pinch-off / cutoff voltage, negative for n-JFET) the channel is fully depleted and \(i_D=0\). For a given \(v_{GS}>V_P\), increasing \(v_{DS}\) eventually pinches off the drain end: saturation (also called the pinch-off region in older JFET texts). Below that, the JFET looks like a voltage-controlled resistor (ohmic / triode region). The Shockley equation in saturation is \(i_D=I_{DSS}(1-v_{GS}/V_P)^2\). \(I_{DSS}\) is the saturation current at \(v_{GS}=0\). p-channel JFETs reverse all polarities.

MOSFET types. Enhancement nMOS (the default digital FET): no inversion channel at \(v_{GS}=0\); a channel forms when \(v_{GS}>V_{tn}>0\). Depletion nMOS has an implanted channel and a negative \(V_t\), analogous to a JFET. pMOS enhancement has \(V_{tp}<0\) and conducts for \(v_{GS}<V_{tp}\) (i.e. gate sufficiently more negative than source). Bulk (body, substrate) is a fourth terminal. In discrete three-terminal parts the bulk is tied to the source. In ICs the pMOS bulk is usually \(V_{DD}\) and the nMOS bulk is \(V_{SS}\), so a source not at the rail sees body effect: \(|V_t|\) increases as the source-body reverse bias grows.

MOSFET regions (nMOS, \(v_{DS}>0\)):

- Cut-off: \(v_{GS}<V_{tn}\), \(i_D\approx 0\) (ignore subthreshold unless asked).
- Triode / linear / ohmic: \(v_{GS}>V_{tn}\) and \(v_{DS}<v_{GS}-V_{tn}\) (overdrive). Channel continuous; \(i_D\) depends on both \(v_{GS}\) and \(v_{DS}\). Used as a switch with small \(r_{DS,on}\) and as the resistive load in some analog circuits.
- Saturation / active / pentode: \(v_{GS}>V_{tn}\) and \(v_{DS}\ge v_{OV}=v_{GS}-V_{tn}\). Channel pinched at the drain; \(i_D\) is set by \(v_{GS}\) (square law) plus a weak \(v_{DS}\) dependence (channel-length modulation, \(\lambda\)). This is the analog amplifying region. Note the naming collision: BJT "saturation" is the switch-on region; MOSFET "saturation" is the analog region. Always say which device.

The long-channel square law \(i_D=\frac12\mu C_{ox}(W/L)(v_{GS}-V_t)^2(1+\lambda v_{DS})\) is the UG workhorse. Short-channel devices in modern CMOS are closer to linear in overdrive; UG exams still use square law unless a process card says otherwise.

Biasing JFETs. Self-bias: source resistor \(R_S\), gate grounded through \(R_G\). Then \(v_{GS}=-i_D R_S\), which is substituted into Shockley and solved (quadratic, or graphical). Voltage-divider bias plus \(R_S\) is more stable. Never forward-bias the JFET gate in analog bias; a few tenths of a volt forward and the gate diode conducts.

Biasing MOSFETs. Enhancement nMOS cannot use JFET-style \(v_{GS}=0\) self-bias as the only mechanism because it would be off. Common discrete circuits: drain-feedback bias (\(R_G\) from drain to gate, \(v_{GS}=v_{DS}\)), and voltage-divider plus source resistor, identical in topology to BJT divider bias but with \(I_G=0\) exactly, so the divider is unloaded. Constant-current bias (a current mirror or a JFET CCS) sets \(I_D\) and lets \(v_{GS}\) find the value required by the square law. In ICs, NMOS and PMOS current mirrors and differential pairs with tail sources are the default.

Small-signal. FET: \(g_m=\partial i_D/\partial v_{GS}\) at the Q-point. For Shockley JFET, \(g_m=g_{m0}(1-V_{GS}/V_P)\) with \(g_{m0}=2I_{DSS}/|V_P|\). For square-law MOSFET, \(g_m=\mu C_{ox}(W/L)(V_{GS}-V_t)=\sqrt{2\mu C_{ox}(W/L)I_D}=2I_D/V_{OV}\). Output resistance \(r_o=1/(\lambda I_D)\). Gate is an open circuit at DC; at high frequency \(C_{gs}\) and \(C_{gd}\) (Miller) appear.

CMOS as complementary pair. A pMOS on top of an nMOS sharing the gate and drain is the inverter of unit 14. For analog, the same pair is a push-pull output or a transmission gate (nMOS+pMOS in parallel with complementary gates) that passes analog levels in both directions without the \(V_t\) drop of a single pass transistor.

Analog switch caveat: an nMOS pass gate charged to \(V_{DD}\) on the drain can only pass \(V_{DD}-V_t\) (and body effect makes it worse). Full-rail analog multiplexers therefore use transmission gates or bootstrapped gates.

## Equations

n-JFET saturation (Shockley), \(V_P<0\), \(V_P\le v_{GS}\le 0\):

\[
i_D=I_{DSS}\left(1-\frac{v_{GS}}{V_P}\right)^2.
\]

Ohmic JFET (qualitative UG): \(i_D\approx 2I_{DSS}(1-v_{GS}/V_P)v_{DS}/(-V_P)\) for small \(v_{DS}\).

nMOS square law, saturation, \(v_{OV}=v_{GS}-V_{tn}>0\), \(v_{DS}\ge v_{OV}\):

\[
i_D=\frac12 k_n' \frac{W}{L} v_{OV}^2 (1+\lambda v_{DS}),\qquad k_n'=\mu_n C_{ox}.
\]

Triode nMOS, \(v_{DS}<v_{OV}\):

\[
i_D=k_n'\frac{W}{L}\left[(v_{GS}-V_t)v_{DS}-\frac12 v_{DS}^2\right].
\]

On-resistance of a deep-triode switch (\(v_{DS}\) small):

\[
r_{DS,on}=\frac{1}{k_n'(W/L)(v_{GS}-V_t)}.
\]

Body effect:

\[
V_t=V_{t0}+\gamma\left(\sqrt{|2\phi_F+V_{SB}|}-\sqrt{|2\phi_F|}\right).
\]

Transconductance:

\[
g_m=\frac{2I_D}{|V_P|}\left(1-\frac{V_{GS}}{V_P}\right)\quad\mathrm{(JFET)},\qquad g_m=\sqrt{2k_n'(W/L)I_D}=\frac{2I_D}{V_{OV}}\quad\mathrm{(MOS)}.
\]

\[
r_o=\frac{1}{\lambda I_D}.
\]

Self-bias JFET: substitute \(V_{GS}=-I_D R_S\) into Shockley and solve the quadratic in \(\sqrt{I_D}\).

CS voltage gain (source degenerated by unbypassed \(R_S\)):

\[
A_v=-\frac{g_m R_D'}{1+g_m R_S}.
\]

Without degeneration, \(A_v=-g_m R_D'\). Source follower \(A_v=g_m R_S'/(1+g_m R_S')\).

## Methods

1. Name the device and the region before writing an equation. Check \(v_{GS}\) against \(V_t\) or \(V_P\), then check \(v_{DS}\) against \(v_{OV}\).
2. JFET self-bias: write Shockley, replace \(v_{GS}\) by \(-I_D R_S\), take square roots carefully (only the physical root with \(I_D>0\) and \(V_P\le V_{GS}\le 0\)).
3. MOSFET divider bias: because \(I_G=0\), \(V_G\) is the unloaded divider. Then \(V_S=I_D R_S\), \(V_{GS}=V_G-V_S\), plug into square law. Quadratic again. Confirm saturation: \(V_{DS}=V_{DD}-I_D(R_D+R_S)\ge V_{GS}-V_t\).
4. Enhancement MOSFET with drain-feedback: \(V_{DS}=V_{GS}\), which automatically satisfies saturation if \(V_t>0\) because \(V_{DS}=V_{GS}>V_{GS}-V_t\).
5. Small-signal: find \(I_D\) first, then \(g_m\) from the Q-point identity, not from a guessed \(V_{OV}\). Short DC supplies, open current sources.
6. Body effect: only if \(V_{SB}\ne 0\). Discrete 3-pin MOSFETs with source-bulk strapped have \(\gamma\) irrelevant.
7. pMOS: use \(|v_{GS}|\), \(|V_{tp}|\), and current out of the drain toward the source in the usual analog current-source orientation, or consistently use negative voltages.

Design check: nMOS, \(k_n'(W/L)=0.5\,\mathrm{mA/V^2}\), \(V_t=0.8\,\mathrm{V}\), want \(I_D=0.5\,\mathrm{mA}\) in saturation. Then \(0.5=0.25(V_{GS}-0.8)^2\Rightarrow V_{OV}=\sqrt{2}=1.414\,\mathrm{V}\), \(V_{GS}=2.21\,\mathrm{V}\). Need \(V_{DS}\ge 1.41\,\mathrm{V}\).

## Mistakes

- Calling MOSFET saturation the switching region. In MOS analog, saturation is the constant-current region. The switch uses triode.
- Forward-biasing a JFET gate in a bias calculation. If \(V_{GS}\) comes out positive for an n-JFET, the Shockley model is invalid.
- Using Shockley for an enhancement MOSFET, or square law for a JFET without translating parameters. \(I_{DSS}\) is not \(k V_t^2\) unless you derive the correspondence.
- Forgetting that MOSFET divider bias is unloaded (\(I_G=0\)) and then "correcting" it with a BJT-style \(R_{Th}/(\beta+1)\) term that does not exist.
- Dropping \(\lambda\) when \(r_o\) is needed for a high-gain CS stage, or inserting a random \(r_o\) when \(\lambda\) was not given.
- Body of an on-chip nMOS tied to \(V_{SS}\) while the source sits at \(2\,\mathrm{V}\): \(V_t\) is not \(V_{t0}\).
- pMOS \(V_{GS}\) computed as \(V_G-V_S\) with both voltages near \(V_{DD}\) but forgetting the sign: conduction needs \(V_{GS}\) negative and more negative than \(V_{tp}\).
- Treating \(C_{gd}\) as only \(C_{gd}\) at the input of a CS stage; Miller multiplies it.
- Analog pass-transistor: expecting \(V_{out}=V_{DD}\) through an nMOS with gate at \(V_{DD}\). You get \(V_{DD}-V_t\).
- Mixing \(g_m=2I_D/|V_P|\) (that's \(g_{m0}\), only at \(V_{GS}=0\)) with the actual \(g_m\) at the biased \(V_{GS}\).

A JFET used as a voltage-controlled resistor (below pinch-off, small \(v_{DS}\)) is the analog mute, the AGC element in a Wien-bridge, and the variable-\(r_{ds}\) in some filter circuits. The control voltage is \(v_{GS}\); the resistance from drain to source is \(r_0/(1-v_{GS}/V_P)\) in the usual linearisation, with \(r_0=V_P/(2I_{DSS})\) at \(v_{GS}=0\). The signal on the channel must stay small compared with \(V_P\), otherwise the resistor is nonlinear and generates distortion. A MOSFET in deep triode is the same idea with \(r_{DS,on}=1/[k(v_{GS}-V_t)]\).

Depletion MOSFETs still exist as constant-current diodes (a JFET or depletion MOSFET with gate tied to source, operating at \(I_{DSS}\)) and as load devices in old NMOS logic. Enhancement MOSFETs dominate. Dual-gate MOSFETs (cascode on one die) appear in RF mixers; treat them as two nMOS in series with a second gate that sets gain.

Channel-length modulation \(\lambda\) is the FET Early effect. \(r_o=1/(\lambda I_D)\) limits the intrinsic gain \(g_m r_o=\sqrt{2k I_D}/(\lambda I_D)\propto 1/\sqrt{I_D}\). That is why analog CMOS often runs moderate currents in long devices when gain matters, and high currents in wide devices when \(g_m\) (speed, noise) matters. UG numericals that omit \(\lambda\) are telling you that \(R_D\) is small enough to hide \(r_o\).

Matching: two MOSFETs with the same \(W/L\) and the same \(v_{GS}\) (a mirror) copy currents only if \(v_{DS}\) also matches or if \(\lambda=0\). A cascode mirror raises output resistance to order \(g_m r_o^2\). Discrete lab parts are not matched; IC problems may say "matched pair" and then you *do* write \(I_1=I_2\).

Safe operating area for a power MOSFET is a different plot from a BJT (no second breakdown of the same kind, but a linear-mode hot-spot issue still exists). Switching converters belong in the power-electronics pack; here, the FET is an analog device or a logic switch.

FETs replace the BJT wherever high input impedance, no gate DC current, or complementary CMOS layout is the point. The algebra is square-law rather than exponential; the biasing discipline is the same: fix a current, stay in the analog region, linearise, then compute gain.
