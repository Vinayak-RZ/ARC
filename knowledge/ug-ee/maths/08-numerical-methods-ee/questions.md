# Questions — Numerical methods for EE

## Q1

### Given

\(f(x)=x^3-x-1\). Interval \([1,2]\). (One real root lives there: \(f(1)=-1\), \(f(2)=5\).)

### Find

The bisection midpoint after three bisections (four evaluations of the midpoint if counting the first mid), starting with \(a=1\), \(b=2\). Report the interval after three bisections and its midpoint.

### Solution

Start \([1,2]\), \(f(1)<0\), \(f(2)>0\).

1. Mid \(1.5\), \(f(1.5)=3.375-1.5-1=0.875>0\) → new interval \([1,1.5]\).
2. Mid \(1.25\), \(f(1.25)=1.953125-1.25-1=-0.296875<0\) → \([1.25,1.5]\).
3. Mid \(1.375\), \(f(1.375)=2.599609375-1.375-1=0.224609375>0\) → \([1.25,1.375]\).

Midpoint of the current interval: \(1.3125\). Width \(0.125\) versus original width \(1\), factor \(1/8=2^{-3}\).

### Answer

After 3 bisections: interval \([1.25,1.375]\), midpoint \(1.3125\)

## Q2

### Given

\(f(x)=x^2-2\), Newton start \(x_0=1.5\). (Root \(\sqrt{2}\).)

### Find

\(x_1\) and \(x_2\).

### Solution

\(f'=2x\).
\[
x_1=1.5-\frac{2.25-2}{3}=1.5-\frac{0.25}{3}=1.5-0.083\overline{3}=1.416\overline{6}.
\]
Exactly \(x_1=17/12\).
\[
x_2=\frac{17}{12}-\frac{(17/12)^2-2}{2\cdot 17/12}=\frac{17}{12}-\frac{(289-288)/144}{17/6}=\frac{17}{12}-\frac{1/144}{17/6}.
\]
\[
\frac{1/144}{17/6}=\frac{6}{144\cdot 17}=\frac{1}{24\cdot 17}=\frac{1}{408},\qquad x_2=\frac{17}{12}-\frac{1}{408}=\frac{578-1}{408}=\frac{577}{408}.
\]
Numerically \(x_2=1.414215686\ldots\) versus \(\sqrt{2}=1.414213562\ldots\).

### Answer

\(x_1=1.416\overline{6}=17/12\), \(x_2=577/408\approx 1.414216\)

## Q3

### Given

Approximate \(I=\int_0^1 e^{-x}\,dx\) with the trapezoid rule, \(n=2\) panels (\(h=0.5\)). True value \(1-e^{-1}\).

### Find

The trapezoid estimate \(T\) and the absolute error \(|T-I|\).

### Solution

\(f(0)=1\), \(f(0.5)=e^{-0.5}\approx 0.60653066\), \(f(1)=e^{-1}\approx 0.36787944\).
\[
T=\frac{0.5}{2}\big(1+2\cdot 0.60653066+0.36787944\big)=0.25\cdot 2.58094076=0.64523519.
\]
True \(I=1-e^{-1}\approx 0.63212056\). Error \(\approx 0.01311\).

### Answer

\(T\approx 0.64524\), \(|T-I|\approx 0.01311\)

## Q4

### Given

\[
A=\begin{pmatrix}2&1\\1&2\end{pmatrix},\qquad b=\begin{pmatrix}4\\5\end{pmatrix}.
\]
An approximate solve \(\tilde{x}=(1.0, 1.4)^T\) (not exact).

### Find

The residual \(r=b-A\tilde{x}\) and \(\|r\|_\infty\).

### Solution

\[
A\tilde{x}=\begin{pmatrix}2+1.4\\1+2.8\end{pmatrix}=\begin{pmatrix}3.4\\3.8\end{pmatrix},\qquad r=\begin{pmatrix}4-3.4\\5-3.8\end{pmatrix}=\begin{pmatrix}0.6\\1.2\end{pmatrix}.
\]
\(\|r\|_\infty=1.2\). (Exact \(x\) from Cramer: \(\det=3\), \(x=(1,2)^T\); the guess is not close, and the residual shows it.)

### Answer

\(r=(0.6,1.2)^T\), \(\|r\|_\infty=1.2\)

## Q5

### Given

Central difference for \(f(x)=\sin x\) at \(x=0\), \(h=0.1\) rad. True \(f'(0)=1\).

### Find

The difference approximation and the absolute error.

### Solution

\[
\frac{\sin(0.1)-\sin(-0.1)}{0.2}=\frac{2\sin 0.1}{0.2}=10\sin 0.1.
\]
\(\sin 0.1\approx 0.09983341664\), so approximation \(\approx 0.998334166\). Error \(\approx 1.666\times 10^{-3}\).
(The leading term of the truncation is \(-h^2 f'''(0)/6=-0.01/6\approx -0.001667\), matching.)

### Answer

\(\approx 0.998334\), absolute error \(\approx 0.001666\)
