# Diode, SCR, MOSFET, IGBT, and SOA

A power converter is only as honest as the switch that opens and closes the current. Undergraduate power electronics treats four families as the default toolkit: the power diode, the silicon-controlled rectifier (thyristor, SCR), the power MOSFET, and the insulated-gate bipolar transistor (IGBT). The same chapter introduces the safe operating area (SOA), because a device that survives a DC rating on the datasheet can still fail on a switching locus that the student never drew. This unit is device-level. Circuit topologies live in later units; here the job is to know what a switch can do, how it is gated, what voltage and current it blocks, and which thermal and dynamic limits must sit on the same page as the average-current formula.

## Concepts

A power semiconductor switch is a controllable or uncontrollable valve between two power terminals, with a third terminal (gate or base) that decides the valve state when the device is controllable. Uncontrollable here means the power diode: it conducts when forward-biased and blocks when reverse-biased, with no gate. Controllable devices split into latching (thyristors) and non-latching (MOSFET, IGBT, BJT). Latching devices stay on after a gate pulse until the anode current falls below a holding value. Non-latching devices require a continuous gate (or base) command to stay on.

The power diode in converter analysis is not the small-signal Shockley toy from analog electronics, even though the same physics sits underneath. Forward drop at rated current is typically 0.7–1.2 V for silicon pn diodes and 0.3–0.8 V for Schottky parts. Reverse recovery is the UG-critical dynamic: when the diode is forced from forward current to reverse block, stored charge must be swept out, producing a reverse-recovery current spike \(I_{rr}\) for a time \(t_{rr}\). Fast-recovery and Schottky diodes exist because that spike dumps energy into the complementary transistor and rings snubber networks. In an uncontrolled rectifier the diode is the whole converter. In a chopper or inverter the freewheel diode is as important as the controlled switch.

The SCR (thyristor) has four layers (p-n-p-n) and three terminals: anode, cathode, and gate. A positive gate pulse relative to the cathode injects carriers that regenerative feedback latches the device on. Once latched, the gate loses control. Turn-off requires the anode current to fall below the holding current \(I_H\) for longer than the circuit-commutated turn-off time \(t_q\). That is why line-commutated rectifiers can use SCRs on AC mains (the current naturally goes through zero) and why DC choppers historically needed forced-commutation networks. Ratings that appear in every exam: latching current \(I_L\) (minimum anode current that must be reached during the gate pulse or the device unlatches when the pulse ends), holding current \(I_H\) (usually \(I_H < I_L\)), gate trigger current \(I_{GT}\) and voltage \(V_{GT}\), forward breakover voltage, and reverse blocking voltage. Two-transistor analogy (pnp plus npn with collector–base interconnection) is the standard UG picture of latching. An SCR is not a MOSFET: you cannot PWM it at tens of kilohertz with a gate-off command. GTO and IGCT exist as turn-off thyristors; they are named on syllabi but the default UG switch for forced turn-off is now the IGBT or MOSFET.

A power MOSFET is a voltage-controlled majority-carrier device. Gate–source voltage above threshold inverts the channel; drain current in the linear (ohmic) region looks like \(I_D = V_{DS}/R_{DS(on)}\) for first-cut converter loss. \(R_{DS(on)}\) has a positive temperature coefficient, which helps paralleling. Body diode is intrinsic (p-body to n-drain) and is a slow-ish pn diode unless the part is a synchronous-rectifier MOSFET with characterized reverse recovery. Capacitances \(C_{iss}\), \(C_{oss}\), \(C_{rss}\) set gate-drive charge \(Q_g\) and switching energy. MOSFETs win at low voltage and high frequency: 12 V, 48 V, and many 100–200 V rails. They lose to IGBTs when the blocking voltage is hundreds to thousands of volts and the current is tens to hundreds of amperes at a few kilohertz to a few tens of kilohertz, because MOSFET \(R_{DS(on)}\) grows unkindly with voltage rating.

An IGBT combines a MOSFET gate with a bipolar conduction path. The symbol looks like a MOSFET with a p-collector. On-state is a voltage \(V_{CE(sat)}\) (often 1.5–3 V) rather than a resistance, so conduction loss is \(V_{CE(sat)} I_C\) and does not shrink as kindly at light load as a MOSFET’s \(I^2 R\). Tail current at turn-off is the bipolar leftover: current continues after the gate is down, adding switching loss. IGBTs dominate 600 V–1700 V motor-drive and PFC inverter stages at UG depth. Reverse voltage is not a native IGBT talent; an anti-parallel diode (module co-pack) is assumed in voltage-source inverters.

