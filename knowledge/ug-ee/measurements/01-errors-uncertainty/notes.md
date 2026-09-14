# Gross, systematic, and random error; limiting error

A measurement is a comparison of an unknown quantity against a standard. The number on a meter is not the true value: it is an estimate, and the job of this unit is to say how far that estimate may lie from the truth and how errors combine when you add, multiply, or take ratios. Undergraduate electrical measurements treat three classical buckets (gross, systematic, random), the instrument-class idea of limiting error, and the first statistical language (mean, standard deviation, probable error) used in a lab notebook. Later units put these ideas onto bridges, analog instruments, instrument transformers, digital meters, transducers, and magnetic calibration. Nothing here replaces a full metrology course: the GUM Type A/Type B split is mentioned so you can read a calibration certificate, not so you become a metrologist.

## Concepts

Error is \( \delta A = A_m - A_t \), measured minus true. Relative error is \( \delta A / A_t \), often as a percent of reading. Correction is \( -\delta A \): you add the correction to the reading to recover an estimate of the true value. If a voltmeter reads 101.2 V and a standard says 100.0 V, the error is \( +1.2 \) V and the correction is \( -1.2 \) V. Mixing the sign of correction is the most common arithmetic bug in a lab report.

Gross errors are human or procedural disasters: misreading a scale, using the wrong range, a loose banana plug, recording 7.3 when the needle is at 3.7, forgetting a CT ratio. They are not modelled; they are prevented by procedure (two observers, a checklist, a photograph of the setup, a sanity bound from KCL or rated power). If a result is physically impossible (efficiency 140%, a CT secondary open while the primary carries load), treat it as gross until proven otherwise.

Systematic errors are repeatable biases. They have a sign. Instrument calibration offset, a meter whose spring has taken a set, thermoelectric EMFs in DC millivolt work, a shunt that runs hot and changes resistance, loading of a high-impedance node by a 20 kΩ/V voltmeter, frequency error of a moving-iron meter on a non-sinusoid, the ratio and phase errors of a CT — all systematic. You reduce them by calibration, by a better instrument, by a null method, by reversing leads (to cancel thermal EMFs), or by computing a loading correction. You do not reduce them by repeating the same biased measurement ten times and averaging: the average of a biased set is still biased.

Random errors scatter from reading to reading with no preferred sign: observer parallax on an analog scale, quantization dither, thermal noise, slight contact resistance, supply flicker. They are described statistically. The arithmetic mean of \( n \) repeated observations is the usual estimate of the centre. The sample standard deviation \( s \) estimates the scatter. For a Gaussian cloud, about 68% of readings lie within \( \pm s \) of the mean and about 95% within \( \pm 2s \). Probable error is the half-width of the 50% interval, \( 0.6745\,s \) for a normal law — a classical exam phrase, less used in modern certificates. Repeating and averaging reduces the standard uncertainty of the mean as \( s/\sqrt{n} \), not as \( s/n \).

Accuracy is closeness to the true value (small systematic plus small random). Precision is tightness of repeats (small random), even if all repeats sit 3% high. Resolution is the smallest change the instrument can indicate (a digit, a fraction of a scale division). Sensitivity is \( \mathrm{d}(\text{output})/\mathrm{d}(\text{measurand}) \); a galvanometer may be very sensitive and still inaccurate if its scale factor is wrong. Threshold (or dead band) is the smallest change that produces any detectable output. Span is full-scale minus zero. Linearity error is the maximum deviation from a straight calibration line, usually as a percent of span. Hysteresis is the difference between up-scale and down-scale readings at the same measurand.

Limiting error (guarantee error, maximum possible error) is the manufacturer’s worst-case bound, not a standard deviation. An analog instrument of class index \( K \) has limiting error \( K \) percent of full-scale deflection (FSD), not of the reading, unless the data sheet says otherwise. A 0–100 V class 1.0 meter may be wrong by 1 V anywhere on the scale; at a 20 V reading that is 5% of reading. Digital multimeters usually quote \( \pm(a\%\text{ of reading} + b\text{ digits} + c\%\text{ of range}) \). Always convert both terms to volts (or amperes) before adding, then convert the sum to a percent of the actual reading if the problem asks for relative limiting error.

When a result \( y = f(x_1,x_2,\ldots) \) is computed from several measurements, limiting errors combine by a first-order worst-case expansion: \( \Delta y \approx \sum |\partial f/\partial x_i|\,\Delta x_i \). For a sum or difference, absolute limiting errors add. For a product or quotient, relative limiting errors add. For \( y = k x^n \), the relative limiting error is \( |n| \) times that of \( x \). This is conservative: it assumes every error takes the sign that hurts \( y \). A statistical (RSS) combination \( \sqrt{\sum (\partial f/\partial x_i)^2 u_i^2} \) is tighter and is what a GUM uncertainty budget uses; UG exams usually want the conservative limiting-error form unless they say “standard uncertainty” or “r.m.s.”.

