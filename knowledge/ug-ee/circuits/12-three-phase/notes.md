# Balanced and unbalanced three-phase

Three-phase is the industrial AC default: three voltages 120° apart, constant instantaneous power when balanced, and economical conductors. UG circuit courses treat Y and Δ sources and loads, line vs phase quantities, balanced reduction to one phase, and a first look at unbalanced loads via per-phase or mesh methods. Sequence components belong mainly to power systems; here we stay with circuit laws.

## Concepts

A balanced three-phase set is \( v_a = V_m \cos\omega t \), \( v_b = V_m \cos(\omega t - 120^\circ) \), \( v_c = V_m \cos(\omega t + 120^\circ) \) (abc sequence). The opposite phase order is acb. Instantaneous sum of balanced voltages is zero; they can be generated with a three-wire source and no neutral current. Instantaneous power \( p_a+p_b+p_c = 3 V_\mathrm{ph,rms} I_\mathrm{ph,rms} \cos\theta \) is constant, which is why three-phase motors run smoothly.

Wye (Y) connection: phase voltage is from line to neutral. Line voltage is between lines, \( V_L = \sqrt{3} V_P \) and leads the corresponding phase voltage by 30° in abc. Line current equals phase current in Y. Delta (Δ): phase voltage equals line voltage; line current is \( \sqrt{3} \) times phase current and lags (or leads, depending on labeling) by 30°. Mixing Y source with Δ load is normal; convert everything to one equivalent Y for balanced analysis.

Four-wire Y: a neutral conductor carries the residual current. In balance, \( I_n = 0 \). In unbalance, \( I_n = -(I_a+I_b+I_c) \). Three-wire Y loads with no neutral force \( I_a+I_b+I_c = 0 \) even if impedances differ, which shifts the load-neutral voltage (floating neutral). That shift is the usual unbalanced homework.

Power: \( P = \sqrt{3} V_L I_L \cos\theta \) for balanced three-phase, where θ is the phase impedance angle, not the angle between VL and IL (those are 30° off). Two-wattmeter method measures three-phase power on three-wire lines: \( P = W_1 + W_2 \), and \( \tan\theta = \sqrt{3}(W_1-W_2)/(W_1+W_2) \) in the balanced case.

Unbalanced Δ: each phase impedance sees a known line voltage, so three independent single-phase problems, then line currents are differences of phase currents. Unbalanced Y with neutral: three independent phase problems. Unbalanced Y without neutral: solve a 2×2 nodal at the floating star point, or use mesh.

Per-phase equivalent: one line-to-neutral source, one ZY, one line current. Multiply P by 3. Never put VL across ZY.

Line drop and a short feeder: if each line has impedance Zline, the balanced per-phase model is Vs_phase in series with Zline and ZY. Voltage regulation is the same single-phase calculation. Unbalanced line impedances plus unbalanced loads need three-phase circuit laws or, in power systems, sequence networks. This circuits unit stops at unequal Z loads on a balanced source, which already shows a floating-neutral shift and a Δ with unequal branch currents.

Phasor diagrams worth drawing: (1) VL triangle, VP from centroid to vertices for Y; (2) I_phase along each VP for a resistive Y; (3) I_L as VP minus neighbor currents for Δ. The 30° shift between VL and VP is visible as a side of the triangle versus a radius. Students who memorize “VL leads VP by 30°” without a sequence will get the lagging sequence wrong; draw abc counterclockwise or clockwise once and stick to it.

Power in unbalanced systems: P = Σ V_phase I_phase cosθ_k for four-wire Y, or Σ Re(V I*) on each branch of a Δ, plus line resistances if modeled. There is no single pf for an unbalanced load that is as meaningful as the balanced pf; one can define pf = P/S with S = Σ |Vk Ik| or with a vector S, and those differ. UG answers should compute total P and total |S| as specified, not invent a pf.

Two-wattmeter method: meters in lines A and B, voltage coils to line C (three-wire). W1 = Re(V_AC I_A*), W2 = Re(V_BC I_B*). Sum is total P for any three-wire load, balanced or not, because of Tellegen and I_A+I_B+I_C=0. For balanced loads the difference encodes Q. If pf is 0.5, one wattmeter reads zero; below that it reverses. That is a standard lab observation, not a broken meter.

Safety and grounding: the neutral of a Y source is often earthed. A four-wire system then has line-to-earth ≈ VP. A Δ source may be corner-earthed or floating. This is installation practice; the circuit model still needs a reference node. Do not short a line to earth in a homework schematic unless the problem is a fault (power pack).

