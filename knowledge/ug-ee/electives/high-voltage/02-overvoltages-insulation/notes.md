# Lightning, switching overvoltages, and insulation coordination

Plant that survived a factory impulse test still has to live under lightning, switching, and temporary overvoltages on the network. This unit is travelling waves, reflection, Bewley lattice, lightning and switching surge magnitudes at UG level, arresters, and the coordination of BIL/BSL with arrester protective levels. Breakdown physics and laboratory generation stay in unit 01. Power-frequency Ferranti and load-rejection voltages overlap the core T&D pack; here they are sources of TOV for arrester energy.

## Concepts

A surge on a line travels at a fraction of the speed of light, \(v=1/\sqrt{LC}=c/\sqrt{\varepsilon_r\mu_r}\) in a cable, \(\approx 300\,\mathrm{m/\mu s}\) on overhead. Surge impedance \(Z_c=\sqrt{L/C}\) is about 300–400 Ω overhead and 20–50 Ω for a cable. A travelling voltage \(v\) and current \(i\) on a forward wave satisfy \(v=Z_c i\). At a junction, reflection and refraction coefficients for voltage are

\[
\Gamma_v=\frac{Z_2-Z_1}{Z_2+Z_1},\qquad T_v=\frac{2Z_2}{Z_2+Z_1},
\]

with \(T_v=1+\Gamma_v\). Open circuit: \(\Gamma_v=1\), voltage doubles. Short circuit: \(\Gamma_v=-1\), voltage zeros, current doubles. Resistive termination \(R=Z_c\): no reflection. Bewley lattice ( Bewley diagram ) tracks successive reflections versus time; at any point the voltage is the sum of all forward and backward waves that have arrived. UG problems are lossless lines and lumped resistive or open/short ends; a transformer is often a large inductance (open on the surge time scale, then a transferred surge via capacitance).

Lightning: a current source in the 1–200 kA class (median tens of kA) with a front of a few microseconds. Stroke to a phase conductor (shielding failure) injects \(I\) into \(\approx Z_c/2\) if the line is long both ways, so \(V=I Z_c/2\) can be megavolts — the insulator flashes and the surge chops. Stroke to a shield wire or tower: tower-top voltage \(I R_f + L di/dt\) with footing resistance \(R_f\); if that voltage exceeds insulator CFO, backflashover. Overhead ground wire and low footing resistance are the primary lightning protection of EHV lines; arresters (line arresters) appear on problem feeders and unshielded MV. Standard 1.2/50 µs is a laboratory wave that represents the *voltage* stress; lightning *current* waves for arresters are 8/20 µs (distribution discharge) and 10/350 µs (direct stroke energy).

Switching overvoltages: energizing an unloaded line, reclosing with trapped charge, interrupting inductive current (chopping, unit of switchgear), capacitor-bank switching, and out-of-phase closing. At EHV, switching surges, not lightning, often size the phase-to-earth insulation (BSL, switching impulse withstand). Statistical switching (closing resistors, controlled closing) keeps the 2% overvoltage below a planning level (often in the 2–2.5 pu range depending on voltage class and practice). Temporary overvoltages (TOV): Ferranti on a long open line, load rejection, ground-fault factor on an ungrounded or impedance-grounded system (healthy phase up to \(\sqrt{3}\) pu), ferroresonance. Arresters must survive TOV for the specified duration without absorbing a lightning-sized energy by mistake — TOV is a voltage-withstand issue more than an energy issue if the arrester stays out of conduction; if TOV enters the conduction knee, energy becomes a problem.

Insulation coordination (IEC 60071 language at UG depth): assign a set of *withstand* voltages to equipment (LIWV / BIL for lightning, SIWV / BSL for switching, power-frequency) and a set of *protective levels* to arresters, with a margin. Protective ratio ≈ equipment withstand / arrester protective level, typically > 1.2–1.4 depending on steepness, separation, and standard. Separation distance: the arrester at the transformer terminals protects better than an arrester 40 m away; the travelling-wave oscillation between arrester and transformer can overshoot. Rod gaps and spark gaps are cheap and slow-to-undefined; they do not clamp, they flash, and they cause an outage. Gapped SiC arresters are legacy. Metal-oxide (ZnO, gapless) arresters are the default: a highly nonlinear \(I=kV^\alpha\) with \(\alpha\) large, residual voltage \(U_p\) at a stated discharge current (e.g. 10 kA 8/20), and an energy class (IEC line-discharge class or thermal energy rating). Continuous operating voltage \(U_c\) must sit above system maximum phase-to-earth with a TOV margin.

BIL examples (order, not a code): 11 kV class equipment might be 75 or 95 kV BIL; 132 kV class a few hundred kV; 400 kV class over a megavolt. Always use the number the problem gives. Chopped-wave tests on transformers stress inter-turn insulation more than a full wave of the same peak.

Transferred surges: a lightning wave on an HV winding couples capacitively to the LV at the first instant (\(C_{HL}\) versus \(C_L\)), then inductively. UG capacitive divider: \(V_{LV}\approx V_{HV} C_{HL}/(C_{HL}+C_{LV})\). That is why an LV arrester still belongs on a distribution transformer even if the HV arrester exists.

Earth-wire shielding angle: a geometric construction (usually 30° or less at EHV) so that most strokes hit the shield. Electrogeometric model (striking distance \(\propto I^{0.65}\) or similar) is named; UG may compute a simple angle, not a full CIGRE failure rate.

