# DC–DC choppers: buck, boost, buck–boost, duty

A chopper is a switched DC–DC converter. A controlled switch (MOSFET, IGBT, historically a commutated SCR) periodically connects a DC source to an LC filter and load. The duty ratio \(D=t_{\mathrm{on}}/T_s\) is the primary control knob. UG courses treat the non-isolated buck, boost, and buck–boost in continuous conduction mode (CCM) as the core, then mention discontinuous mode (DCM), four-quadrant choppers, and isolated cousins (forward, flyback) by name. Average voltage and inductor volt-second balance are the method, not small-signal PWM IC design.

## Concepts

Switching DC rather than linear-dropping it is the efficiency story: an ideal switch and diode dissipate nothing, and the inductor and capacitor only store energy. Real devices add \(I^2R\), \(V_F\), and switching energy (unit 01). The pedagogical converter still starts ideal.

Buck (step-down): switch in series with the source, diode freewheeling the inductor when the switch is off, inductor in series with the load, capacitor across the load. In CCM the inductor never reaches zero current. Volt-second balance on \(L\): during \(DT_s\) the inductor sees \(V_{in}-V_{out}\); during \((1-D)T_s\) it sees \(-V_{out}\) (ideal diode). Setting the average inductor voltage to zero gives

\[
V_{out}=D V_{in}.
\]

Load current equals average inductor current. Inductor current ripple is \(\Delta i_L=(V_{in}-V_{out})DT_s/L=(1-D)V_{out}T_s/L\). Capacitor current is the AC part of \(i_L\) if the load is DC, so voltage ripple \(\Delta v_C\approx \Delta i_L T_s/(8C)\) for a triangular inductor current. The switch voltage stress is \(V_{in}\); diode stress is \(V_{in}\).

Boost (step-up): switch to ground after the inductor, diode from the switch node to the output capacitor. When the switch is on, the inductor charges from \(V_{in}\); when off, \(L\) plus \(V_{in}\) feed the output. CCM balance:

\[
V_{out}=\frac{V_{in}}{1-D}.
\]

\(D=0\) gives \(V_{out}=V_{in}\) (diode always on, like a pass-through). \(D\to 1\) would demand infinite voltage; in practice the controller never parks at 100% on, and losses plus DCM change the curve. Output capacitor supplies the load during the on interval, so capacitor ripple is larger than the buck for the same \(C\): \(\Delta v_C\approx I_{out} D T_s/C\). Switch stress is \(V_{out}\); diode stress is \(V_{out}\). Average inductor current is \(I_{out}/(1-D)\), larger than the load — the input current is continuous, which is why boosts appear as PFC front ends.

Buck–boost (inverting): switch in series with \(V_{in}\), inductor from the switch node to ground, diode from the switch node to a negative output capacitor (one common drawing). CCM:

\[
V_{out}=-\frac{D}{1-D}V_{in}.
\]

Magnitude can be above or below \(V_{in}\). Input current is chopped (switch current); output current is chopped (diode current). Both capacitors/filters have a harder job than in the buck. Switch and diode stress is \(V_{in}-V_{out}=V_{in}/(1-D)\) in magnitude. A non-inverting buck–boost (four-switch) exists; UG default is the inverting one-switch cell. Cuk and SEPIC are named relatives with extra capacitors; they are not required for every exam.

Duty ratio is defined on the controlled switch: \(D=t_{\mathrm{on}}/T_s\), \(0\le D\le 1\). Frequency \(f_s=1/T_s\) is chosen from magnetics size versus switching loss (unit 11). Open-loop, \(V_{out}\) follows the CCM formulae if the load is heavy enough to stay in CCM. Closed-loop, a compensator adjusts \(D\) to regulate \(V_{out}\) against \(V_{in}\) and load; UG problems usually give \(D\) or ask for \(D\).

CCM versus DCM: the inductor current touches zero in DCM. Then the simple \(D\) formulae fail. Boundary: \(\Delta i_L/2 = I_{L,\mathrm{avg}}\). For a buck, \(I_{L,\mathrm{avg}}=I_{out}\), so the critical load is \(I_{\mathrm{crit}}=(1-D)V_{out}T_s/(2L)\). Lighter loads enter DCM and \(V_{out}\) rises toward \(V_{in}\) (buck) if \(D\) is held fixed. Always state the mode.

