# BPVE Spectrum: Multiple Strain Comparison
type = "LS"     # LS, LI, CS, CI
col = 11        # Select tensor component

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

outfile = sprintf("sigma_%s_%s_all.pdf", type, component)

set terminal pdfcairo enhanced font "Arial,30" size 6,6
set output outfile

set title "BPVE Conductivity (Sigma-LS-yyy)"
set xlabel "Frequency (eV)"
set ylabel "Conductivity (Ang {/Symbol m}A/V^{2})"
set grid
set key top right

plot \
  "0.9LS.dat" using 1:col title "0.9%" with lines lw 5, \
  "2.2LS.dat" using 1:col title "2.2%" with lines lw 5, \
  "4LS.dat"   using 1:col title "4%"   with lines lw 5, \
  "6LS.dat"   using 1:col title "6%"   with lines lw 5, \
  "7.8LS.dat" using 1:col title "7.8%" with lines lw 5, \
  "12LS.dat"  using 1:col title "12%"  with lines lw 5 lc rgb 'orange'
