# Combinational logic: gates, mux, decoder, adder, hazards

Combinational logic is memoryless: outputs are functions of present inputs only (after a delay). This unit turns Boolean algebra into gate networks, catalogues the MSI blocks every datasheet still names (MUX, DEMUX, decoder, encoder, adder, comparator), and treats static hazards so that a glitch is not a surprise.

## Concepts

Gate primitives: AND, OR, NOT, NAND, NOR, XOR, XNOR. Positive logic: high = 1. Negative logic (rare in UG except as a warning) swaps AND/OR interpretations. NAND-NAND realisation of SOP: De Morgan says an AND-OR is a NAND of NANDs (with inverted inputs becoming bubbles that cancel on NAND inputs). NOR-NOR realises POS. Mixed-logic drawing (bubbles on wires) is the professional way to keep inversion from generating extra inverters.

Two-level vs multi-level: two-level is fast (two gate delays) and expensive in literals; multi-level factored logic saves gates and often maps better onto LUTs and standard cells. Technology mapping is a later CAD course; here, count gate delays along the longest path as \(t_{pd}\).

Decoder: \(n\) inputs, \(2^n\) one-hot outputs (enable permitting). 2-to-4, 3-to-8 (74138), 4-to-16. Building a large decoder from smaller ones: use the enable pins as the extra address bits. Encoder: the reverse, usually *priority* encoder so that if two inputs are high the larger index wins (74148). Without priority, two-hot is undefined.

Multiplexer: \(2^n\) data inputs, \(n\) select bits, one output. \(Y=\sum_i d_i m_i(s)\). A MUX is a universal combinational block: tie the data pins to 0, 1, or literals and you realise any \(n\)-variable function of the select lines (Shannon expansion). Demultiplexer: one data in, \(2^n\) outputs selected by address — a decoder with an enable used as data.

Adders. Half adder: \(S=A\oplus B\), \(C=AB\). Full adder: \(S=A\oplus B\oplus C_{in}\), \(C_{out}=AB+C_{in}(A\oplus B)\) (or majority \(AB+BC+CA\)). Ripple-carry: FA chain, \(t_{pd}\approx n t_{carry}\). Carry-lookahead: generate \(G_i=A_i B_i\), propagate \(P_i=A_i\oplus B_i\) (or \(A_i+B_i\)), \(C_{i+1}=G_i+P_i C_i\), group lookahead for 4 bits (74182). Carry-select and carry-skip are named for exams. BCD adder: 4-bit binary add plus a correction (add 6) when the sum \(>9\) or a nibble carry occurs. Comparator: identity \(XNOR\) tree plus a magnitude circuit; 7485 is the TTL part.

ALU idea: a 1-bit slice that MUX-selects AND/OR/XOR/ADD. Bit-slice 74181 is historical; the concept is current.

Other MSI: XOR as controlled inverter, parity tree, 7-segment decoder (BCD to a,b,c,d,e,f,g), barrel of tri-states. Tri-state: output can be 0, 1, or Z (high impedance). A bus is several tri-states tied together with at most one enabled; two enabled with opposite values is contention (smoke, or at least \(I_{OL}\) fights \(I_{OH}\)).

Hazards. A static-1 hazard: output should stay 1 but glitches 0 because one AND term turns off before another turns on, when a single input changes. Cause: adjacent minterms not covered by a common product in the SOP. Cure: add the consensus term (the prime implicant that covers the transition). Static-0 hazard is the POS dual. Dynamic hazard: multiple transitions on a single input change, from multi-level reconvergent fan-out. Function hazards exist when two inputs change at once (no single-input-change cover can fix those; use Gray codes or synchronise). Essential hazards belong to asynchronous sequential circuits (next unit).

Delay model: inertial delay ignores pulses narrower than a threshold; transport delay copies them. UG timing analysis uses a single \(t_{pd}\) per gate unless min/max is given. Contamination delay \(t_{cd}\) (min delay) matters for hold time in sequential circuits.

Don't-cares in MUX/decoder implementations: unused decoder outputs, or MUX data pins that correspond to unused input vectors, may be tied to 0 or to a convenient literal.

Parity generators and checkers are XOR trees plus an optional invert for odd parity. A 9-bit even-parity transmitter on 8 data bits is one XOR reduction. Comparators of magnitude (A>B, A=B, A<B) cascade: the 7485 has cascade inputs so that you can stack 4-bit slices. For a UG numerical, equality is AND of XNORs; greater-than is a priority inspection from the MSB.

Open-collector AND-OR-invert (AOI) gates were the TTL way to do wired combination. CMOS uses transmission-gate muxes and static CMOS AOI cells instead. The Boolean function is the same; the electrical rules are unit 12.

## Equations

MUX:

\[
Y=\sum_{i=0}^{2^n-1} d_i\, m_i(s_{n-1},\ldots,s_0).
\]

Full adder:

\[
S=A\oplus B\oplus C_{in},\qquad C_{out}=AB+BC_{in}+CA.
\]

