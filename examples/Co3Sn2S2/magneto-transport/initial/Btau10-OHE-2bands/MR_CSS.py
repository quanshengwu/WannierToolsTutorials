import re
import numpy as np
import scipy.io as sio
from scipy.interpolate import interp1d
from scipy.optimize import fsolve

# Magnetization function
def Magnet_BT(Barray, T, alpha):
    kb=1.0; qJ=175.0
    B=np.array(Barray, dtype=float)
    M=np.zeros_like(B)
    beta=1.0/(kb*T)
    for i, Bval in enumerate(B):
        f_sup=abs(np.tanh(alpha*Bval))
        s0=0.5 if Bval>0 else (-0.5 if Bval<0 else 1e-4)
        fun=lambda s: np.tanh(beta*(Bval+qJ*s))/s-1
        try:
            sol=fsolve(fun, s0, maxfev=10000)
            sval=sol[0]
        except:
            sval=0.0
        if sval*Bval<0: sval=-sval
        M[i]=sval*f_sup
    return M

# Read header
btaulist_pattern = re.compile(r"^#\s*Btaulist\s*=\s*(.*)")
decimal_pattern = r"([+-]?\d*\.\d+(?:[eE][+-]?\d+)?)"
with open('sigma_bands_mu_0.0meV.dat') as f:
    for line in f:
        m3 = btaulist_pattern.match(line)
        if m3:
            Btau_array = [float(val) for val in re.findall(decimal_pattern, m3.group(1))]
            BTauNum = len(Btau_array);break

# Parameters
Brange=15
Band_array=[39,40]
T_array=np.array([20,30,40,50])
folder_index=2; T=50; T_actual=30; B_coer_length=300
B_internum=3003; dB_length=2400
AHC_cal=0.12046739e4; M_scal=1.0

tau_scal=0.04
delta_tau=1.2
tauT=np.array([[0,0,0,4+delta_tau],[0,0,0,6-delta_tau]])*tau_scal
idx=np.where(T_array==T)[0][0]
tau=tauT[:,idx]; tau_cm=tau*1e-12*1e-2

# Load sigma bands
sigma_data={b: np.loadtxt(f'sigma_band_{b}_mu_0.00eV_T_{T:.2f}K.dat') for b in Band_array}
rawB=sigma_data[Band_array[0]][:,0]
Btau=np.linspace(rawB[0],rawB[-1],BTauNum)

# Build sigma arrays
sigmat={i: np.zeros((BTauNum,len(Band_array))) for i in range(1,10)}
for j,b in enumerate(Band_array):
    dat=sigma_data[b]
    for i in range(1,10):
        f=interp1d(dat[:,0],dat[:,i],kind='linear',bounds_error=False,fill_value=0)
        sigmat[i][:,j]=f(Btau)
# scale by tau
sig_bt={i: sigmat[i]*tau_cm for i in sigmat}

# B grids
B_least=Btau/np.max(tau)
B_inter=np.linspace(B_least[0],B_least[-1],B_internum)
B_inter_sym=np.concatenate((-B_inter[::-1][:-1],B_inter))
B_internum_sym=B_inter_sym.size

# Sum conductivities
Bmag=np.vstack([Btau/t for t in tau]).T
comp_map={1:'xx',2:'xy',3:'xz',4:'yx',5:'yy',6:'yz',7:'zx',8:'zy',9:'zz'}
Sigma={name:np.zeros_like(B_inter) for name in comp_map.values()}
for i, name in comp_map.items():
    for j in range(len(Band_array)):
        c=interp1d(Bmag[:,j],sig_bt[i][:,j],kind='cubic',bounds_error=False,fill_value=0)
        Sigma[name]+=c(B_inter)
# Symmetrize
def sym(arr,odd=False): return np.concatenate((-arr[::-1][:-1],arr)) if odd else np.concatenate((arr[::-1][:-1],arr))
sig_sym={
    'xx':sym(Sigma['xx']),
    'xy':sym(Sigma['xy'],odd=True),
    'xz':sym(Sigma['xz'],odd=True),
    'yx':sym(Sigma['yx'],odd=True),
    'yy':sym(Sigma['yy']),
    'yz':sym(Sigma['yz'],odd=True),
    'zx':sym(Sigma['zx'],odd=True),
    'zy':sym(Sigma['zy'],odd=True),
    'zz':sym(Sigma['zz'])
}

# Generate hysteresis magnetization
alpha=500
slope=(Magnet_BT(B_inter[dB_length+1:dB_length+2],T_actual,alpha)[0]-Magnet_BT(B_inter[1:2],T_actual,alpha)[0])/(B_inter[dB_length+1]-B_inter[1])
Mag1=np.zeros(B_internum_sym)
Mag2=np.zeros(B_internum_sym)
# Branch 1 (decreasing field)
Mag1[:B_internum-1]=Magnet_BT(B_inter_sym[:B_internum-1],T_actual,alpha)
Mag1[B_internum-1:B_internum-1+B_coer_length+1]=Magnet_BT(np.array([B_inter_sym[B_internum-2]]),T_actual,alpha)[0] + slope*(B_inter_sym[B_internum-1:B_internum-1+B_coer_length+1]-B_inter_sym[B_internum-2])
Mag1[B_internum-1+B_coer_length+1:]=Magnet_BT(B_inter_sym[B_internum-1+B_coer_length+1:],T_actual,alpha)
# Branch 2 (increasing field)
Mag2[B_internum:]=Magnet_BT(B_inter_sym[B_internum:],T_actual,alpha)
Mag2[B_internum-1-B_coer_length:B_internum]=Magnet_BT(np.array([B_inter_sym[B_internum]]),T_actual,alpha)[0] + slope*(B_inter_sym[B_internum-1-B_coer_length:B_internum]-B_inter_sym[B_internum])
Mag2[:B_internum-1-B_coer_length]=Magnet_BT(B_inter_sym[:B_internum-1-B_coer_length],T_actual,alpha)

# Compute resistivity and MR
rho_int=[];sigma_int=[]; MR=[]
for Mag in [Mag2,Mag1]:
    rho_branch=[]; sigma_branch=[]; MRb=[]
    for i,Bv in enumerate(B_inter_sym):
        s0=np.array([[sig_sym['xx'][i],sig_sym['xy'][i],sig_sym['xz'][i]],[sig_sym['yx'][i],sig_sym['yy'][i],sig_sym['yz'][i]],[sig_sym['zx'][i],sig_sym['zy'][i],sig_sym['zz'][i]]])
        AHE=np.array([[0,Mag[i]*AHC_cal,0],[-Mag[i]*AHC_cal,0,0],[0,0,0]])
        sB=s0+AHE
        inv0=np.linalg.inv(s0); invB=np.linalg.inv(sB)
        sigma_branch.append(sB)
        rho_branch.append(invB)
        if i==B_internum-1:
            rho0=invB[0,0]
    for i,Bv in enumerate(B_inter_sym):
        MRb.append((rho_branch[i][0,0]-rho0)/rho0)
    rho_int.append(rho_branch); sigma_int.append(sigma_branch); MR.append(np.array(MRb))

# Save
sio.savemat('CSS_30K.mat',{
    'B_inter_sym':B_inter_sym,
    'Magnet1_sym':Mag1,
    'Magnet2_sym':Mag2,
    'MR_inter':MR,
    'Btau':Btau,
    'sigmaxx_btau':sig_bt[1],
    'sigmaxy_btau':sig_bt[2],
    'Band_array':np.array(Band_array),
    'tau':tau,
    'rho_int':rho_int,
    'sigma_int':sigma_int
})
