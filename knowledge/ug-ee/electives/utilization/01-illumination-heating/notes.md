# Laws of illumination and electric heating

Utilization of electrical energy is the UG elective that turns kWh into light, heat, welding, and (in unit 02) traction. This unit is photometry — inverse-square and Lambert cosine laws, MSCP, utilization and depreciation factors, a first lamp taxonomy — and electric heating: resistance, induction, dielectric, and arc furnaces. Traction mechanics wait for the next folder. Illumination numbers here are engineering lux calculations, not architectural lighting design software.

## Concepts

Luminous flux \(\Phi\) is lumen (lm), the photometric counterpart of watt, weighted by the eye’s \(V(\lambda)\). Luminous intensity \(I\) of a source in a direction is candela (cd) \(=\mathrm{lm/sr}\). Illuminance \(E\) on a surface is lux (lx) \(=\mathrm{lm/m}^2\). Luminance \(L\) is \(\mathrm{cd/m}^2\). Mean spherical candle power (MSCP) is the average intensity over \(4\pi\) steradians: \(\mathrm{MSCP}=\Phi/(4\pi)\) if \(\Phi\) is total flux of an isotropic source. Mean hemispherical candle power uses \(2\pi\). Lamp efficacy is \(\mathrm{lm/W}\).

Inverse-square law: a point source, illuminance on a surface facing the source, \(E=I/d^2\). If the surface is tilted, Lambert’s cosine law: \(E=(I/d^2)\cos\theta\), with \(\theta\) between the ray and the surface normal. A source that itself is a Lambertian diffuser has intensity \(I(\alpha)=I_0\cos\alpha\) relative to its own normal; combining both cosines is a standard numerical. The inverse-square law fails inside an integrating sphere, very near an extended luminaire, and in a room where inter-reflection (utilization factor) dominates.

Room calculation (lumen method):

\[
E=\frac{N\times\Phi_{\mathrm{lamp}}\times\mathrm{UF}\times\mathrm{MF}}{A},
\]

where UF (utilization / coefficient of utilization) is the fraction of lamp lumens that reach the working plane, MF (maintenance / depreciation factor) is dirt and lumen depreciation (\(<1\)), \(A\) is the area. Room index \(K=LW/(H(L+W))\) (or a close variant) and room-surface reflectances pick UF from a table; UG problems usually give UF and MF. Spacing-to-height ratio (SHR) keeps uniformity; too wide a spacing makes dark pools between luminaires even if the average lux is legal.

Lamps (taxonomy, not a catalogue): incandescent / halogen — low efficacy, high CRI, hot. Fluorescent and CFL — ballast, mercury, better lm/W. HID (HPS, metal halide, mercury vapour) — streets and high bays, run-up time, mercury/sodium. LED — high lm/W, driver electronics, thermal pad, dimming; UG numericals still use \(\Phi\) and efficacy the same way. Stroboscopic effect on rotating machinery: discharge lamps on 50 Hz; high-frequency ballasts or LED drivers reduce it. Glare, colour rendering (CRI), and correlated colour temperature are named so a factory floor is not lit with low-pressure sodium just because lm/W is high.

Laws that are not inverse-square: a uniformly radiating infinite line (some street-lighting approximations) has \(E\propto 1/d\), not \(1/d^2\). Do not invent that unless the problem states a line source.

Electric heating converts electrical energy to heat with a defined efficiency (often near 1 for resistance in a well-lagged oven, much less for a poorly insulated furnace). Resistance heating: \(P=I^2 R=V^2/R\). Direct (current through the charge: salt bath, electrode boiler, some glass) versus indirect (heating elements radiate/convect to the charge: ovens, furnaces). Element materials: nichrome, kanthal, silicon carbide, molybdenum disilicide — temperature and atmosphere decide. Time to heat a mass: \(mc\Delta\theta=\eta P t\) minus losses if given; UG often assumes a constant loss or a lumped efficiency \(\eta\).

Induction heating: eddy currents in a conducting charge in a coil’s AC field. Power \(\propto B^2 f^2 t^2\) in the skin-limited crude model, or \(\propto I_{\mathrm{coil}}^2\sqrt{f}\) depending on the regime; use the formula the problem gives. Skin depth \(\delta=\sqrt{2\rho/(\omega\mu)}\) sets whether heating is surface (hardening, high f) or through (melting, lower f, or a laminated charge). The coil is the primary of a transformer; the charge is a single-turn secondary. Power factor is poor; capacitors compensate. Coreless versus channel furnaces.

