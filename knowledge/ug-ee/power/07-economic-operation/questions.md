# Questions — IC, B-coefficients, penalty factor

Original numbers. Powers in MW, incremental costs in ₹/MWh.

## Q1

### Given

Two thermal units, lossless network:

\[
C_1=400+8.0 P_1+0.004 P_1^2,\qquad C_2=600+6.5 P_2+0.005 P_2^2
\]

in ₹/h with \(P\) in MW. Load \(P_D=400\ \mathrm{MW}\). No generator limits bind.

### Find

Economic dispatch \(P_1,P_2\) and system \(\lambda\).

### Solution

\[
\mathrm{IC}_1=8.0+0.008 P_1,\qquad \mathrm{IC}_2=6.5+0.010 P_2.
\]

Set \(\mathrm{IC}_1=\mathrm{IC}_2=\lambda\) and \(P_1+P_2=400\):

\[
8.0+0.008 P_1=6.5+0.010(400-P_1)=6.5+4.0-0.010 P_1=10.5-0.010 P_1.
\]
\[
8.0+0.008 P_1=10.5-0.010 P_1,\qquad 0.018 P_1=2.5,\qquad P_1=138.89\ \mathrm{MW}.
\]
\[
P_2=261.11\ \mathrm{MW},\qquad\lambda=8.0+0.008\times 138.89=9.111\ \mathrm{₹/MWh}.
\]

Check: \(\mathrm{IC}_2=6.5+0.010\times 261.11=9.111\).

### Answer

\(P_1=138.9\ \mathrm{MW}\), \(P_2=261.1\ \mathrm{MW}\), \(\lambda=9.111\ \mathrm{₹/MWh}\)

## Q2

### Given

Same costs as Q1, but \(P_1^{\max}=120\ \mathrm{MW}\), \(P_2^{\max}=300\ \mathrm{MW}\), \(P_D=400\ \mathrm{MW}\), lossless.

### Find

Dispatch and \(\lambda\) of the remaining free unit.

### Solution

The unconstrained \(P_1=138.9\ \mathrm{MW}\) exceeds \(120\ \mathrm{MW}\). Set \(P_1=120\ \mathrm{MW}\), \(P_2=280\ \mathrm{MW}\).

\[
\lambda=\mathrm{IC}_2=6.5+0.010\times 280=9.30\ \mathrm{₹/MWh}.
\]

At the bound, \(\mathrm{IC}_1=8.0+0.008\times 120=8.96<\lambda\), consistent with a cheap unit held at maximum.

### Answer

\(P_1=120\ \mathrm{MW}\), \(P_2=280\ \mathrm{MW}\), \(\lambda=9.30\ \mathrm{₹/MWh}\)

## Q3

### Given

Loss formula \(P_L=0.00012 P_1^2+0.00005 P_1 P_2+0.00010 P_2^2\) MW with \(P\) in MW. Operating point \(P_1=150\ \mathrm{MW}\), \(P_2=250\ \mathrm{MW}\).

### Find

\(P_L\) and incremental transmission losses \(\partial P_L/\partial P_1\), \(\partial P_L/\partial P_2\).

### Solution

The given expansion is already \(B_{11}P_1^2+B_{12}^{\mathrm{written}}P_1 P_2+B_{22}P_2^2\) with the cross coefficient as written (not doubled in the formula). Then

\[
P_L=0.00012(150)^2+0.00005(150)(250)+0.00010(250)^2=2.70+1.875+6.25=10.825\ \mathrm{MW}.
\]
\[
\frac{\partial P_L}{\partial P_1}=2(0.00012)P_1+0.00005 P_2=0.036+0.0125=0.0485,
\]
\[
\frac{\partial P_L}{\partial P_2}=0.00005 P_1+2(0.00010)P_2=0.0075+0.050=0.0575.
\]

### Answer

\(P_L=10.83\ \mathrm{MW}\); ITL\(_1=0.0485\); ITL\(_2=0.0575\)

## Q4

### Given

ITL values from Q3. Incremental costs at that point: \(\mathrm{IC}_1=9.20\ \mathrm{₹/MWh}\), \(\mathrm{IC}_2=9.00\ \mathrm{₹/MWh}\).

### Find

Penalty factors \(L_1,L_2\) and the penalized incremental costs \(\mathrm{IC}_i L_i\).

### Solution

\[
L_1=\frac{1}{1-0.0485}=1.0510,\qquad L_2=\frac{1}{1-0.0575}=1.0610.
\]
\[
\mathrm{IC}_1 L_1=9.20\times 1.0510=9.669,\qquad \mathrm{IC}_2 L_2=9.00\times 1.0610=9.549.
\]

Plant 2 still looks slightly cheaper on a penalized basis at this (not yet coordinated) point.

### Answer

\(L_1=1.051\), \(L_2=1.061\); penalized ICs \(9.67\) and \(9.55\ \mathrm{₹/MWh}\)

## Q5

### Given

A single quadratic unit \(C=200+7P+0.006 P^2\) ₹/h supplies \(180\ \mathrm{MW}\) lossless. No limits.

### Find

\(\lambda=\mathrm{IC}(180)\) and the cost rate \(C(180)\).

### Solution

\[
\mathrm{IC}=7+0.012 P=7+0.012\times 180=9.16\ \mathrm{₹/MWh}.
\]
\[
C=200+7\times 180+0.006\times 180^2=200+1260+194.4=1654.4\ \mathrm{₹/h}.
\]

### Answer

\(\lambda=9.16\ \mathrm{₹/MWh}\); \(C=1654.4\ \mathrm{₹/h}\)

## Q6

### Given

Coordination without limits: \(\mathrm{IC}_1=5+0.02 P_1\), \(\mathrm{IC}_2=4+0.04 P_2\), \(L_1=1.05\), \(L_2=1.02\) (held constant for one iteration), \(P_1+P_2=P_D+P_L=320\ \mathrm{MW}\).

### Find

\(P_1,P_2,\lambda\) from \(\mathrm{IC}_i L_i=\lambda\).

### Solution

\[
(5+0.02 P_1)1.05=(4+0.04 P_2)1.02=\lambda.
\]
\[
5.25+0.021 P_1=4.08+0.0408 P_2.
\]

With \(P_2=320-P_1\):

\[
5.25+0.021 P_1=4.08+0.0408(320-P_1)=4.08+13.056-0.0408 P_1=17.136-0.0408 P_1.
\]
\[
0.0618 P_1=11.886,\qquad P_1=192.33\ \mathrm{MW},\qquad P_2=127.67\ \mathrm{MW}.
\]
\[
\lambda=(5+0.02\times 192.33)\times 1.05=8.847\times 1.05=9.289\ \mathrm{₹/MWh}.
\]

### Answer

\(P_1=192.3\ \mathrm{MW}\), \(P_2=127.7\ \mathrm{MW}\), \(\lambda=9.29\ \mathrm{₹/MWh}\)
