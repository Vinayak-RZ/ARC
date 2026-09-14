# Magnetic measurements and the calibration chain

Measuring \( B \), \( H \), flux, and permeability is how you populate a magnetic-circuit model and how you certify that a shunt, a CT, or a wattmeter still means what its scale says. This unit is the ballistic galvanometer and fluxmeter, a B–H loop from a ring or Epstein frame, a sketch of permeameters, and the calibration / traceability chain that ties student instruments back toward national standards. It closes the measurements pack: errors (unit 01) meet magnetic quantities and a documented chain of comparisons.

## Concepts

Magnetic flux \( \Phi \) through a search coil of \( N \) turns produces an induced charge (ballistic) or a time-integrated voltage (fluxmeter) when the flux changes. Faraday: \( v = N \mathrm{d}\Phi/\mathrm{d}t \). Integrate: \( \int v\,\mathrm{d}t = N \Delta\Phi \). A ballistic galvanometer is a PMMC with a long period: a pulse of charge \( Q=\int i\,\mathrm{d}t \) through it gives a first throw \( \theta \) proportional to \( Q \) if the pulse is short compared with the period. With circuit resistance \( R \), \( Q=N\Delta\Phi/R \) (search coil closed through the galvo). Then \( \Delta\Phi = (R/N) k \theta \) with \( k \) the ballistic constant in C/rad (or mm throw). Reverse the current in a magnetizing winding, or yank the search coil off a magnet, to produce \( \Delta\Phi \).

A fluxmeter is essentially an integrating millivoltmeter (or a heavily overdamped galvanometer with negligible restoring torque): the pointer deflection stays at a value \( \propto \Delta\Phi \) until you reset. Modern digital fluxmeters integrate \( v(t) \) in firmware. Either way you are measuring change of flux, not absolute flux, unless you start from a known zero (coil withdrawn to infinity, or a superconducting shield, or a well-argued \( B=0 \)).

B–H loop: for a ring specimen of mean circumference \( \ell \), \( N_1 \) magnetizing turns, current \( I \), \( H = N_1 I/\ell \) (ampere’s law, uniform ring). A secondary \( N_2 \) gives \( \Delta\Phi = A\Delta B \), so \( \Delta B = \Delta\Phi/A \). Step \( I \), measure each \( \Delta B \), accumulate \( B \) from a demagnetized origin (or from a saturation turning point). Hysteresis loop area is energy per cycle per volume, \( \oint H\,\mathrm{d}B \). Epstein frame: a standardized square of strip samples, 25 cm, used for electrical steel loss (hysteresis + eddy) at 50/60 Hz and 1.5 T or 1.7 T. Form factor of the induced voltage must be 1.11 (sine \( B \)); a feedback amplifier on modern testers enforces that. Student ballistic loops are DC (point by point); Epstein is AC loss.

Permeability \( \mu=B/H \), relative \( \mu_r=\mu/\mu_0 \). Incremental permeability is a small-signal slope on the loop. Apparent permeability of an open sample is ruined by demagnetizing fields; that is why rings and Epstein closed magnetic circuits exist. A search coil around a bar in air does not give the material \( B \)–\( H \) curve of the steel.

Other magnetic instruments: Hall probe (transverse voltage \( \propto I B \) in a semiconductor, needs calibration, excellent for air-gap B), NMR teslameter (proton resonance, a primary-ish standard for uniform fields), rotating-coil gaussmeters, Rogowski coil (air-cored toroid, \( v\propto\mathrm{d}i/\mathrm{d}t \), integrate for current — no saturation). Magnetometer for Earth’s field. Current balance (SI ampere, historical) and Kibble balance (modern mass/electrical SI) are metrology, not a student lab, but they sit at the top of the electrical chain.

Calibration chain (traceability): a measurement is traceable if there is an unbroken documented series of calibrations back to a stated reference (national or international), each with an uncertainty. Hierarchy, coarsest to finest in a teaching lab: the working DMM on the bench → a laboratory calibrator or 6½-digit standard → a departmental standard resistor / voltage reference → a national lab (NPL, NIST, PTB) realization of the SI. Magnetic: a search coil plus fluxmeter calibrated against a known mutual inductor (\( M \): \( \Delta\Phi = M\Delta I \)) whose \( M \) was measured against a calculable geometry or a national mutual-inductance standard. Do not claim “traceable” because a sticker says 2021 if you cannot show the certificate and the uncertainty.

Working standards in electrical labs: standard cells (historical Weston) and now zener / Josephson voltage; standard resistors (manganin, oil bath) and now quantized Hall; standard capacitors (fused silica, calculable Thompson–Lampard); mutual inductors for flux. Time/frequency from GPS or a departmental oscillator, itself compared to a national clock — frequency is the easiest SI quantity to get well.

Instrument calibration versus adjustment: calibration is comparison and a certificate (as-found, as-left). Adjustment is turning the brake magnet or a DMM’s internal cal constants. A calibration interval (yearly, 90 days) is a risk choice, not a physics constant. Before a GATE-style experiment you still zero, check a known point, and write the class index.

Mutual inductance method for fluxmeter constant: pass \( \Delta I \) through the primary of a known \( M \); secondary into the fluxmeter; \( N\Delta\Phi = M\Delta I \) for a 1-turn equivalent; actually \( \int v\,\mathrm{d}t = M\Delta I \). That calibrates the integrator in volt-seconds.

Demagnetization: an AC field slowly reduced to zero, or reversing DC of decreasing amplitude, to start a virgin curve. Residual magnetism in CTs (unit 04) is the same physics.

Safety: magnetizing currents on thick rings can be tens of amperes; search-coil voltages on a large \( \mathrm{d}\Phi/\mathrm{d}t \) can surprise. Epstein frames at 1.7 T are not toys.

