# Questions — Linear ODEs and constant-coefficient systems

## Q1

### Given

The homogeneous equation \(\ddot{y}+5\dot{y}+6y=0\), with \(y(0)=2\), \(\dot{y}(0)=-1\).

### Find

\(y(t)\) for \(t\ge 0\).

### Solution

Characteristic equation \(r^2+5r+6=0=(r+2)(r+3)\). Roots \(r=-2,-3\). General solution:
\[
y(t)=c_1 e^{-2t}+c_2 e^{-3t}.
\]
\[
\dot{y}(t)=-2c_1 e^{-2t}-3c_2 e^{-3t}.
\]
Initial conditions:
\[
c_1+c_2=2,\qquad -2c_1-3c_2=-1.
\]
From the first, \(c_2=2-c_1\). Second: \(-2c_1-3(2-c_1)=-1\Rightarrow -2c_1-6+3c_1=-1\Rightarrow c_1=5\), \(c_2=-3\).
\[
y(t)=5e^{-2t}-3e^{-3t}.
\]
Check: \(y(0)=5-3=2\), \(\dot{y}(0)=-10+9=-1\).

### Answer

\(y(t)=5e^{-2t}-3e^{-3t}\)

## Q2

### Given

Series RLC with \(L=1\ \mathrm{H}\), \(C=1/4\ \mathrm{F}\), \(R=1\ \Omega\), source \(v_s=8\ \mathrm{V}\) DC for \(t>0\), capacitor voltage \(v_C\) as the unknown. The ODE is \(\ddot{v}_C + \dot{v}_C + 4 v_C = 32\) (from \(LC=1/4\), \(R/L=1\), \(1/LC=4\), right-hand side \(v_s/(LC)=32\)). Initial rest: \(v_C(0^+)=0\), \(\dot{v}_C(0^+)=0\).

### Find

\(v_C(t)\) for \(t>0\).

### Solution

Homogeneous: \(r^2+r+4=0\), discriminant \(1-16=-15\), \(r=-1/2 \pm j\sqrt{15}/2\). Underdamped with \(\zeta\omega_n=1/2\), \(\omega_d=\sqrt{15}/2\). Particular solution: constant \(v_p=32/4=8\ \mathrm{V}\) (DC capacitor equals the source).
\[
v_C(t)=e^{-t/2}\big(A\cos\omega_d t + B\sin\omega_d t\big)+8,\qquad \omega_d=\sqrt{15}/2.
\]
\(v_C(0)=A+8=0\Rightarrow A=-8\).
\[
\dot{v}_C = -\tfrac12 e^{-t/2}(A\cos\omega_d t+B\sin\omega_d t)+e^{-t/2}(-A\omega_d\sin\omega_d t+B\omega_d\cos\omega_d t).
\]
At \(t=0\): \(-\tfrac12 A + B\omega_d = 0\Rightarrow B\omega_d = A/2 = -4\Rightarrow B=-4/\omega_d=-8/\sqrt{15}\).
\[
v_C(t)=8 + e^{-t/2}\left(-8\cos\omega_d t - \frac{8}{\sqrt{15}}\sin\omega_d t\right),\quad \omega_d=\frac{\sqrt{15}}{2}.
\]

### Answer

\(v_C(t)=8-e^{-t/2}\big(8\cos(\sqrt{15}\,t/2)+(8/\sqrt{15})\sin(\sqrt{15}\,t/2)\big)\ \mathrm{V}\)

## Q3

### Given

\(\dot{x}=Ax\) with
\[
A=\begin{pmatrix}0&1\\-2&-3\end{pmatrix},\qquad x(0)=\begin{pmatrix}1\\0\end{pmatrix}.
\]

### Find

\(x_1(t)\), the first state.

### Solution

\(\det(\lambda I-A)=\lambda(\lambda+3)+2=\lambda^2+3\lambda+2=(\lambda+1)(\lambda+2)\). Eigenvalues \(\lambda=-1,-2\).

For \(\lambda=-1\): \((A+I)v=0\), \(A+I=\begin{pmatrix}1&1\\-2&-2\end{pmatrix}\), so \(v_1=\begin{pmatrix}1\\-1\end{pmatrix}\).

For \(\lambda=-2\): \(A+2I=\begin{pmatrix}2&1\\-2&-1\end{pmatrix}\), \(v_2=\begin{pmatrix}1\\-2\end{pmatrix}\).

\[
x(t)=c_1\begin{pmatrix}1\\-1\end{pmatrix}e^{-t}+c_2\begin{pmatrix}1\\-2\end{pmatrix}e^{-2t}.
\]
At \(t=0\): \(c_1+c_2=1\), \(-c_1-2c_2=0\Rightarrow c_1=-2c_2\), then \(-2c_2+c_2=1\Rightarrow c_2=-1\), \(c_1=2\).
\[
x_1(t)=2e^{-t}-e^{-2t}.
\]

### Answer

\(x_1(t)=2e^{-t}-e^{-2t}\)

## Q4

### Given

\(\ddot{y}+4y=8\cos 2t\), \(y(0)=0\), \(\dot{y}(0)=0\). (Resonance: forcing frequency equals the natural frequency \(2\).)

### Find

\(y(t)\) for \(t\ge 0\).

### Solution

Homogeneous: \(r^2+4=0\), \(r=\pm j2\), \(y_h=A\cos 2t+B\sin 2t\). Ordinary trial \(C\cos 2t+D\sin 2t\) duplicates \(y_h\). Use
\[
y_p=t(C\cos 2t+D\sin 2t).
\]
Differentiate:
\[
\dot{y}_p=(C\cos 2t+D\sin 2t)+t(-2C\sin 2t+2D\cos 2t),
\]
\[
\ddot{y}_p=2(-2C\sin 2t+2D\cos 2t)+t(-4C\cos 2t-4D\sin 2t).
\]
Then \(\ddot{y}_p+4y_p=-4C\sin 2t+4D\cos 2t\) (the \(t\) terms cancel). Set equal to \(8\cos 2t\):
\[
-4C=0,\qquad 4D=8\Rightarrow C=0,\ D=2.
\]
\[
y(t)=A\cos 2t+B\sin 2t+2t\sin 2t.
\]
\(y(0)=A=0\). \(\dot{y}=2B\cos 2t+2\sin 2t+4t\cos 2t\) after \(A=0\). \(\dot{y}(0)=2B=0\Rightarrow B=0\).
\[
y(t)=2t\sin 2t.
\]
Secular growth is the mathematical signature of undamped resonance.

### Answer

\(y(t)=2t\sin 2t\)

## Q5

### Given

First-order circuit law \(\tau\dot{v}+v=10\), \(\tau=0.2\ \mathrm{s}\), \(v(0^+)=2\ \mathrm{V}\).

### Find

The time \(t_1>0\) at which \(v(t_1)=8\ \mathrm{V}\), and \(v(t)\) itself.

### Solution

\[
v(t)=10+(2-10)e^{-t/0.2}=10-8e^{-5t}.
\]
Set \(10-8e^{-5t_1}=8\): \(2=8e^{-5t_1}\), \(e^{-5t_1}=1/4\), \(-5t_1=\ln(1/4)=-\ln 4\), \(t_1=(\ln 4)/5= (2\ln 2)/5\).
Numerically \(\ln 2\approx 0.693147\), so \(t_1\approx 0.2773\ \mathrm{s}\).

### Answer

\(v(t)=10-8e^{-5t}\ \mathrm{V}\), \(t_1=(2\ln 2)/5\approx 0.277\ \mathrm{s}\)
