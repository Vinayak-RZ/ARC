# Speed-time curves and mechanics of the train

Electric traction is utilization on wheels: a locomotive or EMU converts electrical power into tractive effort against mass, gradient, and drag, on a schedule defined by a speed–time curve. This unit is trapezoidal and quadrilateral speed–time curves, average and RMS speed, specific energy, adhesion, and the mechanics of acceleration. Converter and motor control sit in electric-drives and power-electronics packs; here the train is a point mass with a traction characteristic.

## Concepts

A suburban service is a sequence of start, accelerate, (maybe coast), brake, stop, dwell. Plot speed \(v\) against time \(t\). The trapezoidal curve is accelerate at constant \(\alpha\) to \(v_m\), run at \(v_m\), brake at constant \(\beta\) to rest. The quadrilateral (or trapezoid with coasting) inserts a coasting interval where tractive effort is zero and drag plus gradient slow the train. Peak speed \(v_m\) is not the same as average speed \(v_{\mathrm{avg}}=D/T\) over the run (distance \(D\), time \(T\) excluding or including dwell — the problem must say). Schedule speed includes dwell; average running speed does not. RMS speed \(v_{\mathrm{rms}}=\sqrt{(1/T)\int v^2\,dt}\) matters because motor heating and some energy terms track \(v^2\) or current related to speed on a given characteristic.

Distance is the area under the speed–time curve. For a trapezoid with acceleration time \(t_1=v_m/\alpha\), braking time \(t_3=v_m/\beta\), free-run time \(t_2=T-t_1-t_3\),

\[
D=\frac{v_m}{2}t_1+v_m t_2+\frac{v_m}{2}t_3=v_m T-\frac{v_m^2}{2}\Bigl(\frac{1}{\alpha}+\frac{1}{\beta}\Bigr).
\]

If the run is so short that there is no free-run (triangular curve), \(v_m\) is limited by \(D\) and the two ramps. Coasting saves energy (you do not keep feeding \(P=Fv\)) at the cost of time; a higher initial \(v_m\) plus coast can still meet the schedule.

Tractive effort \(F\) at the wheels (or drawbar) must cover:

- Acceleration of translational mass: \(m\alpha\).
- Rotary inertia of axles and motor: accounted as an additive mass, \(m_{\mathrm{eff}}=m(1+\gamma)\) with \(\gamma\sim 0.08\)–\(0.15\) typical UG, or as \(J\alpha/r^2\).
- Gradient: \(mg\sin\theta\approx mg i\) for small \(i\) in pu (a 1% grade is \(i=0.01\)). In train units, kg/tonne or N/tonne appear; be consistent. A 1 in \(n\) gradient is \(i=1/n\).
- Train resistance: a Davis-style \(R=A+Bv+Cv^2\) (journal, flange, aerodynamic). UG often uses a constant N/tonne plus a \(v^2\) term, or a single given N/t.

Coasting: \(F_{\mathrm{traction}}=0\), so \(m_{\mathrm{eff}} a= -R \pm mg i\). Braking: mechanical, rheostatic, or regenerative (unit of drives); the speed–time brake ramp \(\beta\) is a service brake rate, not necessarily the adhesion limit.

Adhesion: the rail can supply at most \(\mu N\) per driven axle (with \(N\) the axle load, \(\mu\) 0.15–0.3 dry, much less wet). If the demanded \(F\) exceeds adhesion, wheelslip. Starting tractive effort is adhesion-limited; high-speed effort is motor/inverter limited (power limit \(P=Fv\) so \(F=P/v\) falls). A typical DC-series or V/f-plus-slip traction characteristic: constant \(F\) up to a base speed, then constant power, then maybe a further weakening. UG numericals often give a constant \(F\) during the acceleration ramp (the trapezoid assumption).

Specific energy consumption: Wh/t·km or kWh/t·km, energy at the pantograph or third rail divided by (mass × distance). Accelerating energy \(\tfrac12 m_{\mathrm{eff}} v_m^2\) plus losses and gravity (recovered on down grades if regenerative). For a trapezoid without coasting or gradient, a classic decomposition is accelerating energy plus energy against resistance during the run, minus energy returned in braking if regenerative. UG problems that forbid regeneration dump braking energy in resistors or shoes.

