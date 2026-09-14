# Inverter interface and islanding at UG level

Unit 01 made power at the terminals of a PV array, a turbine, or a diesel. This unit is how that power meets a 50 Hz (or 60 Hz) grid: the inverter as a current or voltage source, PLL, P–Q dispatch, harmonics, ride-through as a name, and islanding detection. It is not a firmware course and not a grid-code lawyer’s appendix. Protection-and-switchgear remains the relay pack; here the DG *is* the source that those relays may see.

## Concepts

A grid-tied PV or Type-4 wind plant presents a VSI (voltage-source inverter) at the point of common coupling (PCC) through a filter (L, LCL) and usually a transformer. In the usual *grid-following* control, the inverter is a current source in the PLL frame: a phase-locked loop estimates the PCC angle \(\theta\), \(d\)–\(q\) current commands set \(P\) and \(Q\),

\[
P=\frac32(v_d i_d+v_q i_q),\qquad Q=\frac32(v_q i_d-v_d i_q)
\]

in SI peak conventions (or \(3 V_{\mathrm{ph,rms}} I\cos\phi\) in phasors). With \(v_q=0\) by PLL alignment, \(P\propto i_d\), \(Q\propto -i_q\) (sign of \(Q\) depends on the \(q\) definition). MPPT (unit 01) sets the P command up to the inverter rating; Q command may be zero (unity pf), a voltage droop, or a grid-code schedule. Current limit: \(|i|\) cannot exceed the semiconductor rating, so a voltage sag that tries to hold P will hit the current ceiling and P falls — that is why fault contribution of an inverter is typically 1.1–1.5 pu current, not the 5–8 pu of a synchronous machine.

Grid-forming inverters *make* the voltage and frequency (droop \(P\)–\(f\), \(Q\)–\(V\), or a virtual synchronous machine). They can black-start a microgrid. Most rooftop PV today is still grid-following and *cannot* energize a dead feeder by design. Intentional islanding of a microgrid needs at least one grid-forming source (inverter or diesel). Unintentional islanding is the hazard: a feeder trips at the substation, DG keeps a pocket of load alive at a foreign voltage and frequency, line crews see a live line, and reclosing the substation breaker is out-of-phase.

Islanding detection, UG split:

- Passive: under/over voltage (27/59), under/over frequency (81), rate of change of frequency (ROCOF), vector shift. Cheap; fail to detect a *balanced* island where DG power ≈ local load (non-detection zone, NDZ).
- Active: the inverter perturbs (impedance measurement, active frequency drift, Sandia frequency shift). Smaller NDZ; can interact with other inverters.
- Transfer-trip / direct transfer trip (DTT): the feeder breaker tells the DG to stop. Communications, not a local guess. Used on larger MV DG.
- IEEE 1547 / IEC 61727 / local grid codes specify trip times and voltage/frequency windows; UG remembers that anti-islanding exists and that a matched P–Q island is the hard case, not the numbers of a particular year of 1547.

Reclosing: distribution reclosers wait 0.3–2 s; DG must cease to energize before the reclose (or the reclose must be blocked). A synchronous DG island can run on governor/AVR and look “fine” to passive relays if load matches — that is the classic NDZ. Inverters often drift because the PLL and the P–f or Q–V loops are not a perfect match to the load; active methods exploit that.

Harmonics: a PWM inverter has switching-frequency sidebands (filter them with LCL) and low-order harmonics from dead time and from a distorted PCC voltage (the current loop follows a dirty v, or the PLL is dirty). Grid codes cap \(I_{\mathrm{THD}}\) and individual harmonics. Resonance of an LCL with a capacitor bank on a weak feeder is a real commissioning problem; UG names it. Do not treat the inverter as a sinusoidal voltage behind \(X''\) unless the problem says grid-forming.

Ride-through (LVRT / FRT): old anti-islanding tripped on any sag; modern codes demand that large plants *stay connected* through a specified voltage–time envelope and often inject reactive current. That is the opposite of a 27 trip. UG: small rooftop may still trip; a 50 MW wind plant will have an LVRT curve. Do not set 27 instantaneous at 0.9 pu on a plant that must ride through 0.2 pu for 150 ms.

