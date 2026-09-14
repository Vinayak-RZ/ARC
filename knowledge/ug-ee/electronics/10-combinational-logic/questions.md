# Worked questions — combinational logic

## Q1
### Given
\(f(A,B,C)=\sum m(1,2,4,7)\). Implement with a 4-to-1 MUX, selects \(A,B\) (A MSB), data pins may be 0, 1, \(C\), or \(\bar C\).
### Find
The four data inputs \(D_0..D_3\).
### Solution
Shannon on \(AB\): \(AB=00\): \(f=\bar C\cdot m(0)+\ldots\) remaining \(C\) as the only variable: \(m1=001\) so \(f=C\) when \(AB=00\). \(AB=01\) (\(m2=010\), \(m3=011\)): \(f=1\) for \(C=0\), \(0\) for \(C=1\) \(\Rightarrow \bar C\). \(AB=10\) (\(m4=100\), \(m5=101\)): \(f=1\) for \(C=0\), \(0\) for \(C=1\) \(\Rightarrow \bar C\). \(AB=11\) (\(m6=110\), \(m7=111\)): \(f=0\) for \(C=0\), \(1\) for \(C=1\) \(\Rightarrow C\). So \(D_0=C\), \(D_1=\bar C\), \(D_2=\bar C\), \(D_3=C\).
### Answer
\(D_0=C\), \(D_1=\bar C\), \(D_2=\bar C\), \(D_3=C\)

## Q2
### Given
Full adder inputs \(A=1\), \(B=1\), \(C_{in}=1\).
### Find
\(S\) and \(C_{out}\).
### Solution
\(S=1\oplus 1\oplus 1=1\), \(C_{out}=1\) (majority of three 1s). Check: sum bit of \(1+1+1=3=11_2\).
### Answer
\(S=1\), \(C_{out}=1\)

## Q3
### Given
Two BCD digits added in binary: \(0111+0110\) (7+6).
### Find
The BCD sum digit and the decimal carry.
### Solution
Binary nibble sum \(0111+0110=1101=13_{10}\). \(13>9\), so add 0110: \(1101+0110=1\,0011\). BCD digit 0011 (3), carry 1. Check: 7+6=13.
### Answer
Digit \(0011\), carry \(1\)

## Q4
### Given
SOP \(f=AB+\bar A C\). A single-input change \(A:1\to 0\) while \(B=C=1\).
### Find
Whether a static-1 hazard exists, and the consensus term that removes it.
### Solution
When \(B=C=1\), \(f=A+\bar A=1\) should stay 1. \(AB\) turns off before \(\bar A C\) turns on if \(A\) and \(\bar A\) are delayed differently. Adjacent minterms \(ABC\) and \(\bar A BC\) are not covered by one product. Consensus of \(AB\) and \(\bar A C\) is \(BC\). Cover \(f=AB+\bar A C+BC\) is hazard-free for single-input changes.
### Answer
Static-1 hazard yes; add \(BC\)

## Q5
### Given
3-to-8 decoder, active-high outputs, enable \(E=1\). Inputs \(A_2A_1A_0=101\).
### Find
Which output \(Y_i\) is 1, and how to realise \(g=\sum m(1,5,7)\) with this decoder plus one OR gate.
### Solution
\(101_2=5\), so \(Y_5=1\), others 0. \(g=Y_1+Y_5+Y_7\).
### Answer
\(Y_5=1\); \(g=Y_1\lor Y_5\lor Y_7\)
