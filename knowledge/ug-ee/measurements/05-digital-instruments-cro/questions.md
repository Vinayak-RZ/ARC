# Questions — DMM, CRO/DSO, Lissajous

Original pedagogical numbers.

## Q1

### Given

Dual-slope DVM with \( T_1=80.0 \) ms, reference \( V_r=5.00 \) V, deintegrate time \( T_2=24.0 \) ms.

### Find

Unknown DC input \( V_x \).

### Solution

\( V_x=V_r T_2/T_1=5\times 24/80=1.50 \) V.

### Answer

\( 1.50 \) V.

## Q2

### Given

A sine wave occupies 6.00 vertical divisions peak-to-peak at 2.00 V/div with a 10× probe, and 5.00 horizontal divisions per period at 200 µs/div.

### Find

Peak-to-peak voltage, RMS (sine), period, and frequency.

### Solution

\( V_{pp}=6\times 2\times 10=120 \) V. \( V_{\mathrm{rms}}=120/(2\sqrt{2})=42.4 \) V. \( T=5\times 200\,\mu\mathrm{s}=1.00 \) ms. \( f=1.00 \) kHz.

### Answer

\( V_{pp}=120 \) V; \( V_{\mathrm{rms}}=42.4 \) V; \( T=1.00 \) ms; \( f=1.00 \) kHz.

## Q3

### Given

Lissajous ellipse, equal frequencies. Vertical intercept 1.50 div, vertical maximum 3.00 div.

### Find

Phase difference magnitude.

### Solution

\( \sin\phi=1.50/3.00=0.500 \), \( \phi=30.0^\circ \) (or \( 150^\circ \) from orientation).

### Answer

\( 30^\circ \) (or \( 150^\circ \) if the ellipse leans the other family).

## Q4

### Given

Oscilloscope analog bandwidth 50.0 MHz. Use \( t_r=0.35/B \).

### Find

Approximate 10%–90% rise time of the scope alone.

### Solution

\( t_r=0.35/(50\times 10^6)=7.0 \) ns.

### Answer

\( 7.0 \) ns.

## Q5

### Given

DSO real-time sample rate 2.00 MSa/s. A student measures a 1.50 MHz sine without equivalent-time sampling.

### Find

Whether Nyquist is satisfied and a possible aliased frequency.

### Solution

Nyquist frequency \( 1.00 \) MHz. \( 1.50 \) MHz aliases to \( |1.50-2.00|=0.50 \) MHz.

### Answer

Nyquist violated; alias near \( 0.50 \) MHz.

## Q6

### Given

DMM DC spec \( \pm(0.08\%\text{ of reading}+3\text{ counts}) \), 20.00 V range (0.01 V/count), reading 12.00 V.

### Find

Absolute limiting uncertainty of the reading.

### Solution

\( 0.0008\times 12.00 + 3\times 0.01 = 0.0096+0.030=0.0396 \) V.

### Answer

\( 0.040 \) V (40 mV).
