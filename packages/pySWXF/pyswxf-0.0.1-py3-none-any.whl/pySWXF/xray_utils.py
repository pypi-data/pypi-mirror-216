# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 08:41:22 2022

@author: lluri
"""
import xraydb as xdb
import scipy.constants as scc
import numpy as np
def n_to_rho(material,n,energy):
    mat = xdb.chemparse(material)
    A = 0
    Z = 0
    for key in mat:
        A += mat[key]*xdb.atomic_mass(key)
        delta,_,_ = xdb.xray_delta_beta(key,xdb.atomic_density(key),energy)
        Z += mat[key]*(xdb.atomic_number(key)+delta)
    rho = n*A/Z/scc.N_A/1e6
    return rho
def rho_to_n(material,rho,energy):
    delta, beta, _ = xdb.xray_delta_beta(material, rho, energy)
    n = 1-delta - 1j*beta
    return n
def rho_to_rhoe(material,rho,energy):
    lam = scc.h*scc.c/scc.e/energy
    k = 2*np.pi/lam
    delta, beta, _ = xdb.xray_delta_beta(material, rho, energy)
    r0 = scc.physical_constants['classical electron radius'][0]
    rhoe = delta*k**2/2/np.pi/r0
    return rhoe
