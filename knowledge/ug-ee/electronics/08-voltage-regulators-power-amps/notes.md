# Series voltage regulators and class A/B/AB power amplifiers

A small-signal amplifier is allowed to dissipate milliwatts into a 10 kΩ load. A power stage must deliver watts into 8 Ω or a 5 V rail at amperes, stay inside the SOA, and keep the output voltage independent of line and load. This unit covers the series linear regulator (Zener reference plus emitter follower, then the 78xx idea), dropout and ripple rejection, and the class-A / class-B / class-AB output stages that make analog power.

## Concepts

A linear series regulator is a closed-loop voltage-series feedback amplifier whose output is a DC voltage. The pass element (BJT or MOSFET) sits in series with the unregulated input. A reference (Zener, or a bandgap on-chip) is compared with a fraction of \(V_{out}\). The error amplifier drives the pass element so that \(\beta V_{out}=V_{ref}\), hence \(V_{out}=V_{ref}/\beta\). Discrete UG circuit: Zener plus resistor as reference, NPN emitter follower as pass transistor, sometimes a second transistor as a primitive error amp (the "amplified Zener" / series regulator with feedback). Three-terminal ICs (7805, LM317) are this loop with thermal shutdown and current limit.

Dropout: \(V_{in}-V_{out}\) must exceed \(V_{CE,sat}\) (plus a base-drive budget) for an NPN; a PNP or PMOS low-dropout (LDO) topology can run to a few hundred millivolts. Power in the pass element is \(P_D=(V_{in}-V_{out})I_L\). Heatsink design uses \(\theta_{JA}\) so that \(T_j=T_a+P_D\theta_{JA}<T_{j,\max}\). Current limit: a sense resistor in the emitter (or a foldback network) steals base current when \(I_L R_{sense}\approx 0.7\,\mathrm{V}\). Foldback reduces \(I_{limit}\) as \(V_{out}\) collapses, so a short dissipates less than \(V_{in} I_{limit}\).

