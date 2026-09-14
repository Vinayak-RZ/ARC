# Memory, PLA/PAL, and HDL intro (Verilog/VHDL)

Digital systems that outgrow a handful of flip-flops store bits in arrays and specify those arrays in a hardware description language. UG EE courses treat ROM, RAM, and the PLA/PAL/CPLD/FPGA ladder far enough to decode a part, compute capacity, and read a page of Verilog or VHDL without claiming to be an ASIC course.

## Concepts

Memory organisation: \(2^n\) addresses of \(m\)-bit words, capacity \(2^n\times m\) bits. A 32 K × 8 device has 15 address pins, 8 data pins, and \(32\times 1024\times 8=256\) Kbits. Byte vs word addressing, little-endian vs big-endian (byte order inside a 16- or 32-bit word). Chip-select \(\overline{CS}\), output-enable \(\overline{OE}\), write-enable \(\overline{WE}\). Several chips expand width (tie addresses, separate data nibbles) or depth (decode extra address bits onto \(\overline{CS}\)).

ROM (read-only at run time). Mask ROM is programmed at fabrication. PROM is one-time fusible. EPROM (2532-era) is UV-erased. EEPROM and Flash are electrically erasable; Flash erases by blocks. ROM implements combinational logic: the address is the input vector, the data is the output. A truth table of \(n\) inputs and \(m\) outputs is a \(2^n\times m\) ROM. That is often cheaper than gates when \(n\) is moderate and the function is messy (microcode, sine tables, 7-segment plus extras).

RAM. SRAM: six-transistor (or 8T) bit cell, latch, fast, used as registers, caches, FPGA LUTs' cousins. DRAM: one transistor plus a capacitor, dense, needs refresh (every few milliseconds), row/column multiplexed addresses (RAS/CAS). UG depth: know that DRAM is analog-in-a-trench and that a controller refreshes; do not design a DDR PHY. Dual-port SRAM appears in FIFOs. Volatile vs non-volatile: RAM loses state at power-off unless battery-backed; ROM/Flash does not.

PLA (programmable logic array): programmable AND plane and programmable OR plane. You program which literals enter which product, and which products enter which sum. PAL/GAL: programmable AND, *fixed* OR (fewer fuses, faster historically). PLA can share products across outputs; PAL cannot (each OR has a dedicated AND set). CPLD: PAL-like blocks plus an interconnect. FPGA: LUTs (small memories that implement any \(k\)-input function) plus flip-flops plus programmable routing. A 4-LUT is a 16×1 SRAM. UG exam question: "which architecture has both planes programmable?" Answer: PLA.

FSM in ROM: address = {state, inputs}, data = {next-state, outputs}. That is a microcoded controller. One-hot vs encoded state is a ROM-width trade.

HDL. Verilog and VHDL are *concurrent* languages: `always` / `process` blocks describe hardware that exists in parallel, not a CPU program that runs in order except inside a clocked block. Two modelling levels UG must distinguish:

- Structural: instances and wires (`and u1(y,a,b);`).
- Behavioural combinational: `assign y = a & b;` or a process with a full sensitivity list and every output assigned on every path.
- Sequential: `always @(posedge clk)` / `rising_edge(clk)` with non-blocking `<=` in Verilog for registers.

Blocking `=` vs non-blocking `<=` in Verilog sequential blocks: use `<=` for flip-flops. Mixing them is a race in simulation. Incomplete sensitivity lists in combinational `always @(*)` (older `@ (a or b)`) infer latches. Incomplete case / if without a default infers latches. That is the #1 HDL exam and lab failure.

VHDL types: `std_logic` (`0,1,Z,X,-,H,L,W,U`) vs Verilog 4-state `0,1,x,z`. Resolved types for buses. `ieee.numeric_std` for arithmetic; `std_logic_arith` is the old trap.

Testbench: stimulus on inputs, clock generator, compare outputs; HDL-simulators (Icarus, GHDL, ModelSim). Synthesis vs simulation: `initial`, `#delay`, and file I/O are simulation-only. What you synthesise is registers + combinational clouds + memories the tool can infer (`reg [7:0] mem [0:255];` plus a clocked write).

Reset in HDL: async `if (!rst_n) q<=0; else q<=d;` vs sync reset in the clocked branch. Match the board.

This unit does not replace a digital-design course's RTL style guide. It is enough to read a 20-line module, say whether it infers a latch, a FF, or pure combo, and to size a memory from its pinout.

Address decoding to mix RAM and ROM on a microprocessor bus (the microprocessors elective) is the same \(\overline{CS}\) decoder as depth expansion. Partial decoding (using only some address bits) aliases the memory into multiple holes; full decoding is unique. UG numericals that give a map `0x0000–0x1FFF = ROM` are asking for A15–A13 = 000 on \(\overline{CS}_{ROM}\).

