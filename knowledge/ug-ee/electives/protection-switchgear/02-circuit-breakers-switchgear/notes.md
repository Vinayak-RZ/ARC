# Arc interruption, circuit-breaker types, and GIS

A relay decision is useless unless a circuit breaker interrupts the current and withstands the recovery voltage. This unit is the switchgear half of the elective: the arc, restrike and RRRV, breaker ratings, oil / air-blast / vacuum / SF6 technologies, isolators and earthing switches, and a first look at gas-insulated switchgear (GIS). Protection logic stays in unit 01. Insulation coordination of the substation (BIL, arresters) lives in the high-voltage elective.

## Concepts

An AC circuit breaker does not “stop current.” It opens contacts, draws an arc, and waits for a current zero. Near zero the plasma cools, the gap dielectric recovers, and the power-system transient recovery voltage (TRV) appears across the contacts. If the dielectric strength rises faster than the TRV, interruption succeeds. If the TRV wins, the arc reignites (reignition at a modest voltage a few tens of microseconds after zero, or restrike at a later peak). Current chopping is interruption of a small inductive current *before* natural zero; the trapped inductive energy \( \tfrac12 L i_{\mathrm{ch}}^2 \) charges stray capacitance and can produce a high chopping overvoltage \( i_{\mathrm{ch}}\sqrt{L/C} \). Vacuum breakers chop more readily than oil; surge capacitors or arresters protect motor and transformer inductances.

Rate of rise of recovery voltage (RRRV) is the initial slope of the TRV. Short-line fault (kilometric fault) is the harsh case for EHV breakers: a fault a few kilometres out produces a triangular travelling-wave TRV with a very high RRRV even though the current is slightly less than a bolted bus fault. Breaker type tests include terminal faults, short-line faults, out-of-phase switching, and capacitive switching (unloaded lines and capacitor banks). Capacitive switching risks restrike: the capacitor holds a DC voltage, the source swings to the opposite peak, and a late restrike can escalate to 3 pu or more. Modern SF6 and vacuum designs with controlled timing reduce that; UG still computes the 2 pu first-restrike picture.

Ratings printed on a nameplate, UG meanings:

- Rated voltage: highest system voltage the breaker may see continuously.
- Rated normal current: heating of the closed path (contacts, tank).
- Rated short-circuit breaking current: RMS AC component the breaker can interrupt (often with a DC offset factor, the “%dc” or time constant of the network).
- Rated short-circuit making current: peak the breaker can close onto, typically \( 2.5 \) times the RMS breaking current at 50 Hz (2√2 with a standard DC offset).
- Rated short-time withstand: thermal \( I^2 t \) for 1 s or 3 s while delayed protection waits.
- Rated operating sequence: e.g. O–0.3 s–CO–3 min–CO for auto-reclose duty.
- Breaking capacity in MVA is a legacy product \( \sqrt{3}\, V I_{\mathrm{sc}} \); modern IEC prefers kA at a stated kV.

Oil circuit breakers: the arc cracks oil into hydrogen and other gases; gas blast and oil turbulence extinguish. Bulk-oil versus minimum-oil. Fire, carbon, and maintenance put them on the way out except as legacy. Air-blast: a stored high-pressure air blast. Noisy, compressor plant, historically EHV. Vacuum: contacts in a sealed bottle, mean free path longer than the gap, metal-vapour arc that diffuses at current zero. Dominant at MV (3.3–36 kV), compact, many operations, chopping and contact welding are the design issues. SF6: excellent dielectric and a high thermal-interruption capability by attaching electrons and by blowing gas through a nozzle (puffer, self-blast, or mixed). Dominant at HV/EHV. Environmental pressure on SF6 as a greenhouse gas is pushing alternatives (vacuum at higher voltages, fluoronitrile mixes); UG still analyses SF6 puffers because that is what existing yards contain.