SOA is the region of \(v\)–\(i\) the die may occupy without thermal or second-breakdown failure. A DC SOA is a bounded rectangle or a derated polygon on \(V_{DS}\) versus \(I_D\) (or \(V_{CE}\) versus \(I_C\)) for a stated case temperature and pulse width. Switching SOA (RBSOA for bipolar/IGBT) is a different plot: the turn-off locus must stay inside a clamped voltage and a peak current. Forward-bias SOA and reverse-bias SOA are named separately on BJT/IGBT sheets. Students who size a switch from average current only, and ignore the peak at commutation plus the voltage overshoot from layout inductance, leave the SOA. Thermal resistance \(\theta_{JC}\) and \(\theta_{JA}\) convert dissipation to junction temperature; \(T_J = T_A + P_D \theta_{JA}\) (or a chain through the heatsink). Exceeding \(T_{J,\max}\) is a slow SOA violation. Exceeding \(V_{BR}\) is a fast one.

Other syllabus devices in one paragraph so they do not surprise an exam: the GTO (gate turn-off thyristor) can be turned off by a large negative gate current; the MCT is historical; the TRIAC is two SCRs inverse-parallel with a shared gate, used in AC voltage controllers; the diac is a bidirectional breakover trigger; the IGBT module often includes a NTC thermistor. Snubbers and gate drivers are neighboring units; here, remember that a MOSFET gate is a capacitor that must be charged through a resistor, and an SCR gate is a current pulse with a specified width.

Paralleling and series connection: MOSFETs parallel reasonably because of \(R_{DS(on)}(T)\). IGBTs need matched gate drive and sometimes small emitter resistors. Thyristors in series need sharing resistors and \(dv/dt\) snubbers; in parallel they need matching or forced current share. \(dv/dt\) can false-trigger an SCR (displacement current through the Miller-like junction capacitance); datasheets give a critical \(dv/dt\). \(di/dt\) at turn-on can crowd current and fail the die; a small anode inductor or a gate-current limit appears in older commutation designs.

Switching loss versus conduction loss is the first design split. Conduction: diode \(V_F I_{avg}\) plus a small \(r_f I_{rms}^2\); MOSFET \(I_{rms}^2 R_{DS(on)}\); IGBT \(V_{CE(sat)} I_{avg}\) plus tail. Switching: \(\frac12 V I (t_r+t_f) f_{sw}\) as a crude triangle, plus diode recovery \(Q_{rr} V f_{sw}\). Hard-switched converters pay the full \(VI\) overlap. Resonant and ZVS/ZCS families (named, not designed here) move the locus toward the axes of the SOA.

## Equations

Forward diode (constant-drop plus resistance, UG converter model):

\[
v_D = V_F + r_f i_D,\qquad P_{\mathrm{cond}} \approx V_F I_{\mathrm{avg}} + r_f I_{\mathrm{rms}}^2.
\]

SCR latching condition during a gate pulse of width \(t_g\): anode current must reach \(I_L\) before the pulse ends, and after latching \(i_A > I_H\). Turn-off:

\[
t_{\mathrm{off,circuit}} > t_q,\qquad i_A(t) < I_H \text{ for a reverse-bias interval}.
\]

MOSFET ohmic conduction and gate charge:

\[
P_{\mathrm{cond}} = I_{D,\mathrm{rms}}^2 R_{DS(on)}(T_J),\qquad Q_g = \int i_g\,dt,\qquad \bar{I}_g = Q_g f_{sw}.
\]

Approximate hard-switched overlap energy (triangle, one transition):

\[
E_{\mathrm{on}} \approx \tfrac12 V_{DC} I_L t_{\mathrm{on}},\qquad P_{\mathrm{sw}} \approx (E_{\mathrm{on}}+E_{\mathrm{off}}) f_{sw}.
\]

IGBT conduction:

\[
P_{\mathrm{cond}} \approx V_{CE(sat)} I_{C,\mathrm{avg}} + r_{CE} I_{C,\mathrm{rms}}^2.
\]

Junction temperature (single thermal resistance to ambient, or a sum of case and sink):

\[
T_J = T_A + P_D(\theta_{JC}+\theta_{CS}+\theta_{SA}),\qquad P_D = P_{\mathrm{cond}}+P_{\mathrm{sw}}+P_{\mathrm{drive}}.
\]

SOA as a constraint, not a formula: for a pulse of width \(t_p\),

\[
(v(t),i(t)) \in \mathrm{SOA}(t_p, T_C)\quad\forall t.
\]

Critical rates (thyristor):

\[
\frac{dv}{dt} < \left(\frac{dv}{dt}\right)_{\mathrm{crit}},\qquad \frac{di}{dt} < \left(\frac{di}{dt}\right)_{\mathrm{crit}}.
\]