Motors as balanced loads: a three-phase induction motor in a circuits course is a balanced Y or Δ of Z(s) at one slip. You are not asked for the torque-slip curve here; you are asked for IL and P. The same √3 VL IL cosθ formula applies. Starting current is larger because |Z| is smaller; that is a different Z, still balanced. Write sequence (abc or acb) on the phasor diagram before placing the 30° arrows, and state whether 415 V is VL.

## Equations

Balanced Y: \( V_L = \sqrt{3} V_P \), \( I_L = I_P \). Balanced Δ: \( V_L = V_P \), \( I_L = \sqrt{3} I_P \).

\( P = 3 V_P I_P \cos\theta = \sqrt{3} V_L I_L \cos\theta \). \( Q = \sqrt{3} V_L I_L \sin\theta \). \( S = \sqrt{3} V_L I_L \).

Δ–Y: \( Z_Y = Z_\Delta / 3 \).

Floating-neutral: \( \mathbf{V}_n = (\mathbf{V}_a Y_a + \mathbf{V}_b Y_b + \mathbf{V}_c Y_c)/(Y_a+Y_b+Y_c) \) relative to source neutral if the source is balanced Y.

Neutral current four-wire: \( \mathbf{I}_n = \mathbf{I}_a+\mathbf{I}_b+\mathbf{I}_c \).

## Methods

For balanced: convert Δ loads to Y, reduce to per-phase, solve I_P, reconstruct line currents 120° apart, compute P as 3 I^2 R. For unbalanced Δ: each branch current \( (V_{ab})/Z_{ab} \), then \( I_a = I_{ab} - I_{ca} \). For unbalanced four-wire Y: each \( I_k = V_k / Z_k \). For three-wire unbalanced Y: nodal at star point.

Draw a phasor diagram of line voltages as an equilateral triangle. Put phase voltages inside for Y. Check that a balanced set sums to zero.

Design pf correction in three-phase with three capacitors in Δ (each sees VL) or Y (each sees VP). \( Q_C \) total as in single-phase, split three ways.

A balanced numerical ritual: (1) convert the load to Y if needed, (2) VP = VL/√3, (3) IP = VP/ZY, (4) IL = IP for Y, (5) P = 3 IP² R, (6) Q = 3 IP² X, (7) check √3 VL IL cosθ. If step 5 and step 7 disagree, the 30° mix-up happened. For unbalanced Δ, never use the √3 IL formula; compute each branch, then each line as a difference. For floating-neutral Y, compute Vn first, then each (Vk − Vn)/Zk. A sanity check: if two phases are equal Z and the third is open on three-wire, the two live phases share a series path across one line voltage, so |Ia| = |VL/(Za+Zb)|, not VP/Za. That is Q5’s lesson in slogan form.

## Mistakes

Using \( P = 3 V_L I_L \cos\theta \). Putting line voltage across a Y phase impedance. Assuming In = 0 when the load is unbalanced four-wire. Using the 30° shift with the wrong sequence. Adding three wattmeter readings that already include a factor. Converting ZΔ to ZY as 3Z instead of Z/3. Treating unbalanced three-wire Y as three independent phases. Mixing peak and RMS in √3. Using single-phase pf-correction C on a line-to-line voltage with a formula that assumed phase voltage. Drawing abc as 90° apart. Using VP = √3 VL. Placing a single-phase wattmeter’s current coil in a line and its voltage coil line-to-neutral and calling that the total three-phase power (it is one phase of a four-wire Y only). Assuming a Δ motor’s nameplate 415 V means VP = 415/√3 when the windings are Δ (they see 415 V). Forgetting that In in a four-wire unbalanced Y is a phasor sum, not a scalar sum of RMS currents. Using P = 3 VL IP. Designing pf-correction capacitors in Y but sizing them with VL in V². A worked caution: a 3-wire motor with a blown fuse in one line is no longer balanced; the remaining two lines and the motor’s internal Δ or Y need a new circuit model, not the √3 formula. That is an unbalanced problem, and using the balanced P formula understates the line current in the surviving phases. Also, “415 V three-phase” in India is line-to-line unless a problem explicitly says phase. Write VL or VP on every number. Neutral current is not “the leftover RMS”; it is the closing phasor of the three line currents and can exceed a line current in a badly unbalanced four-wire feeder. Draw that closing triangle before trusting a scalar guess. Label each line current with both magnitude and angle so the vector sum for In is a real calculation, not an RMS add of three scalars. RMS addition would hide cancellation completely.
