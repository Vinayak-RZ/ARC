# Gaseous, liquid, and solid breakdown, and HV testing

High-voltage engineering at UG is why insulation works until it does not, and how a laboratory proves a piece of plant. This unit is breakdown in gas, liquid, and solid, plus the generation and measurement of power-frequency, DC, and lightning-impulse voltages. Overvoltages on the system and insulation coordination are unit 02.

## Concepts

Air is the default insulation of overhead lines and AIS substations. Breakdown of a uniform gap is described first by Townsend and then by streamers. Townsend: an electron avalanche \(\mathrm{e}^{\alpha x}\) with ionization coefficient \(\alpha(E,p)\), secondary emission \(\gamma\) at the cathode. Self-sustaining condition \(\gamma(\mathrm{e}^{\alpha d}-1)=1\). Paschen’s law: breakdown voltage of a uniform gas gap is a function of the product \(pd\) (pressure × gap), \(V_b=f(pd)\), with a minimum (about 327 V for air near \(pd\approx 0.7\,\mathrm{Pa\cdot m}\) in SI, historically 5.5 mmHg·cm). The left of the minimum is vacuum-like (too few collisions); the right is the usual engineering slope, roughly \(V_b\approx 24.2\delta d + 6.08\sqrt{\delta d}\) kV for large uniform air gaps with relative density \(\delta\). Non-uniform gaps break down far below the uniform value: corona starts at a critical surface gradient (Peek’s law for wires), a glow or streamer fills space charge, and a leader can bridge metres. Sphere gaps are nearly uniform on the axis if spacing is less than the radius; they are a standard measuring device. Rod–plane and rod–rod are the engineering geometries of towers and bushings.

Streamer (Kanal) criterion: when the avalanche head’s space-charge field is comparable to the applied field, photoionization ahead of the avalanche makes a thin conducting filament. This is why long gaps do not wait for Townsend’s cathode feedback from the far electrode. Polarity: a positive rod–plane in air typically breaks at a lower voltage than negative for long gaps (positive streamers propagate more readily). Corona loss, RI, and ozone on transmission lines are the same physics at a gradient that does not yet flash over.

Vacuum breakdown is not Paschen’s left branch in a simple way: at very low \(pd\), breakdown is electrode-surface (microparticles, field emission, whiskers). Vacuum bottles in MV switchgear exploit this; a small gap holds tens of kilovolts if the surface is clean.

Liquid dielectrics (transformer oil, ester fluids): breakdown is rarely the intrinsic molecular strength. Moisture, fibres, and particles form a bridge; gas bubbles (Paschen inside the bubble) trigger; stressed oil in a uniform gap still depends on gap, time, and contamination. Water-in-oil ppm is a maintenance number. Impulse strength is higher than power-frequency strength (time to form a bridge). Needle–sphere tests and IEC oil-cup tests are quality checks, not a design \(E_{\mathrm{max}}\) for a transformer duct — ducts use creep, oil-paper combination, and oil velocity.

Solid dielectrics (porcelain, glass, XLPE, epoxy, oil-paper): several mechanisms. Intrinsic (electronic) breakdown is a high MV/cm number you never reach in service. Thermal breakdown: dielectric loss \(V^2\omega C\tan\delta\) heats the volume, conductivity rises, thermal runaway; more likely in thick lossy insulation at AC. Electromechanical: electrostatic compressive force versus Young’s modulus, a low-strain collapse in soft materials. Partial discharge in voids: a cavity with lower \(\varepsilon\) and a Paschen-sized \(pd\) discharges each half-cycle; ozone and nitric acids eat organic insulation; treeing (electrical trees, water trees in XLPE) grows from the PD site to puncture. Surface tracking and erosion on polluted outdoor insulation is a creepage problem, not a volume \(E\). Composite and porcelain shed profiles, and hydrophobicity of silicone, are the engineering answers.

Generation of test voltages:

- Power frequency: cascade transformers (several units in series, isolating transformers for the upper tanks), sometimes with a reactor for capacitive loads (cables, GIS).
- High DC: Cockcroft–Walton (Greinacher) multiplier, n stages, no-load \(V=2n V_{\mathrm{max}}\) of the supply peak, load-dependent droop and ripple \(\propto I f^{-1} C^{-1} n^2\) or \(n^3\) depending on which capacitor stack; electrostatic generators are named only.
- Lightning impulse: Marx generator, n stages charged in parallel, discharged in series through spark gaps, \(V\approx n V_{\mathrm{charge}}\). Wave-shaping \(R_s,R_p,C_s,C_b\) produce the standard 1.2/50 µs lightning impulse (front 1.2 µs, tail to half-value 50 µs) or 250/2500 µs switching impulse.
- High-current impulse for arresters and earth grids: a different bank, 8/20 µs or 10/350 µs, not a voltage Marx.

Measurement: sphere gap (tables of peak voltage versus diameter and spacing, air density correction). Capacitive divider for AC and impulse (damped capacitive for impulse). Resistive divider for DC. Electrostatic voltmeter. Schering bridge for \(C\) and \(\tan\delta\) of a specimen at power frequency: the unknown \(C_x,R_x\) balanced against a standard capacitor and a variable \(R,C\); dissipation factor is read from the arm ratio. Partial-discharge measurement (pC, radio influence) is a commissioning and factory test; UG treats it as “voids discharge below breakdown.”

