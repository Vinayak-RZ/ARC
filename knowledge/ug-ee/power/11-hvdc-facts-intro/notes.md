# HVDC and FACTS at undergraduate level

High-voltage DC (HVDC) and flexible AC transmission systems (FACTS) are the controllable-power overlay on an otherwise mostly passive AC grid. A first course does not design valve snubbers or MMC capacitors; it explains why DC links exist, the two classical converter families (line-commutated current-source and voltage-source/MMC), the basic real-power formula of a DC line, and the FACTS zoo at the level of what each device controls (series \(X\), shunt \(Q\), or both). Power-electronics internals live in the power-electronics pack. Voltage-control capacitors and reactors that are switched, not power-electronic, live in unit 12.

## Concepts

Why HVDC: (1) two AC systems that do not share a stable common frequency, or that would fight through a high-angle AC tie, can exchange scheduled power through DC without a synchronism constraint; (2) long overhead or cable distance — AC cables pay a charging-Mvar tax that HVDC cables do not; (3) right-of-way: a bipolar DC line can carry more P for a given conductor and insulation width than a three-phase AC line in some comparisons; (4) controllable P, fast reversal on VSC, modulation for damping. Why not always HVDC: converter cost, harmonics (LCC), reactive-power demand (LCC), DC fault interruption (VSC, improving with breakers and MMC), and multiterminal protection complexity.

Line-commutated converters (LCC, thyristor, current-source): a 12-pulse bridge (two 6-pulse bridges fed by Y and Δ windings) is the classic terminal. DC current is unidirectional in the valves; power reversal is by DC voltage polarity reversal. The inverter needs a reasonably strong AC system (minimum short-circuit ratio) to commutate. Reactive power consumption is on the order of 50–60% of P at typical firing/extinction angles; large filter and shunt-capacitor banks sit at the AC yard. Overlap angle \(\mu\) reduces DC voltage. UG formulas:

\[
V_{d0}=\frac{3\sqrt{2}}{\pi}V_{LL},\qquad V_d=V_{d0}\cos\alpha-\frac{3\omega L_c}{\pi}I_d
\]

for a 6-pulse bridge (12-pulse scales voltages with series bridges). Extinction angle \(\gamma\) at the inverter, with \(\gamma_{\min}\) against commutation failure. Harmonics: 6-pulse has 5th and 7th on AC, 6th on DC; 12-pulse cancels those, leaving 11th/13th and 12th.

Voltage-source converters (VSC, IGBT or similar, including MMC): DC voltage polarity stays the same; power reversal is by current reversal — natural for DC cables with no voltage reversal. Independent P and Q control at the AC terminal within the current limit (a P–Q disk). Weak-AC and even black-start capability that LCC lacks. DC faults: a two-level VSC diode path can feed a DC short from the AC side unless extra switches or a DC breaker interrupt; MMC with full-bridge submodules can drive DC voltage down. Filters are smaller than LCC. This is the technology of recent cable links and of many back-to-back ties.

Point-to-point, back-to-back (no DC line, only converters, for asynchronous interconnection), and multiterminal (several converters on one DC grid). Bipolar: two poles, earth or metallic return; a pole outage can still carry about half with earth return if permitted. Monopolar earth-return has environmental and transformer-DC-bias issues.

Power on a DC line: \(P=V_d I_d\). Two terminals, resistances \(R\), \(P\) is set by the current order and the voltage difference. LCC uses current control at one end and voltage (or \(\gamma\)) control at the other; a VDCOL (voltage-dependent current order limit) reduces \(I_d\) during AC depressions. VSC uses a DC-voltage-controlling terminal and a P-controlling terminal, analogous to slack and PV in AC, or droop in multiterminal.

FACTS (IEEE-style names, UG meanings):

- Switched shunt capacitors/reactors and on-load tap changers are “slow FACTS” cousins; true FACTS are power-electronic.

- SVC (static var compensator): thyristor-controlled reactor plus switched or thyristor-switched capacitors. A variable shunt susceptance \(B\) at a bus, with a V–I characteristic and a slope. Controls voltage, provides damping if modulated, cannot exchange P except losses.

- STATCOM: VSC shunt, current source within a ±I limit, better low-voltage performance than SVC (SVC’s capacitive \(I=\omega C V\) collapses with V; STATCOM can hold current).

- TCSC (thyristor-controlled series capacitor): variable series capacitive reactance in a line, raises \(P_{\max}=EV/(X-X_C)\), used for series compensation with control (subsynchronous resonance is a design constraint).

- SSSC: VSC in series, injects a voltage in quadrature with current (reactive series).

- UPFC: series plus shunt VSCs sharing a DC bus; can control P and Q on a line and bus voltage, the most general two-bus controller.

- HVDC itself is sometimes listed as a “network FACTS” because it controls P on a corridor.

UG exam skill: given a lossless line \(P=(V_s V_r/X)\sin\delta\), say whether a series device (changes \(X\)) or a shunt device at the midpoint (raises midpoint V, equivalent to a smaller effective X for P) is being used. Midpoint shunt compensation to \(V_m=V\) on a line with two equal \(X/2\) halves gives \(P=(2V^2/X)\sin(\delta/2)\), which has a higher small-angle stiffness.

Subsynchronous resonance (SSR) with series capacitors and thermal-plant shafts is a warning label on high series compensation, not a full eigenvalue study here.