Four-quadrant (class E / dual-converter-like chopper, H-bridge): two buck legs can apply \(+V_{in}\), \(-V_{in}\), or PWM averages in between, and current can reverse. DC drives (unit 09) use this for motoring and regeneration in both directions. First-quadrant chopper is the buck motoring quadrant. Second-quadrant is a boost from the machine (regeneration into the DC bus).

Isolated converters: insert a transformer. Forward is a transformer-isolated buck (reset winding or active clamp). Flyback is an isolated buck–boost (coupled inductor). Push-pull, half-bridge, and full-bridge isolated bucks appear in SMPS courses. This unit’s algebra still starts from \(D\) and volt-second balance, with the turns ratio \(n\) multiplying \(V_{out}\).

Synchronous rectification replaces the diode with a MOSFET to cut \(V_F\) loss at low voltage. Dead time is required. UG analysis can still use the diode CCM equations as a first cut, then replace \(V_F\) with \(I R_{DS(on)}\).

Volt-second balance is not a trick, it is KVL averaged. In periodic steady state the inductor current ends the period where it started, so the net change is zero, so the average voltage is zero. Charge balance is KCL averaged on the capacitor. Together they give the conversion ratio without solving differential equations. The differential equations still decide the ripple and the CCM/DCM boundary, which is why a complete answer names \(L\), \(f_s\), and \(I_{load}\), not only \(D\). If a question gives only \(V_{in}\) and \(D\) and says CCM, it is licensing \(V_{out}=D V_{in}\) (buck) and nothing else.

Waveforms to be able to sketch from memory, buck CCM: switch node is a rectangle \(V_{in}\) then 0; inductor current is a rising then falling triangle on a DC pedestal; capacitor current is that triangle with the DC load removed; output voltage is a small parabolic ripple. Boost CCM: inductor current triangle on a larger pedestal \(I_{out}/(1-D)\); diode current is a pulse of width \((1-D)T_s\); capacitor current is that pulse minus \(I_{out}\), so the capacitor discharges the whole on-time. Those sketches are how you derive \(\Delta v_C\) without a textbook figure.

Loss-aware conversion ratios are first-order perturbations. A buck with diode \(V_F\) is \(V_{out}=D V_{in}-(1-D)V_F\) if the switch is ideal. A boost with diode \(V_F\) cannot quite reach \(V_{in}/(1-D)\). Switch \(R_{DS(on)}\) looks like a small extra series resistor on the input or on \(L\), depending on the topology. Efficiency \(\eta\) then makes \(I_{in}=P_{out}/(\eta V_{in})\). Exam numbers that look inconsistent (input current larger than the ideal \(D I_{out}\) or \((1-D)\) relation) are usually asking for that \(\eta\).

Control comments at UG depth: voltage-mode PWM sets \(D\) from a compensator versus a ramp (unit 07). Current-mode inner loop commands the inductor peak. Neither loop is designed in this unit, but both still obey the same steady-state \(D\). A current-mode buck in CCM still has \(V_{out}=D V_{in}\) in the ideal average; the loop only changes how \(D\) is chosen each cycle. Open-loop lab tests should use a fixed \(D\) and a load heavy enough for CCM, then verify \(V_{out}\) with a DMM and ripple with a scope across the capacitor, not at the switch node.

Isolated cousins map onto the three cells. Forward: buck with a transformer, \(V_{out}=n D V_{in}\), reset required. Flyback: buck–boost with a coupled inductor, \(V_{out}=n D V_{in}/(1-D)\) in CCM (sign depends on dotted output). Isolated boosts exist but are rarer on UG papers. Once the cell is named, reuse the same \(D\) algebra and put \(n\) in the obvious place.

Four-quadrant H-bridge averaging is the DC-drive link. Bipolar PWM spends part of the period at \(+V_{in}\) and part at \(-V_{in}\), so the mean is \((2D-1)V_{in}\) and it is zero at \(D=0.5\). Unipolar PWM of an H-bridge can produce a three-level voltage and a mean \(D_{\mathrm{eff}} V_{in}\) with a different definition of \(D_{\mathrm{eff}}\). Read the definition printed in the question. Regenerative current (machine as source) flows back through diodes or through synchronous MOSFETs into the DC bus; the bus must accept that energy (brake chopper or another load).

## Equations

Duty and period:

