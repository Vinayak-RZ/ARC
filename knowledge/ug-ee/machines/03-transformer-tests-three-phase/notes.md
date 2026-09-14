# OC/SC, regulation, three-phase connections

Open-circuit (OC, no-load) and short-circuit (SC) tests are how a transformer equivalent circuit is identified from measurements, without a full-load bank. Regulation and efficiency then follow from that circuit. Three-phase banks (and three-phase cores) extend the same per-phase model: connection (Y, Δ, zigzag) sets line-to-phase ratios, phase shift, and a path for triplen harmonics. This unit is laboratory algebra plus connection geometry. It assumes the single-phase equivalent circuit of the previous unit.

The pedagogical point is that two tests split the model. OC at rated voltage sees the shunt branch because series drops are tiny at no-load current. SC at rated current sees the series branch because the shunt is starved of voltage. Mixing the tests — OC at reduced voltage, SC at rated voltage — wrecks the split.

## Concepts

Open-circuit test: rated voltage is applied to one winding, usually the LV winding for convenience and safety; the other winding is open. Instruments read \(V_\mathrm{OC}\), \(I_\mathrm{OC}\), and \(P_\mathrm{OC}\). The power is core loss (plus a negligible \(I_\mathrm{OC}^2 R\) in the excited winding). Shunt parameters on the excited side:

\[
R_c = \frac{V_\mathrm{OC}^2}{P_\mathrm{OC}},\qquad |Z_\phi| = \frac{V_\mathrm{OC}}{I_\mathrm{OC}},\qquad I_c=\frac{V_\mathrm{OC}}{R_c},\qquad I_m=\sqrt{I_\mathrm{OC}^2-I_c^2},\qquad X_m=\frac{V_\mathrm{OC}}{I_m}.
\]

Some texts use \(1/R_c\) and \(1/X_m\) as parallel admittances from \(P/V^2\) and \(Q/V^2\) with \(Q=\sqrt{(VI)^2-P^2}\). Same circuit.

Short-circuit test: one winding is shorted, usually the LV; reduced voltage is applied to the other, usually HV, until rated current flows. Instruments read \(V_\mathrm{SC}\), \(I_\mathrm{SC}\), \(P_\mathrm{SC}\). The voltage is a few percent of rated, so core flux is small and core loss is neglected next to copper loss. Series parameters on the excited side:

\[
Z_\mathrm{eq}=\frac{V_\mathrm{SC}}{I_\mathrm{SC}},\qquad R_\mathrm{eq}=\frac{P_\mathrm{SC}}{I_\mathrm{SC}^2},\qquad X_\mathrm{eq}=\sqrt{Z_\mathrm{eq}^2-R_\mathrm{eq}^2}.
\]

Percent impedance is \(Z_{\%}=(V_\mathrm{SC}/V_\mathrm{rated})\times 100\) when \(I_\mathrm{SC}\) is rated current.

Regulation from the approximate circuit was given last unit. Equivalent-circuit parameters from OC/SC plug into that formula. Efficiency uses \(P_\mathrm{OC}\) as core loss at rated voltage and \(P_\mathrm{SC}\) as full-load copper loss (if SC was run at rated current). At load fraction \(x\), copper loss is \(x^2 P_\mathrm{SC}\).

Three-phase transformers may be a single three-limb or five-limb core, or a bank of three single-phase units. Per-phase equivalent circuit is the single-phase model. Line voltages and currents depend on Y or Δ:

- Wye: \(V_\mathrm{L}=\sqrt{3} V_\mathrm{ph}\), \(I_\mathrm{L}=I_\mathrm{ph}\). Neutral may be accessible.
- Delta: \(V_\mathrm{L}=V_\mathrm{ph}\), \(I_\mathrm{L}=\sqrt{3} I_\mathrm{ph}\). No isolated neutral; triplen currents can circulate in the delta.

Turns ratio of a three-phase transformer is specified as a line-to-line voltage ratio on the nameplate. Phase turns ratio equals line ratio for Y–Y and Δ–Δ, and differs by \(\sqrt{3}\) for Y–Δ and Δ–Y. Example: 11 kV / 415 V Dyn11 has HV phase voltage \(11000/\sqrt{3}\) if the HV is wye, LV phase voltage 415 V if the LV is delta.