Dead-tank versus live-tank: dead-tank has earthed metal enclosure (CT cores often around the bushings); live-tank has porcelain or composite chambers at line potential on post insulators. GIS puts the live parts in SF6-filled metal enclosures at a few atmospheres, with bus ducts, disconnectors, earthing switches, and CTs/VTs as modules. Footprint collapses compared with air-insulated switchgear (AIS). Partial discharge, particle traps, and very fast transients (VFT) from disconnector restrikes in GIS are specialist topics named here: a disconnector in GIS restrikes many times while opening a small capacitive current, launching ns-front waves that stress windings and secondary circuits. Earthing switches in GIS may be high-speed to close onto trapped charge.

Isolator (disconnector) versus breaker versus load-break switch: a breaker interrupts fault current. An isolator provides a visible (or assured) isolating gap for maintenance and is not rated to interrupt load, let alone fault — interlocks prevent opening when the breaker is closed. A load-break switch interrupts load current but not full fault current; fuses or a backup breaker handle faults. Earthing switches apply a deliberate earth for work. Transfer bus, main-and-transfer, double-bus, breaker-and-a-half, and ring-bus are layout names: they decide how many breakers a line uses and whether a breaker outage takes the line out. Breaker-and-a-half is the EHV favourite (two lines, three breakers).

Arc voltage is tens to a few hundreds of volts in a well-designed interrupter, small compared with system kV, so the current during the arcing window is still essentially the prospective short-circuit current. Energy in the arc is \(\int v_{\mathrm{arc}} i\,dt\), which heats oil, ablates nozzles, and erodes vacuum contacts. Breaking a small current can be *harder* than a large current for chopping and for capacitive restrike; “small current is easy” is a low-voltage intuition that fails at EHV.

DC interruption is a different problem: no natural zero. HVDC breakers (mechanical with a resonant current-zero injection, or hybrid power-electronic) are not this unit’s design job; the AC current-zero story is.

Reclosing: on overhead lines most faults are transient (lightning, galloping). A high-speed reclose (0.3–1 s dead time) restores the line if the arc path has de-ionized. Cables and GIS do not get high-speed reclose onto a likely permanent fault. Single-pole reclose on EHV keeps two phases closed for stability; the secondary arc on the open phase must extinguish, sometimes with a four-legged shunt reactor.

Switchgear selection on a UG paper is a table: voltage class, fault kA from the study, normal current from load plus margin, indoor/outdoor, AIS vs GIS by space and pollution, vacuum vs SF6 by voltage. Do not specify an oil breaker for a new 33 kV indoor switchboard.

## Equations

Prospective three-phase fault at a breaker (from the core fault pack, as a rating check):

\[
I_{\mathrm{sc}}=\frac{V_{\mathrm{LL}}/\sqrt{3}}{Z_{\mathrm{th}}}.
\]

Making current (50 Hz, standard offset, IEC-style factor 2.5):

\[
i_{\mathrm{make}}=2.5\, I_{\mathrm{sc,rms}}.
\]

Breaking current for rating: the RMS AC component at contact separation, with a DC component \( I_{\mathrm{dc}}=I_{\mathrm{ac}}\sqrt{2}\,e^{-t/\tau} \), \(\tau=L/R\) of the Thevenin source. Asymmetrical breaking current \(\sqrt{I_{\mathrm{ac}}^2+I_{\mathrm{dc}}^2}\).

Chopping overvoltage (undamped single-frequency):

\[
V_{\mathrm{ch}}\approx i_{\mathrm{ch}}\sqrt{\frac{L}{C}}.
\]

Capacitive restrike picture (first restrike, lossless): capacitor charged at \(+V_p\), source at \(-V_p\), gap voltage \(2V_p\); after restrike the voltage can ring toward \(-3V_p\) relative to earth on the capacitor.

TRV (simple series L, shunt C, current chopped at peak of a 1−cos wave — textbook two-parameter):

\[
v_{\mathrm{TRV}}(t)=V_p\bigl(1-\cos\omega_0 t\bigr),\qquad \omega_0=1/\sqrt{LC},\qquad \mathrm{RRRV}\sim V_p\omega_0.
\]