Dielectric heating: insulating lossy dielectrics (wood, plastic, food) in an RF or microwave field. Power density \(\omega\varepsilon_0\varepsilon_r E^2\tan\delta\). Frequency 1–100 MHz (RF) or 2.45 GHz (microwave). Uniformity is a standing-wave problem; UG computes P from \(E\), \(f\), \(\tan\delta\).

Arc furnaces: steel scrap, AC or DC arc, tens of MW. Load is violently fluctuating; flicker and unbalance on the grid are the power-quality cousins. Electrode consumption and transformer tap changers are operations. Resistance of the arc falls as current rises (negative incremental resistance); the supply reactance stabilizes. UG may compute energy per tonne if kWh/t is given, or a simple three-phase power \(S=\sqrt{3} V I\).

Welding: resistance (spot) welding \(I^2 R t\) at the nugget; arc welding as a controlled arc with a constant-current source. Mentioned so heating and welding do not share one formula blindly.

Infrared heating is radiation from a hot element, \(\sigma T^4\), useful for surfaces. Not dielectric, not induction.

Safety and utilization: IP ratings of luminaires in wet process areas, isolation of electrode boilers, RF leakage, arc-flash at furnace secondaries. None of these change \(E=I\cos\theta/d^2\); they change whether the installation is legal.

## Equations

Point source, cosine law:

\[
E=\frac{I}{d^2}\cos\theta\qquad(\mathrm{lx\ if\ }I\mathrm{\ in\ cd,\ }d\mathrm{\ in\ m}).
\]

Isotropic MSCP:

\[
\mathrm{MSCP}=\frac{\Phi}{4\pi},\qquad \Phi=4\pi\,\mathrm{MSCP}.
\]

Lumen method:

\[
N=\frac{E A}{\Phi_{\mathrm{lamp}}\,\mathrm{UF}\,\mathrm{MF}}.
\]

Room index (rectangular, work-plane height \(H_m\) to luminaires):

\[
K=\frac{L W}{H_m(L+W)}.
\]

Lambertian intensity: \(I(\alpha)=I_n\cos\alpha\). Combined: \(E=I_n\cos\alpha\cos\theta/d^2\).

Solid angle of a small patch: \(\mathrm{d}\Omega=\mathrm{d}A\cos\theta/d^2\), \(\mathrm{d}\Phi=I\,\mathrm{d}\Omega\).

Resistance heat:

\[
P=I^2 R=\frac{V^2}{R}=VI.
\]

Energy to raise temperature:

\[
\eta P t = mc\Delta\theta + Q_{\mathrm{loss}}.
\]

Skin depth:

\[
\delta=\sqrt{\frac{2\rho}{\omega\mu}}=\sqrt{\frac{\rho}{\pi f\mu}}.
\]

Dielectric power (volume):

\[
P=\omega\varepsilon_0\varepsilon_r E^2\tan\delta\times\mathrm{volume}.
\]

Three-phase furnace or heater:

\[
P=\sqrt{3}\, V_L I_L\cos\phi.
\]

Wien / Stefan–Boltzmann (infrared elements): \(P_{\mathrm{rad}}=\varepsilon\sigma A T^4\).

## Methods

1. Illumination point calculation: draw the geometry, identify \(\theta\) at the surface and \(\alpha\) at the luminaire if Lambertian, compute \(d\), apply \(E=I\cos\theta/d^2\) or both cosines. Superpose several lamps.
2. Average lux: lumen method with given UF and MF. Ceiling-to-next-integer \(N\), then check SHR if a spacing is asked.
3. Inverse problem: required MSCP or lamp wattage from \(E\) and efficacy.
4. Heating: write energy balance \(mc\Delta\theta=\eta Pt\) or include a given kW of loss. For three-phase, use \(\sqrt{3}VI\cos\phi\).
5. Induction: compute \(\delta\); if \(\delta\) is much less than thickness, heating is surface. Do not mix dielectric \(\tan\delta\) into a steel billet problem.
6. Dielectric: confirm \(E\) is the field in the material (not the air-gap field unless they are the same). Frequency in rad/s for \(\omega\).
7. Furnace: if kWh/t and tonnes/h are given, \(P=(\mathrm{kWh/t})\times(\mathrm{t/h})\).

