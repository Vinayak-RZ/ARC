# Converter magnetics and thermal: inductors, transformers, heatsinks

Every converter that is not a theoretical switch-diode pair stores energy in inductors and transformers and dumps loss into silicon and copper that a heatsink must carry to air. Undergraduate power electronics needs enough magnetics to size a chopper inductor and a high-frequency transformer from volt-seconds, and enough thermal resistance arithmetic to predict \(T_J\). This is not a magnetics-design course (no finite-element core loss maps) and not a CFD heatsink course.

## Concepts

An inductor in a CCM chopper is an energy bucket: \(\tfrac12 L I^2\) swings as the current ripples, but a DC (or low-frequency) bias stores a large mean energy. The core must not saturate at \(I_{\mathrm{peak}}=I_{\mathrm{dc}}+\Delta i/2\). Faraday: \(v=N d\phi/dt\), so the volt-second product \(\int v\,dt = N A_e \Delta B\). For a buck on-interval, \((V_{in}-V_{out})D T_s = N A_e \Delta B\). Choosing \(\Delta B\) (often 0.2–0.3 T at high frequency for ferrite, more for iron powder that also stores energy in a distributed gap) sets \(N A_e\). Inductance \(L=N^2/R_{\mathrm{rel}}\). Gapping a ferrite increases reluctance, stores energy in the gap (\(B^2/2\mu_0\) per volume), and linearizes \(L\). Powder cores have distributed gap. Saturable cores are for specialised snubbers, not for CCM buck L.

Current ripple specification, typically 20–40% of \(I_L\), is how UG problems give enough to compute \(L=V D/(f \Delta i)\). Skin and proximity effects increase AC copper loss at \(f_s\); a first-cut uses DC resistance plus a factor, or Litz at high \(f_s\). Window area must fit \(N\) turns of a current-rated wire.

Transformers in isolated converters transfer volt-seconds without (ideally) storing energy. Magnetizing inductance \(L_m\) is large; magnetizing current is a small triangle set by \(V T_{on}=L_m \Delta i_m\). Forward converters need a reset path so \(B\) returns to the starting point each cycle (third winding, RCD clamp, or active clamp). Flyback transformers are inductors with a secondary: they *do* store \(\tfrac12 L_p I_p^2\) and dump it to the secondary when the switch opens. Area-product methods: \(A_p=A_e A_w\) scales with power and frequency. Turns ratio \(n=N_s/N_p\) sets \(V_s=n V_p\) during conduction of the corresponding winding. Leakage inductance \(L_{\sigma}\) is the snubber’s enemy (unit 08). Isolation voltage is a safety rating, not a Faraday number.

Core loss: Steinmetz \(P_v=k f^\alpha \hat B^\beta\) as a named fit; UG may just say “core loss rises with \(f\) and \(B\).” Copper loss \(I_{\mathrm{rms}}^2 R_{\mathrm{ac}}\). Temperature rise of the mag part is often estimated from surface area and an empirical mW/cm² rule; exams more often stop at \(L\), \(N\), and \(\Delta B\).

Thermal chain for semiconductors (repeat from unit 01, now with sink sizing):

\[
T_J=T_A+P_D(\theta_{JC}+\theta_{CS}+\theta_{SA}).
\]

\(\theta_{SA}\) is the sink-to-ambient resistance, a function of sink volume, fin design, and airflow. Natural convection might be 2–5 K/W for a small extruded sink; forced air is lower. Thermal grease \(\theta_{CS}\approx 0.2\)–\(1\,\mathrm{K/W}\) depending on package. Derating: some datasheets want \(T_J\le 125^\circ\mathrm{C}\) even if \(T_{J,\max}=150^\circ\mathrm{C}\). Parallel devices share \(\theta\) only if they share the sink well; a hotter device takes more MOSFET current (\(R_{DS(on)}\) up) which actually helps share, whereas IGBTs can hog.

Losses to put in \(P_D\): conduction, switching, diode recovery, gate drive (small), snubber (can be large). A 92% efficient 1 kW converter still dumps 87 W — that is a real sink, not a TO-220 tab in still air.