Crest speed versus average: suburban EMUs have high \(\alpha\) (many driven axles) to raise average speed without a high \(v_m\) that would waste energy as \(\propto v_m^2\). Main-line locomotives have higher \(v_m\) and lower \(\alpha\). That is why the quadrilateral with coasting is a suburban trick.

Supply: 1.5 kV or 750 V DC third rail / overhead; 25 kV 50 Hz AC overhead (common main line); 15 kV 16.7 Hz in some countries. On-board transformer and converters for AC; substations with rectifiers for DC. Voltage drop along a feeding section limits train current; UG may compute \(I=P/V\) and a simple \(IR\) drop. Regenerative braking on DC needs a receptive line (another train motoring, or inverters at the substation).

Mechanics of a train on a curve: extra resistance \(\propto 1/R_{\mathrm{curve}}\), sometimes given as N/t. Not a dynamics of hunting; just extra \(F\).

Dead-man’s handle, ATP, and signalling headways set the minimum \(T\) more than physics does on a real railway. The speed–time curve still has to fit the block.

## Equations

Kinematics, constant \(\alpha,\beta\):

\[
t_1=\frac{v_m}{\alpha},\qquad t_3=\frac{v_m}{\beta},\qquad D=v_m T-\frac{v_m^2}{2}\Bigl(\frac{1}{\alpha}+\frac{1}{\beta}\Bigr).
\]

Average speed \(v_{\mathrm{avg}}=D/T\). Schedule speed \(D/(T+t_{\mathrm{dwell}})\).

\[
v_{\mathrm{rms}}^2=\frac{1}{T}\int_0^T v^2\,dt.
\]

For a trapezoid that reaches \(v_m\):

\[
\int v^2\,dt=\alpha^2\frac{t_1^3}{3}+v_m^2 t_2+\beta^2\frac{t_3^3}{3}=\frac{v_m^3}{3\alpha}+v_m^2 t_2+\frac{v_m^3}{3\beta}.
\]

Effective mass: \(m_{\mathrm{eff}}=m(1+\gamma)\).

Tractive effort (straight, upgrade \(i\)):

\[
F=m_{\mathrm{eff}}\alpha + mg i + R(v).
\]

Power at wheels: \(P=Fv\). Electrical power \(P/\eta\).

Adhesion limit: \(F\le \mu m_{\mathrm{driven}} g\) (driven mass, not the whole train, unless all axles are motored).

Specific energy (no regen, level, resistance \(R\) constant, trapezoid) — energy at wheels:

\[
W=\tfrac12 m_{\mathrm{eff}} v_m^2 + R D
\]

in joules; divide by \(m D\) and convert to Wh/t·km. Regenerative braking can return a fraction \(\eta_{\mathrm{b}}\) of \(\tfrac12 m_{\mathrm{eff}} v_m^2\) minus the part used against drag during braking.

Gradient: 1 in \(n\) means \(i=1/n\), \(F_g=mg/n\).

## Methods

1. Sketch the speed–time curve. Classify trapezoid, triangle, or quadrilateral with coasting.
2. Write \(D=\) area. Solve for the unknown among \(D,T,v_m,\alpha,\beta\).
3. Compute \(v_{\mathrm{avg}}\) and, if asked, \(v_{\mathrm{rms}}\) from the integral above.
4. Convert tonnes to kg. Apply \(\gamma\) to get \(m_{\mathrm{eff}}\). Resolve gradient as \(i=1/n\) or % .
5. \(F=m_{\mathrm{eff}}\alpha+mgi+R\). Check adhesion. \(P=Fv\) at the speed asked (often at \(v_m\) or at start — start is \(v\approx 0\), so power is small even if \(F\) is large).
6. Energy: \(\int P\,dt=\int F v\,dt\). For constant \(F\) during acceleration, \(\int F v\,dt=F D_{\mathrm{acc}}\). Add resistance over the whole \(D\). Subtract regenerated braking energy if allowed.
7. Specific energy: Wh per tonne-km, watching the \(3.6\times 10^6\,\mathrm{J}=1\,\mathrm{kWh}\) conversion.

Worked pattern — trapezoid: \(\alpha=0.6\,\mathrm{m/s}^2\), \(\beta=0.8\,\mathrm{m/s}^2\), \(v_m=20\,\mathrm{m/s}\), \(T=60\,\mathrm{s}\). \(t_1=33.3\,\mathrm{s}\) wait: \(t_1=20/0.6=33.33\,\mathrm{s}\), \(t_3=25\,\mathrm{s}\), sum already 58.3 s, so \(t_2=1.7\,\mathrm{s}\). \(D=20\times 60-\tfrac12\times 400\times(1/0.6+1/0.8)=1200-200\times 2.083=783\,\mathrm{m}\). If \(t_1+t_3>T\), the trapezoid is impossible — go to a triangular curve with a lower \(v_m\).