Short-line fault: sawtooth of amplitude \(\propto x I Z_c\) and time \(\propto x/c\), so RRRV \(\propto I Z_c / (2 x/c)\) is high when \(x\) is small. \(Z_c\) is the line surge impedance.

MVA legacy:

\[
S_{\mathrm{sc}}=\sqrt{3}\, V_{\mathrm{LL}} I_{\mathrm{sc}}.
\]

Arc energy (order-of-magnitude):

\[
E_{\mathrm{arc}}\approx V_{\mathrm{arc}} I_{\mathrm{arc}} t_{\mathrm{arc}}.
\]

## Methods

1. From the fault study, read \(I_{\mathrm{sc}}\) at the breaker bus at maximum generation. Apply the making factor 2.5 (or the factor the problem states). Compare with the nameplate kA.
2. Check normal current: load plus transformer capability plus a margin; ambient and enclosure derating if given.
3. For TRV problems, identify terminal fault (1−cos) versus short-line (sawtooth). Compute \(\omega_0=1/\sqrt{LC}\) if L and C are given; RRRV is the initial slope.
4. Chopping: take \(i_{\mathrm{ch}}\) from the problem (vacuum often a few amperes), \(L\) of the load, \(C\) of the surge capacitor or bushing, evaluate \(i\sqrt{L/C}\), compare with insulation or arrester rating.
5. Capacitive switching: draw source sinusoid and trapped DC; first possible restrike at about 2 pu across the gap; mention that a second restrike can escalate.
6. Layout: count how many breakers must open to isolate a fault in main-and-transfer versus breaker-and-a-half. Isolators open only after the breaker confirms open.
7. GIS versus AIS: space, pollution, indoor urban, and VFT/disconnector caution. Do not omit earthing switches on a GIS one-line.

Worked pattern — making: \(I_{\mathrm{sc}}=31.5\,\mathrm{kA}\) RMS. \(i_{\mathrm{make}}=2.5\times 31.5=78.8\,\mathrm{kA}\) peak. A breaker rated 31.5 kA breaking / 80 kA making is acceptable; 25 kA is not.

Worked pattern — chop: \(i_{\mathrm{ch}}=4\,\mathrm{A}\), \(L=0.40\,\mathrm{H}\), \(C=4\,\mathrm{nF}\). \(\sqrt{L/C}=\sqrt{10^8}=10^4\), \(V_{\mathrm{ch}}=40\,\mathrm{kV}\). A 3.3 kV motor wants a surge capacitor to raise \(C\) and cut \(V_{\mathrm{ch}}\).

## Mistakes

Opening an isolator on load. Specifying breaking kA without a making-current check. Using \(\sqrt{2}\) as the making factor (that is the peak of the AC component only, not the offset peak). Reclosing onto a cable fault as if it were an overhead lightning flashover. Treating vacuum chopping as negligible on a dry-type transformer or a motor. Confusing restrike (late, high voltage) with reignition (soon after zero). Using DC interruption intuition (force current to zero with an arc chute) on an AC EHV TRV problem. Forgetting that a short-line fault is severe because of RRRV, not because the current is larger than a bus fault. Mixing RMS breaking current with peak making current in the same inequality. Assuming SF6 GIS needs no earthing switch. Drawing a load-break switch as fault-rated. Computing MVA as \(V I\) without \(\sqrt{3}\) on a three-phase nameplate. Ignoring DC offset when the problem gives \(X/R\) and a contact-parting time. Calling a disconnector a circuit breaker because it is drawn as a square on a sloppy one-line.

TRV and power-frequency withstand are different tests. A breaker can interrupt 40 kA and still fail a lightning impulse on the open gap if the open-gap BIL is wrong; that is insulation, not interruption. Keep the two rating families separate.

Environmental and safety notes that stay UG: oil fire; SF6 by-products after heavy arcing (do not sniff a tank); vacuum bottle integrity (a “vacuum checker”); GIS enclosure currents and earthing. None of these change the RRRV formula; they change whether the yard is allowed to exist.

Auto-reclose dead time is not TMS. TMS is a relay curve; dead time is a mechanical and de-ionization wait. Mixing them produces a coordination graph that never existed.
