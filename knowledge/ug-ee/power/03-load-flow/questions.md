# Questions — Ybus, Gauss–Seidel, Newton–Raphson intro

Original numbers. Per-unit on a common base. Polar angles in degrees unless a Jacobian step needs radians.

## Q1

### Given

Three-bus network, all values pu. Series branches (no shunt): \(z_{12}=j0.20\), \(z_{13}=j0.40\), \(z_{23}=j0.25\). No tap transformers.

### Find

The \(3\times 3\) bus admittance matrix \(Y_\mathrm{bus}\).

### Solution

Branch admittances: \(y_{12}=1/(j0.20)=-j5.0\), \(y_{13}=-j2.5\), \(y_{23}=-j4.0\). Off-diagonals \(Y_{ik}=-y_{ik}\), so \(Y_{12}=j5.0\), \(Y_{13}=j2.5\), \(Y_{23}=j4.0\). Diagonals:

\[
Y_{11}=y_{12}+y_{13}=-j5-j2.5=-j7.5,
\]
\[
Y_{22}=y_{12}+y_{23}=-j5-j4=-j9.0,
\]
\[
Y_{33}=y_{13}+y_{23}=-j2.5-j4=-j6.5.
\]

So

\[
Y_\mathrm{bus}=j\begin{pmatrix}-7.5&5.0&2.5\\5.0&-9.0&4.0\\2.5&4.0&-6.5\end{pmatrix}.
\]

(The matrix is purely imaginary; the \(j\) multiplies every entry.)

### Answer

\(Y_\mathrm{bus}=j\begin{pmatrix}-7.5&5&2.5\\5&-9&4\\2.5&4&-6.5\end{pmatrix}\ \mathrm{pu}\)

## Q2

### Given

Two-bus system. Slack bus 1: \(V_1=1.02\angle 0^\circ\ \mathrm{pu}\). PQ bus 2: injection \(P_2+jQ_2=-0.50+j(-0.20)\ \mathrm{pu}\) (load). \(Y_{11}=-j10\), \(Y_{12}=Y_{21}=j10\), \(Y_{22}=-j10\) (pure series \(j0.1\)). Flat start \(V_2^{(0)}=1.00\angle 0^\circ\).

### Find

\(V_2\) after one Gauss–Seidel iteration (no acceleration).

### Solution

\[
V_2^{(1)}=\frac{1}{Y_{22}}\left(\frac{P_2-jQ_2}{(V_2^{(0)})^*}-Y_{21}V_1\right).
\]

\(P_2-jQ_2=-0.50-j(-0.20)=-0.50+j0.20\). \(V_2^{(0)*}=1\).

\[
\frac{P_2-jQ_2}{V_2^*}=-0.50+j0.20,
\]
\[
Y_{21}V_1=(j10)(1.02)=j10.2,
\]
\[
\text{parenthesis}=-0.50+j0.20-j10.2=-0.50-j10.0.
\]
\[
V_2^{(1)}=\frac{-0.50-j10.0}{-j10}=\frac{(-0.50-j10.0)(j)}{10}=\frac{-j0.50+10}{10}=1.00-j0.050.
\]

Magnitude \(1.00125\angle -2.86^\circ\) approximately.

### Answer

\(V_2^{(1)}=1.00-j0.050\ \mathrm{pu}\) (\(1.001\angle -2.86^\circ\))

## Q3

### Given

After voltages \(V_1=1.00\angle 0^\circ\), \(V_2=0.98\angle -4^\circ\ \mathrm{pu}\) on a line \(z=j0.20\ \mathrm{pu}\) (no charging).

### Find

Real power \(P_{12}\) from bus 1 to bus 2 in pu.

### Solution

\[
P_{12}=\frac{V_1 V_2}{X}\sin(\theta_1-\theta_2)=\frac{(1.00)(0.98)}{0.20}\sin 4^\circ=4.90\times 0.06976=0.3418\ \mathrm{pu}.
\]

### Answer

\(0.342\ \mathrm{pu}\)

## Q4

### Given

