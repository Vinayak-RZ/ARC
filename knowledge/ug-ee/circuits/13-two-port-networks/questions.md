# Questions — z, y, h, ABCD parameters

Original pedagogical numbers.

## Q1

### Given

T-network: 4 Ω in the top left, 6 Ω in the top right, 12 Ω shunt to the common ground.

### Find

z-parameters (I2 into port 2).

### Solution

z11 = 4+12 = 16 Ω, z22 = 6+12 = 18 Ω, z12 = z21 = 12 Ω (open-circuit transfer: I1=1 A, I2=0, V2 = 12 V).

### Answer

z11 = 16 Ω, z12 = z21 = 12 Ω, z22 = 18 Ω.

## Q2

### Given

The z of Q1.

### Find

Derive y-parameters as Z inverse.

### Solution

det z = 16×18 − 144 = 144. y11 = z22/Δ = 18/144 = 0.125 S, y22 = 16/144 = 0.1111 S, y12 = y21 = −12/144 = −0.08333 S.

### Answer

y11 = 0.125 S, y12 = y21 = −0.0833 S, y22 = 0.111 S.

## Q3

### Given

Design a symmetric T (za = zb) with z11 = 25 Ω and z12 = 10 Ω.

### Find

za and shunt zc.

### Solution

z12 = zc = 10 Ω. z11 = za + zc = 25 ⇒ za = 15 Ω = zb.

### Answer

Series arms 15 Ω, shunt 10 Ω.

## Q4

### Given

A student computes ABCD A = V1/V2 with port 2 shorted.

### Find

Explain the correct test for A.

### Solution

A is the open-circuit voltage ratio V1/V2 with I2 = 0 (port 2 open), not shorted. Shorted port 2 is the B (or y) family of tests. With the short, V2 = 0 so A is undefined.

### Answer

A uses port 2 open: A = V1/V2 | I2=0.

## Q5

### Given

Two identical reciprocal two-ports each with A=2, B=5 Ω, C=0.2 S, D=1.5, cascaded (check AD−BC).

### Find

Whether each is reciprocal, and the cascade A.

### Solution

AD−BC = 2×1.5 − 5×0.2 = 3 − 1 = 2 ≠ 1, so not reciprocal (and not a passive T of R,L,C with the usual convention). Still cascade: \( \begin{bmatrix}2&5\\0.2&1.5\end{bmatrix}^2 = \begin{bmatrix}4+1&10+7.5\\0.4+0.3&1+2.25\end{bmatrix} = \begin{bmatrix}5&17.5\\0.7&3.25\end{bmatrix} \). Cascade A = 5.

### Answer

Not reciprocal (AD−BC=2); cascade A = 5.

(If a problem required a reciprocal example, scale C to 0.1 S so AD−BC=1; that is a different network.)
