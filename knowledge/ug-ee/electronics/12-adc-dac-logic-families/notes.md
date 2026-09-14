# DAC, ADC, and TTL/CMOS logic families

Connecting the analog world to bits needs converters; connecting chips to each other needs agreed voltage levels, currents, and timing. This unit covers DAC architectures and the LSB arithmetic, ADC types that UG exams actually name (flash, SAR, dual-slope, sigma-delta at a cartoon level), sampling notes that overlap the signals pack, and the TTL vs CMOS level, loading, and interconnection rules.

## Concepts

A DAC maps an \(N\)-bit digital word to an analog voltage or current. Resolution: 1 LSB \(= V_{\mathrm{FS}}/2^N\) (or \(V_{\mathrm{FS}}/(2^N-1)\) if the full-scale is the all-1s voltage — read the problem). Offset error: output at code 0. Gain error: slope error. INL: deviation of each code's midpoint from the straight line. DNL: step size minus 1 LSB; DNL \(<-1\) LSB means a missing code. Monotonicity: output never decreases as the code increases; guaranteed if DNL \(>-1\) LSB.

Architectures. Weighted-resistor: \(N\) switches, resistors \(R,2R,4R,\ldots\). Fast in principle, unbuildable at 12 bits because \(2^{N-1}R\) and analog switch resistance wreck the ratios. R-2R ladder: only two values, truncated at each bit by a 2R to ground and R to the next node; the Thevenin at the MSB is \(V_{\mathrm{ref}}/2\), etc. Current-steering (weighted current sources) is the high-speed bipolar/CMOS choice. Charge-redistribution capacitor DACs dominate SAR ADCs. PWM plus a low-pass filter is a cheap DAC (class-D's cousin).

An ADC maps a voltage to a code. Quantisation error \(\pm\frac12\) LSB if we round to nearest; RMS about \(V_{\mathrm{LSB}}/\sqrt{12}\). SNR of an ideal full-scale sine is \(6.02N+1.76\) dB. Sampling: Nyquist \(f_s>2f_{\max}\), anti-alias filter in front. Aperture jitter smears high-frequency samples.

Flash ADC: \(2^N-1\) comparators, resistor string, thermometer code, then a priority encoder. Fast, hungry, used above a few hundred megahertz at 6–8 bits. SAR: binary search with one comparator, a DAC, and \(N\) cycles. The UG workhorse for 12-bit microcontroller pins. Dual-slope: integrate the input for a fixed \(T\), then de-integrate a reference; the de-integrate time is proportional to \(V_{in}\). Excellent rejection of line-frequency interference if \(T\) is a line period; slow; classic DMM front-end. Pipeline ADC: cascaded low-resolution stages (mentioned). Sigma-delta: oversampling plus a loop that shapes quantisation noise out of band, then a digital decimator. UG depth: block diagram and the words "oversampling" and "noise shaping", not loop-filter design.

Reference. Every converter is only as good as \(V_{\mathrm{ref}}\). A ratiometric connection (sensor and ADC sharing the same \(V_{\mathrm{ref}}\)) cancels first-order reference drift.

Logic families. TTL (74xx, 74LS, 74ALS, 74F): bipolar, classic 5 V, input is an emitter (or PNP) that sources current when low. Levels (standard TTL): \(V_{IL,\max}=0.8\,\mathrm{V}\), \(V_{IH,\min}=2.0\,\mathrm{V}\), \(V_{OL,\max}=0.4\,\mathrm{V}\), \(V_{OH,\min}=2.4\,\mathrm{V}\). Noise margins \(NM_L=0.4\,\mathrm{V}\), \(NM_H=0.4\,\mathrm{V}\). Fan-out: \(I_{OL}/I_{IL}\) (low is usually the limiter, 16 for 74, 20 for LS). Totem-pole output must not be tied together; open-collector + pull-up is the wired-AND.

CMOS (4000, 74HC, 74HCT, 74AC, 74AHC, 74LVC): MOSFET gates, rail-to-rail outputs, \(V_{OH}\approx V_{CC}\), \(V_{OL}\approx 0\), thresholds near \(V_{CC}/2\) for HC (not TTL-compatible). 74HCT is CMOS with TTL-compatible input thresholds for mixing with LS. Static current near zero; dynamic \(P=f C V^2\). Unused inputs must be tied (not left floating — a floating CMOS gate is an analog amplifier of noise). 4000 series is slow and 3–15 V; HC is 2–6 V.

Interfacing. TTL → CMOS HC at 5 V: \(V_{OH,TTL}=2.4\,\mathrm{V}\) is not a legal HC high (needs \(\approx 3.5\,\mathrm{V}\)). Pull-up, or use HCT, or a dedicated translator. CMOS HC → TTL: usually OK at 5 V because HC \(V_{OH}\) is nearly 5 V and \(I_{OH}\) is enough for a few LS loads; check \(I_{OL}\). 3.3 V CMOS ↔ 5 V: need a translator or 5 V-tolerant pins. Mixing families without reading \(V_{IH}/V_{OH}\) is the most common lab failure in this unit.

Open-collector / open-drain: wire-AND (active-low OR). Pull-up \(R\) sized for rise time \(0.69 R C_{bus}\) vs \(I_{OL}\) sink when low. Schmitt-input gates clean up slow edges.

Resolution vs accuracy. A 16-bit ADC with 50 mV of offset is a very fine, very wrong meter. Calibration (offset/gain trims, or a system two-point cal) is how instruments become accurate; resolution is free from \(N\) once the analog front-end is quiet enough. Effective number of bits (ENOB) from an SNR measurement is the honest \(N\). UG problems that give only \(N\) and \(V_{\mathrm{ref}}\) want the ideal LSB, not ENOB.

Successive-approximation walk-through (keep the table on paper). Start with MSB=1, others 0. If the DAC output is above \(V_{in}\), clear the MSB; else keep it. Repeat for bit \(N-2\) down to 0. After \(N\) steps the register is the code. The DAC must be monotonic. An extra sample clock at the front is not a conversion bit.

R-2R ladder analysis: starting at the LSB, each node sees 2R to the switch (to \(V_{\mathrm{ref}}\) or ground) and 2R equivalent to the right, so the Thevenin looking toward the LSB is \(R\) in series with \(V/2\) of the previous node. That is why bits weight \(1/2, 1/4, 1/8, \ldots\) with only two resistor values. Analog switch resistance in series with the 2R legs is the practical INL limiter unless the switches are at the ground side of a current-mode ladder.

## Equations

LSB and full-scale (straight binary unipolar, \(V_{\mathrm{FS}}\) at code \(2^N\)):

\[
V_{\mathrm{LSB}}=\frac{V_{\mathrm{ref}}}{2^N},\qquad V_{\mathrm{out}}=D\cdot V_{\mathrm{LSB}}.
\]

Quantisation SNR (full-scale sine, ideal):

\[
\mathrm{SNR}=6.02N+1.76\,\mathrm{dB}.
\]

Quantisation error bound (rounding): \(|e_q|\le V_{\mathrm{LSB}}/2\).

R-2R MSB weight: \(V_{\mathrm{ref}}/2\).

SAR cycles: \(N\) comparisons for \(N\) bits (plus a sample). Flash comparators: \(2^N-1\).

Dual-slope: \(V_{in}=V_{\mathrm{ref}} T_{\mathrm{deint}}/T_{\mathrm{int}}\).

TTL fan-out (low):

\[
N_L=\left\lfloor\frac{I_{OL,\max}}{I_{IL}}\right\rfloor.
\]

Noise margins:

\[
NM_H=V_{OH,\min}-V_{IH,\min},\qquad NM_L=V_{IL,\max}-V_{OL,\max}.
\]

CMOS dynamic power (single rail, load \(C\)):

\[
P_{\mathrm{dyn}}=f C V_{CC}^2.
\]

## Methods

1. DAC code to voltage: convert the binary to decimal \(D\), multiply by \(V_{\mathrm{LSB}}\). Watch whether all-1s is \(V_{\mathrm{ref}}(1-2^{-N})\) or \(V_{\mathrm{ref}}\).
2. ADC: divide \(V_{in}\) by \(V_{\mathrm{LSB}}\), round to nearest (or truncate, if the problem says so), clamp to \(0..2^N-1\).
3. Error budget: add offset, gain, INL as the problem states; do not invent DNL if only INL is given.
4. Family mixing: write both sides' \(V_{OH,\min}\) vs \(V_{IH,\min}\) and \(V_{OL,\max}\) vs \(V_{IL,\max}\), then currents. If a voltage test fails, name the translator.
5. Fan-out: compute high and low separately; take the min. Include the pull-up current of open-collectors in the low budget.
6. Unused CMOS inputs: tie to \(V_{CC}\) or GND (through a resistor if the lab is nervous). Unused TTL inputs float high *in theory* and fail in practice — tie them too.

## Mistakes

- Off-by-one full-scale: using \(2^N-1\) in the denominator when the datasheet uses \(2^N\), or the reverse. The difference is 1 LSB at full scale.
- Flash ADC: \(2^N\) comparators. It is \(2^N-1\).
- SAR: claiming \(2^N\) cycles. It is \(N\) (binary search).
- Dual-slope: forgetting that line-frequency rejection needs \(T_{\mathrm{int}}=k/f_{\mathrm{line}}\).
- SNR formula applied to a DC input. The 1.76 dB is for a full-scale sine.
- TTL fan-out computed from voltages instead of currents.
- Driving 74HC inputs with 74LS outputs at 5 V without a pull-up or HCT. \(V_{OH}=2.4\,\mathrm{V}\) vs \(V_{IH}=3.5\,\mathrm{V}\).
- Floating CMOS inputs on a board that "worked on the bench" and fails later. The input is oscillating in the linear region and cooking the part.
- Wired-AND of totem-pole outputs. That is contention, not open-collector.
- Assuming 3.3 V LVCMOS can swallow 5 V. Many parts are *not* 5 V tolerant.

Sample-and-hold in front of a SAR: acquire for \(t_{acq}\), then hold while the binary search runs. Droop \(dv/dt=I_{leak}/C\) must stay well under 1/2 LSB during the conversion. A 10 nA leak on 1 nF is 10 V/s, which is 10 mV in 1 ms — several LSBs of a 12-bit 5 V ADC. That is why SH capacitors are not random ceramics with huge leakage, and why conversion time is in the datasheet budget.

Missing codes vs non-monotonic DACs. A DAC that steps backward for an increasing code is a disaster in a SAR feedback loop (the search can hang). INL can be large while DNL stays \(>-1\) LSB (bowed but monotonic). Specsmanship: always read DNL if you care about missing codes.

Logic thresholds vs analog. A TTL input between 0.8 V and 2.0 V is *undefined*, not "kinda high". Do not operate there except during a fast edge. Slow edges on TTL inputs cause oscillation and extra \(I_{CC}\); use a Schmitt-trigger input (74LS14). CMOS HC has a wide analog region around \(V_{CC}/2\) where both MOSFETs conduct; a floating or slow input heats the package.

Converters are scaled references plus a search; logic families are voltage-and-current contracts. Write the contract numbers before you write the schematic. If two families disagree on a volt, that is not a "maybe"; it is a translator or a different part. Dual-slope DMMs still beat cheap SAR parts on 50 Hz rejection when \(T_{\mathrm{int}}\) is 20 ms or 40 ms; that is why bench meters are slow and quiet. Flash ADC bubble errors in the thermometer code are why the encoder is a priority encoder, not a naive binary adder of ones. Gray-code flash encoders exist specifically to make a single bubble a one-LSB error instead of a wild-code jump on the binary output.