PQ bus scheduled \(P^{\mathrm{sch}}=-0.80\ \mathrm{pu}\), \(Q^{\mathrm{sch}}=-0.30\ \mathrm{pu}\). Calculated from the present voltage estimate: \(P^{\mathrm{calc}}=-0.74\ \mathrm{pu}\), \(Q^{\mathrm{calc}}=-0.22\ \mathrm{pu}\).

### Find

Power mismatches \(\Delta P\) and \(\Delta Q\) as used in Newton–Raphson with \(\Delta S=S^{\mathrm{sch}}-S^{\mathrm{calc}}\).

### Solution

\[
\Delta P=-0.80-(-0.74)=-0.06\ \mathrm{pu},\qquad \Delta Q=-0.30-(-0.22)=-0.08\ \mathrm{pu}.
\]

The negative mismatches mean the network is supplying more \(P\) and \(Q\) than the load (injections less negative than scheduled); NR will move \(V,\theta\) to increase the load-like (more negative) calculated injections.

### Answer

\(\Delta P=-0.06\ \mathrm{pu}\), \(\Delta Q=-0.08\ \mathrm{pu}\)

## Q5

### Given

Two-bus lossless line \(X=0.25\ \mathrm{pu}\). Slack \(V_1=1.0\angle 0\). Unknowns at bus 2: \(\theta_2\), \(V_2\). Flat start \(V_2=1.0\), \(\theta_2=0\). Load injection schedule \(P_2=-0.40\ \mathrm{pu}\), \(Q_2=-0.10\ \mathrm{pu}\). Injection into the network at bus 2 is \(P_2=(V_1 V_2/X)\sin(\theta_2-\theta_1)\), which is negative when \(\theta_2<\theta_1\). At flat start, \(P_2^{\mathrm{calc}}=0\) and \(Q_2^{\mathrm{calc}}=[V_2^2-V_1 V_2\cos(\theta_2-\theta_1)]/X=0\).

Jacobian diagonals at this point for unknowns \((\theta_2,V_2)\): \(H=\partial P_2/\partial\theta_2=V_1 V_2/X=4.0\), \(N=\partial P_2/\partial V_2=0\) at \(\theta=0\), \(M=\partial Q_2/\partial\theta_2=0\) at \(\theta=0\), \(L=\partial Q_2/\partial V_2=(2V_2-V_1)/X=4.0\), with \(Q_2=[V_2^2-V_1 V_2\cos(\theta_2-\theta_1)]/X\).

### Find

The first NR updates \(\Delta\theta_2\) (radians) and \(\Delta V_2\).

### Solution

Mismatches: \(\Delta P_2=P_2^{\mathrm{sch}}-P_2^{\mathrm{calc}}=-0.40-0=-0.40\), \(\Delta Q_2=-0.10-0=-0.10\).

Decoupled at this point:

\[
H\Delta\theta_2=\Delta P_2\ \Rightarrow\ 4.0\,\Delta\theta_2=-0.40\ \Rightarrow\ \Delta\theta_2=-0.10\ \mathrm{rad},
\]
\[
L\Delta V_2=\Delta Q_2\ \Rightarrow\ 4.0\,\Delta V_2=-0.10\ \Rightarrow\ \Delta V_2=-0.025\ \mathrm{pu}.
\]

New estimate: \(\theta_2=-0.10\ \mathrm{rad}=-5.73^\circ\), \(V_2=0.975\ \mathrm{pu}\).

### Answer

\(\Delta\theta_2=-0.10\ \mathrm{rad}\), \(\Delta V_2=-0.025\ \mathrm{pu}\)

## Q6

### Given

A PV bus scheduled \(V=1.04\ \mathrm{pu}\), \(P=0.60\ \mathrm{pu}\). After a GS voltage update the complex result is \(V=1.028+j0.070\ \mathrm{pu}\) before magnitude restoration.

### Find

The restored PV voltage phasor (magnitude forced to \(1.04\), angle unchanged).

### Solution

\[
|V|=\sqrt{1.028^2+0.070^2}=1.0304,\qquad \theta=\tan^{-1}(0.070/1.028)=3.896^\circ.
\]
\[
V_{\mathrm{restored}}=1.04\angle 3.896^\circ=1.0376+j0.0706\ \mathrm{pu}.
\]

### Answer

\(1.04\angle 3.90^\circ\ \mathrm{pu}\)