Lookahead:

\[
C_{1}=G_0+P_0 C_0,\quad C_{2}=G_1+P_1 G_0+P_1 P_0 C_0,\quad \ldots
\]

BCD correction: if \(S_3S_2S_1S_0>1001\) or carry, add \(0110_2\).

Static-1 hazard on \(x\) in SOP: if two minterms that differ only in \(x\) are in different products, the consensus of those products is required.

Gate delay path: \(t_{pd,path}=\sum t_{pd,i}\). XOR from four NAND: 3 NAND delays typical.

## Methods

1. From spec to gates: truth table or \(\sum m(\cdot)\), K-map, SOP, NAND-NAND. Count literals and gate delays.
2. MUX implementation of \(f(A,B,C)\): put \(A,B\) on select (say), Shannon-expand on those, residual functions of \(C\) are 0, 1, \(C\), \(\bar C\) on the data pins.
3. Decoder + OR: OR together the minterm outputs that are 1. Decoder + NOR is the maxterm dual.
4. Adder timing: ripple — delay proportional to width. If a question gives \(t_{XOR}\) and \(t_{AND/OR}\), the carry path is the AND-OR, not the sum XOR.
5. Hazard hunt: list single-input transitions that should keep \(f=1\). If the two minterms are not in one circled group, add the bridging implicant.
6. Tri-state: write an enable table; prove at most one driver is on.

## Mistakes

- Building a MUX from a decoder and then forgetting the data AND-gates (a decoder is not a MUX).
- Priority encoder: treating two-hot as the binary OR of the indices.
- Full adder carry as \(AB+C_{in}\) (missing the rest of the majority).
- BCD: adding 6 always, including when the binary nibble is already \(\le 9\).
- Hazard: adding a redundant term for a transition that already shares a product, or failing to add one for a corner-to-corner K-map pair that is adjacent in Gray sense.
- Assuming combinational logic has no glitches because "there is no memory." Hazards *are* glitches in combinational logic.
- NAND-NAND: leaving the output NAND as an AND because "SOP used AND-OR."
- Select-bit order on a MUX: swapping MSB/LSB permutes the data pins and implements the wrong function.
- Tri-state bus with two enables overlapping for a nanosecond: that is still contention if \(t_{pd}\) overlap exists; use break-before-make or a MUX.
- Counting decoder outputs as active-high when the 74138 is active-low. Polarity of the part is in the datasheet.

Worked MUX-as-function example that students under-use: any 3-variable \(f\) is four residual functions of the remaining variable. Those residuals are only \(0,1,C,\bar C\). If you ever need a residual like \(BC\), you chose the wrong select bits or you need a larger MUX. An 8-to-1 MUX can implement any 3-variable function by tying data pins to 0 or 1 (the minterm list). A 4-to-1 plus a few NOT gates is the usual cheaper drawing.

Carry-lookahead delay is why 4-bit groups exist. The 74181 ALU plus 74182 lookahead is a museum piece that still teaches \(G\) and \(P\). For a 16-bit add, four 4-bit groups and one lookahead compute \(C_4,C_8,C_{12},C_{16}\) in a few gate delays instead of 16 ripple carries. Exam algebra stops at writing \(C_2=G_1+P_1 G_0+P_1 P_0 C_0\); you do not have to expand \(C_{16}\).

Seven-segment decoder: BCD to segments. Don't-cares on 1010–1111 may be mapped to blank, to "garbage", or to hex digits A–F. Lab mistake: driving common-cathode vs common-anode parts with the wrong polarity.

Hazards vs races vs metastability. A hazard is combinational. A race is asynchronous sequential (two state variables changing). Metastability is a flip-flop timing violation. Using the three words as synonyms loses marks.

Combinational design is a pipeline: specify, minimise, map to the allowed parts, then check delay and single-input glitches. The next unit adds clocks. If a glitch on a combinational output clocks a FF, you have already failed the next unit; AND the decode with a clock strobe or use a synchronous enable. Fan-in: a 12-input AND built from 2-input gates is a tree, not one gate; delay is logarithmic in fan-in. Fan-out: a single output driving 20 inputs plus 30 cm of wire may violate \(t_{pd}\) even if the Boolean function is one gate. Buffer the net. Karnaugh leftover: after a minimal SOP, check each pair of adjacent 1s. If any pair is not co-circled, you still have a static-1 hazard even though the Boolean function is already minimal in literals. Hazard-free covers are allowed to be slightly larger than a minimum-literal cover; that is the point of the consensus term. Decoder enable trees: a 4-to-16 from two 3-to-8 parts uses the extra address bit on complementary enables. Write the enable Boolean before you wire it, or one of the two chips stays dark. Priority-encoder "first one wins" is always from a documented end (usually the highest index); reversing the priority without renaming the outputs is a specification bug. Barrel shifters are cascaded MUXes; a 32-bit rotate is still combinational if you pay the MUX depth in delay. That delay is why barrel shifters are pipelined in CPUs.
