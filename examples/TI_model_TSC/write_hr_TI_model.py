#!/usr/bin/env python
import sys
import os
import numpy as np
from datetime import datetime

"""
Obtain a tight binding Hamiltonian of Haldane model with Wannier90 format
"""
# maximum dimension for hr matrix
norbs= 4
nrpts= 7

# hr matrix 
hmnr= np.zeros((norbs,norbs,nrpts), dtype= np.complex128)

# WS points
irvec= np.zeros((3,nrpts), dtype= np.int32)

# degeneracy
dege= np.zeros((nrpts), dtype= np.int32)+ 1

# define tight-binding parameters
t=0.5; M=2.5; m0=-1.0;

# Pauli matrix
sigma0= np.array([[1., 0.],  [0., 1.]], dtype=np.float64)
sigmax= np.array([[0., 1.],  [1., 0.]], dtype=np.float64)
sigmay= np.array([[0.,-1.j], [1.j,0.]], dtype=np.complex128)
sigmaz= np.array([[1., 0.],  [0.,-1.]], dtype=np.float64)


# 0 0 0
ir= 0
irvec[0, ir]= 0
irvec[1, ir]= 0
irvec[2, ir]= 0
hmnr[:, :, ir]= M*np.kron(sigma0, sigmaz)

# 1 0 0
ir= ir+1
irvec[0, ir]= 1
irvec[1, ir]= 0
irvec[2, ir]= 0
hmnr[:, :, ir]= -1.j*t*np.kron(sigmax,sigmax)\
                + m0/2.*np.kron(sigma0,sigmaz)

#-1 0 0
ir= ir+1
irvec[0, ir]=-1
irvec[1, ir]= 0
irvec[2, ir]= 0
hmnr[:, :, ir]= 1.j*t*np.kron(sigmax,sigmax)\
                + m0/2.*np.kron(sigma0,sigmaz)

# 0 1 0 
ir= ir+1
irvec[0, ir]= 0
irvec[1, ir]= 1
irvec[2, ir]= 0
hmnr[:, :, ir]= -1.j*t*np.kron(sigmay,sigmax)\
                + m0/2.*np.kron(sigma0,sigmaz)

# 0 -1 0
ir= ir+1
irvec[0, ir]= 0
irvec[1, ir]=-1
irvec[2, ir]= 0
hmnr[:, :, ir]= 1.j*t*np.kron(sigmay,sigmax)\
                + m0/2.*np.kron(sigma0,sigmaz)

# 0 0 1
ir= ir+1
irvec[0, ir]= 0
irvec[1, ir]= 0
irvec[2, ir]= 1
hmnr[:, :, ir]= -1.j*t*np.kron(sigmaz,sigmax)\
                + m0/2.*np.kron(sigma0,sigmaz)

# 0 0 -1
ir= ir+1
irvec[0, ir]= 0
irvec[1, ir]= 0
irvec[2, ir]=-1
hmnr[:, :, ir]= 1.j*t*np.kron(sigmaz,sigmax)\
                + m0/2.*np.kron(sigma0,sigmaz)


#print "dump hr.dat..."
with open('wannier90_hr.dat','w') as f:
    line="TSC model with t="+str(t)+", M="+str(M)+", m0="+str(m0)+".  Ref:PhysRevLett.107.097001(2011)"+'\n'
    f.write(line)
    nl = np.int32(np.ceil(nrpts/15.0))
    f.write(str(norbs)+'\n')
    f.write(str(nrpts)+'\n')
    for l in range(nl):
        line="    "+'    '.join([str(np.int32(i)) for i in dege[l*15:(l+1)*15]])
        f.write(line)
        f.write('\n')
    for irpt in range(nrpts):
        rx = irvec[0,irpt];ry = irvec[1,irpt];rz = irvec[2,irpt]
        for jatomorb in range(norbs):
            for iatomorb in range(norbs):
               rp =hmnr[iatomorb,jatomorb,irpt].real
               ip =hmnr[iatomorb,jatomorb,irpt].imag
               line="{:8d}{:8d}{:8d}{:8d}{:8d}{:20.10f}{:20.10f}\n".format(rx,ry,rz,jatomorb+1,iatomorb+1,rp,ip)	
               f.write(line)