Capacitors are thermal too: ESR loss \(I_{\mathrm{rms}}^2 R_{\mathrm{ESR}}\), ripple current rating. Electrolytics on a rectifier DC link are often the life-limit, not the IGBT.

Forced-air versus liquid cooling is named. Junction-to-case is not optional: you cannot “heatsink away” a \(\theta_{JC}\) that already puts \(T_J\) over the limit at the given \(P_D\).

EMI inductors (common-mode chokes) are magnetics that should not saturate on differential load current; they use high-\(\mu\) cores with balanced windings. UG mentions them as filter parts.

Core selection is a material-and-frequency sentence. Silicon steel is for 50 Hz transformers and for DC chokes that need high saturation flux (1.5 T class) and can tolerate iron loss at line frequency. Ferrite (MnZn) is the 20–200 kHz default: lower \(B_{sat}\) (0.3–0.4 T), much lower loss at \(f_s\). Iron powder and sendust store energy with a distributed gap and a soft saturation curve, which is kind to CCM boost inductors that see a DC bias. Nanocrystalline cores appear in common-mode chokes. Using a 50 Hz EI lamination as a 50 kHz flyback core is a heater, not a transformer.

The area-product argument, without turning it into a design spreadsheet: transferred power, flux swing, current density, and window utilisation multiply to a minimum \(A_e A_w\). Frequency sits in the denominator (more volt-seconds per second means less core). That is why a 100 W flyback at 100 kHz is a small pot core and a 100 W 50 Hz transformer is a handful. UG numericals almost always give \(A_e\) and ask for \(N\), or give \(L\) and \(\Delta i\) and ask for \(L\).

Leakage inductance is set by geometry: interleaved windings reduce it; separate bobbin chambers increase it (and increase isolation). Flyback designers sometimes want a little leakage for zero-voltage opportunities; forward and bridge designers usually want as little as possible because leakage energy hits the clamp. The clamp energy \(\tfrac12 L_{\sigma} I^2 f_{sw}\) is a real thermal term in unit 08 and here.

Thermal interfaces: mica plus grease versus silicone pads versus direct-bonded copper in a power module. Each has a \(\theta_{CS}\). A TO-247 on a dry sink can be a kelvin per watt extra. Parallel IGBTs on one sink still need matched \(V_{CE}\) and a common gate-drive return so they switch together; otherwise one die takes the switching energy. MOSFETs share better in conduction because \(R_{DS(on)}\) rises with temperature. Derate current if the sink is in a 50 °C cabinet, not a 25 °C datasheet ambient.

Capacitor life is thermal and voltage. Ripple current heats ESR, which heats the electrolyte, which raises ESR. DC-link electrolytics are often the first wear-out in a VSI. Film capacitors take high RMS at high frequency (snubbers, resonant tanks) with lower ESR. UG problems that give ESR and \(I_{\mathrm{rms}}\) want \(P=I^2 R\) and maybe a temperature rise if \(\theta\) is given.

## Equations

Volt-second and flux:

\[
\int v\,dt = N A_e \Delta B,\qquad L=\frac{N^2}{\mathcal{R}},\qquad \mathcal{R}=\frac{\ell_g}{\mu_0 A_g}+\frac{\ell_c}{\mu_r\mu_0 A_e}.
\]

Buck \(L\) from ripple:

\[
L=\frac{V_{out}(1-D)}{f_s\Delta i_L}.
\]

Boost:

\[
L=\frac{V_{in} D}{f_s\Delta i_L}.
\]

Energy in a gap (approximate, all energy in gap):

\[
E=\frac{B^2}{2\mu_0} A_g \ell_g =\tfrac12 L I^2.
\]

Transformer reset (forward, third-winding 1:1): off-time must satisfy \(V_{in} t_{\mathrm{reset}}\ge V_{in} t_{\mathrm{on}}\) so \(D\le 0.5\) in the simple case.

Flyback:

\[
\frac{V_{out}}{V_{in}}=\frac{N_s}{N_p}\frac{D}{1-D}\quad\text{(CCM)}.
\]

Steinmetz (named):