Duty in later chopper units uses these switches but does not change the device equations. Peak switch voltage in a buck is \(V_{in}\) plus ringing; in a boost it is \(V_{out}\) plus ringing. Always add the spike when checking \(V_{BR}\).

## Methods

1. Name the device class before writing KVL. Diode: on if \(v\) would be forward, off if reverse (check recovery separately). SCR: on only after a gate pulse *and* \(i_A>I_L\); stays on until \(i_A<I_H\). MOSFET/IGBT: on while the gate command is asserted (plus delay times \(t_{d(on)}\), \(t_r\), \(t_{d(off)}\), \(t_f\)).
2. Draw the switching locus on a \(v\)–\(i\) plane. Hard turn-off of an inductive load is a near-constant-current rise of voltage, then current fall — that rectangle must fit in RBSOA. A clamp (freewheel diode, RCD snubber) is how you keep the locus legal.
3. Loss budget: compute RMS and average currents from the topology (later units), then apply the conduction formulas here. Add switching energy times \(f_{sw}\). If \(T_J\) exceeds the rating, either enlarge the sink, slow the switching (usually worse), or change device.
4. Gate drive: MOSFET/IGBT need a voltage (typically 10–15 V, sometimes 0/15 or −5/15). SCR needs a current pulse. Never treat an SCR gate as a CMOS input. Include a gate resistor to set \(di/dt\) of the channel and to damp oscillation.
5. Freewheel path: every inductive current must have a diode or a synchronous switch. Forgetting the diode is a device-destruction method, not a converter.
6. Ratings: \(V_{RRM}\) / \(V_{DSS}\) / \(V_{CES}\) must exceed the worst-case bus plus spike. Average current rating is not the same as RMS or peak. Datasheet average current assumes a specified waveform and case temperature.
7. Parallel/series: check sharing. Do not assume two IGBTs split current equally because the schematic is symmetric.

Worked pattern — MOSFET chopper switch: \(V_{in}=48\,\mathrm{V}\), \(I_L=8\,\mathrm{A}\) continuous, \(D=0.6\), \(f_{sw}=50\,\mathrm{kHz}\), \(R_{DS(on)}=25\,\mathrm{m}\Omega\), overlap times \(t_{on}=t_{off}=40\,\mathrm{ns}\). Conduction: \(I_{rms}=I_L\sqrt{D}=6.20\,\mathrm{A}\), \(P_{\mathrm{cond}}=0.96\,\mathrm{W}\). Switching: \(P_{\mathrm{sw}}\approx 48\cdot 8\cdot 40\times 10^{-9}\cdot 50000=0.77\,\mathrm{W}\) (using \(V I t f\) per edge, two edges). Junction rise depends on \(\theta_{JA}\). The 48 V bus needs a MOSFET rated well above 48 V (80–100 V class is typical) because of ringing.

## Mistakes

- Treating an SCR like a transistor that turns off when the gate goes low. The gate does not turn it off.
- Using \(I_H\) and \(I_L\) interchangeably. Latching is during the pulse; holding is after.
- Sizing a MOSFET from average current and \(R_{DS(on)}\) at 25 °C. \(R_{DS(on)}\) may nearly double at \(T_J=125^\circ\mathrm{C}\).
- Ignoring the body diode reverse recovery in a half-bridge. Dead time plus \(Q_{rr}\) dumps a current spike into the incoming MOSFET.
- Reading SOA as “rated volts times rated amps.” A 600 V, 50 A IGBT is not a 30 kW DC switch; the DC SOA is much smaller, and switching SOA is another plot.
- Forgetting tail current in IGBT switching-loss estimates (using only \(t_f\) of the MOSFET-like edge).
- Putting a MOSFET in a line-commutated rectifier and expecting it to behave as an SCR (or the reverse).
- Assuming Schottky diodes block hundreds of volts at negligible drop; silicon carbide Schottky parts exist, but silicon Schottky voltage is limited.
- Computing diode conduction loss as \(V_F I_{rms}\) or \(V_F I_{peak}\). Average current multiplies the constant drop; RMS multiplies the resistive part.
- Omitting \(dv/dt\) snubbers on series thyristors and then blaming “mystery” false triggering.
- Using \(P=VI\) with peak voltage and peak current as if it were continuous dissipation.
- Confusing TRIAC quadrants with SCR polarity: a TRIAC can conduct both ways; an SCR cannot.
- Checking only \(V_{BR}\) and not the avalanche energy if the layout rings above the clamp.

This unit’s switches reappear in every later converter. If the device model is wrong, the rectifier overlap, the chopper duty formula, and the inverter dead-time all inherit the error.