Tests on plant: power-frequency withstand (one minute wet/dry), lightning impulse withstand (BIL), switching impulse at EHV, chopped impulse on transformers (stresses turns), DC on cables (historical; AC/VLF and oscillating-wave are modern cable tests because DC can leave space charge in XLPE). Polarity and sequence of impulse tests follow a standard; UG computes a Marx voltage and a 1.2/50 shape, not a full IEC sequence.

Safety in the HV hall: earth stick, interlocks, distance, never assume a capacitor is discharged. Sphere gaps can radiate a loud bang. This is not optional colour; it is part of the method.

## Equations

Paschen (uniform, Townsend):

\[
V_b=f(pd),\qquad \gamma(\mathrm{e}^{\alpha d}-1)=1,\qquad \alpha=p\,F(E/p).
\]

Uniform air, large \(d\), relative density \(\delta\) (Peek-style engineering fit, kV peak / cm-class — use the problem’s constants if given):

\[
V_b\approx 24.2\,\delta d + 6.08\sqrt{\delta d}\quad(\mathrm{kV},\ d\ \mathrm{in\ cm}).
\]

Peek corona onset gradient for a wire (kVpeak/cm, \(\delta\) relative air density, \(m\) surface factor, \(r\) cm):

\[
E_c=m\delta\bigl(30 + 9/\sqrt{\delta r}\bigr).
\]

Cockcroft–Walton no-load, n stages, transformer peak \(V_m\):

\[
V_{\mathrm{DC}}=2 n V_m.
\]

Ripple (order, n stages, load I, stage C, frequency f) — one common form:

\[
\delta V\approx \frac{I}{fC}\frac{n(n+1)}{2}.
\]

Marx n stages, charge voltage \(V_0\):

\[
V_{\mathrm{impulse}}\approx n V_0
\]

before wave-shaping drop. Standard lightning impulse: front \(T_1=1.2\,\mu\mathrm{s}\), tail \(T_2=50\,\mu\mathrm{s}\) (IEC tolerances exist; UG uses the nominal).

Schering balance (specimen \(C_x\) with series loss \(R_x\), standard \(C_s\), arms \(R_3,C_4,R_4\)) in the usual textbook arrangement:

\[
C_x=C_s\frac{R_4}{R_3},\qquad \tan\delta=\omega C_4 R_4.
\]

(Use the arm labels the problem draws; do not swap \(R_3\) and \(R_4\).)

Capacitive divider:

\[
V_{\mathrm{low}}=V_{\mathrm{high}}\frac{C_1}{C_1+C_2}.
\]

Thermal breakdown (qualitative energy): loss density \(\omega\varepsilon E^2\tan\delta\); runaway when cooling cannot match.

## Methods

1. Identify the medium (gas/liquid/solid) and the field (uniform sphere, rod–plane, void in a solid). Pick Townsend/Paschen, streamer/corona, particle-bridge, or PD/treeing.
2. For air gaps, apply density \(\delta\) (temperature, pressure, humidity if given). Sphere-gap measurement: read spacing, apply correction, report peak kV.
3. For a multiplier or Marx, count stages, compute no-load voltage, then apply load droop or wave-shaping efficiency if given.
4. Impulse shape: confirm front and tail from the circuit’s \(R,C\) only if the problem gives the standard relations; otherwise treat 1.2/50 as the definition of the test.
5. Schering: draw the bridge, write the two balance equations, extract \(C_x\) and \(\tan\delta\). High \(\tan\delta\) means lossy or wet insulation, not automatically “about to puncture.”
6. Oil: never quote a single kV/mm as intrinsic; compare the measured cup value with the specification.
7. Safety: discharge, earth, lock.

Worked pattern — Paschen reminder: doubling the gap at constant p does not double \(V_b\) near the minimum; it does, approximately, on the right-hand linear part. Worked pattern — Marx: 12 stages at 100 kV charge, ideal \(1.2\,\mathrm{MV}\); a 10% wave-shaping drop gives 1.08 MV at the test object.

## Mistakes

Using Paschen \(pd\) with \(d\) in metres and a constant fitted in cm. Treating a rod–plane as a uniform gap. Reporting RMS when the sphere-gap table is peak (or the reverse). Cockcroft–Walton \(V=n V_m\) instead of \(2n V_m\) for the usual full-wave n-stage stack. Marx charged in series (it charges in parallel). Applying a DC cable test protocol to XLPE as if space charge did not exist. Calling corona “breakdown” (corona is partial; flashover is complete). Ignoring polarity on a rod–plane. Using a resistive divider on a 1.2 µs front (bandwidth). Swapping Schering arms so \(\tan\delta\) is \(\omega C_x R_x\) computed from the wrong pair. Thermal-breakdown thinking on a thin film that actually failed by PD in a void. Vacuum-gap design using the atmospheric Paschen slope. Forgetting air-density correction on a hot day in an outdoor sphere-gap measurement.

Insulation “strength” is geometry- and time-dependent. A 1 min AC test, a 1.2/50 impulse, and a 10 year service life are three different numbers. Do not quote one kV/mm for all three.

Partial discharge inception voltage (PDIV) is below breakdown. A factory PD test can fail a transformer that still holds the one-minute AC withstand. That is the point of the PD test.

Cascade transformers need a rating for capacitive current of the object, not only kV. A GIS test set without a compensating reactor may stall on charging Mvar.

Humidity and rain change wet flashover more than dry. A sphere-gap indoor measurement on a dry day is not the withstand of an outdoor rod–rod under rain. Creepage, not just gap millimetres, governs polluted porcelain. Keep the laboratory number and the service number labelled as such.
