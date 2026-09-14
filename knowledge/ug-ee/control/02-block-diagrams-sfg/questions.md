# Questions — Block reduction, Mason gain

Original pedagogical numbers.

## Q1

### Given

Unity negative feedback. Forward path \(G(s)=4/(s+2)\), feedback \(H=1\).

### Find

Closed-loop \(T(s)=Y(s)/R(s)\) and DC gain \(T(0)\).

### Solution

\(T=G/(1+G)=[4/(s+2)]/[1+4/(s+2)]=4/(s+6)\). \(T(0)=4/6=2/3\).

### Answer

\(T(s)=4/(s+6)\); \(T(0)=2/3\).

## Q2

### Given

Forward \(G_c=K\), plant \(G=3/(s(s+3))\), unity negative feedback.

### Find

\(T(s)=Y/R\) in terms of \(K\).

### Solution

\(L=3K/[s(s+3)]\), \(T=L/(1+L)=3K/[s^2+3s+3K]\).

### Answer

\(T(s)=3K/(s^2+3s+3K)\).

## Q3

### Given

Two cascaded plants \(G_1=2/(s+1)\), \(G_2=5/(s+4)\), with a parallel forward bypass \(G_3=1\) from the same input to the same summing output (all added), no feedback.

### Find

\(Y/U\).

### Solution

Series of \(G_1,G_2\) in parallel with \(G_3\): \(G_1 G_2+G_3=10/[(s+1)(s+4)]+1=[10+(s+1)(s+4)]/[(s+1)(s+4)]=(s^2+5s+14)/[(s+1)(s+4)]\).

### Answer

\(Y/U=(s^2+5s+14)/[(s+1)(s+4)]\).

## Q4

### Given

SFG: forward path \(P_1=G_1 G_2 G_3\). Loops: \(L_1=-G_2 H_1\) (touching \(P_1\)), \(L_2=-G_3 H_2\) (touching \(P_1\)), and \(L_1,L_2\) share the node after \(G_2\) so they touch each other. No other paths.

### Find

Mason \(T=Y/U\).

### Solution

\(\Delta=1-(L_1+L_2)=1+G_2 H_1+G_3 H_2\) (no nontouching product). \(\Delta_1=1\) because both loops touch \(P_1\). \(T=G_1 G_2 G_3/(1+G_2 H_1+G_3 H_2)\).

### Answer

\(T=G_1 G_2 G_3/(1+G_2 H_1+G_3 H_2)\).

## Q5

### Given

Plant \(G=2/(s+1)\), unity negative feedback with controller \(G_c=4\). Disturbance \(D\) adds at the plant output (\(Y=GU+D\)).

### Find

\(Y(s)/D(s)\) with \(R=0\), and \(Y/R\) with \(D=0\). Check \(S+T\).

### Solution

\(L=G_c G=8/(s+1)\). \(T=Y/R=L/(1+L)=8/(s+9)\). \(S=Y/D=1/(1+L)=(s+1)/(s+9)\). Sum: \((8+s+1)/(s+9)=1\).

### Answer

\(Y/D=(s+1)/(s+9)\); \(Y/R=8/(s+9)\); \(S+T=1\).