## Equations

Faraday integral:

\[
\int v\,\mathrm{d}t = N\Delta\Phi,\qquad \Delta B=\frac{\Delta\Phi}{A}.
\]

Ballistic throw (ideal):

\[
Q=\frac{N\Delta\Phi}{R}=k_q\theta,\qquad \Delta\Phi=\frac{R k_q\theta}{N}.
\]

Ring specimen:

\[
H=\frac{N_1 I}{\ell},\qquad B=\mu H\quad(\text{linear only}).
\]

Hysteresis energy density per cycle: \( w=\oint H\,\mathrm{d}B \) (J/m³). Steinmetz sketch \( P_h = k_h f B_m^{n} \) with \( n\sim 1.6 \) — empirical, not a law.

Mutual-inductance calibration:

\[
\int v\,\mathrm{d}t = M\Delta I.
\]

Hall: \( V_H = k_H I B \) (geometry and \( n,e,t \) in the semiconductor).

Rogowski:

\[
v = -\mu_0 n A \frac{\mathrm{d}i}{\mathrm{d}t},\qquad i(t)=\frac{1}{\mu_0 n A}\int v\,\mathrm{d}t.
\]

Traceability combination: if each link has standard uncertainty \( u_i \), a simple model is \( u_c=\sqrt{\sum u_i^2} \) along the chain for that quantity (GUM); UG labs more often add a manufacturer spec as Type B (unit 01).

Epstein specific total loss \( P_s \) in W/kg from measured power into the magnetizing winding minus \( I^2 R \) of copper, divided by active mass, at a stated \( B_m \) and \( f \).

## Methods

Flux change: decide \( \Delta\Phi \) (reverse \( I \), or remove coil). Compute \( R \) of the closed secondary circuit. Apply the ballistic constant from a recent \( M\Delta I \) calibration, not from a 10-year-old lab sheet without checking.

B–H: demagnetize; step \( H \); record throws; accumulate \( B \); plot. Correct for air flux if the coil is larger than the sample (\( B_{\mathrm{meas}}A_{\mathrm{coil}}=B_{\mathrm{iron}}A_{\mathrm{iron}}+B_{\mathrm{air}}A_{\mathrm{gap}} \)).

Calibrate a fluxmeter: known \( M \), known \( \Delta I \), known expected volt-seconds, adjust scale or compute a factor.

Calibrate a DMM on DC volts: a multifunction calibrator or a Kelvin–Varley divider plus a standard cell/zener. Record as-found error, adjust if allowed, as-left, and environmental conditions.

When writing a certificate in a student report: identify the unit under test, the standard, the procedure, the results, the uncertainty model (even if it is only class index plus standard’s spec), date, and who signed. That is the chain’s paperwork.

Hall probe: zero in a mu-metal shield or far from iron; align for max reading (cosine error); do not drop; current through the Hall element is part of the scale factor.

## Mistakes

Treating a fluxmeter reading as absolute \( B \) without a defined zero or area.

Using \( H=NI/\ell \) on an open bar (demag field).

Forgetting \( N \) of the search coil (\( \Delta\Phi \) versus \( N\Delta\Phi \)).

Ballistic: pulse not short compared with the period, or an underdamped swing read as if ballistic constant still applied.

Epstein: reporting DC ballistic \( \mu \) as 50 Hz loss data.

Calibration: “traceable to NPL” with no certificate path.

Reversing a Hall probe 180° and not noticing the sign, then averaging two wrong magnitudes.

Rogowski: leaving a winding gap (not a closed toroid of ampere-turns around the conductor) so nearby return currents pollute \( i \).

Magnetizing a CT with DC during a resistance test and then using it for a 0.2 class metering job without demagnetizing.

Mixing cgs gauss/oersted with tesla/(A/m): \( 1\,\mathrm{T}=10^4\,\mathrm{G} \), \( H \) in A/m versus oersted (\( 1\,\mathrm{Oe}=1000/(4\pi) \) A/m). Pick SI.

A ballistic walk-through: \( N=50 \), \( R=200\,\Omega \), \( k_q=2.00\,\mu\mathrm{C} \) per radian, throw 0.150 rad. \( Q=0.300\,\mu\mathrm{C} \). \( \Delta\Phi=Q R/N=0.300\times 10^{-6}\times 200/50=1.20\,\mu\mathrm{Wb} \). If \( A=4.00 \) cm², \( \Delta B=0.00300 \) T.

Ring: \( \ell=0.400 \) m, \( N_1=200 \), \( I=1.50 \) A, \( H=200\times 1.50/0.400=750 \) A/m. If \( B=0.90 \) T, \( \mu_r=B/(\mu_0 H)=0.90/(4\pi\times 10^{-7}\times 750)=955 \).

Mutual cal: \( M=10.0 \) mH, \( \Delta I=2.00 \) A, \( \int v\,\mathrm{d}t=0.0200 \) V·s. If the fluxmeter reads 0.0194 V·s, factor \( 0.0200/0.0194=1.031 \).

Hall: \( k_H=1.50 \) V/(A·T), \( I=0.100 \) A, \( V_H=12.0 \) mV, \( B=V_H/(k_H I)=0.0800 \) T.

Energy of a loop: a rectangular sketch 800 A/m by 1.2 T, area \( 960 \) J/m³ per cycle. At 50 Hz, 48 kW/m³ — a crude hysteresis-only number, not a substitute for Epstein total loss.

Traceability sketch: working meter ±0.05%, lab standard ±0.01%, national ±0.002%. RSS ≈ 0.051% if you combine them as standard uncertainties — the working meter dominates. Improving the national link does nothing until the working meter is better. That is the practical moral of the chain.
