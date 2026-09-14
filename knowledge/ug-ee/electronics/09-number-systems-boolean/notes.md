# Number systems, codes, and Boolean algebra

Digital electronics begins with how we write numbers and how we manipulate truth values. UG EE courses expect fluent conversion among decimal, binary, octal, and hexadecimal, the usual codes (BCD, Gray, Excess-3, ASCII as a named table), signed representations, and Boolean algebra through De Morgan and canonical forms. Gates as hardware wait for the next unit; the algebra here is the specification language.

## Concepts

A positional number system of radix \(r\) writes \(N=\sum_k d_k r^k\) with digits \(0\le d_k<r\). Binary (\(r=2\)) is the hardware radix because a node is high or low. Hexadecimal (\(r=16\), digits 0–9 then A–F) is binary grouped by fours: one hex digit is a nibble. Octal groups by threes. Conversion decimal→binary uses repeated division by 2 for the integer part and repeated multiplication by 2 for the fraction; the other direction is a weighted sum. Fractional binaries terminate only if the denominator's prime factors are 2; 0.1 decimal is a repeating binary fraction, which is why `0.1 + 0.2` surprises people in floating point (that surprise is a DSP elective; here, just know that many decimal fractions have no finite binary representation).

Bits, nibbles, bytes, words: a byte is 8 bits in every UG machine this pack cares about. The MSB is the leftmost digit in the usual writing; in little-endian *memory* the least-significant *byte* is stored first. Do not confuse bit order with byte order.

Signed integers. Sign-magnitude wastes a bit and has two zeros. Ones' complement (bitwise not) also has two zeros and awkward end-around carry. Two's complement is the representation of record: negate by invert-plus-one, range of an \(n\)-bit word is \(-2^{n-1}\) to \(2^{n-1}-1\), addition is identical to unsigned addition, and overflow is carry-into-MSB XOR carry-out-of-MSB. Arithmetic right shift preserves the sign bit. UG exam favourite: interpret the same bit pattern as unsigned, as two's complement, and as BCD, and get three different magnitudes.