Transformer interface: many inverters are three-phase three-wire; a Δ–Y transformer provides the zero-sequence path for the feeder. Grounding of the Y determines whether an earth fault on the feeder is seen. G59/G99 (UK) and similar interconnection rules are named as “there is a standard,” not copied.

Power factor and Q: at the PCC, \(S=\sqrt{P^2+Q^2}\le S_{\mathrm{rated}}\). Exporting P at 0.95 leading or lagging is a voltage-control tool (unit 01’s \(\Delta V\approx (RP+XQ)/V\)). Weak grids (high \(X/R\)) need Q; high \(R/X\) rural feeders need P reduction or R-compensation more than Q.

PLL basics: a Park transform of the PCC voltage, PI on \(v_q\) to drive it to zero, integral is \(\omega\). A phase jump (fault, island) makes a transient in \(\omega_{\mathrm{est}}\). SRF-PLL is the UG block; sequence-filter PLLs for unbalanced faults are named. Loss of PLL in a deep sag is why some current references freeze or switch to an internal oscillator (grid-forming behaviour under fault).

Synchronous DG (diesel, small hydro, CHP): interconnection is a generator with a breaker, reverse-power (32) if it must not motor, loss-of-mains (ROCOF/vector shift), and short-circuit contribution into the existing coordination study. It is not “an inverter with a PLL.” Keep the two one-lines different.

## Equations

Three-phase inverter power (rms phasors):

\[
P=\sqrt{3}\, V_{LL} I_L\cos\phi,\qquad Q=\sqrt{3}\, V_{LL} I_L\sin\phi.
\]

Current-limited fault (order of magnitude):

\[
I_{\mathrm{fault}}\approx 1.1\text{–}1.5\, I_{\mathrm{rated}}\quad(\mathrm{grid\text{-}following\ VSI}).
\]

Apparent-power disk:

\[
P^2+Q^2\le S_{\mathrm{rated}}^2.
\]

Simple P–f droop (grid-forming):

\[
\omega=\omega_0-m_p(P-P_0),\qquad V=V_0-m_q(Q-Q_0).
\]

Feeder \(\Delta V\) (repeat from unit 01, interconnection use):

\[
\Delta V\approx\frac{RP+XQ}{V}.
\]

THD:

\[
I_{\mathrm{THD}}=\frac{\sqrt{\sum_{h\ge 2} I_h^2}}{I_1}.
\]

Island power mismatch (passive NDZ intuition): if \(\Delta P=P_{\mathrm{DG}}-P_{\mathrm{load}}\) and \(\Delta Q=Q_{\mathrm{DG}}-Q_{\mathrm{load}}\) are both small, \(V\) and \(f\) stay inside the 27/59/81 windows.

PLL (qualitative SRF): \(\dot{\theta}=\omega_0+K_p v_q+K_i\int v_q\).

Ride-through: voltage–time envelope \(V_{\mathrm{PCC}}(t)\) must remain above a piecewise curve; no equation to memorize beyond “area of required stay-in.”

Filter (single L):

\[
v_{\mathrm{inv}}-v_{\mathrm{pcc}}=L\frac{\mathrm{d}i}{\mathrm{d}t}.
\]

PWM voltage (from the PE pack, linear SPWM): \(V_{LL,1}\approx 0.612\, m_a V_{\mathrm{dc}}\).

## Methods

