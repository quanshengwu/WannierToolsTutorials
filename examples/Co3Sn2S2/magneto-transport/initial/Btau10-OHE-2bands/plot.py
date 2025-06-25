import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt

data=sio.loadmat('CSS_30K.mat')
B=data['B_inter_sym'].flatten()
Mag1=data['Magnet1_sym'].flatten(); Mag2=data['Magnet2_sym'].flatten()
MR=data['MR_inter']
Btau=data['Btau'].flatten()
sigxx=data['sigmaxx_btau']
sigxy=data['sigmaxy_btau']
bands=data['Band_array'].flatten().astype(int)
tau=data['tau'].flatten()
rho_int=data['rho_int']
sigma_int=data['sigma_int']

Bshow=15
colors=['b','r']
# Magnetization loop
plt.figure(figsize=(6,6))
plt.gca().tick_params(axis='both', labelsize=20, width=2, direction='in')
for spine in plt.gca().spines.values():
    spine.set_linewidth(2)
plt.plot(B,Mag2,linewidth=3.5,color=colors[0])
plt.plot(B,Mag1,linewidth=3.5,color=colors[1])
plt.xlim([-Bshow,Bshow]); plt.xlabel('B (T)',fontsize=20); plt.ylabel('M/Ms',fontsize=20); plt.tight_layout(); plt.savefig('M.pdf')


# MR loop
plt.figure(figsize=(6,6))
plt.gca().tick_params(axis='both', labelsize=20, width=2, direction='in')
for spine in plt.gca().spines.values():
    spine.set_linewidth(2)
for i in range(2): plt.plot(B,100*MR[i],linewidth=3.5,color=colors[i])
plt.xlim([-Bshow,Bshow]); plt.ylim([-5,100]);plt.xlabel('B (T)',fontsize=20); plt.ylabel('MR (%)',fontsize=20); plt.tight_layout(); plt.savefig('MR.pdf')

# sigmaxx_OHE
plt.figure(figsize=(6,6))
plt.gca().tick_params(axis='both', labelsize=20, width=2, direction='in')
for spine in plt.gca().spines.values():
    spine.set_linewidth(2)
for idx,b in enumerate(bands): plt.plot(Btau,sigxx[:,idx],'*-',linewidth=1)
plt.xlabel(fr'$B\tau (\tau={tau} ps)$',fontsize=20); plt.ylabel(r'$\sigma_{xx} (\rm S/\rm cm)$',fontsize=20); plt.legend([f'band{b}' for b in bands]); plt.tight_layout(); plt.savefig('sigmaxx_OHE.pdf')

# sigmaxy_OHE
plt.figure(figsize=(6,6))
plt.gca().tick_params(axis='both', labelsize=20, width=2, direction='in')
for spine in plt.gca().spines.values():
    spine.set_linewidth(2)
for idx,b in enumerate(bands): plt.plot(Btau,sigxy[:,idx],linewidth=3.5,color=colors[idx])
plt.xlabel(fr'$B\tau (\tau={tau} ps)$',fontsize=20); plt.ylabel(r'$\sigma_{xy} (\rm S/\rm cm)$',fontsize=20); plt.legend([f'band{b}' for b in bands]); plt.tight_layout(); plt.savefig('sigmaxy_OHE.pdf')

# rho_xx loop
plt.figure(figsize=(6,6))
plt.gca().tick_params(axis='both', labelsize=20, width=2, direction='in')
for spine in plt.gca().spines.values():
    spine.set_linewidth(2)
for i in range(2):
    arr=[m[0,0] for m in rho_int[i]]; arr=np.array(arr)*1e6
    plt.plot(B,arr,linewidth=3.5,color=colors[i])
plt.xlim([-Bshow,Bshow]); plt.ylim([15,45]); plt.xlabel('B (T)',fontsize=20); plt.ylabel(r'$\rho_{xx} (\mu\Omega \rm cm)$',fontsize=20); plt.tight_layout(); plt.savefig('rhoxx.pdf')

# sigma_xy with AHE
plt.figure(figsize=(6,6))
plt.gca().tick_params(axis='both', labelsize=20, width=2, direction='in')
for spine in plt.gca().spines.values():
    spine.set_linewidth(2)
for i in range(2):
    arr=[m[0,1] for m in sigma_int[i]]
    plt.plot(B,arr,linewidth=3.5,color=colors[i])
plt.xlim([-Bshow,Bshow]); plt.ylim([-4000,4000]);plt.xlabel('B (T)',fontsize=20);plt.ylabel(r'$\sigma_{xy} (\rm S/\rm cm)$',fontsize=20); plt.tight_layout(); plt.savefig('sigmaxy.pdf')

# rho_yx loop
plt.figure(figsize=(6,6))
plt.gca().tick_params(axis='both', labelsize=20, width=2, direction='in')
for spine in plt.gca().spines.values():
    spine.set_linewidth(2)
for i in range(2):
    arr=[m[1,0] for m in rho_int[i]]; arr=np.array(arr)*1e6
    plt.plot(B,arr,linewidth=3.5,color=colors[i])
plt.xlim([-Bshow,Bshow]); plt.ylim([-4,4]);plt.xlabel('B (T)',fontsize=20);plt.ylabel(r'$\rho_{yx} (\mu\Omega \rm cm)$',fontsize=20); plt.tight_layout(); plt.savefig('rhoyx.pdf')

