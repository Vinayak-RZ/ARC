# Questions — Describing function, limit cycles intro

Original pedagogical numbers.

## Q1

### Given

Ideal relay \(\pm 2\) (so \(M=2\)). Linear plant \(L(s)=12/[s(s+1)(s+2)]\).

### Find

The DF predicted frequency and the amplitude \(A\) at the relay input.

### Solution

Relay \(N(A)=8/(\pi A)\). Intersections where \(L(j\omega)\) is negative real, i.e. the Routh crossing of \(1+K L_0=0\) with \(L_0=1/[s(s+1)(s+2)]\), \(K_u=6\) as in earlier units, \(\omega_u=\sqrt{2}\). At that point \(K_{\mathrm{eq}}L_0=-1\) with \(K_{\mathrm{eq}}=6\), so \(N(A)=6=8/(\pi A)\) ⇒ \(A=8/(6\pi)=0.424\). Frequency \(\omega=\sqrt{2}=1.414\,\mathrm{rad/s}\). Check: \(L(j\omega)=12 G_0\), wait the plant is \(12 G_0\) with \(G_0=1/[s(s+1)(s+2)]\). Then \(1+N\cdot 12 G_0=0\) ⇒ \(N\cdot 12=K_u^{\mathrm{of}}G_0=6\) ⇒ \(N=0.5\). I mixed the 12. Characteristic of \(1+K/[s(s+1)(s+2)]\) has \(K_u=6\). Here \(K_{\mathrm{eff}}=12 N(A)\), set \(12 N=6\) ⇒ \(N=0.5=8/(\pi A)\) ⇒ \(A=8/(0.5\pi)=5.093\). Frequency still \(\omega=\sqrt{2}\).

### Answer

\(\omega=1.414\,\mathrm{rad/s}\); \(A=5.09\).

## Q2

### Given

Saturation of slope 1 and levels \(\pm 1\). For \(A=2\), use the saturation DF formula.

### Find

\(N(2)\) and \(-1/N(2)\).

### Solution

\(M/A=1/2\). \(\sin^{-1}(0.5)=\pi/6=0.5236\). \(\sqrt{1-0.25}=\sqrt{0.75}=0.8660\). \(N(2)=(2/\pi)(0.5236+0.5\times 0.8660)=(2/\pi)(0.5236+0.4330)=0.609\). \(-1/N=-1.643\).

### Answer

\(N(2)=0.609\); \(-1/N=-1.64\).

## Q3

### Given

A DF intersection at \(A=0.8\) is claimed for a saturation with \(M=1\), slope 1.

### Find

Whether that amplitude is consistent with saturation DF (does the nonlinearity even saturate?).

### Solution

For \(A\le M=1\), saturation DF is \(N=1\) (linear region). \(A=0.8<1\) is not saturating; \(-1/N=-1\), independent of \(A\) in that range. A distinct intersection labelled \(A=0.8\) cannot come from the saturating formula. It would be the linear Nyquist hitting \(-1\), i.e. a linear \(j\omega\) eigenvalue, not a nonlinear cycle at 0.8.

### Answer

Inconsistent; \(A=0.8<M\) is still linear (\(N=1\)).

## Q4

### Given

Dead-zone DF is zero at \(A=0^+\) and positive for \(A\) above the zone. Linear \(L(j\omega)\) is a type-1 plant that never reaches the point at infinity needed... simpler: \(L\) encircles nothing and stays to the right of \(-0.5\). The dead-zone \(-1/N(A)\) occupies \((-\infty,-1/N_{\max}]\) on the real axis with \(N_{\max}=0.5\), so \(-1/N_{\max}=-2\).

### Find

Whether DF predicts a limit cycle.

### Solution

\(-1/N\) runs from \(-\infty\) to \(-2\). \(L(j\omega)\) never left of \(-0.5\), so it never meets \([-2,-\infty)\). No intersection. No DF limit cycle.

### Answer

No DF-predicted limit cycle.

## Q5

### Given

Ideal relay \(\pm 1\) and \(L(s)=4/s^2\).

### Find

The relation between \(A\) and \(\omega\) from harmonic balance, and why DF does not select a unique pair.

### Solution

\(N(A)=4/(\pi A)\). \(L(j\omega)=4/(-\omega^2)=-4/\omega^2\). Balance: \(-4/\omega^2=-1/N=-\pi A/4\) ⇒ \(4/\omega^2=\pi A/4\) ⇒ \(A=16/(\pi\omega^2)\). One equation, two unknowns: a continuum. \(L\) is not strictly low-pass in a way that kills harmonics uniquely (pure double integrator, relative degree 2 but phase locked at \(-180^\circ\) for all \(\omega\)). DF filtering hypothesis is degenerate; a unique cycle is not predicted.

### Answer

\(A=16/(\pi\omega^2)\); no unique \((\omega,A)\) (degenerate DF).
