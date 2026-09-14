# Questions — Short/medium/long lines, ABCD

Original numbers. Per-phase RMS phasors unless noted. Balanced three-phase.

## Q1

### Given

A short three-phase line: \(Z=4+j20\ \Omega\) per phase. Receiving-end line-to-line voltage \(132\ \mathrm{kV}\). Load \(80\ \mathrm{MW}\) at \(0.80\) lagging pf.

### Find

Sending-end line-to-line voltage magnitude.

### Solution

Phase voltage at R, taken as reference:

\[
V_R=\frac{132}{\sqrt{3}}=76.210\ \mathrm{kV}.
\]

Per-phase complex power \(S_R=(80/3)+j(80/3)\tan(\cos^{-1}0.8)=26.667+j20.000\ \mathrm{MVA}\).

\[
I_R=\left(\frac{S_R}{V_R}\right)^*=\frac{26.667-j20.000}{76.210}\ \mathrm{kA}=0.3500-j0.2624\ \mathrm{kA}.
\]

\[
V_S=V_R+I_R Z
\]
\[
I_R Z=(0.3500-j0.2624)(4+j20)=1.400+j7.000-j1.050+5.248=6.648+j5.950\ \mathrm{kV}.
\]
\[
V_S=76.210+6.648+j5.950=82.858+j5.950\ \mathrm{kV},\qquad |V_S|=83.071\ \mathrm{kV\ phase}.
\]

Line-to-line sending magnitude: \(\sqrt{3}\times 83.071=143.88\ \mathrm{kV}\).

### Answer

\(143.9\ \mathrm{kV}\)

## Q2

### Given

Nominal-\(\pi\) medium line: series \(Z=j40\ \Omega\), total shunt \(Y=j3.2\times 10^{-4}\ \mathrm{S}\) (split equally).

### Find

ABCD parameters.

### Solution

\[
\frac{Y}{2}=j1.6\times 10^{-4}\ \mathrm{S}.
\]
\[
A=D=1+\frac{YZ}{2}=1+(j3.2\times 10^{-4})(j40)/2=1+j^2(0.0128)/2=1-0.0064=0.9936.
\]
\[
B=Z=j40\ \Omega.
\]
\[
C=Y\left(1+\frac{YZ}{4}\right)=j3.2\times 10^{-4}\bigl(1+(j3.2\times 10^{-4})(j40)/4\bigr)
\]
\[
=j3.2\times 10^{-4}(1-0.0032)=j3.1898\times 10^{-4}\ \mathrm{S}.
\]

Check: \(AD-BC=(0.9936)^2-(j40)(j3.1898\times 10^{-4})=0.98724+0.012759=1.000\) (within rounding).

### Answer

\(A=D=0.9936\), \(B=j40\ \Omega\), \(C=j3.190\times 10^{-4}\ \mathrm{S}\)

## Q3

### Given

Lossless line reactance \(X=100\ \Omega\) per phase (short-line model). Sending and receiving phase voltages \(V_S=V_R=127.0\ \mathrm{kV}\) (corresponding to \(220\ \mathrm{kV}\) line-to-line). Angle \(\delta=20^\circ\).

### Find

Three-phase real power transferred sending to receiving.

### Solution

\[
P_{1\phi}=\frac{V_S V_R}{X}\sin\delta=\frac{(127.0\times 10^3)^2}{100}\sin 20^\circ=5.516\times 10^7\ \mathrm{W}=55.16\ \mathrm{MW}.
\]

Three-phase: \(3\times 55.16=165.5\ \mathrm{MW}\). Equivalently with line-to-line voltages:

\[
P_{3\phi}=\frac{V_{LL,S}V_{LL,R}}{X}\sin\delta=\frac{220^2}{100}\sin 20^\circ=165.5\ \mathrm{MW}.
\]

### Answer

\(165.5\ \mathrm{MW}\)

## Q4

### Given

A long-line lossless model with \(A=0.90\angle 3^\circ\) and sending line-to-line voltage held at \(400\ \mathrm{kV}\). Receiving end open.

### Find

Receiving-end line-to-line voltage magnitude (Ferranti).

### Solution

\(I_R=0\) implies \(V_S=A V_R\), so \(|V_R|=|V_S|/|A|\). Using line-to-line magnitudes (same ratio as phase):

\[
|V_{R,LL}|=\frac{400}{0.90}=444.4\ \mathrm{kV}.
\]

The angle of \(A\) rotates the phasor but does not change this magnitude result.

### Answer

\(444.4\ \mathrm{kV}\)

## Q5

### Given

Positive-sequence \(z=0.03+j0.32\ \Omega/\mathrm{km}\), \(y=j3.0\times 10^{-6}\ \mathrm{S/km}\), length \(80\ \mathrm{km}\). Use the short-line model (ignore \(y\)) for series impedance, and also compute total charging Mvar at \(220\ \mathrm{kV}\) if the line were energized at rated voltage with both ends at \(220\ \mathrm{kV}\) (approximate: \(Q_c=V^2 B\) three-phase with \(B=\mathrm{Im}(y)\ell\)).

### Find

Series \(Z\) for the short-line model, and total three-phase charging Mvar at \(220\ \mathrm{kV}\).

### Solution

\[
Z=(0.03+j0.32)\times 80=2.4+j25.6\ \Omega.
\]

\[
B=3.0\times 10^{-6}\times 80=2.4\times 10^{-4}\ \mathrm{S}.
\]

Three-phase charging with line-to-line \(V=220\ \mathrm{kV}\):

\[
Q_c=V_{LL}^2 B=(220)^2(2.4\times 10^{-4})=11.616\ \mathrm{Mvar}.
\]

(The same as \(3 V_\phi^2 B\).)

### Answer

\(Z=2.4+j25.6\ \Omega\); \(Q_c=11.62\ \mathrm{Mvar}\)

## Q6

### Given

Equivalent-\(\pi\) series arm \(Z'=j80\ \Omega\) and each shunt \(Y'/2=j2.0\times 10^{-4}\ \mathrm{S}\). Receiving phase voltage \(V_R=133.0\angle 0^\circ\ \mathrm{kV}\), \(I_R=0.40\angle -25^\circ\ \mathrm{kA}\).

### Find

Sending phase voltage \(V_S\).

### Solution

Nominal/equivalent \(\pi\): \(V_S=(1+Z'Y'/2)V_R+Z'I_R\).

\[
Z'Y'/2=(j80)(j2.0\times 10^{-4})=-0.016,
\]
\[
A=1-0.016=0.984.
\]
\[
A V_R=0.984\times 133.0=130.872\ \mathrm{kV}.
\]
\[
I_R=0.40(\cos(-25)+j\sin(-25))=0.3625-j0.1690\ \mathrm{kA},
\]
\[
Z'I_R=j80(0.3625-j0.1690)=13.520+j29.000\ \mathrm{kV}.
\]
\[
V_S=130.872+13.520+j29.000=144.392+j29.000\ \mathrm{kV}=147.3\angle 11.35^\circ\ \mathrm{kV}.
\]

### Answer

\(147.3\angle 11.35^\circ\ \mathrm{kV}\) (phase)
