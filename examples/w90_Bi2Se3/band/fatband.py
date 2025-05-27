import pyprocar

element1="Bi"
element2="Se"
#element3="Mg"
atoms1=[0,1]
atoms2=[2,3,4]
#atoms3=[8,9,10,11]
emin=-15
emax=13

# pyprocar.repair('PROCAR','PROCAR-repaired')

# element1
pyprocar.bandsplot(linewidth=[3],clim=[0,1], code='vasp', cmap='hot_r', dirname='./', elimit=[emin,emax], mode='parametric', atoms=atoms1, orbitals=[0], show=False, title='fatband_%s_s'%(element1), savefig='fatband_%s_s.pdf'%(element1))
pyprocar.bandsplot(linewidth=[3],clim=[0,1], code='vasp', cmap='hot_r', dirname='./', elimit=[emin,emax], mode='parametric', atoms=atoms1, orbitals=[1,2,3], show=False, title='fatband_%s_p'%(element1), savefig='fatband_%s_p.pdf'%(element1))
pyprocar.bandsplot(linewidth=[3],clim=[0,1], code='vasp', cmap='hot_r', dirname='./', elimit=[emin,emax], mode='parametric', atoms=atoms1, orbitals=[4,5,6,7,8], show=False, title='fatband_%s_d'%(element1), savefig='fatband_%s_d.pdf'%(element1))
#pyprocar.bandsplot(clim=[0,1], code='vasp', cmap='hot_r', dirname='./', elimit=[emin,emax], mode='parametric', atoms=atoms1, orbitals=[9,10,11,12,13,14,15], show=False, title='fatband_%s_f'%(element1), savefig='fatband_%s_f.pdf'%(element1))

# element2
pyprocar.bandsplot(linewidth=[3],clim=[0,1], code='vasp', cmap='hot_r', dirname='./', elimit=[emin,emax], mode='parametric', atoms=atoms2, orbitals=[0], show=False, title='fatband_%s_s'%(element2), savefig='fatband_%s_s.pdf'%(element2))
pyprocar.bandsplot(linewidth=[3],clim=[0,1], code='vasp', cmap='hot_r', dirname='./', elimit=[emin,emax], mode='parametric', atoms=atoms2, orbitals=[1,2,3], show=False, title='fatband_%s_p'%(element2), savefig='fatband_%s_p.pdf'%(element2))
pyprocar.bandsplot(linewidth=[3],clim=[0,1], code='vasp', cmap='hot_r', dirname='./', elimit=[emin,emax], mode='parametric', atoms=atoms2, orbitals=[4,5,6,7,8], show=False, title='fatband_%s_d'%(element2), savefig='fatband_%s_d.pdf'%(element2))

# element3
# pyprocar.bandsplot(clim=[0,1], code='vasp', cmap='hot_r', dirname='./', elimit=[emin,emax], mode='parametric', atoms=atoms3, orbitals=[0], show=False, title='fatband_%s_s'%(element3), savefig='fatband_%s_s.pdf'%(element3))
# pyprocar.bandsplot(clim=[0,1], code='vasp', cmap='hot_r', dirname='./', elimit=[emin,emax], mode='parametric', atoms=atoms3, orbitals=[1,2,3], show=False, title='fatband_%s_p'%(element3), savefig='fatband_%s_p.pdf'%(element3))
# pyprocar.bandsplot(clim=[0,1], code='vasp', cmap='hot_r', dirname='./', elimit=[emin,emax], mode='parametric', atoms=atoms3, orbitals=[4,5,6,7,8], show=False, title='fatband_%s_d'%(element3), savefig='fatband_%s_d.pdf'%(element3))
