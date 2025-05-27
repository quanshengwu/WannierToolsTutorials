set encoding iso_8859_1
#set terminal  postscript enhanced color
#set output 'landaulevel_B.eps'
set terminal  pngcairo truecolor enhanced  font ",60" size 1920, 1680
#set terminal  png truecolor enhanced  font ",60" size 1920, 1680
set output 'landaulevel_B.png'
unset key
set pointsize 0.8
set border lw 3 
#set xtics font ",36"
#set ytics font ",36"
#set xlabel font ",36"
#set xlabel "Phi per cell"
 set xlabel "{/Symbol F}/{/Symbol F}_0"
set ylabel "Energy (eV)"
set title "Hofstadter butterfly with Nq=100 at k=(0.16667, 0, 0)" font ",40"
#set xtics offset 0, -1
set xrange[0:1]
set xtics ("0" 0,"0.5" 0.5,"1" 1)
set ytics ("-10" -10, "-5" -5, "0" 0, "5" 5, "10" 10)
#set ylabel offset -1, 0 
rgb(r,g,b) = int(r)*65536 + int(g)*256 + int(b)
plot 'landaulevel_B.dat' u 1:3 w p  pt 7  ps 1
