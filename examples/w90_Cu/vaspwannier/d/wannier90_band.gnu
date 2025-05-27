set data style dots
set nokey
set xrange [0: 6.57039]
set yrange [  2.45674 : 10.82669]
set arrow from  1.73809,   2.45674 to  1.73809,  10.82669 nohead
set arrow from  2.60713,   2.45674 to  2.60713,  10.82669 nohead
set arrow from  3.22164,   2.45674 to  3.22164,  10.82669 nohead
set arrow from  5.06516,   2.45674 to  5.06516,  10.82669 nohead
set xtics (" G "  0.00000," X "  1.73809," W "  2.60713," K "  3.22164," G "  5.06516," L "  6.57039)
 plot "wannier90_band.dat"