\[
P_{\mathrm{core}}=k f^\alpha \hat B^\beta \times\mathrm{volume}.
\]

Thermal:

\[
T_J=T_A+P_D\sum\theta_i,\qquad \theta_{SA}=\frac{T_S-T_A}{P_D}.
\]

Heatsink required:

\[
\theta_{SA}\le\frac{T_{J,\max}-T_A}{P_D}-\theta_{JC}-\theta_{CS}.
\]

Capacitor ESR loss: \(P_{\mathrm{ESR}}=I_{\mathrm{rms}}^2 R_{\mathrm{ESR}}\).

## Methods

1. From topology, write \(\Delta i\) spec and \(V_L\) in each interval. Solve \(L\). Check peak current against saturation \(I_{\mathrm{sat}}=B_{\mathrm{sat}} A_e N/L\) (or from the core’s AL value and \(B_{\mathrm{sat}}\)).
2. Transformer: volt-second on the primary, pick \(B_{\mathrm{pk}}\), get \(N_p=V T/(A_e\Delta B)\). Ratio from voltages plus diode drops. Provide reset.
3. Thermal: sum device losses, compute \(\theta_{SA}\) needed, pick a sink (or fail the design). Do not iterate \(R_{DS(on)}(T)\) unless asked; if asked, one iteration from 25 °C to predicted \(T_J\) is enough.
4. Gap: if \(\tfrac12 L I^2\) cannot fit in the core volume without saturation, add gap. Recalculate \(N\) so \(L\) is restored.
5. RMS currents from the converter unit feed copper loss. Use \(I_{\mathrm{rms}}\), not \(I_{\mathrm{avg}}\), in \(R_{\mathrm{ac}}\).
6. Capacitor ripple current from the topology (boost capacitor current is almost the diode current minus DC load).

Worked pattern — buck L: \(V_{out}=12\,\mathrm{V}\), \(D=0.3\), \(f_s=50\,\mathrm{kHz}\), \(\Delta i=1.2\,\mathrm{A}\). \(L=12\times 0.7/(50000\times 1.2)=140\,\mu\mathrm{H}\). Peak (say \(I=5\,\mathrm{A}\)) \(5.6\,\mathrm{A}\). Energy \(2.2\,\mathrm{mJ}\). That energy must sit mostly in the gap of a ferrite core; a gapless high-\(\mu\) core of the same \(A_e\) would saturate at a small fraction of 5 A.

## Mistakes

- Using \(L=V/(2\pi f I)\) from 50 Hz mains magnetics on a 50 kHz chopper.
- Forgetting the gap: a high-\(\mu\) ferrite inductor saturates at almost no DC current.
- Forward transformer without reset (\(B\) walks into saturation).
- Treating a flyback coupled inductor as an ideal transformer that cannot store energy.
- Thermal: using \(\theta_{JA}\) of a free-air datasheet *and* adding a sink (double counting, or mixing conditions).
- Computing copper loss with average current.
- Sizing the sink for conduction loss only while switching at 20 kHz with slow IGBTs.
- Ignoring that \(\theta_{SA}\) rises if the sink is in a closed box (the “ambient” is not 25 °C room air).
- Capacitor: using \(C=I\Delta t/\Delta V\) but forgetting RMS ripple heating.

A practical iteration: (1) assume \(T_J=100^\circ\mathrm{C}\), look up \(R_{DS(on)}\) or \(V_{CE(sat)}\) at that temperature, (2) recompute \(P_D\), (3) recompute \(T_J\), (4) stop when the two \(T_J\) values agree within a few kelvin. One iteration is enough for UG. Skipping the temperature coefficient of \(R_{DS(on)}\) underestimates MOSFET loss, sometimes by a factor of two.

Magnetics set \(L\) and \(N\); thermal sets whether the silicon can run that current continuously. Dual converters and cycloconverters (last unit) are still limited by both. Ferrite \(\Delta B\) at 50 kHz is not the 1.5 T of a 50 Hz transformer; if a numerical produces \(B>0.3\,\mathrm{T}\) on ferrite, the core is the wrong material or \(N\) is too small.