1. Classify the source: grid-following inverter, grid-forming inverter, or synchronous DG. Draw P, Q, and current limit.
2. Interconnection study at UG: reverse power, voltage rise at min load / max DG, fault current (inverter clipped, machine from \(X'\)), protection (27/59/81, 32, 50/51, transfer trip if given).
3. Islanding: compute \(\Delta P,\Delta Q\) if load and DG are given. If both ≈ 0, say passive NDZ; recommend active or DTT.
4. Rating: \(S=\sqrt{P^2+Q^2}\). If Q support is required, derate P.
5. Harmonics: if \(I_h\) are given, THD; otherwise name LCL and switching frequency as the mitigation.
6. Reclose coordination: DG trip time < reclose dead time, or supervisory transfer trip.
7. Do not use infinite-bus \(P=EV\sin\delta/X\) as the PV inverter model unless the problem says grid-forming with an internal \(E\angle\delta\).

Worked pattern — disk: \(S=100\,\mathrm{kVA}\), P from MPPT \(80\,\mathrm{kW}\). \(|Q|\le\sqrt{100^2-80^2}=60\,\mathrm{kvar}\).

Worked pattern — island: DG 50 kW, load 50 kW + 2 kvar of magnetizing, inverter at unity pf. \(\Delta P=0\), \(\Delta Q=-2\,\mathrm{kvar}\). Voltage may stay, frequency may drift slowly; 81 might eventually trip, 27/59 might not. Active islanding or DTT is the reliable answer.

## Mistakes

Treating a rooftop inverter as a voltage source behind \(X_d'\) for a bolted-fault kA. Setting 27 so tight that LVRT is impossible on a plant that must ride through. Assuming passive 81 always catches an island (matched NDZ). Grid-forming and grid-following drawn as the same block. \(P=\sqrt{3}VI\) without \(\cos\phi\) when Q is nonzero, then claiming S = P. Reclosing onto an island without a synch-check. Using Type-3 DFIG fault-current numbers on a Type-4 full converter (different). PLL angle as the *power-angle* \(\delta\) of a synchronous machine in \(P=EV\sin\delta/X\) without a grid-forming inner voltage. THD of voltage and current swapped. Anti-islanding as a substitute for a mechanical disconnect that the utility can see. Diesel ROCOF settings copied onto a stiff inverter plant (different inertia). Exporting P on a weak rural feeder and “fixing” voltage only with Q when \(R\gg X\).

IEEE 1547 editions differ. Do not quote a trip time from memory as if it were physics. The physics is NDZ, current limit, and PLL.

A microgrid *intentional* island is a feature: grid-forming, load shedding, black start. An *unintentional* island is a protection failure. The same inverter firmware can do both; the difference is a transfer-trip and a mode switch, not a different MPPT.

Unit 01’s \(C_p\) and FF do not change because a PLL exists. Keep device power and interconnection in separate calculations, then clip \(P\) by \(S_{\mathrm{rated}}\) and by current limit under sag.

Unbalanced faults: a three-wire inverter cannot feed \(I_0\). Negative-sequence current may be controlled to zero (balanced currents) or used to support the healthy phases, depending on the code. UG fault studies that put a PV plant into the sequence network as a positive-sequence current source plus \(I_2=0\) are consistent with that. A grounded-Y synchronous DG *does* feed \(I_0\) and changes residual-current protection. Mixing those two models on one feeder is a coordination bug.

Weak-grid PLL: a large inverter on a high-\(Z\) feeder can make the PCC angle a function of its own current (the plant is a fraction of the short-circuit level). SRF-PLL then hunts. Short-circuit ratio \(\mathrm{SCR}=S_{\mathrm{sc}}/S_{\mathrm{plant}}\) below about 3 is the UG warning flag, the same language as LCC-HVDC in the core pack. Grid-forming or a slower PLL is the mitigation; “just raise \(K_p\)” is not.

LCL resonance: capacitor current plus grid inductance makes a peak near a kilohertz. Active damping in the current loop or a damping resistor in the capacitor branch knocks it down. A THD number that explodes after a feeder capacitor bank is switched in is this peak, not a new PWM strategy. Report the switching frequency and the filter as a pair.

Cease-to-energize is not the same as an isolation gap. A visible or lockable disconnect is still required for crew safety even if the inverter’s 27/81 opened. Anti-islanding is the automatic layer; the disconnect is the procedural layer. Do not skip the disconnect on a one-line because the NDZ paragraph was long.
