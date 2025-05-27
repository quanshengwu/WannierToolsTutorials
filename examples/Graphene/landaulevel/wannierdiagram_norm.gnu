 set terminal pngcairo enhanced color font ",60" size 1920, 1680
 set output 'wannierdiagram.png'
 set pm3d
set size 0.9,1
set origin 0.05,0
set palette rgb 21,22,23
 #set isosamples 50,50
 set view map
 unset ztics
 unset surface
 unset key
 set ylabel "n/n_s"
#set title "Wannier diagram"
set title "Wannier diagram with Nq=   400"
 #set yrange [   ] noextend
 #set xlabel "{/Symbol F}/{/Symbol F}_0"
 #set xlabel "Phi/Phi_0 per unit cell"
 set xlabel "{/Symbol F}/{/Symbol F}_0"
set xrange [0:1 ] noextend
set ytics ("0"    0.00000,"0.5"    0.5,"1"    1) 
set xtics ("0"    0.00000,"0.5"    0.5,"1"    1) 
splot 'wannierdiagram_norm.dat' u 1:2:(log($3)) w pm3d #lc palette
 #splot 'wannierdiagram.dat' u 1:3:(log($4)) w pm3d #lc palette