## Mistakes

Using \(v_{\mathrm{avg}}=(0+v_m)/2\) on a trapezoid that has a long free-run (that formula is the triangle). Forgetting rotary inertia \(\gamma\). Applying adhesion to the whole train mass when only the loco axles are driven (a trailing stock train). Gradient 1 in 100 treated as \(45^\circ\). Mixing km/h and m/s in \(\alpha=v/t\). Power at start as \(F v_m\). Specific energy in J/kg without converting to Wh/t·km when the question asked railway units. Coasting with \(F=F_{\mathrm{acc}}\) still applied. Regenerating on a DC section that the problem said was non-receptive. Distance as \(v_m T\) without subtracting the two triangular corners. RMS speed as arithmetic mean. \(P=\sqrt{3}VI\) on a DC third-rail train. Using passenger-elevator kinematics without mass of the train.

Schedule speed is not average running speed. Dwell at stations is a large fraction of suburban \(T\); raising \(\alpha\) helps running time but not dwell.

Energy \(\tfrac12 mv^2\) uses \(m_{\mathrm{eff}}\) if rotary inertia was included in the motion; do not add \(\gamma\) twice.

A constant-power acceleration is not a straight line on the \(v\)–\(t\) plot (\(a=P/(mv)\) so \(v^2=2(P/m)t\)). The trapezoid’s straight ramp is a constant-force assumption. If the characteristic is given as constant power, integrate that instead of using \(t=v/\alpha\) with a single \(\alpha\).

Coasting on a level track with a Davis \(R=A+Bv+Cv^2\) is not a straight slope on the speed–time curve. At high speed the \(Cv^2\) term bites and the coast deceleration grows; at low speed the curve flattens toward \(A/m_{\mathrm{eff}}\). UG problems that give a single N/t for coasting licensed a constant deceleration \(\beta_{\mathrm{coast}}=R/m_{\mathrm{eff}}\). Use that if given; do not invent a quadratic if the data are a single number. On a down grade, coasting can *increase* speed (overhaul). Then the quadrilateral must include a brake or a regen hold, not an unbounded coast.

Specific energy on an up-and-down profile is not the level-track formula. Gravity energy \(mgh\) is paid on the climb and, with regenerative braking and a receptive line, partly returned on the descent. Without regen it heats shoes or resistors. A problem that gives a rolling resistance and a net change of altitude wants \(W=\tfrac12 m_{\mathrm{eff}}(v_2^2-v_1^2)+R D+mg\Delta h\) between two speed samples, not only \(\tfrac12 m v_m^2+RD\).

Substation spacing on DC: train current \(I=P/V\) at the worst simultaneous accelerating load, feeder resistance \(2\rho\ell/A\) if go-and-return, voltage at the train \(V_s-IR\). A 750 V third rail that sags to 500 V at the train is a traction problem, not a lighting one. AC 25 kV sags less for the same MW because \(I\) is smaller; transformer tap and booster transformers are the MV details, named only.

Notch control on a classical DC locomotive (series-parallel, field weakening) produces a family of \(F(v)\) curves. The speed–time trapezoid is then an envelope, not a single \(\alpha\). If the exam gives notches, integrate piecewise; if it gives one \(\alpha\), it already averaged the notches.

Adhesion \(\mu\) falls with speed and with contamination. A starting \(F\) that was legal at \(\mu=0.25\) is not legal at \(\mu=0.08\) in rain. Sanding and weight transfer (bogie pitch) are the mechanical remedies; they do not change \(m_{\mathrm{eff}}\alpha\) in the equation, they change the cap on \(F\).

Triangular (no free-run) distance \(D=v_m^2/(2\alpha)+v_m^2/(2\beta)\). Solving for the peak speed that just meets \(D\) and the two ramps is \(v_m=\sqrt{2D/(1/\alpha+1/\beta)}\). That is the short-station formula. Using the long-run trapezoid on a 400 m metro hop over-predicts \(v_m\) and under-predicts \(\alpha\) needed.
