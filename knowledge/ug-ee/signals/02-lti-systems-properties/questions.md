## Q1
### Given
The system \(y(t)=t\,x(t-1)\).
### Find
Whether the system is linear, time-invariant, memoryless, and causal.
### Solution
Linearity: \(t\bigl(a x_1(t-1)+b x_2(t-1)\bigr)=a\,t x_1(t-1)+b\,t x_2(t-1)\), so linear.

Time-invariance: the output of a delayed input \(x(t-t_0)\) is \(t\,x(t-t_0-1)\). The delayed original output is \((t-t_0)x(t-t_0-1)\). These differ when \(t_0\neq 0\). Time-varying.

Memoryless: \(y(t)\) uses \(x(t-1)\), not \(x(t)\). Has memory.

Causal: \(y(t)\) depends on the input at time \(t-1\le t\), never on the future. Causal.
### Answer
Linear, time-varying, has memory, causal.

## Q2
### Given
\(y[n]=x[n]+x[n+1]\).
### Find
Linearity, time-invariance, causality, invertibility on the space of all two-sided sequences.
### Solution
The map is a linear combination of shifts, hence linear and time-invariant (FIR). It uses \(x[n+1]\), a future sample, so it is noncausal.

Suppose \(y\equiv 0\). Then \(x[n+1]=-x[n]\) for all \(n\), so \(x[n]=(-1)^n c\). For \(c\neq 0\) this nonzero sequence produces the zero output. The null space is nontrivial, so the system is not invertible on all sequences.

(If one restricts to finite-energy sequences, the same alternating sequence is not in \(\ell^2\), but \(H(z)=1+z\) still has a zero on the unit circle and there is no BIBO-stable causal inverse.)
### Answer
Linear, TI, noncausal, not invertible on all sequences.

## Q3
### Given
\(y(t)=\int_{t-2}^{t} x(\tau)\,d\tau\).
### Find
An impulse response if the system is LTI, and whether it is causal and memoryless.
### Solution
The output is a sliding integral of width 2. Superposition and a constant window imply LTI. The response to \(\delta(t)\) is 1 for \(0\le t\le 2\) and 0 otherwise: \(h(t)=u(t)-u(t-2)\).

Causality: \(h(t)=0\) for \(t<0\), and the integral only looks backward from \(t\) to \(t-2\). Causal. Not memoryless: a two-second history is used.
### Answer
\(h(t)=u(t)-u(t-2)\); causal; has memory.

## Q4
### Given
\(y(t)=\bigl(x(t)\bigr)^2\).
### Find
Linearity and time-invariance, and whether an inverse exists on real CT signals.
### Solution
\((x_1+x_2)^2\neq x_1^2+x_2^2\) in general, so nonlinear. A time shift: \([x(t-t_0)]^2=y(t-t_0)\), so time-invariant.

Many-to-one: \(x\) and \(-x\) produce the same output, so not invertible on all real signals. Restricting to nonnegative inputs, \(y=\sqrt{x}\) with the nonnegative square root inverts the map pointwise.
### Answer
Nonlinear, TI, not invertible on all real CT signals.

## Q5
### Given
A discrete system \(y[n]=\sum_{k=0}^{n} x[k]\) for all \(n\in\mathbb{Z}\), with the understanding that the sum is empty (hence 0) when \(n<0\), and \(x\) may be two-sided.
### Find
Causality, time-invariance, and the output when \(x[n]=\delta[n-3]\).
### Solution
For \(n<0\) the stated sum is empty so \(y[n]=0\) regardless of the past of a two-sided \(x\) on \(n<0\). That already shows the map as written is not the usual accumulator on \(\mathbb{Z}\).

Take \(x=\delta[\,\cdot\,-3]\). Then \(y[n]=0\) for \(n<3\) and \(y[n]=1\) for \(n\ge 3\), i.e. \(y[n]=u[n-3]\).

If the same rule is applied to \(x_1[n]=\delta[n]\) one gets \(y_1[n]=u[n]\). Shifting that output by 3 gives \(u[n-3]\), which matches \(y\). For this pair the TI test passed, but consider \(x[n]=\delta[n+5]\), supported on the negative axis: the system outputs 0 for every \(n\) because no term with \(k\ge 0\) is ever 1. The shifted output of \(\delta[n]\) would be \(u[n+5]\), which is not identically zero. Therefore the system is time-varying. It is causal: \(y[n]\) uses only \(x[0],\ldots,x[n]\) for \(n\ge 0\) and is 0 for \(n<0\).
### Answer
Causal, time-varying; \(y[n]=u[n-3]\) for \(x=\delta[\,\cdot\,-3]\).

## Q6
### Given
\(y(t)=x(t/3)\).
### Find
Linearity, time-invariance, memory, causality.
### Solution
Scaling the amplitude of \(x\) scales \(y\); sums pass through. Linear.

Delay: input \(x(t-t_0)\) produces \(x(t/3-t_0)\). Delayed output is \(x((t-t_0)/3)=x(t/3-t_0/3)\). Not equal. Time-varying.

At time \(t=3\), \(y(3)=x(1)\), which is a past value if we imagine running in \(t\), but at time \(t=0\), \(y(0)=x(0)\). At time \(t=-3\), \(y(-3)=x(-1)\), and \(-1>-3\), so the output at \(-3\) uses a future input value. Not causal on \(\mathbb{R}\).

The output at \(t\) generally uses \(x\) at a different instant, so the system has memory in the standard classification (not a static map of \(x(t)\)).
### Answer
Linear, time-varying, has memory, noncausal.
