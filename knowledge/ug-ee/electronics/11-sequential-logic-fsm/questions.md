# Worked questions — latches, flip-flops, counters, FSM

## Q1
### Given
JK flip-flop, present \(Q=1\), inputs \(J=0\), \(K=1\), active clock edge arrives. Characteristic \(Q^+=J\bar Q+\bar K Q\).
### Find
\(Q^+\) immediately after the edge.
### Solution
\(Q^+=0\cdot 0+\bar 1\cdot 1=0\). The \(K=1\) with \(Q=1\) resets. Same from the JK table: \(JK=01\) means reset.
### Answer
\(Q^+=0\)

## Q2
### Given
Synchronous 4-bit binary up-counter, D-FFs, present state \(Q_3Q_2Q_1Q_0=1011_2\).
### Find
The four D inputs that produce the next count, and the next state.
### Solution
Next should be \(1100_2=12\). \(D_0=\bar Q_0=0\), \(D_1=Q_1\oplus Q_0=1\oplus 1=0\), \(D_2=Q_2\oplus(Q_1 Q_0)=0\oplus 1=1\), \(D_3=Q_3\oplus(Q_2 Q_1 Q_0)=1\oplus 0=1\). Next state \(1100\).
### Answer
\(D_3D_2D_1D_0=1100\), next state \(1100_2\)

## Q3
### Given
Clock period constraint: \(t_{cq}=2.5\,\mathrm{ns}\), combinational \(t_{pd}=6.0\,\mathrm{ns}\), \(t_{su}=1.2\,\mathrm{ns}\), skew \(0.4\,\mathrm{ns}\). Hold check: \(t_{cd,FF}=0.6\,\mathrm{ns}\), \(t_{cd,comb}=0.2\,\mathrm{ns}\), \(t_h=0.5\,\mathrm{ns}\), same skew.
### Find
Minimum \(T_{clk}\) and whether hold is met.
### Solution
\(T_{clk}\ge 2.5+6.0+1.2+0.4=10.1\,\mathrm{ns}\). Hold: \(0.6+0.2=0.8\), need \(\ge 0.5+0.4=0.9\). \(0.8<0.9\), hold fails.
### Answer
\(T_{clk}\ge 10.1\,\mathrm{ns}\); hold not met (0.8 ns < 0.9 ns)

## Q4
### Given
Moore FSM, 2-bit state, D-FFs. States: idle \(00\), s1 \(01\), s2 \(11\), back to idle (Gray-ish). Input \(x\): stay in idle while \(x=0\); if \(x=1\) go idle\(\to\)s1\(\to\)s2\(\to\)idle regardless of \(x\) after leaving idle. Output \(z=1\) only in s2.
### Find
Boolean \(D_1,D_0,z\) in terms of \(Q_1,Q_0,x\) (minimal SOP, unused state \(10\) treated as don't-care for next-state except it must not be required).
### Solution
Label \(Q_1Q_0\): idle 00, s1 01, s2 11, unused 10. Next: 00 --x=0→ 00, x=1→ 01; 01 → 11 always; 11 → 00 always. \(D_1D_0=Q^+\). \(D_0=1\) for next of idle when \(x=1\) (next 01) and not otherwise from listed states: from table \(D_0=\bar Q_1\bar Q_0 x + \bar Q_1 Q_0=\bar Q_1(\bar Q_0 x+Q_0)\). \(D_1=1\) for next of s1 (01→11): \(D_1=\bar Q_1 Q_0\). \(z=Q_1 Q_0\). (Unused 10 left unspecified.)
### Answer
\(D_1=\bar Q_1 Q_0\), \(D_0=\bar Q_1(\bar Q_0 x+Q_0)\), \(z=Q_1 Q_0\)

## Q5
### Given
8-bit SISO shift register, initially \(0000\,0001\), clocked 3 times, serial input held at 0 (shift toward MSB, LSB is the serial input stage).
### Find
The register contents after 3 clocks.
### Solution
Each clock inserts 0 at LSB and shifts left: \(0000\,0010\), \(0000\,0100\), \(0000\,1000\).
### Answer
\(00001000\)