Clock notation (Dyn11, YNd1, …) states LV connection, HV connection, and phase displacement in hours of 30°. Dyn11 means delta LV, wye HV? Standard IEC order is HV then LV: Dyn11 is HV delta, LV wye, LV lagging HV by 330° or leading by 30° depending on the hour convention — the hour is the LV phasor position relative to HV. Students must use the standard they are given. What matters physically: Y–Δ introduces a 30° shift; Y–Y and Δ–Δ can be 0° or 180° (additive/subtractive polarity, or zigzag). Parallel operation of two three-phase transformers requires the same ratio, the same %Z (approximately), the same polarity, and the same clock number. Mismatched 30° shift produces circulating current.

Zigzag (Zn) windings provide a neutral and a low-impedance path to earth-fault zero sequence, used as grounding transformers. Open-delta (V–V) uses two transformers to serve a three-phase load at reduced capacity: available VA is \(1/\sqrt{3}\) of the rating of three units, or equivalently 57.7% of a full bank of the same two units plus a third identical one. Scott-T converts three-phase to two-phase; it is historical but still in some syllabi.

Triplen harmonics (3, 9, …) in magnetizing current are co-phasal in three phases. In a wye without a neutral they cannot flow in the lines; flux then distorts unless a delta or a three-limb core provides a path. A Δ winding lets triplen current circulate, keeping flux closer to sinusoidal. Three-limb cores have no closed iron path for zero-sequence flux (it must go through air/tank), which also limits third-harmonic flux. Five-limb cores and banks of three single-phase units do have a zero-sequence iron path; they need a delta or a connected neutral to avoid third-harmonic voltages.

Tertiary windings are often delta, for harmonics, unbalanced loads, and station service. They appear on the nameplate as a third voltage.

On-load tap changers sit on the HV winding. Regulation calculations with taps change \(a\) and sometimes the referred \(Z\).

Temperature correction: DC winding resistance is measured cold and corrected to 75 °C (copper) for loss guarantees. SC test \(R_\mathrm{eq}\) is AC resistance including eddy in the conductors; it is slightly above DC.

## Equations

OC (excited side):

\[
P_\mathrm{OC}=V_\mathrm{OC} I_\mathrm{OC}\cos\phi_0,\qquad R_c=\frac{V_\mathrm{OC}^2}{P_\mathrm{OC}},\qquad X_m=\frac{V_\mathrm{OC}}{\sqrt{I_\mathrm{OC}^2-(V_\mathrm{OC}/R_c)^2}}.
\]

SC (excited side, rated current):

\[
R_\mathrm{eq}=\frac{P_\mathrm{SC}}{I_\mathrm{SC}^2},\qquad Z_\mathrm{eq}=\frac{V_\mathrm{SC}}{I_\mathrm{SC}},\qquad X_\mathrm{eq}=\sqrt{Z_\mathrm{eq}^2-R_\mathrm{eq}^2}.
\]

Approximate regulation (lagging \(\theta\)):

\[
\mathrm{reg}\approx \frac{I R_\mathrm{eq}\cos\theta + I X_\mathrm{eq}\sin\theta}{V}
\]

and for leading, the \(X\) term subtracts.

Efficiency at load fraction \(x\) and power factor \(\mathrm{pf}\):

\[
\eta=\frac{x S_\mathrm{r}\,\mathrm{pf}}{x S_\mathrm{r}\,\mathrm{pf}+P_\mathrm{OC}+x^2 P_\mathrm{SC}}.
\]

Maximum efficiency at given PF when \(x^2 P_\mathrm{SC}=P_\mathrm{OC}\), so \(x=\sqrt{P_\mathrm{OC}/P_\mathrm{SC}}\).

Y and Δ:

\[
V_\mathrm{L,Y}=\sqrt{3}V_\mathrm{ph},\quad I_\mathrm{L,Y}=I_\mathrm{ph};\qquad V_\mathrm{L,\Delta}=V_\mathrm{ph},\quad I_\mathrm{L,\Delta}=\sqrt{3}I_\mathrm{ph}.
\]

Open-delta throughput for two identical units each rated \(S_1\):

\[
S_\mathrm{V}=\sqrt{3}\,S_1.
\]

Three-phase bank of three units each \(S_1\) would be \(3S_1\); the V–V bank is \(S_\mathrm{V}/(3S_1)=1/\sqrt{3}\approx 0.577\) of that.

Per-phase VA of a three-phase transformer: \(S_\mathrm{3\phi}/3\). Use phase voltage and phase current in the single-phase equivalent circuit.

