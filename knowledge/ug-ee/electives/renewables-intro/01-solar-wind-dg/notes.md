# Solar PV, wind turbines, and distributed generation

A first renewables elective is device physics enough to read an I–V curve, a wind-power curve, and a one-line with DG. Grid codes, PLL, and islanding are unit 02. This unit is PV equivalent circuit and fill factor, MPPT as an idea, wind Betz and \(C_p(\lambda)\), and what “distributed generation” means on a UG feeder.

## Concepts

Photovoltaic cell: a p–n junction illuminated so that photocurrent \(I_{ph}\) (roughly proportional to irradiance \(G\)) drives a current out of the terminals. The single-diode model is

\[
I=I_{ph}-I_s\bigl(\mathrm{e}^{q(V+IR_s)/(a kT)}-1\bigr)-\frac{V+IR_s}{R_{sh}}.
\]

UG numericals often drop \(R_s,R_{sh}\) and use \(I=I_{sc}-I_0(\mathrm{e}^{V/V_t'}-1)\), or they give the I–V curve as a table. Short-circuit current \(I_{sc}\approx I_{ph}\) at \(V=0\). Open-circuit voltage \(V_{oc}\) from \(I=0\), logarithmic in \(I_{ph}\) and therefore only weakly dependent on \(G\). Maximum-power point (MPP) \((V_{mp},I_{mp})\) is the knee; fill factor \(\mathrm{FF}=V_{mp}I_{mp}/(V_{oc}I_{sc})\). Efficiency \(\eta=P_{\max}/(G A)\). Temperature: \(I_{sc}\) rises slightly with \(T\), \(V_{oc}\) falls (\(\sim -2\,\mathrm{mV/K}\) per cell, order of magnitude), so power falls with heat. Irradiance: \(I_{sc}\propto G\), \(V_{oc}\) almost flat, so \(P_{\max}\) roughly \(\propto G\).

Series cells add voltage (a 60- or 72-cell module, \(V_{oc}\) tens of volts). Parallel strings add current. A shaded cell in a string becomes reverse-biased and can hot-spot; bypass diodes across groups of cells are the mitigation. Blocking diodes or more often smart electronics stop reverse current into a sleeping string. Modules into arrays: \(V_{\mathrm{string}}=N_s V_{\mathrm{mod}}\), \(I_{\mathrm{array}}=N_p I_{\mathrm{mod}}\) at a given operating point if identically irradiated.

MPPT (maximum-power-point tracking): a DC–DC converter or the inverter’s DC stage adjusts the effective load so that the array sits at the knee. Perturb-and-observe and incremental conductance are the two UG names: move \(V\), watch \(P\), keep going if \(P\) rose. Partial shading makes multiple knees; a global search or per-module MPPT (microinverters, DC optimizers) is the practical fix. UG computes \(P_{\max}=\mathrm{FF}\,V_{oc}I_{sc}\) when FF is given, or reads the knee off a curve.

Insolation versus irradiance: irradiance is W/m² instantaneous; insolation / irradiation is J/m² or kWh/m² over a period. Air mass AM1.5, 1000 W/m², 25 °C cell is the standard test condition (STC). NOCT is a more realistic module temperature. Do not use STC power as the energy yield without a performance ratio (soiling, temperature, inverter, mismatch) — UG problems that ask kWh usually give equivalent sun hours or a PR.

Wind: power in the airflow through area \(A\) is \(\tfrac12\rho A v^3\). A turbine extracts a fraction \(C_p\), the power coefficient, \(P=\tfrac12\rho A C_p v^3\). Betz limit: \(C_p\le 16/27\approx 0.593\) for an actuator-disk inviscid theory. Real large turbines peak \(C_p\) around 0.45–0.50. \(C_p\) is a function of tip-speed ratio \(\lambda=\omega R/v\) and pitch \(\beta\). Cut-in, rated, and cut-out wind speeds: below cut-in, \(P=0\); between rated and cut-out, pitch or stall holds \(P\approx P_{\mathrm{rated}}\); above cut-out, shut down. Capacity factor is annual energy divided by \(P_{\mathrm{rated}}\times 8760\,\mathrm{h}\), often 0.25–0.45 depending on site — not the same as \(C_p\).

Machine types (names): Type 1 fixed-speed induction; Type 2 WRIM with rotor resistance; Type 3 DFIG (partial converter on the rotor); Type 4 full converter (PMSG or induction). UG intro does not design the DFIG; it places the converter. A small off-grid wind machine may be a PMSG into a rectifier and dump load.

Distributed generation (DG): generation connected to the distribution system (LV or MV), not to the bulk transmission network. PV rooftop, small wind, diesel, small hydro, CHP, battery-plus-inverter. Effects at UG level: reverse power on a feeder that was designed radial, voltage rise at light load (\(V\approx V_0+R P+X Q\) on a simple feeder), fault-current contribution (inverters are current-limited, synchronous DG is not), protection coordination (unit of protection), and islanding (unit 02). A diesel genset is a synchronous machine with a governor and AVR; its I–V is not a PV curve. Microgrid: a cluster of DG plus loads that can island intentionally — named here, controls in unit 02.

Hybrid: PV plus battery plus diesel is a common UG block diagram. The battery is an energy buffer (kWh) with a power limit (kW) and a C-rate. Do not size kWh from kW or the reverse.

Limits of this unit: no full semiconductor device physics, no CFD of blades, no electricity-market tariff design. If a number is needed, it is \(I_{sc},V_{oc},\mathrm{FF},C_p,\lambda\), or a feeder voltage rise.

## Equations

PV ideal-diode (no Rs, Rsh):

\[
I=I_{ph}-I_0\bigl(\mathrm{e}^{V/(n V_T)}-1\bigr),\qquad V_T=kT/q.
\]

\[
V_{oc}=n V_T\ln\bigl(I_{ph}/I_0+1\bigr).
\]

\[
\mathrm{FF}=\frac{V_{mp}I_{mp}}{V_{oc}I_{sc}},\qquad P_{\max}=\mathrm{FF}\,V_{oc}I_{sc},\qquad\eta=\frac{P_{\max}}{G A}.
\]

Irradiance scaling (first cut): \(I_{sc}(G)=I_{sc,\mathrm{STC}}(G/G_{\mathrm{STC}})\).

Array: \(V_{\mathrm{oc,string}}=N_s V_{oc}\), \(I_{\mathrm{sc,array}}=N_p I_{sc}\).

Wind:

\[
P_{\mathrm{air}}=\frac12\rho A v^3,\qquad P=C_p P_{\mathrm{air}},\qquad A=\pi R^2,
\]
\[
\lambda=\frac{\omega R}{v},\qquad C_{p,\mathrm{Betz}}=\frac{16}{27}.
\]

Rated to cut-out: \(P\approx P_{\mathrm{r}}\). Capacity factor:

\[
\mathrm{CF}=\frac{E_{\mathrm{year}}}{P_{\mathrm{r}}\times 8760\,\mathrm{h}}.
\]

Simple feeder voltage rise (receiving-end load convention reversed for export):

\[
\Delta V\approx \frac{R P+X Q}{V}.
\]

Diesel / gas energy: \(E=\eta_{\mathrm{th}} m H\) if a thermal efficiency and heating value are given.

## Methods

1. PV: from STC \(I_{sc},V_{oc},\mathrm{FF}\) (or \(P_{\mathrm{mpp}}\)) scale current with \(G\), optionally drop \(V_{oc}\) with a given temperature coefficient, compute \(P\). Series/parallel as counts of modules.
2. If an I–V equation is given, \(P=VI\), set \(\mathrm{d}P/\mathrm{d}V=0\) or scan; otherwise use FF.
3. MPPT: state that the converter presents \(R_{\mathrm{in}}=V_{mp}/I_{mp}\). Do not confuse MPPT with islanding.
4. Wind: compute \(A\), \(P_{\mathrm{air}}\), apply \(C_p(\lambda)\) if given or a single \(C_p\). Check cut-in / rated / cut-out before using \(v^3\).
5. \(\lambda=\omega R/v\); if RPM is given, convert to rad/s.
6. DG feeder: sign of \(P\) at the substation reverses when DG exceeds load. Voltage rise uses \(P>0\) export in the \(\Delta V\) formula above.
7. Energy: integrate power or use equivalent hours × PR for PV; CF × 8760 for wind.

Worked pattern — PV: module \(V_{oc}=38\,\mathrm{V}\), \(I_{sc}=9.0\,\mathrm{A}\), \(\mathrm{FF}=0.78\), \(G=800\,\mathrm{W/m}^2\), assume \(I_{sc}\propto G\), \(V_{oc}\) unchanged. \(I_{sc}'=7.2\,\mathrm{A}\), \(P_{\max}=0.78\times 38\times 7.2=213\,\mathrm{W}\).

Worked pattern — wind: \(R=40\,\mathrm{m}\), \(v=10\,\mathrm{m/s}\), \(\rho=1.225\,\mathrm{kg/m}^3\), \(C_p=0.45\). \(A=5027\,\mathrm{m}^2\), \(P_{\mathrm{air}}=3.08\,\mathrm{MW}\), \(P=1.39\,\mathrm{MW}\).

## Mistakes

Using \(P=\tfrac12\rho A v^3\) as the electrical output (missing \(C_p\)). \(C_p>16/27\). Capacity factor confused with \(C_p\). \(P\propto v^2\) (that is force, not power). PV \(P\propto G^2\). Adding module watts in series (series adds volts). \(V_{oc}\) scaling linearly with \(G\). FF > 1. Tip-speed ratio with \(\omega\) in r/min. Area as \(2\pi R\) (circumference). Feeder voltage drop formula with the wrong sign so export looks like a sag. STC power times 24 h as daily energy. Diesel DG treated as current-limited like an inverter during a fault. Bypass diode as a blocking diode (different job). MPPT as a maximum-*voltage* tracker that parks at \(V_{oc}\) (that is zero power).

Betz is an upper bound on *aerodynamic* \(C_p\), not on the electrical efficiency of the gearbox and generator. Electrical \(\eta\) multiplies \(C_p\).

Partial shading: two series modules, one at 1000 W/m² and one at 200 W/m², do not produce the average current at \(V_{oc,sum}\). The string current is near the shaded \(I_{sc}\) unless a bypass diode conducts. That is why one shaded module can kill a string’s power.

Wind \(v^3\) makes siting matter more than nameplate. A 20% higher mean wind is not 20% more energy.

DG is not a slack bus. A rooftop inverter is a P–Q (or P–V) injection with a current limit, not an infinite bus. Load-flow intuition from the core power pack still applies; the sign of P at some buses flipped.

Temperature coefficient on \(V_{oc}\) is usually given in %/K or mV/K per cell. A 72-cell module at 25 °C STC, cells 45 °C hotter, \(\mu_V=-0.32\,\%/\mathrm{K}\), loses \(0.32\times 45\approx 14\%\) of \(V_{oc}\). Current rises maybe 0.05 %/K, which does not save the power. NOCT yield estimates bake this in; a raw STC × sun-hours over-predicts summer kWh in a hot climate and under-predicts a cold high-irradiance site. Performance ratio 0.75–0.85 is the UG lump of inverter, soiling, mismatch, and temperature if the problem does not split them.

Wind Weibull: mean \(v\) is not the cube-mean. Energy uses \(\langle v^3\rangle\), which is larger than \((\langle v\rangle)^3\). A site quoted as “6 m/s mean” with \(k=2\) Weibull has more energy than a constant 6 m/s. If the exam gives only a single \(v\), it wants \(v^3\) at that speed, not a distribution. Cut-out at 25 m/s means those hours contribute zero, not \(C_p P_{\mathrm{air}}\). Rated region is a pitch hold: \(C_p\) is *reduced* on purpose so \(P\) stays at \(P_r\) while \(v^3\) would have grown.

DFIG (Type 3) processes only a slip fraction of power through the rotor converter, roughly \(|s|P_{\mathrm{air}}\) plus losses, so a 3 MW machine might have a 1 MW converter. Type 4 processes all of it. Fault current and Q capability differ; unit 02 will not let you use a synchronous \(X'\) on Type 4. This unit only needs the name and the power path.

Diesel DG: specific fuel consumption g/kWh or a heat rate. Fuel tank kWh is \(m H\eta\), not the kVA of the alternator. A 100 kVA genset at 0.8 pf is 80 kW electrical; the fuel bill follows kWh, not kVA. Reverse power when the PV on the same bus pushes the diesel into motoring is a 32 trip, not a PV I–V problem.

Simple payback and LCOE are not this pack. If a problem gives ₹/kWh and a yield, it is arithmetic, not a device curve.

Module nameplate \(P_{\mathrm{mpp,STC}}\) is not \(V_{oc}I_{sc}\). Using \(V_{oc}I_{sc}\) without FF over-states power by \(1/\mathrm{FF}\approx 1.3\). Using \(V_{mp}I_{sc}\) is also wrong. FF exists because the knee is inside the rectangle.
