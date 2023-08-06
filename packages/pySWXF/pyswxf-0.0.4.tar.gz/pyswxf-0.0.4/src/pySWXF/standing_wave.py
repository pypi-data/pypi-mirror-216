# -*- coding: utf-8 -*-
"""
Created on Thu May 26 11:08:01 2022

@author: lluri
"""

#%% load in the files you plan to use
import xraydb as xdb
import numpy as np
from . import refl_funs
mlayer_rough =  refl_funs.mlayer_rough 
import scipy.constants as scc


def reflection_matrix(alpha,E,layers):
    '''
    reflection_matrix(alpha,E,layers)

    Parameters
    ----------
    alpha : numpy array float 
        incident angles (in radians).
    E : float
        incident energy (eV).
    layers : array of layers 
        each layer has a material (e.g. 'H2O') and density (g/cc) a thickness
        and a roughness.  
    The sig and thickness for the zeroth layer are thrown away as they have no meaning.

    Returns
    ----------
    T : numpy array (n_alpha, n_layer)
        Transmission matrix returned by mlayer or mlayer_rough
    R : numpy array (n_alpha, n_layer)
        Reflectivity matrix returned by mlayer or mlayer_rough.
    kz : numpy array (n_alpha, n_layer)
        wavevector matrix returned by mlayer or mlayer_rough. (units of inv meters)
    '''   
    k0 = 2*np.pi*E*scc.e/scc.h/scc.c
    nl  = len(layers)
    n_r = np.zeros(nl,complex)
    h_i = np.zeros(nl-1)
    sig_i = np.zeros(nl-1)
    z = 0
    for  i, (material, density, thick, rough)   in enumerate(layers):
        delta,beta,att = xdb.xray_delta_beta(material,density,E)
        n_r[i] = 1-delta+1j*beta 
        if i>0:
            h_i[i-1] = z
            z -= thick*scc.angstrom;
            sig_i[i-1] = rough*scc.angstrom
    T,R,kz,X,rr,tp,zd  = mlayer_rough(alpha,k0,n_r,h_i,sig_i)
    return T,R,kz,X,rr,tp,zd




def standing_wave(z,T,R,kz,h_i):
    '''
    standing_wave(T,R,kz,z)
    
    Function to calculate the electric field standing wave 
    
    Parameters
    ----------
    z : numpy array (1d)
        heights relative to top surface at which to calculate
            the standing wave.
    T : numpy array (n_alpha, n_layer)
        Transmission matrix returned by mlayer or mlayer_rough
    R : numpy array (n_alpha, n_layer)
        Reflectivity matrix returned by mlayer or mlayer_rough.
    kz : numpy array (n_alpha, n_layer)
        wavevector matrix returned by mlayer or mlayer_rough.
    h_i : numpy array (n_layer-1)
        array of interface height positions

            
    Here n_alpha is the number of angles input to mlayer and n_layer the
    number of layers input to mlayer.

    Returns
    -------
    I : numpy array (n_z,n_alpha)
        Standing wave intensity.
    E : numpy array (n_z,n_alpha)
        Electric field intensity.

    '''
    n_alpha,n_layer = np.shape(T)
    n_z = len(z)
    E = np.zeros((n_z,n_alpha))+0j   
    for i in range(n_layer):
        if i == 0:
            wz = z >= h_i[i]
        elif i == n_layer-1:
            wz = z < h_i[i-1]
        else :
            wz = (z < h_i[i-1])*(z >= h_i[i])
        # only do calculation for subset of z values
        tz = z[wz]
        n_tz = len(tz)
        T_full = np.broadcast_to(T[:,i],(n_tz,n_alpha))
        R_full = np.broadcast_to(R[:,i],(n_tz,n_alpha))
        kz_full = np.broadcast_to(kz[:,i],(n_tz,n_alpha))
        z_full = np.transpose(np.broadcast_to(tz,(n_alpha,n_tz)),(1,0))
        
        E[wz,:] = np.exp(-1j*kz_full*z_full)*T_full
        E[wz,:] += np.exp(1j*kz_full*z_full)*R_full
    # expand all the arrays to the same size for multiplying   
    I = np.abs(E)**2
    return I,E
