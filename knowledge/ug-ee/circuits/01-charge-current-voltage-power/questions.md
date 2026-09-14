# Questions — Charge, current, voltage, power, energy

Original pedagogical numbers. Not from GATE or university papers.

## Q1

### Given

The charge entering the plus terminal of a two-terminal device is \( q(t) = 4.8 t^2 - 1.2 t \) millicoulombs for \( t \ge 0 \) with \( t \) in seconds. The voltage across the device is constant at \( 18.5\,\mathrm{V} \) (plus at the same terminal). Passive sign convention holds.

### Find

The instantaneous current \( i(t) \) in milliamperes, the instantaneous power \( p(t) \) in milliwatts, and whether the device absorbs or delivers power at \( t = 0.40\,\mathrm{s} \).

### Solution

Convert \( q \) to coulombs: \( q(t) = (4.8 t^2 - 1.2 t)\times 10^{-3}\,\mathrm{C} \). Then \( i = dq/dt = (9.6 t - 1.2)\times 10^{-3}\,\mathrm{A} = (9.6 t - 1.2)\,\mathrm{mA} \). At \( t = 0.40\,\mathrm{s} \), \( i = 9.6(0.40) - 1.2 = 2.64\,\mathrm{mA} \). Power \( p = vi = 18.5 \times 2.64\times 10^{-3} = 48.84\times 10^{-3}\,\mathrm{W} = 48.84\,\mathrm{mW} \). Positive \( p \) under PSC means absorption.

### Answer

\( i(t) = (9.6t - 1.2)\,\mathrm{mA} \); \( p(0.40\,\mathrm{s}) = 48.84\,\mathrm{mW} \) absorbed.

## Q2

### Given

A linear resistor \( R \) carries \( i(t) = 0.25\cos(100\pi t)\,\mathrm{A} \). Over one period the absorbed energy is \( 0.3125\,\mathrm{J} \). The period is \( 20\,\mathrm{ms} \).

### Find

Derive \( R \) from the energy definition, and state the average power.

### Solution

Energy over one period \( T = 0.020\,\mathrm{s} \) is \( W = \int_0^T i^2 R\,dt = R \int_0^T (0.25)^2 \cos^2(100\pi t)\,dt \). The average of \( \cos^2 \) over an integer number of half-cycles is \( 1/2 \), so \( W = R (0.0625)(1/2) T = R(0.03125)(0.020) = 6.25\times 10^{-4} R \). Set equal to \( 0.3125 \): \( R = 0.3125 / 6.25\times 10^{-4} = 500\,\Omega \). Average power \( P_\mathrm{avg} = W/T = 0.3125/0.020 = 15.625\,\mathrm{W} \), which also equals \( I_\mathrm{rms}^2 R \) with \( I_\mathrm{rms} = 0.25/\sqrt{2} \).

### Answer

\( R = 500\,\Omega \); \( P_\mathrm{avg} = 15.625\,\mathrm{W} \).

## Q3

### Given

A lab supply must deliver \( 7.4\,\mathrm{V} \) at up to \( 1.8\,\mathrm{A} \) to a resistive load for \( 45 \) minutes, and must also be able to absorb \( 0.40\,\mathrm{A} \) at the same voltage for \( 8 \) minutes during a regeneration interval.

### Find

Design the energy budget: energy delivered, energy absorbed, and the minimum watt-hour rating if one bidirectional converter handles both intervals without other losses.

### Solution

Delivered energy \( W_\mathrm{del} = 7.4 \times 1.8 \times 45 \times 60 = 35964\,\mathrm{J} = 9.990\,\mathrm{Wh} \). Absorbed energy \( W_\mathrm{abs} = 7.4 \times 0.40 \times 8 \times 60 = 1420.8\,\mathrm{J} = 0.3947\,\mathrm{Wh} \). Net energy leaving the converter over the combined session is \( 9.990 - 0.3947 = 9.595\,\mathrm{Wh} \). The converter must be rated for both quadrants: source power \( 7.4\times 1.8 = 13.32\,\mathrm{W} \) and sink power \( 7.4\times 0.40 = 2.96\,\mathrm{W} \). A conservative energy rating is the delivered \( 10\,\mathrm{Wh} \) class (round up), not the net.

### Answer

Deliver \( 9.99\,\mathrm{Wh} \), absorb \( 0.395\,\mathrm{Wh} \); use a bidirectional supply ≥ \( 13.32\,\mathrm{W} \) source / \( 2.96\,\mathrm{W} \) sink, energy capacity ≥ \( 10\,\mathrm{Wh} \).

## Q4

### Given

Two students debate a capacitor charged to \( 24\,\mathrm{V} \) with \( C = 470\,\mu\mathrm{F} \). Student A says the capacitor “used up” \( \frac12 C V^2 \) as heat while charging through a series resistor from a \( 24\,\mathrm{V} \) DC source. Student B says the resistor dissipated that same amount and the capacitor stored \( \frac12 CV^2 \).

### Find

Explain which claim is correct, and what the DC source supplied.

### Solution

Linear capacitor energy stored is \( w_C = \frac12 (470\times 10^{-6})(24)^2 = 0.13536\,\mathrm{J} \). Charging from a DC source through any positive resistance, the source supplies \( QV = CV^2 = 0.27072\,\mathrm{J} \). Half is stored on \( C \); half is dissipated in the resistor (independent of \( R \), provided \( R > 0 \) and we wait until \( v_C \to 24\,\mathrm{V} \)). Student B is correct. Student A confuses stored energy with dissipated energy. If charging were lossless (ideal current source into \( C \)), the source would supply only \( \frac12 CV^2 \).

### Answer

Student B: capacitor stores \( 0.135\,\mathrm{J} \); resistor dissipates \( 0.135\,\mathrm{J} \); DC voltage source supplies \( 0.271\,\mathrm{J} \).

## Q5

### Given

A current \( i(t) = 3.0\,\mathrm{A} \) for \( 0 \le t < 2\,\mathrm{s} \), then \( i(t) = -1.5\,\mathrm{A} \) for \( 2 \le t \le 6\,\mathrm{s} \), enters the plus terminal of an element whose voltage is \( v = 12\,\mathrm{V} \) constant. At \( t = 0 \), \( q(0) = 0 \).

### Find

\( q(6\,\mathrm{s}) \) and the net energy absorbed from \( t = 0 \) to \( t = 6\,\mathrm{s} \).

### Solution

Charge: \( q(2) = 3.0 \times 2 = 6.0\,\mathrm{C} \). From 2 s to 6 s, \( \Delta q = -1.5 \times 4 = -6.0\,\mathrm{C} \), so \( q(6) = 0 \). Energy: \( W = \int vi\,dt = 12[3.0\times 2 + (-1.5)\times 4] = 12[6 - 6] = 0 \). Instantaneous power is \( +36\,\mathrm{W} \) then \( -18\,\mathrm{W} \); they cancel in the net energy. The element absorbed 72 J then delivered 72 J.

### Answer

\( q(6\,\mathrm{s}) = 0 \); net energy absorbed \( 0\,\mathrm{J} \) (72 J in, 72 J out).
