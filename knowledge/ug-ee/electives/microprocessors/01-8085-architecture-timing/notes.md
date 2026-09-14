# 8085 architecture, timing, and interrupts

The Intel 8085 is the usual first microprocessor in an Indian UG EEE lab: an 8-bit CPU, 16-bit address bus, multiplexed AD0–AD7, and a small, memorisable interrupt structure. This unit is the programmer’s model, bus machine cycles, T-state arithmetic, and the five hardware interrupts. It is not an SoC bring-up, an 8086 protected-mode course, or a copy of any commercial chapter.

## Concepts

The 8085 executes stored programs. A 16-bit program counter (PC) points at the next instruction byte in a 64 KiB address space. An 8-bit accumulator A is the primary ALU operand and the destination of most arithmetic. Six general 8-bit registers B, C, D, E, H, L pair as BC, DE, HL; HL is the usual memory pointer (the “M” operand). A 16-bit stack pointer SP grows downward: PUSH decrements then writes, POP reads then increments. The flags live in a status register F, of which five bits are architected for UG use: sign S (MSB of the result), zero Z, auxiliary carry AC (carry from bit 3 to bit 4, for BCD/DAA), parity P (even parity of the result byte in the 8085), and carry CY (unsigned overflow, also the rotate destination). The unused bits of F are not a free scratch pad.

Internally the CPU is a register file, an 8-bit ALU, an incrementer/decrementer for PC and SP, an instruction decoder and a timing/control unit that sequences machine cycles. Externally the buses are: AD0–AD7 multiplexed address/data, A8–A15 high address, ALE (address latch enable) which must clock an external 8-bit latch so the low address survives while AD becomes data, RD and WR (active low), IO/M (high for I/O machine cycles, low for memory), S0 and S1 status bits that encode the machine-cycle type, CLK OUT, RESET IN/OUT, READY (stretch wait states), HOLD/HLDA for DMA, SID/SOD for a 1-bit serial port, and the interrupt pins TRAP, RST 7.5, RST 6.5, RST 5.5, INTR, plus INTA.

A **T-state** is one period of the internal clock. With a 6 MHz crystal the internal clock is 3 MHz; \(T=1/3\,\mu\mathrm{s}\approx 333\,\mathrm{ns}\). A **machine cycle** is one bus transaction: opcode fetch (typically 4 T-states, sometimes 6 if the opcode is the first byte of an interrupt acknowledge or a halt-related cycle in older notes — UG 8085 opcode fetch is 4 T), memory read (3 T), memory write (3 T), I/O read (3 T), I/O write (3 T), interrupt acknowledge (6 T for INTR’s RST-byte fetch). An **instruction cycle** is one or more machine cycles that complete one opcode. MOV A,B is a register-to-register move: one opcode fetch, 4 T, no memory operand. MOV A,M is opcode fetch plus a memory read of (HL): 4+3=7 T. MVI A,data is opcode fetch plus a memory read of the immediate byte: 7 T. LDA addr is four machine cycles (opcode, low address, high address, data read): \(4+3+3+3=13\) T. STA is 13 T with a write on the last cycle. CALL is 18 T (opcode, two address bytes, two stack writes of PC). RET is 10 T (opcode plus two stack reads).

Opcode fetch timing, the picture every lab asks you to sketch: T1 puts PC on the address bus, ALE high then falling to latch AD0–AD7; IO/M is low; S1 S0 encode fetch. T2 asserts RD, memory drives the opcode onto AD. T3 samples the opcode, releases RD, increments PC. T4 is internal decode/execute for register instructions; if the instruction needs more bytes or a memory operand, further machine cycles follow. READY sampled in T2 can insert WAIT T-states if memory is slow. HOLD sampled can yield the bus after the current machine cycle (HLDA).

Addressing modes in the 8085 set: implied (CMA, RAL), register (MOV r1,r2), immediate (MVI, LXI, ADI), direct 16-bit address (LDA, STA, LHLD, SHLD, JMP, CALL), register-indirect through HL (MOV M,r; ADD M), and the stack (PUSH/POP, CALL/RET). There is no 16-bit arithmetic ALU; DAD rp adds a register pair to HL using the 8-bit ALU twice, 10 T.