Filters and reactive banks at LCC stations must be switched with P level; they also affect nearby AC voltage (unit 12). Commutation failure at the inverter is an AC-voltage-dip problem: the valve does not recover and DC current is interrupted or the bridge shorts. VSC does not commutate from the AC system in the same way.

Short-circuit ratio (SCR) at an LCC inverter is \(S_{\mathrm{sc}}/P_{\mathrm{dc}}\) at the AC bus. Values below about 2–3 (order-of-magnitude UG memory, not a code) mean weak AC: voltage flickers, commutation fails more easily, and a STATCOM or synchronous condenser is often specified. VSC links advertise operation at SCR well below 1, including islanded grids. Effective SCR including nearby shunt capacitors is lower than the raw SCR because capacitors reduce the Thevenin \(X\) in a voltage-sensitive way — treat “ESCR” as a keyword.

Harmonics: a 12-pulse LCC still needs AC filters for 11th and 13th and a DC-side smoothing reactor plus DC filters for 12th. Telephone interference and IEEE/IEC harmonic limits are planning constraints. MMC-VSC has much smaller characteristic harmonics; transformer inrush and control-base harmonics still exist. Do not specify a 1970s filter yard on an MMC station.

Power reversal: LCC bipolar with overhead lines can reverse \(V_d\) in tens of milliseconds to hundreds, but cables with dielectric that dislike reversal prefer VSC. Scheduled seasonal reversal (hydro to thermal and back) is an operations reason to choose VSC or to accept LCC cable-stress limits.

FACTS versus switched shunt: a mechanically switched capacitor is not a FACTS device in the strict CIGRE/IEEE list, but it is the first Q resource. An SVC is the thyristor-controlled upgrade. Exam questions that say “cheapest voltage support at a 132 kV rural bus” want switched capacitors; “fast flicker control at an arc-furnace bus” want SVC or STATCOM. Series devices change P transfer more than they change a local bus V, though the two couple.

UPFC degrees of freedom: shunt VSC holds the DC voltage and the bus \(|V|\) (or Q); series VSC injects \(V_{se}\) with two components, one in quadrature with current (Q on the line) and one in phase (P on the line). That is three AC controls, matching the UPFC’s reputation. A cheaper “IPFC” or “SSSC plus STATCOM” is a subset. UG should not draw an UPFC on every corridor; it is a last-resort controllable-path tool.

## Equations

Six-pulse ideal no-overlap no-delay DC voltage: \(V_{d0}=(3\sqrt{2}/\pi)V_{LL}\). With delay \(\alpha\) and overlap (as above).

Twelve-pulse: two six-pulse bridges in series on DC, \(V_d\) doubles for the same \(V_{LL}\) on each transformer secondary.

DC line: \(I_d=(V_{d,\mathrm{rect}}-V_{d,\mathrm{inv}})/R_{\mathrm{line}}\), \(P_{\mathrm{inv}}=V_{d,\mathrm{inv}}I_d\).

Lossless AC line: \(P=(V_s V_r/X)\sin\delta\). With series capacitor \(X_C\): replace \(X\) by \(X-X_C\).

SVC: \(Q=-B V^2\) with \(B_{\min}\le B\le B_{\max}\) (sign: capacitive \(B>0\) supplies Q to the bus in the generator convention used in many FACTS notes — be consistent with load-convention \(Q_C=-\omega C V^2\) absorbed by a capacitor). STATCOM: \(I_q\) between \(\pm I_{\max}\), \(Q=V I_q\).

Midpoint shunt compensation (equal halves, \(V_m\) fixed):

\[
P=\frac{2 V_s V_m}{X}\sin\frac{\delta}{2}\quad (V_s=V_r=V_m\text{ often}).
\]

## Methods

To decide LCC vs VSC in a one-paragraph design question: long overhead with strong AC and cost pressure → LCC still appears; cable, weak AC, tight Q control, urban VSC → VSC/MMC. Back-to-back asynchronous → either, modern often VSC.

To compute a DC operating point: get \(V_{d0}\) from AC voltage and transformer tap, apply \(\cos\alpha\) and overlap drop, enforce \(I_d\) from current order, check inverter \(\gamma\).

To place FACTS: voltage problem at a bus → shunt SVC/STATCOM or capacitor (unit 12); thermal/angle limit on a corridor → series TCSC/SSSC or a new line or HVDC; simultaneous P and Q steering → UPFC (rare, expensive).

Checks: LCC \(Q\) demand is large and lagging at both ends; VSC \(Q\) can be leading at both; DC \(P\) matches both ends except \(I^2R\); series compensation degree \(X_C/X_{\mathrm{line}}\) often 20–70% in examples, not 100%.

## Mistakes

Saying HVDC “has no reactive power” — the DC line does not, the LCC terminals do. Reversing LCC power without reversing \(V_d\). Treating SVC as a real-power source. Using \(P=V^2/X\) without \(\sin\delta\) after inserting a TCSC. Assuming STATCOM Q falls as \(V^2\) (that is the capacitor). Applying commutation-failure stories to MMC-HVDC as if it were LCC. Forgetting 12-pulse harmonic cancellation and specifying huge 5th-harmonic filters on a 12-pulse yard. Designing a DC cable for voltage reversal when the specification is VSC. Using AC SIL as the HVDC rating. Putting a TCSC in a shunt slot on the one-line. Claiming UPFC is just two SVCs. Ignoring minimum SCR for LCC inverters. Mixing 6-pulse \(V_{d0}\) with a 12-pulse current as if the formulas were interchangeable without series addition of voltages.
