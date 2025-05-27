set data style dots
set nokey
set xrange [0: 2.99975]
set yrange [ -2.13231 :  9.90251]
set arrow from  0.32908,  -2.13231 to  0.32908,   9.90251 nohead
set arrow from  1.21257,  -2.13231 to  1.21257,   9.90251 nohead
set arrow from  2.11626,  -2.13231 to  2.11626,   9.90251 nohead
set xtics (" G "  0.00000," Z "  0.32908," F "  1.21257," G "  2.11626," L "  2.99975)
 plot "wannier90_band.dat"
