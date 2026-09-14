# Worked questions — number systems and Boolean algebra

## Q1
### Given
The decimal number 157 and the fraction 0.625.
### Find
8-bit binary of 157, hexadecimal of 157, and binary of 0.625.
### Solution
\(157=128+29=128+16+8+4+1=10011101_2=0\mathrm{x}9\mathrm{D}\). Fraction: \(0.625\times 2=1.25\to 1\), \(0.25\times 2=0.5\to 0\), \(0.5\times 2=1.0\to 1\), so \(0.101_2\).
### Answer
\(10011101_2\), \(9\mathrm{D}_{16}\), \(0.101_2\)

## Q2
### Given
8-bit pattern \(1101\,0110\).
### Find
The unsigned value, the two's-complement value, and the packed-BCD interpretation if valid.
### Solution
Unsigned: \(128+64+16+4+2=214\). Two's complement: MSB=1 so negative; invert \(0010\,1001\), add 1 \(\to 0010\,1010=42\), value \(-42\). BCD nibbles 1101 and 0110: 1101 is not a BCD digit (13), so packed BCD is invalid.
### Answer
Unsigned 214; two's complement \(-42\); BCD invalid

## Q3
### Given
Binary \(b=1011_2\).
### Find
The 4-bit Gray code, then convert that Gray code back to binary.
### Solution
\(g_3=b_3=1\), \(g_2=b_3\oplus b_2=1\oplus 0=1\), \(g_1=b_2\oplus b_1=0\oplus 1=1\), \(g_0=b_1\oplus b_0=1\oplus 1=0\). Gray \(1110\). Back: \(b_3=1\), \(b_2=1\oplus 1=0\), \(b_1=0\oplus 1=1\), \(b_0=1\oplus 0=1\). Recovers \(1011\).
### Answer
Gray \(1110_2\); reverse conversion \(1011_2\)

## Q4
### Given
\(f(A,B,C)=\sum m(0,2,3,7)\).
### Find
A minimal SOP using a 3-variable K-map (or equivalent grouping).
### Solution
Minterms: \(\bar A\bar B\bar C\), \(\bar A B\bar C\), \(\bar A B C\), \(A B C\). Group \(m0+m2=\bar A\bar C\), group \(m2+m3=\bar A B\), group \(m3+m7=BC\). Minimal: \(\bar A\bar C+BC\) (covers \(m2\) twice; \(m0,m2,m3,m7\) all covered). Check: \(\bar A B\) is not needed because \(m2,m3\) are in the other two groups? \(m3=ABC'?\) \(m3=\bar A B C\) is in \(BC\) only if \(A=1\)? \(BC\) covers \(m3=\bar A BC\) and \(m7=ABC\). \(\bar A\bar C\) covers \(m0=\bar A\bar B\bar C\) and \(m2=\bar A B\bar C\). Yes, \(f=\bar A\bar C+BC\).
### Answer
\(f=\bar A\bar C+BC\)

## Q5
### Given
Even-parity ASCII transmission of the character whose 7-bit code is \(1001101\) (MSB first).
### Find
The 8-bit frame with the parity bit appended as the new MSB, and the Hamming distance to the all-zero word.
### Solution
Seven bits have four 1s (even). Even parity bit is 0. Frame \(0\,1001101\). Distance to 0 is the number of 1s \(=4\).
### Answer
\(01001101\), distance \(4\)

## Q6
### Given
8-bit two's complement addition: \(0100\,1110 + 0011\,1010\).
### Find
The 8-bit sum and whether signed overflow occurred.
### Solution
Binary add: \(01001110+00111010=10001000\). Both addends are positive (MSB 0) and the sum pattern has MSB 1, so signed overflow occurred. Equivalently carry into the MSB is 1 and carry out of the MSB is 0, XOR = 1. The stored pattern is \(10001000\) (which would read as \(-120\) if misinterpreted as a valid two's-complement sum). Unsigned wrap is 136 \(\equiv 8\) plus a carry-out; the question asked for signed overflow.
### Answer
Bit pattern \(10001000\); signed overflow = yes