\[
D=\frac{t_{\mathrm{on}}}{T_s},\qquad T_s=\frac{1}{f_s}.
\]

CCM ideal conversion (continuous inductor current, ideal switches):

\[
\text{Buck: } \frac{V_{out}}{V_{in}}=D,\qquad \text{Boost: } \frac{V_{out}}{V_{in}}=\frac{1}{1-D},\qquad \text{Buck–boost: } \frac{V_{out}}{V_{in}}=-\frac{D}{1-D}.
\]

Volt-second balance (steady state): \(\langle v_L\rangle=0\). Charge balance: \(\langle i_C\rangle=0\).

Buck inductor ripple and CCM boundary:

\[
\Delta i_L=\frac{(V_{in}-V_{out})D}{f_s L}=\frac{V_{out}(1-D)}{f_s L},\qquad I_{\mathrm{crit}}=\frac{\Delta i_L}{2}.
\]

Boost inductor ripple:

\[
\Delta i_L=\frac{V_{in} D}{f_s L},\qquad I_{L,\mathrm{avg}}=\frac{I_{out}}{1-D}.
\]

Non-ideal buck (switch drop \(V_{sw}\), diode \(V_F\)), still CCM, first-order:

\[
V_{out}=D(V_{in}-V_{sw})-(1-D)V_F.
\]

Average input and output power, ideal: \(P_{in}=P_{out}\). Efficiency \(\eta=P_{out}/P_{in}\) then scales \(I_{in}\).

Four-quadrant H-bridge average voltage (bipolar PWM, duty of one pair \(D\)):

\[
V_{out}=(2D-1)V_{in}.
\]

## Methods

1. Identify topology from the switch–diode–L–C arrangement. Write CCM \(V_{out}(D)\) only after confirming CCM (given, or check \(I>\Delta i/2\)).
2. To find \(D\) from voltages: invert the CCM formula. Buck: \(D=V_{out}/V_{in}\). Boost: \(D=1-V_{in}/V_{out}\). Buck–boost: \(D=|V_{out}|/(V_{in}+|V_{out}|)\).
3. Size \(L\) from a ripple spec, typically 20–40% of \(I_L\). Size \(C\) from \(\Delta v\) spec.
4. Device stress: off-state voltage and on-state current (peak \(I_L+\Delta i/2\)). Add ringing margin.
5. If the question gives \(R\), \(f_s\), \(L\), compute \(I_{out}=V_{out}/R\) after finding \(V_{out}\), then test CCM.
6. Chopper-fed DC motor: \(V_t=D V_{bus}=E_a+I_a R_a\) (motoring buck). Regeneration uses a second-quadrant boost relation.

Worked pattern — buck duty and \(V_{out}\): \(V_{in}=48\,\mathrm{V}\), \(D=0.35\), CCM. \(V_{out}=D V_{in}=16.8\,\mathrm{V}\). If \(R=4.2\,\Omega\), \(I_{out}=4.00\,\mathrm{A}\). If \(L=180\,\mu\mathrm{H}\), \(f_s=40\,\mathrm{kHz}\), \(\Delta i_L=16.8(1-0.35)/(40000\times 180\times 10^{-6})=1.52\,\mathrm{A}\). \(\Delta i/2=0.76<4\), CCM holds.

## Mistakes

- Using \(V_{out}=D V_{in}\) on a boost or buck–boost.
- Applying CCM formulae in DCM (light load, small \(L\)).
- Forgetting the boost inductor current is \(I_{out}/(1-D)\), not \(I_{out}\).
- Setting \(D=V_{out}/V_{in}\) for a boost (that is a buck). Boost \(D=1-V_{in}/V_{out}\).
- Ignoring polarity of the classical buck–boost (output is inverted).
- Computing \(\Delta i_L\) with \(T_{\mathrm{on}}\) but the wrong voltage across \(L\).
- Assuming 100% efficiency when the question gives \(V_F\) and \(R_{DS(on)}\); then \(P_{in}\ne P_{out}\).
- Rating the boost switch at \(V_{in}\) instead of \(V_{out}\).
- Using bipolar H-bridge \(V_{out}=D V_{in}\) instead of \((2D-1)V_{in}\).
- Confusing duty of a pulse-skipping DCM controller with the CCM \(D\).

Duty and \(V_{out}\) are the first numbers in any chopper problem. Later drive units reuse the same algebra with a machine back-emf in place of \(R\).
