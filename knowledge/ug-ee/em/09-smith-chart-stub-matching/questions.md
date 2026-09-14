# Questions — Smith chart, single-stub matching

Original pedagogical numbers.

## Q1

### Given

\( Z_0=50.0\,\Omega \), \( Z_L=25.0\,\Omega \).

### Find

Normalized \( z_L \), \(\Gamma_L\), and VSWR.

### Solution

\( z_L=0.500 \). \(\Gamma=(0.5-1)/(0.5+1)=-1/3 \). \( s=(1+1/3)/(1-1/3)=2.00 \).

### Answer

\( z=0.500 \); \(\Gamma=-1/3 \); VSWR \( =2.00 \).

## Q2

### Given

Normalized load \( z_L=1+j \).

### Find

\(\Gamma\) and the normalized admittance \( y_L=1/z_L \).

### Solution

\(\Gamma=(j)/(2+j)=j(2-j)/5=(1+j2)/5=0.200+j0.400 \). \( y_L=1/(1+j)=(1-j)/2=0.500-j0.500 \).

### Answer

\( \Gamma=0.200+j0.400 \); \( y_L=0.500-j0.500 \).

## Q3

### Given

Shorted stub, \( Z_0=50\,\Omega \), length \( \lambda/6 \).

### Find

Normalized \( z_s \) and \( y_s \).

### Solution

\( \beta\ell=60^\circ \), \( z_s=j\tan 60^\circ=j\sqrt{3} \). \( y_s=-j\cot 60^\circ=-j/\sqrt{3} \).

### Answer

\( z_s=j1.73 \); \( y_s=-j0.577 \).

## Q4

### Given

Open stub, \( Z_0=75\,\Omega \), \(\ell=\lambda/8 \).

### Find

\( Z_{\mathrm{in}} \) of the stub alone.

### Solution

\( Z_{\mathrm{in}}=-j Z_0\cot(45^\circ)=-j75\,\Omega \).

### Answer

\( -j75.0\,\Omega \).

## Q5

### Given

A shunt shorted stub is to cancel \( y=1+j0.80 \) at a junction (already \( g=1 \)).

### Find

The smallest \(\ell_s/\lambda>0\) of a shorted stub with \( y_s=-j0.80 \).

### Solution

\( y_s=-j\cot\beta\ell=-j0.80\Rightarrow \cot\beta\ell=0.80 \), \(\beta\ell=51.3^\circ \), \(\ell/\lambda=51.3/360=0.143 \).

### Answer

\( 0.143\lambda \).

## Q6

### Given

Quarter-wave transformer to match \( 200\,\Omega \) to a \( 50.0\,\Omega \) system, both real.

### Find

The transformer \( Z_{0T} \).

### Solution

\( Z_{0T}=\sqrt{50\times 200}=100\,\Omega \).

### Answer

\( 100\,\Omega \).
