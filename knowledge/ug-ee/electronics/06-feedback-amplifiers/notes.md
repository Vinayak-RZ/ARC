# Feedback amplifiers: four topologies and desensitivity

Negative feedback is the reason analog electronics is manufacturable. A gain of 200 000 that varies 3:1 over temperature and \(\beta\) is useless; a closed-loop gain of 10 that follows resistor ratios is the product. This unit classifies the four loop topologies, writes the loop-gain formulas, and tracks desensitivity, bandwidth, distortion, and the impedance transformations that each topology produces. Oscillators (positive feedback at one frequency) are the next unit.

## Concepts

A feedback amplifier samples the output, mixes a function of that sample with the input, and uses the difference (negative feedback) or the sum (positive) to drive the plant. Black's formula for the closed-loop gain of a single-loop system is \(A_f=A/(1+A\beta)\) where \(A\) is the open-loop (controlled-source) gain in the same units as \(A_f\), and \(\beta\) is the reverse transmission of the feedback network. The loop gain \(L=A\beta\) is dimensionless. If \(L\gg 1\), \(A_f\approx 1/\beta\), independent of the messy transistor gain.

Mixing and sampling can each be in series (voltage) or shunt (current), giving four topologies. The names describe *what is sampled at the output* and *how it is mixed at the input*:

1. Voltage-series (series-shunt): sample output voltage (shunt/parallel connection at the load), mix in series at the input. Transducer gain is a voltage gain \(A_v=v_o/v_s\). This is the noninverting op-amp and the emitter-follower (100 % voltage feedback). Input impedance rises, output impedance falls. The topology for voltage amplifiers that should look like a stiff voltage source.
2. Voltage-shunt (shunt-shunt): sample output voltage, mix as a current at a low-impedance input node. Transducer gain is a transresistance \(R_m=v_o/i_s\). Inverting op-amp, transimpedance photodiode amp. Both \(R_{in}\) and \(R_{out}\) fall.
3. Current-series (series-series): sample output current (series connection in the load loop), mix in series at the input. Transducer gain is a transconductance \(G_m=i_o/v_s\). Emitter degeneration \(R_E\) in a CE stage is the canonical example. \(R_{in}\) rises, \(R_{out}\) rises (better current source).
4. Current-shunt (shunt-series): sample output current, mix as a current at the input. Transducer gain is a current gain \(A_i=i_o/i_s\). Less common at UG; a feedback current mirror or a collector-to-base resistor around a CE stage (approximately). \(R_{in}\) falls, \(R_{out}\) rises.