Loading is a systematic effect you can calculate. A voltmeter of resistance \( R_m \) across a Thevenin pair \( (V_{th},R_{th}) \) reads \( V_{th} R_m/(R_{th}+R_m) \). The relative loading error is about \( -R_{th}/R_m \) when \( R_m\gg R_{th} \). An ammeter of resistance \( R_a \) in a loop of resistance \( R \) reduces the current by about \( R_a/R \). A 20 kΩ/V meter on the 10 V range has \( R_m = 200\,\mathrm{k}\Omega \); on the 50 V range it is 1 MΩ — the same movement, a different multiplier, a different loading error. Specify the range, not only the class.

Significant figures and rounding: a class-1 analog reading of 83 V on a 100 V scale does not deserve four digits. Report the reading, the range, the class, and the computed limiting error. Do not round intermediate error arithmetic to one digit and then claim a precise percent.

Static versus dynamic error: a meter with finite damping lags a changing quantity. True-RMS versus average-responding-calibrated-RMS: an average-responding meter scaled for a sine wave reads low on a square wave and high on a peaked waveform (form-factor error). Frequency response of a moving-iron or electrodynamometer instrument is another systematic story, treated in the instrument units.

Standards: a working instrument is compared with a laboratory standard, itself compared with a reference, itself traceable toward a national standard. Traceability is a documented chain with uncertainties, not a sticker that says “calibrated.” Unit 07 returns to the chain for magnetic quantities. Here it is enough that “true value” in a student lab is the value assigned by a better instrument or a standard cell / standard resistor, not a metaphysical constant.

Type A evaluation of uncertainty is statistical analysis of repeated observations. Type B is everything else: a manufacturer’s spec, a previous calibration, a handbook tolerance, a rectangular distribution from a digital resolution of one count. Combined standard uncertainty is RSS of the components; expanded uncertainty multiplies by a coverage factor \( k \) (often 2 for ~95%). UG problems that give only a class index want limiting error, not a GUM budget. Do not invent a \( k \) if the problem never mentioned confidence.

## Equations

Absolute and relative error:

\[
\delta A = A_m - A_t,\qquad \varepsilon = \frac{\delta A}{A_t},\qquad \text{correction} = -\delta A.
\]

Limiting error of an analog instrument of class \( K \) (percent of FSD):

\[
\Delta A = \frac{K}{100}\,A_{\mathrm{FSD}},\qquad
\varepsilon_{\mathrm{reading}} = \frac{\Delta A}{A_m}.
\]

Combination for \( y=f(x,z) \):

\[
\Delta y \approx \left|\frac{\partial f}{\partial x}\right|\Delta x + \left|\frac{\partial f}{\partial z}\right|\Delta z.
\]

Sum/difference: \( \Delta(x\pm z)=\Delta x+\Delta z \). Product/quotient: \( \Delta y/|y| = \Delta x/|x| + \Delta z/|z| \). Power: \( \Delta(x^n)/|x^n| = |n|\,\Delta x/|x| \).

Sample mean and sample standard deviation of \( n \) repeats \( A_i \):

\[
\bar A = \frac{1}{n}\sum_i A_i,\qquad
s = \sqrt{\frac{1}{n-1}\sum_i (A_i-\bar A)^2}.
\]

Standard uncertainty of the mean (Type A): \( u_A = s/\sqrt{n} \). Probable error of a single observation (Gaussian): \( r = 0.6745\,s \).

Voltmeter loading:

\[
V_{\mathrm{read}} = V_{th}\frac{R_m}{R_{th}+R_m},\qquad
\varepsilon_{\mathrm{load}} \approx -\frac{R_{th}}{R_m}\quad (R_m\gg R_{th}).
\]

DMM-style bound (convert digits to the unit of the range first):

\[
\Delta V = \frac{a}{100}V_{\mathrm{read}} + N_{\mathrm{digits}}\times(\text{value of 1 digit}) + \frac{c}{100}V_{\mathrm{range}}.
\]

RSS (only when the problem asks for statistical combination):

\[
u_c(y) = \sqrt{\sum_i \left(\frac{\partial f}{\partial x_i}\right)^2 u^2(x_i)}.
\]

## Methods

Write the true-value equation first, then substitute measured symbols, then differentiate, then put absolute values on every term if you are doing limiting error. For \( P=VI \) that is one line: \( \Delta P/P = \Delta V/V+\Delta I/I \). For \( R=V/I \) the same relative sum. For \( Q=V^2/R \) you get \( 2\Delta V/V+\Delta R/R \). Check dimensions: every term in a relative-error sum is dimensionless.

For an analog meter, convert class to an absolute error using FSD, then divide by the actual reading if a percent-of-reading is required. Never apply the class percent directly to the reading unless the manufacturer explicitly uses percent-of-reading (some digital and some laboratory instruments do).

