# BPVE Spectrum: Type and Component
type = "LS"    # LS, LI, CS, CI
col = 11        # See below 

component = ""
if (col == 2) component = "xxx"
if (col == 3) component = "xxy"
if (col == 4) component = "xxz"
if (col == 5) component = "xyy"
if (col == 6) component = "xyz"
if (col == 7) component = "xzz"
if (col == 8) component = "yxx"
if (col == 9) component = "yxy"
if (col == 10) component = "yxz"
if (col == 11) component = "yyy"
if (col == 12) component = "yyz"
if (col == 13) component = "yzz"
if (col == 14) component = "zxx"
if (col == 15) component = "zxy"
if (col == 16) component = "zxz"
if (col == 17) component = "zyy"
if (col == 18) component = "zyz"
if (col == 19) component = "zzz"

if (type eq "LS") filename = "linear_shift.dat"
if (type eq "LI") filename = "linear_inject.dat"
if (type eq "CS") filename = "circular_shift.dat"
if (type eq "CI") filename = "circular_inject.dat"

outfile = sprintf("sigma_%s_%s.pdf", type, component)

set terminal pdfcairo enhanced font "Arial,30" size 6,6
set output outfile

set title sprintf("BPVE Conductivity (sigma-%s-%s)", type, component)
set xlabel "Frequency (eV)"
set ylabel "Conductivity (Ang {/Symbol m}A/V^{2})
set grid

plot filename using 1:col notitle with lines lw 10