Interrupts are how the outside world preempts the fetch-execute loop. **TRAP** is non-maskable, edge-and-level sensitive (both a rising edge and a held-high level are required, which rejects brief glitches), vector \(0024\mathrm{H}\). **RST 7.5** is maskable, edge-sensitive (a latch remembers the rising edge), vector \(003C\mathrm{H}\). **RST 6.5** and **RST 5.5** are maskable, level-sensitive, vectors \(0034\mathrm{H}\) and \(002C\mathrm{H}\). **INTR** is maskable, level-sensitive, and has no fixed vector: the CPU issues INTA and the interrupting device must put an instruction on the data bus, conventionally an RST n opcode, which vectors to \(8n\). Priority, highest first: TRAP, RST 7.5, RST 6.5, RST 5.5, INTR. After RESET, the maskable interrupts are disabled until EI. DI disables them. TRAP cannot be masked by EI/DI.

**SIM** (Set Interrupt Mask) writes the accumulator into the mask latch and optionally into SOD. Relevant A bits as taught at UG: bit 0 masks RST 5.5, bit 1 masks RST 6.5, bit 2 masks RST 7.5, bit 3 is MSE (must be 1 to update those masks), bit 4 resets the RST 7.5 edge latch, bit 6 is SOD data, bit 7 is SOD enable. **RIM** (Read Interrupt Mask) loads A with pending and mask status: bits 0–2 current masks, bit 3 IE (interrupt enable flip-flop), bits 4–6 pending 5.5/6.5/7.5, bit 7 SID. A polling loop can RIM and test pending bits without taking the interrupt.

On an accepted interrupt the CPU completes the current instruction, disables maskable interrupts (except that TRAP has its own flip-flop story: nested TRAP is blocked until the TRAP service executes EI or RET, depending on the lecture; UG exams usually say “TRAP disables further TRAP until the service completes”), pushes PC onto the stack (high then low, SP decremented twice), and loads PC from the vector. The service routine ends with EI (if maskable interrupts should resume) then RET, or with RIM/SIM as needed. RST n software instructions (\(C7, CF, D7, DF, E7, EF, F7, FF\)) vector to \(0000, 0008, \ldots, 0038\) and are also what an INTR device typically jams during INTA.

I/O in the 8085 is isolated: IN port and OUT port use an 8-bit port address duplicated on AD0–AD7 and A8–A15, IO/M high. Memory-mapped I/O is a board design choice: a device sits in the 64 KiB memory map and is accessed with MOV M, LDA, STA. Isolated I/O gives 256 ports and leaves memory intact; memory-mapped I/O uses the full instruction set on the device but spends address space.

Clock and reset: RESET IN low for several clocks clears PC to \(0000\mathrm{H}\), disables interrupts, and RESET OUT can reset peripherals. The first fetch after reset is therefore from location 0, which is why ROM is mapped low on trainer boards.

DMA: a device asserts HOLD; after the current machine cycle the CPU floats the buses and raises HLDA; the device runs memory cycles; HOLD release returns the CPU. SID/SOD are a 1-bit software UART used in trainers for a console at a few kilobaud, not a 16550.

This unit’s job in an exam is to convert a clock frequency into T-state time, add machine cycles for a named instruction, name the vector and type of each interrupt pin, and write the SIM accumulator for a given mask. The next unit hangs memory and 8255 on the multiplexed bus and introduces the 8051.

## Equations

T-state duration:
\[
T=\frac{1}{f_{\mathrm{clk}}},\qquad f_{\mathrm{clk}}=\frac{f_{\mathrm{xtal}}}{2}\ \text{(8085 internal clock)}.
\]
Instruction time:
\[
t_{\mathrm{ins}}=N_T\,T=\frac{N_T}{f_{\mathrm{clk}}}.
\]
Typical \(N_T\): MOV r,r \(4\); MOV r,M or MVI \(7\); LDA/STA \(13\); LHLD/SHLD \(16\); JMP \(10\); CALL \(18\); RET \(10\); PUSH \(12\); POP \(10\); DAD \(10\); IN/OUT \(10\).