## Methods

Procedure for OC: isolate the unused winding (open, not short). Apply rated voltage at rated frequency to the chosen winding. Read wattmeter, voltmeter, ammeter. Compute \(R_c\) and \(X_m\) on that side. If the equivalent circuit is wanted on the other side, scale \(R_c\) and \(X_m\) by \(a^2\).

Procedure for SC: short the unused winding with a conductor sized for rated current. Apply a reduced voltage, raise until ammeter shows rated current (of the excited winding). Read \(V,I,P\). Compute \(R_\mathrm{eq},X_\mathrm{eq}\) on that side. Do not apply rated voltage to a shorted transformer.

Referring: if OC was done on LV and SC on HV, put \(R_c,X_m\) on LV and \(R_\mathrm{eq},X_\mathrm{eq}\) on HV, then scale one set by \(a^2\) to combine. Draw the circuit and label the side; do not mix numbers.

Regulation problem: convert load to current on the same side as \(Z_\mathrm{eq}\). Use the phasor or the approximate formula. State lagging versus leading.

Three-phase numerical: reduce to per-phase. For a Y–Y bank, phase voltage is line/\(\sqrt{3}\). For a Δ–Δ bank, phase voltage is line voltage. For Y–Δ, sketch HV and LV phasors; the line-to-line ratio on the nameplate is not the turns ratio. Turns ratio \(N_H/N_L = V_{H,\mathrm{ph}}/V_{L,\mathrm{ph}}\).

Parallel operation check list: same voltage ratio, same polarity/clock, %Z within a few percent and similar X/R if circulating current and load sharing both matter. Load shares inversely with \(Z_\mathrm{eq}\) in ohms on a common base.

All-day efficiency: sum energy out over 24 h divided by energy in. Core loss runs whenever the transformer is energized; copper loss follows the load cycle. A distribution transformer with 8 h at full load and 16 h at no load still burns \(24 P_\mathrm{OC}\) of core energy.

When only %Z and X/R are given, reconstruct \(R_\mathrm{eq}+jX_\mathrm{eq}\) on the chosen base: \(|Z|=Z_{\%}/100\times V/I_\mathrm{rated}\), then \(R=|Z|/\sqrt{1+(X/R)^2}\) etc.

## Mistakes

Running SC at rated voltage. That is a fault. \(V_\mathrm{SC}\) is typically 4–8% of rated.

Using OC current as if it were rated current in \(R_\mathrm{eq}=P/I^2\). OC power over \(I_\mathrm{OC}^2\) is not \(R_\mathrm{eq}\); it is related to \(R_c\) in a parallel branch.

Forgetting to refer shunt and series to the same side. Adding HV \(Z_\mathrm{eq}\) to LV \(R_c\) in ohms is meaningless.

Using line voltage in a per-phase circuit that expects phase voltage. A 415 V Y motor on a 415 V transformer secondary has \(V_\mathrm{ph}=240\ \mathrm{V}\) if both are wye.

Paralleling Dy11 with Dy1. The 60° or 30° mismatch (depending on pair) drives huge circulating current.

Treating open-delta capacity as two-thirds of a three-unit bank. It is \(1/\sqrt{3}\), not \(2/3\). Two-thirds is a common wrong memory.

Ignoring the 30° Y–Δ shift in a synchronization or paralleling problem.

Using \(P_\mathrm{SC}\) as core loss. SC power at rated current is copper loss.

Computing \(X_m\) as \(V/I_\mathrm{OC}\) without removing \(I_c\). That is \(|Z_\phi|\), not \(X_m\). On a lossy no-load test the error is visible.

Correcting OC voltage for winding resistance drop. It is second-order at no load; the standard UG split ignores it.

Writing Dyn11 as if the letters were LV first. IEC string is HV connection, LV connection, then clock. Confirm the local convention before asserting which winding is delta.

Using 4.44 in the SC test to find \(B_\mathrm{max}\). SC flux is small; Faraday at \(V_\mathrm{SC}\) gives a small \(\Phi\), which is why core loss is neglected.

Nameplate clock numbers are not a decoration for the equivalent circuit, but they are a hard constraint on paralleling and on which bus a transformer may join. A Dy11 and a Dy5 differ by 180° of LV phase and will fight if paralleled. Record the vector group from the nameplate before writing a single-line diagram. When a problem omits the clock, assume 0° only for Yy0 or Dd0 as stated, never for a Y–Δ pair.
