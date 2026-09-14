## Q1
### Given
\(x(t)=u(t)-u(t-2)\) and \(h(t)=u(t)-u(t-3)\).
### Find
\((x*h)(t)\) for all \(t\).
### Solution
Both are unit-height rectangles, widths 2 and 3, starting at 0. The convolution is the overlap length of \([0,2]\) with \([t-3,t]\).

Overlap is 0 for \(t<0\) and for \(t>5\). For \(0\le t\le 2\) the overlap grows as \(t\). For \(2\le t\le 3\) the overlap is the full width of \(x\), namely 2. For \(3\le t\le 5\) the overlap shrinks as \(5-t\).

Thus \(y(t)=t\) on \([0,2]\), \(y(t)=2\) on \([2,3]\), \(y(t)=5-t\) on \([3,5]\), and 0 elsewhere.
### Answer
\(y(t)=t\bigl(u(t)-u(t-2)\bigr)+2\bigl(u(t-2)-u(t-3)\bigr)+(5-t)\bigl(u(t-3)-u(t-5)\bigr)\).

## Q2
### Given
\(x[n]=\{1,2,3\}\) for \(n=0,1,2\) and \(h[n]=\{4,-1\}\) for \(n=0,1\); both zero elsewhere.
### Find
The linear convolution \(y[n]=x*h\) as a sequence listed from \(n=0\).
### Solution
Polynomial picture: \((1+2z^{-1}+3z^{-2})(4-z^{-1})=4+8z^{-1}+12z^{-2}-z^{-1}-2z^{-2}-3z^{-3}=4+7z^{-1}+10z^{-2}-3z^{-3}\).

Direct sums: \(y[0]=4\), \(y[1]=2\cdot 4+1\cdot(-1)=7\), \(y[2]=3\cdot 4+2\cdot(-1)=10\), \(y[3]=3\cdot(-1)=-3\). Length \(3+2-1=4\).
### Answer
\(y[n]=\{4,7,10,-3\}\) for \(n=0,1,2,3\).

## Q3
### Given
\(h(t)=e^{-2t}u(t)\) and \(x(t)=e^{-5t}u(t)\).
### Find
\(y=x*h\).
### Solution
For \(t<0\) there is no overlap of two causal exponentials, so \(y(t)=0\). For \(t\ge 0\),

\[
y(t)=\int_{0}^{t}e^{-5\tau}e^{-2(t-\tau)}\,d\tau=e^{-2t}\int_{0}^{t}e^{-3\tau}\,d\tau
=e^{-2t}\cdot\frac{1-e^{-3t}}{3}=\frac{1}{3}\bigl(e^{-2t}-e^{-5t}\bigr).
\]

So \(y(t)=\frac13(e^{-2t}-e^{-5t})u(t)\).
### Answer
\(y(t)=\frac13(e^{-2t}-e^{-5t})u(t)\).

## Q4
### Given
A DT LTI system with \(h[n]=\delta[n]-2\delta[n-1]+\delta[n-2]\) and input \(x[n]=u[n]\).
### Find
\(y[n]\) for all \(n\).
### Solution
\(y=h*x=u[n]-2u[n-1]+u[n-2]\).

Evaluate by cases: \(n<0\): \(y=0\). \(n=0\): \(1\). \(n=1\): \(1-2=-1\). \(n\ge 2\): \(1-2+1=0\).

So \(y[n]=\delta[n]-\delta[n-1]\).
### Answer
\(y[n]=\delta[n]-\delta[n-1]\).

## Q5
### Given
Finite sequences \(x[n]=\{1,1\}\) and \(h[n]=\{1,1,1\}\) both starting at \(n=0\).
### Find
Linear convolution length and samples, and the 3-point circular convolution (no padding).
### Solution
Linear: length \(2+3-1=4\), \(y=\{1,2,2,1\}\).

3-point circular: wrap \(x\) to length 3 as \(\{1,1,0\}\). Circular convolution with \(\{1,1,1\}\) is the sum of all samples of \(x\) at every lag, because \(h\) is all ones: each output is \(1+1+0=2\). Equivalently, time-alias the linear result: alias \(y[3]\) onto \(y[0]\), giving \(\{1+1,2,2\}=\{2,2,2\}\).
### Answer
Linear: length 4, \(\{1,2,2,1\}\). Circular length 3: \(\{2,2,2\}\).

## Q6
### Given
\(x(t)=\delta(t-1)+2\delta(t-4)\) and \(h(t)=e^{-t}u(t)\).
### Find
\(y=x*h\).
### Solution
Convolution with a delayed impulse shifts \(h\): \(y(t)=h(t-1)+2h(t-4)=e^{-(t-1)}u(t-1)+2e^{-(t-4)}u(t-4)\).
### Answer
\(y(t)=e^{-(t-1)}u(t-1)+2e^{-(t-4)}u(t-4)\).