RST vector:
\[
\text{vector}(\mathrm{RST}\,n)=8n\quad (n=0\ldots 7),\quad \text{e.g. RST }7\to 0038\mathrm{H}.
\]
Hardware RST 5.5 / 6.5 / 7.5 use \(8\times 5.5=44=002C\mathrm{H}\), \(52=0034\mathrm{H}\), \(60=003C\mathrm{H}\). TRAP \(\to 0024\mathrm{H}\).

SIM mask byte (MSE=1 to take effect):
\[
A = b_7 b_6 b_5 b_4 b_3 b_2 b_1 b_0,\quad
b_3=\mathrm{MSE}=1,\ 
b_2=\mathrm{M7.5},\ 
b_1=\mathrm{M6.5},\ 
b_0=\mathrm{M5.5}
\]
with \(1=\) masked (disabled).

PUSH of register pair rp = rh, rl:
\[
[SP-1]\leftarrow r_h,\quad [SP-2]\leftarrow r_l,\quad SP\leftarrow SP-2.
\]
POP is the reverse: \(r_l\leftarrow[SP]\), \(r_h\leftarrow[SP+1]\), \(SP\leftarrow SP+2\).

Memory size from address lines:
\[
N_{\mathrm{locations}}=2^{n_A}.
\]
Sixteen address bits \(\Rightarrow 65536\) bytes.

## Methods

To time an instruction: look up (or reconstruct) its machine-cycle list, sum T-states, divide by \(f_{\mathrm{clk}}\). Reconstruct from the bytes: one opcode fetch 4 T, each additional memory or I/O byte 3 T, plus extras for stack writes (CALL/PUSH) and for the longer INTA cycle. Do not use 8086 clocks.

To sketch opcode fetch: label T1–T4, ALE pulse in T1, RD low in T2–T3, IO/M low, address stable after the latch, data valid before the end of T3. Mention READY if the question shows wait states: each wait is one extra T with RD still low.

To service an interrupt in a numerical: identify pin, maskable or not, edge or level, vector. If SIM is asked, set MSE=1, put 1 on each mask bit that should be *disabled*, 0 on those that should remain enabled, and set R7.5 if the edge latch must be cleared. Load A then SIM.

To use the stack: draw SP and two memory cells. PUSH writes high register at \(SP-1\) and low at \(SP-2\). A CALL is a PUSH of PC then a load of the 16-bit target. Nested CALLs and interrupts both spend two bytes per frame; a missing RET leaks two bytes per call and will crash when SP walks into code.

To map ROM/RAM on a trainer: ROM at \(0000\mathrm{H}\) (reset and vectors), RAM for stack and data at a high page (often \(2000\mathrm{H}\)–\(27FF\mathrm{H}\) on 2 KiB RAM kits). Set SP to the top of RAM plus one (first PUSH uses the last RAM byte).

When counting machine cycles versus T-states, keep two columns. Examiners mix them: “how many machine cycles in LDA?” is 4, not 13.

## Mistakes

Using the crystal frequency as \(f_{\mathrm{clk}}\). A 6 MHz crystal gives a 3 MHz internal clock; T-states at 167 ns would be wrong.

Saying MOV A,B takes 7 T because “MOV is a memory instruction.” Register MOV is 4 T; M is the memory operand.

Confusing RST 7 (software, vector \(0038\mathrm{H}\)) with RST 7.5 (hardware, \(003C\mathrm{H}\)).

Claiming TRAP is maskable, or that INTR has a fixed vector without INTA.

SIM with MSE=0, then wondering why the mask did not change.

PUSH storing low byte first at \(SP-1\). The 8085 stores high at \(SP-1\), low at \(SP-2\).

Treating READY as an interrupt, or HOLD as an instruction.

Parity flag as “odd parity of 1s” — on the 8085 P is set for *even* parity of the result.

Forgetting that EI is delayed by one instruction (so RET after EI is not immediately interrupted by a still-pending level). That one-instruction delay is why EI; RET is a safe epilogue.

Adding T-states of two instructions without converting to time when the clock is given, or converting only one of them.

Using 8086 bus timing (4-clock T-states with different ALE) on an 8085 diagram.

Writing interrupt vectors as \(7.5\times 8 = 60\mathrm{D} = 003C\mathrm{H}\) correctly but then putting the ISR at \(0038\mathrm{H}\) “because RST 7.”