BCD (8421): each decimal digit encoded as a 4-bit nibble 0000–1001. 1010–1111 are unused and must be detected in BCD adders (add 6 to correct). Excess-3: BCD plus 3, self-complementing (9's complement is bitwise not), historically used in some decimal machines. 2421 and 84-2-1 appear as "name this code" questions. Packed BCD stores two digits per byte; unpacked stores one.

Gray code: adjacent codes differ in one bit. Used on rotary encoders so that a transition cannot produce a spurious intermediate value (in binary, 0111→1000 flips four bits; a Gray encoding of the same step flips one). Binary-to-Gray: \(g_i=b_i\oplus b_{i+1}\) with \(g_{\mathrm{MSB}}=b_{\mathrm{MSB}}\). Gray-to-binary: XOR-scan from the MSB. Reflected Gray is the usual construction.

ASCII: 7-bit character code, often stored in an 8-bit byte with a 0 or a parity bit. '0'–'9' are 0x30–0x39, 'A'–'Z' 0x41–0x5A. Parity: even parity appends a bit so the total number of 1s is even; odd parity the opposite. Hamming distance of two words is the number of differing bits; a code with minimum distance \(d\) can detect \(d-1\) errors and correct \(\lfloor(d-1)/2\rfloor\). Hamming SEC codes (distance 3) are the UG example of extra parity bits at positions 1, 2, 4, … .

Boolean algebra is the algebra of \(\{0,1\}\) with OR (\(+\)), AND (\(\cdot\)), and NOT. Huntington axioms give commutativity, distributivity of each over the other, identities 0 and 1, and complements. Useful theorems: idempotent, absorption \(X+XY=X\), consensus, De Morgan \(\overline{X+Y}=\bar X\bar Y\), \(\overline{XY}=\bar X+\bar Y\). Duality: swap \(+\) and \(\cdot\), 0 and 1. Shannon expansion (Boole's expansion): \(f=x f_x + \bar x f_{\bar x}\).

Canonical forms. Minterm: a product that includes every variable once, true for exactly one input vector. Maxterm: a sum true for all but one vector. Any function is a sum of minterms (canonical SOP, listed as \(\sum m(i)\)) or a product of maxterms (\(\prod M(i)\)). Incomplete functions have don't-cares \(d(j)\) that may be taken as 0 or 1 to help simplification.

Simplification. Algebraic: apply theorems until the literal count stops falling. Karnaugh map: 2, 3, 4, sometimes 5 variables, Gray-coded axes, circle powers-of-two groups of 1s (and don't-cares as 1s when helpful). Prime implicants, essential prime implicants, then a minimal cover. Quine–McCluskey is the tabular form of the same idea, needed when there are more variables than a K-map likes. The result is a two-level SOP or POS that maps onto AND-OR or OR-AND (or NAND-NAND, NOR-NOR) in the next unit.

XOR and XNOR are not in the Huntington basis but are linear over GF(2): \(X\oplus Y=X\bar Y+\bar X Y\). Parity, adders, and Gray conversion are XOR circuits. XOR is its own inverse.

Completeness: NAND is functionally complete (so is NOR). You can build any Boolean function from NAND alone, which is why TTL catalogues led with 7400.

## Equations

Positional evaluation:

\[
N=\sum_{k=-m}^{n} d_k r^k.
\]

Two's complement of an \(n\)-bit pattern \(b\): the integer is \(-b_{n-1}2^{n-1}+\sum_{k=0}^{n-2}b_k 2^k\). Negation: \(\overline{b}+1\) (mod \(2^n\)).

Overflow (two's complement add): \(C_{n-1}\oplus C_n\).

Binary \(\to\) Gray:

\[
g_{n-1}=b_{n-1},\qquad g_k=b_{k+1}\oplus b_k.
\]

Gray \(\to\) binary:

\[
b_{n-1}=g_{n-1},\qquad b_k=b_{k+1}\oplus g_k.
\]

De Morgan (n variables):

\[
\overline{\sum_i x_i}=\prod_i \bar x_i,\qquad\overline{\prod_i x_i}=\sum_i \bar x_i.
\]

Canonical SOP:

\[
f=\sum_{i:f(i)=1} m_i.
\]

Hamming distance: \(d(u,v)=\sum_k (u_k\oplus v_k)\). Even parity bit \(p=\bigoplus_k b_k\).

## Methods

1. Conversions: integer — divide by the new radix, remainders are digits from LSB. Fraction — multiply by the new radix, take the integer parts. Check by converting back.
2. Hex as binary: write each hex digit as four bits, MSB of the nibble on the left. Octal: three bits.
3. Two's complement arithmetic: add as unsigned, discard the final carry, then interpret. To subtract, add the two's complement.
4. BCD add: add nibble-wise in binary, if a nibble is \(>9\) or there was a nibble carry, add 0110 to that nibble.
5. Boolean: put the function in SOP, K-map it, read a minimal SOP, optionally De-Morgan into NAND-NAND.
6. Don't-cares: include a don't-care cell in a group only if it makes the group larger (fewer literals). Never make a new group of only don't-cares.
7. Completeness constructions: NOT \(=\mathrm{NAND}(x,x)\), AND \(=\mathrm{NOT}(\mathrm{NAND}(x,y))\), OR \(=\mathrm{NAND}(\bar x,\bar y)\).

## Mistakes

- Writing 10 decimal as 10 binary. 10 decimal is 1010 binary or 0xA.
- Hex digit F as 15 decimal and then as 1111 binary — those are consistent — but treating F as 16.
- Two's complement: inverting without adding one (that is ones' complement).
- Claiming 8-bit two's complement ranges to \(+128\). It ranges to \(+127\); \(-128\) is 0x80 and has no positive counterpart in 8 bits.
- BCD: allowing 1100 as a digit.
- Gray: XOR-ing with the *left* neighbour vs the *right* and mixing the index convention. Pick MSB-first and stick to it.
- K-map: grouping 6 cells (not a power of two), or wrapping incorrectly (the four corners of a 4-variable map *are* adjacent).
- Forgetting don't-cares and producing a larger SOP than needed.
- Boolean: distributing AND over AND, or writing \(\overline{x+y}=\bar x+\bar y\).
- Parity: even vs odd, and whether the parity bit itself is included in the count — it is.
- ASCII: assuming 'A' is 0x01 or 65 decimal mixed with hex 65.

Exam arithmetic should be done in hex when the word is a multiple of 4 bits, and in binary when a single bit matters (overflow, Gray). Convert to decimal only at the end if the question asked for a magnitude. Mixing radices in the same line of working is how 0xA0 becomes "160 binary".

BCD addition drill. \(58_{10}+47_{10}\): packed BCD 0101 1000 + 0100 0111 = 1001 1111. Low nibble 1111 > 9, add 0110 → 1 0101 with a nibble carry into the high nibble. High nibble 1001+1=1010, which is also >9, add 0110 → 1 0000 plus the previous low nibble 0101, result 0001 0000 0101 which is 105. That is the decimal 105 you wanted. Skipping the +6 correction is the classic error.

K-map wrapping. A 4-variable map is a torus: the leftmost column is adjacent to the rightmost, the top row to the bottom, and the four corners form a group of 4. Groups of 8 are a single literal. Groups of 16 are 1. Never circle 3, 5, 6, 7, or 9 cells.

XOR identities worth memorising: \(X\oplus 0=X\), \(X\oplus 1=\bar X\), \(X\oplus X=0\), \(X\oplus\bar X=1\), association and commutation, and \(X\oplus Y=\overline{X\oplus\bar Y}\). Parity of a bus is a tree of XORs; the tree depth is \(\lceil\log_2 n\rceil\) XOR delays.

Number systems are mechanical. The only conceptual trap is mixing the interpretation (unsigned, two's complement, BCD) of a stored bit pattern. Always name the code before you name the magnitude. A byte 0xFF is 255 unsigned, \(-1\) in 8-bit two's complement, and invalid as packed BCD. Three sentences, three answers, same bits. Hamming SEC on a 4-bit nibble uses three parity bits at positions 1, 2, and 4; the syndrome is the binary index of the flipped bit, or zero if none. That construction reappears when sizing ECC on memory words in the memory unit. Excess-3 self-complement is the 9's complement trick: bitwise invert 0100 (excess-3 for 1) to get 1011, which is excess-3 for 8, and \(1+8=9\).