Line regulation: \(\Delta V_{out}/\Delta V_{in}\) at fixed \(I_L\). Load regulation: \(\Delta V_{out}/\Delta I_L\) at fixed \(V_{in}\). Ripple rejection (PSRR) is the AC version of line regulation; a 100 Hz rectifier hum on \(V_{in}\) is attenuated by the loop gain. A pre-filter capacitor and a post-regulator capacitor (the 7805's 0.33 µF / 0.1 µF) keep the loop quiet. Never float a 78xx without input and output capacitors near the package.

Shunt regulators (Zener across the load, series dropping resistor) waste current in the Zener even at light load and cannot source more than the extra current in \(R_s\). They still appear as exam problems and as references.

Switching regulators (buck/boost) belong to power electronics. Mention only that efficiency \(\eta=P_{out}/P_{in}\) of a linear regulator cannot exceed \(V_{out}/V_{in}\) for a series pass device.

Power amplifiers classify by conduction angle of the output device.

Class A: device conducts \(360^\circ\). Q-point at the centre of the AC load line. Maximum theoretical efficiency 25 % for a resistive collector load, 50 % for transformer-coupled or current-source-loaded class A (the other half of the supply voltage is not wasted in a collector resistor). Distortion can be very low; idle dissipation equals or exceeds the maximum load power. Used in small-signal stages and boutique audio, not in 50 W supplies.

Class B: two complementary devices, each conducting \(180^\circ\), emitter-follower push-pull. Idle current zero. Theoretical efficiency \(78.5\,\%=\pi/4\) at full sine output. Crossover distortion: both devices off near \(v_o=0\) because each \(V_{BE}\) must be overcome. That dead zone is audible and ugly on a scope.

Class AB: bias the two bases a couple of diode drops apart (diode bias, or a \(V_{BE}\) multiplier \(R_2/R_1\) across a transistor). Both devices slightly on at idle, so the handover is smooth. Efficiency a bit below class B; idle dissipation small. This is the analog audio and linear-regulator output stage of record. Thermal coupling of the bias diodes to the output transistors is not optional: as the outputs heat, \(V_{BE}\) falls, idle current would run away (thermal runaway) unless the bias voltage also falls.

Class C: conduction \(<180^\circ\), used with a tuned load in RF, not as a linear audio stage. Class D: switching, PWM, power-electronics territory.

AC load line of a transformer-coupled class-A stage: DC load is the winding resistance (almost vertical if \(R_{Cu}\) is small), AC load is \(n^2 R_L\). Maximum symmetrical swing is \(I_C R_{AC}\) in current and \(V_{CEQ}\) in voltage if the transformer allows \(v_{ce}\) to swing about \(2V_{CC}\). Ratings: \(V_{CE,max}\), \(I_{C,max}\), \(P_{D,max}\), and the SOA curve (second breakdown in BJTs). Never size a power BJT by \(P_D=V_{CE}I_C\) at a point outside the SOA.

Complementary symmetry (NPN+PNP) needs matched \(\beta\) and \(V_{BE}\), which discrete pairs only approximately provide. Quasi-complementary: two NPNs with a PNP driver on one side, common when good PNP power parts were scarce. MOSFET output stages use \(V_{GS}\) bias instead of \(V_{BE}\) and have a different temperature coefficient (\(V_{GS(th)}\) vs mobility) that can be designed for thermal stability.

Heat: \(T_j=T_a+P_D(\theta_{JC}+\theta_{CS}+\theta_{SA})\). Mica washer plus grease is \(\theta_{CS}\). A 5 W dissipation in a TO-220 without a heatsink is a failed part.

## Equations

Series regulator (feedback):

\[
V_{out}=V_{ref}\left(1+\frac{R_1}{R_2}\right)
\]

for the usual divider from \(V_{out}\) to the error-amp inverting input, \(V_{ref}\) on the noninverting input (LM317 uses \(V_{ref}=1.25\,\mathrm{V}\) between \(OUT\) and \(ADJ\)).

Simple Zener-follower:

\[
V_{out}=V_Z-V_{BE},\qquad I_Z=\frac{V_{in}-V_Z}{R_s}-I_B,\qquad I_B=\frac{I_L}{\beta+1}.
\]

Pass dissipation:

\[
P_D=(V_{in}-V_{out})I_L.
\]

Linear-regulator efficiency (series):

\[
\eta=\frac{V_{out}I_L}{V_{in}I_{in}}\approx\frac{V_{out}}{V_{in}}.
\]

Class-A, resistive collector, maximum efficiency:

\[
\eta_{\max}=\frac{P_{L,\mathrm{ac}}}{P_{\mathrm{dc}}}=\frac14=25\,\%.
\]

Class-B push-pull, sine, peak \(V_m\) on each half, rail \(\pm V_{CC}\):

\[
P_{dc}=\frac{2 V_{CC} V_m}{\pi R_L},\quad P_L=\frac{V_m^2}{2R_L},\quad\eta=\frac{\pi}{4}\frac{V_m}{V_{CC}}\le\frac{\pi}{4}.
\]

Crossover-free class-B peak dissipation per transistor occurs below full swing (at \(V_m=2V_{CC}/\pi\)).

\(V_{BE}\) multiplier:

\[
V_{\mathrm{bias}}=V_{BE}\left(1+\frac{R_2}{R_1}\right).
\]

Thermal:

\[
T_j=T_a+P_D\theta_{JA},\qquad \theta_{JA}=\theta_{JC}+\theta_{CS}+\theta_{SA}.
\]

## Methods

1. Regulator DC: assume the loop holds \(V_{out}\) at the designed value. Compute \(I_L\), then \(I_{pass}\), then \(P_D\), then dropout margin \(V_{in,min}-V_{out}\). If \(V_{in}\) sags below dropout, the loop is open and \(V_{out}\) follows \(V_{in}\) minus a \(V_{BE}\) or \(V_{sat}\).
2. Zener-follower: check \(I_Z\) at maximum \(V_{in}\) and minimum \(I_L\) (Zener overload) and at minimum \(V_{in}\) and maximum \(I_L\) (Zener extinguishes, regulation dies).
3. Class-A: draw DC and AC load lines. Maximum undistorted \(V_m\) is the smaller of the distances to cut-off and to saturation along the AC line.
4. Class-B: compute \(P_L\), \(P_{dc}\), \(\eta\), and \(P_{D,\mathrm{each}}=(P_{dc}-P_L)/2\). Size the heatsink for the *worst-case* \(P_D\), not for full-swing efficiency.
5. Class-AB: set idle current a few milliamps to tens of milliamps. Bias network must track \(T_j\).
6. Always check SOA and \(V_{CE,max}\) (inductive kick, transformer doubling).

## Mistakes

- Quoting 78 % efficiency for a class-A stage, or 25 % for class B.
- Forgetting two devices share class-B dissipation; quoting the total as if it were one transistor's \(P_D\).
- Crossover: biasing class B with zero idle and then blaming the speakers. That distortion is the missing \(2V_{BE}\) dead zone.
- Thermal runaway: mounting bias diodes on the chassis instead of on the output-transistor tab.
- Regulator: sizing the series resistor of a Zener reference from the *output* current instead of the Zener's own current budget.
- LDO: using an NPN emitter follower and expecting 0.2 V dropout. The follower needs about 0.7 V plus the error-amp ceiling; dropout is \(>1\,\mathrm{V}\).
- LM317: current through the ADJ divider must greatly exceed \(I_{ADJ}\) (typically 50–100 µA); a 1 MΩ divider will not regulate.
- Efficiency of a 5 V linear regulator from 12 V: students write 90 % because the part "looks efficient". \(\eta\approx 5/12=42\,\%\); the rest is heatsink.
- Transformer-coupled class A: allowing \(v_{CE}\) only up to \(V_{CC}\). The transformer can swing toward \(2V_{CC}\).
- No heatsink calculation. A part rated 50 W *with* \(\theta_{SA}=1^\circ\mathrm{C/W}\) is a 2 W part in free air.

SOA reading. A power BJT datasheet plots \(I_C\) vs \(V_{CE}\) with a thermal limit (hyperbola \(P_D=V_{CE}I_C\)), a current limit, a voltage limit, and a second-breakdown boundary that cuts the hyperbola at high \(V_{CE}\). A class-A stage sitting at \(V_{CE}=30\,\mathrm{V}\), \(I_C=0.5\,\mathrm{A}\) is a 15 W thermal point; if the SOA second-breakdown line is at 0.3 A at 30 V, the device is illegal even though \(P_D<P_{D,\max}\). MOSFET SOA in linear mode has its own spiral of hot-spot issues; switching-mode SOA is more generous.

Current limiting vs foldback. Simple limit: \(I_{max}=0.7/R_{sense}\), constant. Short-circuit dissipation \(V_{in}I_{max}\) can be tens of watts. Foldback: as \(V_{out}\) falls, the limit current falls, so a short dissipates less. The cost is a possible lock-out into a low-current state with a heavy capacitive load at start-up (the load line never crosses the foldback knee). A soft-start current or a foldback disable at start-up is the product fix; UG exams ask you to sketch the foldback I–V.

Ripple and reference. A 78xx PSRR is tens of dB at 120 Hz, worse at high frequency. An RC prefilter on \(V_{in}\) is cheaper than a larger loop. Never share the unregulated rail of a power amplifier with a small-signal op-amp without decoupling; the class-B current pulses modulate the rail and come out as buzz.

Dummy loads and minimum \(I_Q\). Many three-terminal regulators specify a minimum load current (a few milliamps) to stay in regulation. An LED plus resistor is a legal dummy load. LM317 needs about 3.5–10 mA through the divider.

Power electronics in this pack is linear on purpose. Keep the device in the analog region, close a voltage loop for regulation, and spend the rest of the budget on heat. Switching conversion is a different pack; do not mix buck-converter efficiency numbers into a 7805 problem. Linear is \(V_{out}/V_{in}\); switching is a later course.
