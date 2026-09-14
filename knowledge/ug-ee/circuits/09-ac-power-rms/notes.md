# RMS, average and complex power, power factor

AC power is not a single number. Instantaneous power \( p(t) = v(t)i(t) \) pulsates. Average (active) power \( P \) is the DC term of that pulsation and is what does work and what a watthour meter accumulates. Reactive power \( Q \) measures the amplitude of the oscillating energy exchange with L and C. Apparent power \( |S| \) is the product of RMS voltage and current, the sizing quantity for wires and transformers. Power factor is \( P/|S| \). This unit is mandatory in every UG EE programme in the curriculum map.

## Concepts

RMS of a periodic signal is \( X_\mathrm{rms} = \sqrt{\frac1T \int_0^T x^2 dt} \). For a sinusoid of peak \( X_m \), \( X_\mathrm{rms} = X_m/\sqrt{2} \). Average of a sinusoid is zero; average of a rectified sinusoid is \( 2X_m/\pi \). Do not confuse RMS, average, and peak. Heating in a resistor is \( I_\mathrm{rms}^2 R \), which is why RMS is the default AC meter quantity.

In sinusoidal steady state, \( P = V_\mathrm{rms} I_\mathrm{rms} \cos\theta \) where \( \theta = \phi_v - \phi_i \) is the angle of the impedance. \( \cos\theta \) is the power factor, lagging if current lags voltage (inductive), leading if current leads (capacitive). \( Q = V_\mathrm{rms} I_\mathrm{rms} \sin\theta \), positive by the IEEE load convention when the load is inductive (absorbs Q, vars). Complex power \( \mathbf{S} = P + jQ = \mathbf{V}_\mathrm{rms} \mathbf{I}_\mathrm{rms}^* = \frac12 \mathbf{V}_\mathrm{peak} \mathbf{I}_\mathrm{peak}^* \). Apparent power \( S = |S| = V_\mathrm{rms} I_\mathrm{rms} \). Units: W, var, VA. They are dimensionally identical; the names keep engineers from adding them as scalars.

Conservation: complex power balances in a network (Tellegen). Sum of P over all elements is zero (sources vs absorbers). Sum of Q likewise. You may therefore compute load P and Q and infer source S.

Power factor correction: a lagging load draws Q that can be cancelled by a shunt capacitor so that the source current shrinks while P stays the same. The capacitor is sized from \( Q_C = P(\tan\theta_\mathrm{old} - \tan\theta_\mathrm{new}) \). Industrial tariffs penalize low pf; correction is economic, not cosmetic. Overcorrection (leading) can raise voltage on light feeders and is also penalized sometimes.

Instantaneous power: \( p(t) = P + P\cos(2\omega t) + Q\sin(2\omega t) \) in the usual expansion, or \( p = VI\cos\theta + VI\cos(2\omega t+\cdots) \). The double-frequency ripple is why DC links and three-phase (constant instantaneous power when balanced) exist.

Maximum power transfer in AC: \( Z_L = Z_\mathrm{Th}^* \). Then \( P_\mathrm{max} = |V_\mathrm{Th}|^2 / (8 R_\mathrm{Th}) \) for peak phasors, or \( |V_\mathrm{Th,rms}|^2/(4 R_\mathrm{Th}) \). Efficiency is still 50% at the match.

Non-sinusoidal periodic waves: RMS still from the integral; average power is the sum of harmonic powers if v and i are expanded in Fourier series (no cross-frequency average power). UG circuits courses mention this; signals courses develop it.

Meters: a true-RMS meter computes the integral definition, good for sines and many distorted waves. An averaging meter scaled to RMS for a sine (the cheap “RMS” analog movement) lies on triangles and triacs. A wattmeter measures average p(t), hence P, not S. VA is computed from separate Vrms and Irms. A varmeter is a wattmeter with a 90° phase shift in the voltage coil. Power-factor meters exist; at UG it is safer to compute pf from P/S. In three-phase, two-wattmeter readings can each be negative depending on pf; the algebraic sum is still P.

Sign of Q and the generator/load conventions: this corpus uses the load (consumer) convention at a pair of terminals with PSC. Positive P into the load is consumption. Positive Q into the load is inductive vars absorbed (magnetic energy cycling). A capacitor load then has Q negative, i.e. it supplies vars. Generator convention at a source often quotes delivered P as positive; then you have flipped the current. State the convention in the answer if the sign of source power is requested.

