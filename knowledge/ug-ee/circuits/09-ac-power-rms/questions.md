# Questions — RMS, average and complex power, pf

Original pedagogical numbers.

## Q1

### Given

Load voltage RMS phasor \( \mathbf{V} = 120\angle 0^\circ\,\mathrm{V} \), current \( \mathbf{I} = 4.5\angle -28^\circ\,\mathrm{A} \) (into the load plus).

### Find

P, Q, S, and pf (lag/lead).

### Solution

\( \mathbf{S} = \mathbf{V}\mathbf{I}^* = 120 \times 4.5\angle +28^\circ = 540\angle 28^\circ = 476.8 + j253.5 \). \( P = 477\,\mathrm{W} \), \( Q = 254\,\mathrm{var} \) (inductive), \( S = 540\,\mathrm{VA} \), \( \mathrm{pf} = \cos 28^\circ = 0.883 \) lagging.

### Answer

477 W, 254 var, 540 VA, pf 0.883 lagging.

## Q2

### Given

A 230 V RMS, 50 Hz source feeds a 4.8 kW load at 0.72 lagging pf.

### Find

Derive source current, Q, and the shunt C to raise pf to 0.95 lagging.

### Solution

\( I = P/(V\,\mathrm{pf}) = 4800/(230\times 0.72) = 28.99\,\mathrm{A} \). \( \theta_1 = \cos^{-1}0.72 = 43.95^\circ \), \( Q_1 = P\tan\theta_1 = 4800\times 0.965 = 4632\,\mathrm{var} \). \( \theta_2 = \cos^{-1}0.95 = 18.19^\circ \), \( Q_2 = 4800\tan 18.19^\circ = 1577\,\mathrm{var} \). \( Q_C = 4632-1577 = 3055\,\mathrm{var} \). \( C = Q_C/(\omega V^2) = 3055/(2\pi 50 \times 230^2) = 183.7\,\mu\mathrm{F} \). New current \( I' = 4800/(230\times 0.95) = 21.97\,\mathrm{A} \).

### Answer

\( I = 29.0\,\mathrm{A} \); \( Q = 4.63\,\mathrm{kvar} \); \( C = 184\,\mu\mathrm{F} \).

## Q3

### Given

Design a single-phase heater plus series reactor so that a 240 V RMS source delivers 1.50 kW at 0.85 lagging pf.

### Find

R and X.

### Solution

\( S = P/\mathrm{pf} = 1500/0.85 = 1765\,\mathrm{VA} \). \( I = S/V = 7.353\,\mathrm{A} \). \( Z = V/I = 32.64\,\Omega \), \( \theta = \cos^{-1}0.85 = 31.79^\circ \). \( R = 32.64\cos\theta = 27.74\,\Omega \), \( X = 32.64\sin\theta = 17.19\,\Omega \). Check \( P = I^2 R = 54.07\times 27.74 = 1500\,\mathrm{W} \).

### Answer

\( R = 27.7\,\Omega \), \( X_L = 17.2\,\Omega \).

## Q4

### Given

A student computes \( P = (18)(2.0)\cos 40^\circ \) using peak voltage 18 V and peak current 2.0 A.

### Find

Explain the missing factor and the correct P.

### Solution

Peak formula is \( P = \frac12 V_m I_m \cos\theta = 9\cos 40^\circ = 6.89\,\mathrm{W} \). The student reported 13.79 W, twice the average. RMS would be \( (18/\sqrt{2})(2/\sqrt{2})\cos 40 = \) same 6.89 W.

### Answer

Missing 1/2; \( P = 6.89\,\mathrm{W} \).

## Q5

### Given

\( v(t) = 10 + 8\cos 200t\,\mathrm{V} \) across a 5.0 Ω resistor.

### Find

RMS voltage, average power, and whether a DC plus AC average-power formula may superpose.

### Solution

\( V_\mathrm{rms}^2 = 10^2 + (8/\sqrt{2})^2 = 100 + 32 = 132 \), \( V_\mathrm{rms} = 11.49\,\mathrm{V} \). \( P = V_\mathrm{rms}^2 / R = 26.4\,\mathrm{W} \). Superposition of power works here because it is the sum of DC power \( 10^2/5 = 20\,\mathrm{W} \) and AC average \( (8/\sqrt{2})^2 / 5 = 6.4\,\mathrm{W} \); cross term averages to zero over a period. This is allowed for a linear resistor; it is not a violation of “no superposition of power” in the multi-source theorem sense, because we are summing orthogonal Fourier components of the same voltage.

### Answer

\( V_\mathrm{rms} = 11.49\,\mathrm{V} \); \( P = 26.4\,\mathrm{W} \) (20 W DC + 6.4 W AC).