The practical skill is: look at the schematic. If the feedback network taps a node in parallel with the load, it is sampling voltage. If it sits in series with the load current (emitter resistor, current-sense resistor), it is sampling current. If the feedback returns to a node where it steals input current (inverting op-amp summing junction), mixing is shunt. If it returns in a loop that adds a voltage in series with the source (under the emitter, or under the op-amp's input), mixing is series.

Desensitivity. The fractional change \(dA_f/A_f=(1/(1+L)) dA/A\). The desensitivity factor \(D=1+L\) is the loop gain plus one. Distortion generated inside \(A\) is reduced by \(D\). Bandwidth of a dominant-pole \(A(s)=A_0/(1+s/\omega_p)\) stretches by about \(D\): the closed-loop pole is at \(\omega_p(1+A_0\beta)\). Gain-bandwidth product of a voltage-series op-amp loop is roughly constant.

Stability is the cost. Nyquist / Bode: if \(L(j\omega)\) encircles \(-1\), the closed loop oscillates. UG electronics courses state the Barkhausen borderline and demand phase margin in the op-amp compensation sense: a dominant pole (Miller capacitor) makes \(A(s)\) look like an integrator near unity loop gain so that the slope is \(-20\,\mathrm{dB/dec}\) and the phase margin is healthy. Multi-stage discrete amplifiers need the same care; two or three uncompensated poles and a large \(\beta\) will sing.

Loading. Textbook \(A\) is not the datasheet op-amp gain; it is the amplifier's gain *with the feedback network and source and load attached, but with the loop broken*. Break the loop at a series point, inject a test, include \(R_s\) and \(R_L\) and the \(\beta\)-network loading. Two-port (h, y, g, z) parameter methods exist for each topology; for UG, a careful circuit redraw plus hybrid-π usually beats memorising which parameter set goes with which topology.

Series-series \(R_E\) example, worth memorising because it appears in every midterm: CE stage, unbypassed \(R_E\), \(A=g_m\), \(\beta=R_E\) if we think in transconductance, or voltage gain \(A_v=-R_C/(1/g_m+R_E)\). The degeneration desensitises \(g_m\) and raises \(R_{in}\) by \((\beta_{BJT}+1)R_E\).

Voltage-series op-amp: \(\beta=R_1/(R_1+R_f)\), \(A_f=(1+R_f/R_1)\) in the large-loop-gain limit. That \(\beta\) is the reciprocal of the noise gain.

Return ratio vs loop gain: for ideal controlled sources they coincide. With two-way \(\beta\)-networks (resistive pads) there is a slight distinction (Bode's return ratio). UG marking almost always wants Black's formula with a stated \(A\) and \(\beta\).

Positive feedback is not always an oscillator. A Schmitt trigger uses \(L<-1\) at DC on purpose. A regenerative latch is the digital version. This unit stays with \(|1+L|>1\) and negative feedback at the frequencies of interest.

## Equations

Black:

\[
A_f=\frac{A}{1+A\beta}=\frac{A}{1+L},\qquad L=A\beta.
\]

Ideal closed-loop (large \(L\)):

\[
A_f\approx\frac{1}{\beta}.
\]

Desensitivity:

\[
\frac{dA_f}{A_f}=\frac{1}{1+L}\frac{dA}{A}.
\]

Dominant-pole bandwidth stretch:

\[
\omega_{cl}\approx\omega_p(1+A_0\beta).
\]

Impedance transformations (ideal sampling, large \(L\)):

| Topology | \(R_{in,f}\) | \(R_{out,f}\) |
|---|---|---|
| Voltage-series | \(R_{in}(1+L)\) | \(R_{out}/(1+L)\) |
| Voltage-shunt | \(R_{in}/(1+L)\) | \(R_{out}/(1+L)\) |
| Current-series | \(R_{in}(1+L)\) | \(R_{out}(1+L)\) |
| Current-shunt | \(R_{in}/(1+L)\) | \(R_{out}(1+L)\) |

CE with degeneration:

\[
A_v=\frac{v_c}{v_b}\approx -\frac{g_m R_C'}{1+g_m R_E},\qquad R_{ib}=r_\pi+(\beta+1)R_E.
\]

Inverting op-amp as voltage-shunt: \(A=v_o/i_b\) (transresistance of the naked op-amp plus \(R_f\) loading), \(\beta=1/R_f\), \(A_f\approx -R_f\) for current-to-voltage, or \(v_o/v_s\approx -R_f/R_1\) after \(i_s=v_s/R_1\).

## Methods

1. Identify sample and mix by connection, not by hope. Draw the load. Is the feedback network in parallel with it (voltage sample) or in series with its current (current sample)? Draw the input source. Does feedback add a voltage in series (series mix) or dump current at the input node (shunt mix)?
2. Write \(A\) in the units that match \(1/\beta\). If \(\beta\) is dimensionless, \(A\) is a voltage (or current) gain. If \(\beta\) is a conductance, \(A\) is a transresistance.
3. Include loading: compute \(A\) with the \(\beta\)-network attached as a load, loop broken (set the controlled feedback source to zero, keep the resistors).
4. Compute \(L=A\beta\), then \(A_f\), then the closed-loop impedances from the table.
5. For a numerical desensitivity question, logarithmic differentials: 20 % change in \(A\) becomes \(20/D\) % change in \(A_f\).
6. Stability sanity check: count poles of \(L(s)\) in the closed-loop bandwidth. One dominant pole is the UG happy case. If the problem gives a phase margin, require PM \(>45^\circ\) unless told otherwise.

## Mistakes

- Using \(A_f=A/(1+A\beta)\) with a \(\beta\) taken from the wrong topology (voltage divider on a current-sampled loop).
- Forgetting to include \(R_L\) and the \(\beta\)-network in \(A\). An unloaded \(A=200\) can drop to 50 once \(R_f\) loads the collector.
- Sign of \(\beta\): negative feedback means \(1+A\beta\) in the denominator with \(A\beta>0\) in the sign convention of this sheet. Mixing a minus from an inverting \(A\) into \(\beta\) and then another minus produces a positive-feedback formula by accident.
- Claiming \(R_{out}\) always falls. Current sampling raises \(R_{out}\). That is the point of a current source.
- Emitter follower: \(\beta_{fb}=1\), \(A_f\approx 1\), not "no feedback". It is 100 % voltage-series feedback.
- Desensitivity applied to the *resistors* in \(\beta\). Feedback does not desensitise \(\beta\); it *is* \(\beta\). If \(R_f\) drifts, \(A_f\) drifts.
- Loop gain in dB: \(L_{\mathrm{dB}}=20\log|A\beta|\). Adding dB of \(A\) and \(\beta\) is correct only when \(\beta\) is dimensionless; a transresistance \(\beta\) cannot be turned into dB without a reference.
- Stability: "more feedback is always better." More \(\beta\) also eats phase margin in a multi-pole plant.
- Identifying an inverting op-amp as voltage-series because "it is an op-amp voltage amplifier." Mixing is shunt; the input resistance is \(R_1\), not infinite.

Worked identification drill (keep doing this until it is boring). Emitter follower: output taken at the emitter, 100 % of \(v_o\) in series with the input loop → voltage-series, \(\beta=1\). CE with collector-to-base \(R_F\): \(R_F\) is in parallel with the output node and dumps current at the base → voltage-shunt. CE with \(R_E\) unbypassed and output at the collector: the quantity in the emitter is \(i_E\approx i_C\), mixed as a voltage \(i_E R_E\) in series with \(v_\pi\) → current-series. A transimpedance photodiode amp: current in, voltage out, shunt mix at the virtual ground, voltage sample at the output → voltage-shunt.

Distortion reduction is the same \(1/(1+L)\) factor only for distortion generated *inside* \(A\). Distortion from the feedback network (a nonlinear \(R_E\), a transformer) is not reduced. Noise at the input of \(A\) is *not* reduced; it is amplified by \(A_f\). Noise injected at the output is reduced. That is why we still care about the noise of the first transistor even in a high-loop-gain op-amp.

Return difference \(F=1+L\) is Bode's name for the desensitivity factor. Sensitivity of \(A_f\) to \(\beta\) is approximately unity when \(L\) is large: you *want* \(A_f\) to follow \(\beta\). Sensitivity to load \(R_L\) depends on topology: voltage sampling makes \(v_o\) stiff against \(R_L\); current sampling makes \(i_o\) stiff.

The four topologies are one idea drawn four ways. Name what you sample, name how you mix, write Black's formula in matching units, then check impedances against the table. If you cannot name the sampled quantity in one sentence, you are not ready to write \(A\) and \(\beta\). Write that sentence first, then the formula.