Worked pattern — cosine: lamp 800 cd at 4.0 m above a point 3.0 m off-axis on the floor. \(d=5.0\,\mathrm{m}\), \(\cos\theta=4/5=0.80\), \(E=800\times 0.80/25=25.6\,\mathrm{lx}\).

Worked pattern — heat: 50 kg water, 20 °C to 80 °C, \(\eta=0.90\), 3 kW. \(Q=mc\Delta\theta=50\times 4186\times 60=12.56\,\mathrm{MJ}\), \(t=Q/(\eta P)=12.56\times 10^6/(0.9\times 3000)=4650\,\mathrm{s}=1.29\,\mathrm{h}\). (Use the \(c\) the problem states.)

## Mistakes

Forgetting \(\cos\theta\) on a tilted plane. Using \(d\) as the vertical height when the point is off-axis. Mixing MSCP with mean hemispherical CP (factor of 2). UF > 1. MF > 1 (unless the problem defines a “depreciation” as the reciprocal — some old notes write depreciation factor as \(>1\) in the denominator; this pack uses MF \(<1\) in the numerator). Adding lux from two lamps without checking they illuminate the same point. Inverse-square on an integrating-sphere numerical. Dielectric heating formula on a conducting charge (that is induction / \(I^2R\)). Induction formula on wet wood (that is dielectric). Using \(P=VI\) on a three-phase furnace without \(\sqrt{3}\). Energy balance without \(\eta\) when losses were stated. Skin depth with \(f\) in rad/s by mistake. Reporting candela as lux. Using feet in \(d^2\) while claiming lux (SI metres).

Photometric polar curves are not circles. An isotropic assumption is a problem simplification; a real luminaire has a candela table. If the problem gives only MSCP, it licensed the isotropic model.

LED replacements: you cannot swap a 400 W HPS for a 400 W LED and keep the same lux if the UF and distribution changed. Compute from lumens and UF, not from watts.

Arc-furnace flicker is a network problem (Pst, STATCOM) not solved by the heating energy equation. Keep the kWh/t calculation and the flicker complaint in different paragraphs.

A factory lighting numerical should state the working plane (usually 0.75–0.85 m above the floor) because \(H_m\) in the room index is luminaire-to-plane, not ceiling-to-floor. Mounting height errors of a metre swing UF and the inverse-square \(d^2\) together. Maintenance factor is not a fudge to make \(N\) an even number; it is dirt on the luminaire plus lamp lumen depreciation at the replacement interval. If the problem gives depreciation as 1.4 in the denominator, that is the reciprocal of MF = 0.71 — same arithmetic, opposite convention. Write which one you used.

Heating time with a constant loss \(P_{\mathrm{loss}}\) is \(t=mc\Delta\theta/(P\eta-P_{\mathrm{loss}})\), not \(mc\Delta\theta/(\eta P)\) minus a time of losses. If \(\eta P\le P_{\mathrm{loss}}\), the oven never reaches the set point; that is a design fail, not a long wait. Induction-coil kVA is larger than the kW in the charge because pf is 0.1–0.3 uncompensated; capacitors sit next to the coil, not at the 11 kV bus, unless the problem says so. Dielectric heating of a stack of boards needs the field in the wood: two plates with an air gap drop most of the voltage in the air (\(\varepsilon_r\) of wood is larger), so the wood \(E\) is smaller than \(V/\mathrm{gap}_{\mathrm{total}}\). Use the series-capacitance divider if an air gap is drawn.

Spot welding \(I^2 t\) is milliseconds and tens of kiloamperes; oven \(I^2 R\) is minutes and tens of amperes. They share Joule’s law and nothing else in the equipment list. Infrared elements follow \(\sigma T^4\) only if the problem is radiation-dominated; a forced-convection oven is \(h A\Delta\theta\) and a different time estimate.

Glare and CRI do not enter the lux formula, but they enter whether the answer is a legal factory. Low-pressure sodium on a machine-shop floor meets a lumen-method \(E\) and still fails because colour discrimination is gone. State lux first, then the lamp family, when the question asks for both.