When two instruments contribute (a wattmeter current coil and a voltmeter, or two resistors in a computed equivalent), convert each limiting error to the same form (all absolute, or all relative in the derived quantity) before adding. Mixing “1% of FSD” with “2% of reading” without converting is undefined.

For repeated observations: discard a gross outlier only with a stated rule (it failed a sanity check, a connection was found loose). Then compute \( \bar A \) and \( s \). If the problem asks for the limiting error of the mean and gives only a class index, the class still governs: averaging does not shrink a systematic bound. If it asks for the standard error of the mean, use \( s/\sqrt{n} \).

Loading correction: compute \( R_m \) from ohms-per-volt times range, then \( V_{th}=V_{\mathrm{read}}(R_{th}+R_m)/R_m \). Report both the raw reading and the corrected value.

To combine a calibration correction with a random scatter: apply the correction first (remove the known systematic), then treat the residual as random. Do not RSS a known bias with \( s \); correct the bias.

Sanity: a 3½-digit DMM on a 20 V range has resolution 10 mV; quoting 12.3456 V is theatre. A class 0.5, 100 V meter cannot support a 0.01 V argument.

When a problem gives tolerances of components (resistors \( \pm 1\% \)) and asks for limiting error of a computed current, treat those tolerances as limiting errors of the parameters, not as standard deviations, unless it says “standard uncertainty” or gives a distribution.

## Mistakes

Applying class index to the reading instead of FSD on an analog instrument.

Adding relative errors of a sum (use absolute errors for \( x+z \)) or adding absolute errors of a product (use relative).

Averaging to “cancel” a calibration offset.

Forgetting that \( \Delta(x-z) \) is still \( \Delta x+\Delta z \): differences are worse, not better, when \( x\approx z \) (two close voltages subtracted to get a small drop).

Using \( n \) rather than \( n-1 \) in \( s \) is a minor UG issue; using \( s \) as if it were the error of the mean, without \( /\sqrt{n} \), is the real one — or the reverse, dividing a systematic class error by \( \sqrt{n} \).

Loading: quoting \( R_m \) from the 1000 V range while you were on the 10 V range.

Sign of correction versus error.

Reporting probable error, standard deviation, and limiting error as if they were interchangeable words.

Ignoring the “digits” term on a DMM so that a reading of 0.5 V on a 200 V range looks accurate.

Treating a single-shot reading as a Type A evaluation because you wrote \( \pm 1 \) in the last digit: that last digit is Type B (resolution), rectangular, unless you actually repeated the measurement.

Confusing resolution with accuracy: a 6½-digit meter that has not been calibrated in five years can be precise and wrong.

Using RSS in a “limiting error” question, or worst-case addition in a “standard uncertainty” question.

Forgetting to convert all quantities to SI before forming \( \varepsilon \): mixing mA and A in \( P=VI \) is a factor-of-thousand error that no class index will save.

Claiming an efficiency greater than one because energy-meter and wattmeter errors were allowed to stack without a sanity bound.

Writing \( \pm K\% \) on a graph axis without stating of FSD or of reading.

Taking the relative error of a resistor colour-code tolerance as if it applied to a measured resistance from a bridge that is ten times better: the measurement can beat the component tolerance; the reverse is also common (a cheap DMM measuring a 0.01% standard).

A worked pattern that should be muscle memory: \( R_1=100\,\Omega\pm 0.5\% \), \( R_2=200\,\Omega\pm 1\% \), series equivalent. \( R=300\,\Omega \), \( \Delta R = 0.005\times 100 + 0.01\times 200 = 2.5\,\Omega \), relative \( 2.5/300 \approx 0.833\% \). Parallel: \( R=200/3\,\Omega \), relative limiting error \( \Delta R/R = \Delta R_1/R_1\cdot(R/R_1) + \Delta R_2/R_2\cdot(R/R_2) \) from the derivative of \( R=R_1R_2/(R_1+R_2) \), which is not the sum of the two relative errors. Compute the partials; do not guess.

Another pattern: wattmeter reading \( P=VI\cos\phi \). Relative limiting error \( \Delta P/P = \Delta V/V+\Delta I/I+\Delta(\cos\phi)/\cos\phi \). The last term is large at low power factor: a 1% error in \( \phi \) near 90° wrecks \( P \). That is why low-PF wattmeters exist (unit 03) and why you do not claim 1% energy at 0.2 lag from an ordinary dynamometer.

A third pattern: five voltage readings 50.1, 50.4, 49.8, 50.0, 50.2 V. Mean 50.10 V. Deviations \( +0.00,+0.30,-0.30,-0.10,+0.10 \). Sum of squares 0.20. \( s=\sqrt{0.20/4}=\sqrt{0.05}\approx 0.224 \) V. Standard error of the mean \( 0.224/\sqrt{5}\approx 0.100 \) V. If the meter is class 0.5 on 100 V FSD, the systematic bound is 0.5 V, which dominates \( u_A \). Report both; do not hide the class behind the scatter.