Flash vs EEPROM endurance: \(10^4\)–\(10^6\) erase cycles typical, so a wear-levelled log is firmware, not a register file. SRAM endurance is unlimited for UG purposes. FRAM and MRAM exist; name them and move on.

PLA programming table: rows are product terms, columns are literals (true and complement) plus output OR connections. A fuse (or EEPROM bit) present means the literal is *not* in the product (old PAL fuse-blown-to-disconnect convention varies by vendor — read the diagram in the question). UG: count AND rows and OR inputs, do not memorise a 1980s fuse map.

Block RAM vs distributed RAM on an FPGA: BRAM is a hard 18 kbit (or similar) column; distributed RAM is LUTs used as small memories. Inferring a huge async RAM in LUTs is a synthesis accident. Clock the memory. Dual-port contention on the same address in one cycle is undefined unless the datasheet defines write-write priority; avoid it. ROM code tables in reports should be listed in address order with hex data, not as a C array that hides the address map from a marker who is checking the chip-select decode against the full printed board memory map.

## Equations

Capacity:

\[
C_{\mathrm{bits}}=2^{n_{\mathrm{addr}}}\times m_{\mathrm{width}}.
\]

Depth expansion: extra decoder bits \(k\) give \(2^k\) chips of the same width. Width expansion: \(p\) chips in parallel give width \(p m\) at the same depth.

ROM as logic: \(n\) inputs \(\Rightarrow\) \(2^n\) rows. PLA product terms: up to the number of AND rows, independent of \(2^n\) if the function is sparse.

4-LUT:

\[
\mathrm{bits}=2^4=16
\]

per LUT (plus optional FF).

DRAM refresh (order-of-magnitude): \(t_{\mathrm{REF}}\sim 32\)–\(64\,\mathrm{ms}\) for the whole array, distributed as one row every \(t_{\mathrm{REF}}/N_{\mathrm{rows}}\).

## Methods

1. Pin count: \(n=\log_2(\text{words})\), plus data, plus \(\overline{CS},\overline{OE},\overline{WE}\), plus power. Multiplexed DRAM addresses roughly halve the address pins.
2. Expand: draw a decoder onto \(\overline{CS}\) for depth; slice the data bus for width.
3. ROM realisation: list the truth table in address order; that *is* the ROM contents. Unused addresses are 0 or don't-care.
4. PLA vs PAL: count unique product terms. If several outputs share a product, PLA saves rows; PAL repeats them.
5. HDL review: (a) sensitivity list complete? (b) every branch assign every combo output? (c) clocked blocks use non-blocking and only registers on the LHS? (d) no `#delay` in synthesis code.
6. Infer: a clocked `q<=d` is a FF. An `always @*` with an output that is sometimes not assigned is a latch. An `assign` is combo.

## Mistakes

- 32 Kbit vs 32 K×8. Always name words × bits.
- Treating EEPROM as RAM because it is "electrically writable." Write cycles are slow and limited; it is not a register file.
- DRAM without refresh in a timing budget that lasts seconds.
- PLA drawn as a PAL (fixed OR).
- FPGA "gates" quoted from a marketing LUT-to-gate conversion. Count LUTs and FFs.
- Verilog: `always @(posedge clk) q = d;` (blocking) in a multi-FF block, then wondering why simulation order changed the result.
- Incomplete `case` without `default`, inferring latches in what was supposed to be a MUX.
- Sensitivity list `always @(a)` on `y=a&b`, so `b` changes are missed in simulation (synthesis may still be correct — the sim/synth mismatch is the bug).
- Using HDL delays as hardware delays. `#5` does not synthesise a 5 ns inverter.
- Bidirectional data pins without a tri-state enable, so read and write fight.

Harvard vs von Neumann is a computer-architecture sentence: instructions and data in one memory or two. UG microprocessors (the elective pack) care; this unit only needs to know that a ROM can hold a program and a RAM the variables.

FIFO: two clocks, two addresses, a dual-port SRAM plus full/empty flags. Metastability at the gray-coded pointers is a known digital-design pattern; mention it, do not design it here.

Error-correcting memories (ECC DRAM) add Hamming bits per line. A UG exam may ask you to size the extra bits for SEC on a 64-bit word (7 Hamming bits plus optionally an overall parity for SECDED). That is unit 09's Hamming idea applied to a DIMM.

HDL style that synthesis likes: one sequential process/always for FFs, one combinational process/always or continuous assigns for next-state and outputs. Two-process VHDL FSM is the textbook form; one-process is common in Verilog. Both are legal if reset and defaults are complete.

Memory is an array with an address decoder. Programmable logic is memory used as a truth table. HDL is a way to *describe* those structures so that a tool can build them — not a software program that "runs on" the FPGA unless you put a CPU there on purpose. If a simulation shows a latch you did not draw, fix the HDL; do not congratulate yourself on free memory. Synthesis reports (inferred RAM, inferred latch, inferred FF counts) are the checklist; read them.