Cables and GIS change \(Z_c\) and therefore reflection: overhead-to-cable junction reflects a negative voltage wave back on the overhead (voltage drops) and transmits a lower voltage into the cable, but the *current* into the cable is large. The cable still needs its own BIL and often a sheath-voltage limiter. GIS disconnectors produce VFT (unit of switchgear); coordination for VFT is a specialist overlay.

## Equations

Wave speed and surge impedance:

\[
v=\frac{1}{\sqrt{LC}},\qquad Z_c=\sqrt{\frac{L}{C}}.
\]

Forward wave: \(v^+=Z_c i^+\). Backward: \(v^-=-Z_c i^-\). Total \(v=v^++v^-\), \(i=i^++i^-\).

Reflection / refraction (line \(Z_1\) into \(Z_2\)):

\[
\Gamma_v=\frac{Z_2-Z_1}{Z_2+Z_1},\qquad T_v=1+\Gamma_v=\frac{2Z_2}{Z_2+Z_1}.
\]

Open: \(\Gamma_v=1\). Short: \(\Gamma_v=-1\). Matched: \(\Gamma=0\).

Lightning stroke to a conductor, two long directions:

\[
V=\frac{I Z_c}{2}.
\]

Tower backflash (crude):

\[
V_{\mathrm{top}}\approx I R_f + L_{\mathrm{tower}}\frac{di}{dt}.
\]

Arrester residual (from a given \(U_p(I)\), or a power law if given \(\alpha\)):

\[
I=k U^\alpha.
\]

Coordination margin (lightning):

\[
M=\frac{U_{\mathrm{BIL}}}{U_p}-1
\]

(or the protective ratio \(U_{\mathrm{BIL}}/U_p\); use the definition the problem states).

Capacitive transfer:

\[
V_{LV}=V_{HV}\frac{C_{HL}}{C_{HL}+C_{LV}}.
\]

TOV Ferranti (lossless open line, core T&D formula):

\[
V_r=\frac{V_s}{\cos\beta\ell}.
\]

Ground-fault factor on an isolated-neutral system: healthy phase-to-earth approaches \(\sqrt{3}\) times the unfaulted phase-to-earth.

Travel time:

\[
\tau=\ell/v.
\]

Lattice: at \(t=2\tau\) a round trip returns; open-end voltage 2 pu of the incoming step until the next wave.

## Methods

1. Draw the line, junctions, and terminations. Write \(Z_c\) and \(\tau\) for each section. For a step or a rectangular surge, build a Bewley lattice for the asked observation time.
2. Lightning voltage on a line: \(I Z_c/2\) unless a termination is nearby. Compare with insulator CFO; if it flashes, chop the wave in later lattice steps (advanced UG).
3. Backflash: compute \(I R_f\); if \(di/dt\) and \(L\) are given, add them. Lower \(R_f\) (counterpoise) is the usual remedy.
4. Arrester: pick \(U_c\) from system voltage and grounding (TOV). Read \(U_p\) at the coordinating current (5 kA, 10 kA, …). Compare with BIL/BSL and a margin. Place the arrester at the terminals of the protected object if the problem allows.
5. Switching: if the problem is statistical, use the given 2% overvoltage in pu. If it is a trapped-charge reclose, incoming step can be 2 pu before the open-end doubling story (careful: do not double-count).
6. Transformer transfer: capacitive divider at \(t=0^+\).
7. Never coordinate a rod gap as if it had a residual voltage curve.

Worked pattern — junction: 400 Ω overhead into 40 Ω cable. \(\Gamma_v=(40-400)/(40+400)=-0.818\), \(T_v=0.182\). A 800 kV incoming overhead wave puts \(146\,\mathrm{kV}\) into the cable and reflects \(-654\,\mathrm{kV}\) (total overhead at the junction \(146\,\mathrm{kV}\)).

Worked pattern — open line: 250 kV step, open end, \(\tau=200\,\mu\mathrm{s}\). For \(0<t<2\tau\) the sending end (matched source) stays at 250 kV; the open end is 500 kV after \(t=\tau\).

## Mistakes

Using \(V=I Z_c\) for a stroke to a through-conductor (that would be a termination at infinity one way only). Forgetting open-end doubling. Adding BIL and arrester \(U_p\) instead of dividing. Siting the arrester far from the transformer and claiming the same margin. Treating a switching impulse BSL as interchangeable with BIL. Applying a 1.2/50 voltage wave as if it were an 8/20 current through the arrester. Matching \(R=0\) as “no reflection.” Cable \(Z_c=400\,\Omega\). Ignoring ground-fault factor when choosing \(U_c\) on an ungrounded generator bus. Using Ferranti \(\cos\beta\ell\) with \(\beta\ell\) in degrees inside a cosine that expects radians (or the reverse). Lattice with the wrong \(2\tau\) so a reflection arrives a whole transit early. Coordinating on RMS when BIL is a peak impulse. Assuming a gapless ZnO arrester is a short circuit once it conducts (it is a voltage clamp at \(U_p\), still high).

Insulation coordination is a system of numbers, not a single “kV rating.” A transformer can have BIL 650 kV and a bushing with a different BIL; the arrester protects both only if lead lengths are short.

Temporary overvoltage that exceeds \(U_c\) for seconds is an arrester thermal problem. A lightning stroke is an energy and a residual-voltage problem. Do not size the arrester energy class from TOV duration using an 8/20 waveform.

Bewley lattice signs: a negative \(\Gamma\) does not mean the physical voltage went negative unless the sum of waves is negative. Always sum arriving waves.

Shielding angle is not a BIL. A line can be well shielded and still need arresters at the transformer because the last span and the substation entrance are a different geometry.