Power factor correction worked as economics: a 0.7 lag plant drawing 100 kW at 415 V three-phase (numbers belong in the three-phase unit, but the single-phase analog is the same) pays for current in cables and transformers sized on S = P/pf. Raising pf to 0.95 cuts S, hence I, hence I²R losses and maybe the tariff. The capacitor bank is sized on Q, not on P. If the load varies, a fixed bank is right at one operating point and too strong at light load, producing a leading pf and a voltage rise. Automatic steps or a static var system appear in power-system electives; here, compute one C for one P.

Complex S in rectangular form adds for parallel loads: S_total = Σ Sk. That is the fastest way to combine a motor and a heater and a capacitor. Polar form is for reading |S| and pf of the combination. Never add pf values. Never add angles of different loads without going through P and Q.

Energy: kilowatt-hours are the integral of P. Reactive “energy” in kvarh is billed by some utilities but is not work. Instantaneous energy in L and C still uses ½Li² and ½Cv² with instantaneous i and v; those oscillate at 2ω. Average stored energy in an inductor is ½ L I_peak² / 2 = ½ L Irms².

For a purely reactive load P = 0, yet the wires still carry Irms = V/X and have I²R loss if the wires are modeled. An ideal lossless LC has S purely imaginary at the port and zero average P, consistent with Tellegen. Always box P, Q, S, and pf together so a later three-phase problem can reuse the triangle without re-deriving θ.

## Equations

\( V_\mathrm{rms} = V_m/\sqrt{2} \) (sine). \( P = \frac12 V_m I_m \cos\theta = V_\mathrm{rms} I_\mathrm{rms} \cos\theta \).

\( \mathbf{S} = \mathbf{V}_\mathrm{rms}\mathbf{I}_\mathrm{rms}^* = P + jQ \). \( \mathrm{pf} = \cos\theta = P/S \).

\( Q = I_\mathrm{rms}^2 X = V_\mathrm{rms}^2 / X \) with signs from X. Capacitor \( Q_C = -\omega C V_\mathrm{rms}^2 \) (load convention: capacitor generates Q, so the load's absorbed Q decreases).

pf correction: \( C = \dfrac{Q_C}{\omega V^2} \) with \( Q_C = P(\tan\theta_1 - \tan\theta_2) \).

Resistor: \( S = P \), \( Q = 0 \). Inductor: \( P = 0 \), \( Q = I^2 \omega L \). Capacitor: \( P = 0 \), \( Q = -I^2 /(\omega C) \).

Triangle: \( S^2 = P^2 + Q^2 \).

## Methods

Convert all voltages and currents to RMS phasors. Compute \( \mathbf{S} = \mathbf{V}\mathbf{I}^* \) at the load terminals (V and I associated with PSC). Split P and Q. For a source, reverse the current arrow or take \( -\mathbf{V}\mathbf{I}^* \) if PSC was drawn on the source as a load. For pf correction, keep P fixed, compute new Q, difference is the capacitor (or inductor) Q, then C from \( Q = \omega C V^2 \).

If only magnitudes and pf are given, reconstruct the complex current: \( \mathbf{I} = (P - jQ)/V^* \) or \( I = P/(V\,\mathrm{pf}) \) at angle \( \mp \cos^{-1}(\mathrm{pf}) \).

Check: passive network P ≥ 0 at the load, |pf| ≤ 1, S ≥ |P|. Capacitor current leads voltage by 90°, so its Q is negative in the load convention.

A numerical habit: tabulate each element’s S = P + jQ, add the table, compare to the port S. Resistors contribute only P, L only +Q, C only −Q, sources whatever the signs say. If a row is missing, Tellegen will not close. For pf correction, draw the power triangle before and after: same P, shorter Q, shorter hypotenuse S, smaller I. The capacitor’s S is 0 − j QC. If the utility also specifies a maximum leading pf, stop reducing Q before you cross zero by too much. When V is line-to-line in a later three-phase problem, do not reuse a single-phase C formula without converting to phase voltage or using three capacitors.

## Mistakes

Using peak in \( P = VI\cos\theta \) without the 1/2. Adding VA and W as if they were the same. Correcting pf by a series capacitor when the problem is a shunt industrial load (voltage would change). Forgetting \( \mathbf{I}^* \) and getting the wrong sign of Q. Treating a leading pf as inductive. Computing C from \( C = Q/\omega V \) missing V squared. Reporting pf as an angle. Using DC max-power match \( R_L = |Z_\mathrm{Th}| \) instead of conjugate. Averaging instantaneous power by sampling one peak. Mixing line-to-line and phase voltages in a three-phase preview. Assuming a wattmeter reads S rather than P. Using pf = P/Q. Correcting a load by a series capacitor when the voltage at the load must stay fixed (shunt correction keeps VL, series correction changes the divider). Forgetting that Q of a capacitor is −ωC V² with V the voltage actually across that capacitor, which is VP or VL depending on Y or Δ connection.
