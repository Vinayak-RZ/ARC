# Questions — Routh array, parameter range

Original pedagogical numbers. Includes Routh numericals.

## Q1

### Given

Characteristic polynomial \(p(s)=s^4+6s^3+12s^2+10s+3\).

### Find

The Routh array first column and the number of RHP roots.

### Solution

Rows: \(s^4:\ (1,\ 12,\ 3)\). \(s^3:\ (6,\ 10)\). \(s^2\) first entry \((6\cdot 12-1\cdot 10)/6=(72-10)/6=62/6=31/3\); second entry \(3\). \(s^1\) first entry \(\frac{(31/3)\cdot 10-6\cdot 3}{31/3}=(310/3-18)/(31/3)=(310/3-54/3)\cdot 3/31=256/31\). \(s^0:\ 3\). First column: \(1,\ 6,\ 31/3,\ 256/31,\ 3\), all positive. Zero sign changes.

### Answer

First column \(1,\ 6,\ 31/3,\ 256/31,\ 3\); 0 RHP roots.

## Q2

### Given

Unity negative feedback with \(L(s)=K/[s(s+1)(s+2)]\), \(K>0\).

### Find

The open interval of \(K\) for closed-loop asymptotic stability, using Routh.

### Solution

\(p(s)=s(s+1)(s+2)+K=s^3+3s^2+2s+K\). Array: \(s^3:\ 1,\ 2\); \(s^2:\ 3,\ K\); \(s^1:\ (6-K)/3\); \(s^0:\ K\). Need \(K>0\) and \(6-K>0\) ⇒ \(0<K<6\). At \(K=6\), auxiliary from \(s^2\) row: \(3s^2+6=0\) ⇒ \(s=\pm j\sqrt{2}\).

### Answer

\(0<K<6\).

## Q3

### Given

\(p(s)=s^3+2s^2+s+2\).

### Find

Routh first column, number of RHP roots, and a factorization check.

### Solution

\(s^3:\ 1,\ 1\); \(s^2:\ 2,\ 2\); \(s^1:\ (2-2)/2=0\) with second entry 0 — entire zero row? \(s^1\) first entry is 0, and there is no further column, so the \(s^1\) row is a zero row (auxiliary case). Auxiliary from \(s^2\): \(A=2s^2+2\), \(A'=4s\). Replace \(s^1\) by \(4\). \(s^0:\ 2\). First column \(1,2,4,2\), no sign change. \(A=2(s^2+1)=0\) gives \(s=\pm j\). Factor: \(p(s)=(s+2)(s^2+1)\). Two simple \(j\omega\) roots, one LHP root. Not asymptotically stable; 0 RHP roots.

### Answer

First column \(1,2,4,2\) after auxiliary; 0 RHP; \(p=(s+2)(s^2+1)\); marginally stable.

## Q4

### Given

\(p(s)=s^4+2s^3+s^2+2s+K\) with the real parameter \(K\).

### Find

Values of \(K\) for strict Hurwitz stability.

### Solution

\(s^4:\ 1,\ 1,\ K\); \(s^3:\ 2,\ 2\); \(s^2:\ (2-2)/2=0\) first entry identically 0 before \(K\) even enters — first-column zero (not a whole zero row if \(K\) column differs). Compute \(s^2\) second entry: \(K\). First entry of \(s^2\): \((2\cdot 1-1\cdot 2)/2=0\). Degeneracy A for all \(K\). Use \(\varepsilon\) in that first entry: \(s^2:\ \varepsilon,\ K\). Then \(s^1:\ (\varepsilon\cdot 2-2K)/\varepsilon=2-2K/\varepsilon\). For \(\varepsilon\to 0^+\), if \(K\neq 0\) this entry → \(-\mathrm{sign}(K)\cdot\infty\). First column: \(1>0\), \(2>0\), \(\varepsilon>0\), \(2-2K/\varepsilon\), \(K\). For \(K>0\), \(s^1\to-\infty\) (one sign change) then \(s^0>0\) (second sign change) ⇒ 2 RHP. For \(K<0\), \(s^1\to+\infty\) then \(s^0<0\) (one sign change) ⇒ 1 RHP. For \(K=0\), \(p=s(s^3+2s^2+s+2)=s(s+2)(s^2+1)\), a root at 0. No strict Hurwitz \(K\).

### Answer

No real \(K\) makes \(p\) strictly Hurwitz.

## Q5

### Given

\(p(s)=s^3+(6-K)s^2+11s+(6+K)\).

### Find

The range of real \(K\) for asymptotic stability.

### Solution

Need all coefficients positive: \(6-K>0\) ⇒ \(K<6\); \(6+K>0\) ⇒ \(K>-6\); and cubic \(ab>c\): \((6-K)\cdot 11>6+K\) ⇒ \(66-11K>6+K\) ⇒ \(60>12K\) ⇒ \(K<5\). Intersect: \(-6<K<5\). Routh \(s^1\) entry is \((ab-c)/a=(66-11K-6-K)/(6-K)=(60-12K)/(6-K)\), which is positive exactly when \(K<5\) given \(K<6\). \(s^0=6+K>0\) as above.

### Answer

\(-6<K<5\).
