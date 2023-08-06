# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 09:47:57 2018

@author: th0lxl1
"""

from numpy import sqrt, tile, transpose,  sin, exp, zeros
from numpy import linspace
from numpy import sum as nsum
from numpy import abs as nabs


def mlayer_rough(alpha,k0,n_r,zm0,sig):        
    """        
    mlayer(alpha,n,z,sig)
    Updated LBL May 30, 2022 
    from M. Tolan
    X-Ray Scattering from Soft-Matter Thin Films
    Chapter 2, p12 and following

    multi-layer parratt model with roughness
    
    We model the surface as a number of interfaces.  To  avoid confusion, 
    the electron densities are put in as electron density differences.  
    
    Variables:
    alpha --- The incident angle in radians
    k0    --- The magnitude of the wavevector of the light
    n     --- The  indices of refraction 
    z     --- The positions of the interfaces 
    sig   --- The roughness of each interface

    Translated to python August 20, 2018, Laurence Lurio 
    
    Note that R[:,0] is the top layer reflectivity and that T[:,0]
    is meaningless (just equal to 1) T[:,1] is the transmission from
    the first layer to the second layer
    
    O is the top interface
    
    Note index of refraction must be 1 - delta + i beta
    
    Note: T and R stand for the electric fields, not the
    coefficients.  Their form contains the z dependence, e.g
    R exp(+ikz)  and T exp(-ikz), with z a negative number going
    into the material
    """
    la = alpha.shape[0]
    ln = n_r.shape[0] # ln is the number of layers
    # need to subtract off the first index, as Tolan formalism assumes 
    # you are coming in from vacuum
    nr2d = n_r**2-n_r[0]**2
    nr2d = tile(nr2d,(la,1))
    nr2d = nr2d.astype(complex)
    zm = tile(zm0,(la,1))
    sig = tile(sig,(la,1))
    alpha = transpose(tile(alpha,(ln,1)))
    R = zeros((la,ln),dtype=complex)
    T = zeros((la,ln),dtype=complex)
    X = zeros((la,ln),dtype=complex)
    kz=k0*sqrt(sin(alpha)**2 + nr2d)
    rr=(kz[:,0:-1]-kz[:,1:])/(kz[:,0:-1]+kz[:,1:]) # eq. 2.17
    # Here is where the roughness factors in
    rr=rr*exp(-nabs(2*kz[:,0:-1]*kz[:,1:]*sig*sig))
    # tp=tp*exp(nabs((kz[:,0:-1]-kz[:,1:])**2*sig*sig/2))
    tp = 1-rr
    # append 0 and 1 for the reflection and transmission coefficient of the last layer
    
    for jl in range(ln-2,-1,-1):
        # since rr only describes the interfaces, not the layers,
        # the number of rr's is 1 less than the number of kz's
        X[:,jl]=rr[:,jl]+X[:,jl+1]*exp(2j*kz[:,jl+1]*zm[:,jl])
        X[:,jl]=X[:,jl]*exp(-2j*kz[:,jl]*zm[:,jl])
        X[:,jl]=X[:,jl]/(1+rr[:,jl]*X[:,jl+1]*exp(2j*kz[:,jl+1]*zm[:,jl]))
    T[:,0]=1.0
    R[:,0]=X[:,0]
    for jl in range(0,ln-1):
        R[:,jl+1]=(R[:,jl]*exp(-1j*(kz[:,jl+1]-kz[:,jl])*zm[:,jl])
                   -T[:,jl]*rr[:,jl]*exp(-1j*(kz[:,jl+1]+kz[:,jl])*zm[:,jl]))
        R[:,jl+1]=R[:,jl+1]/tp[:,jl]
        T[:,jl+1]=(T[:,jl]*exp(1j*(kz[:,jl+1]-kz[:,jl])*zm[:,jl])
                   -R[:,jl]*rr[:,jl]*exp(1j*(kz[:,jl+1]+kz[:,jl])*zm[:,jl]))
        T[:,jl+1]=T[:,jl+1]/tp[:,jl]
    return([T,R,kz,X,rr,tp,zm0])

def mlayer_conv(alpha,k0,n,z,sig,res,npt):
    dX = linspace(-res, res, num=npt)
    yout=[]
    mu=res/2.35
    norm = nsum(exp(-(dX/mu)**2))
    yout=0
    for delx in dX:
        _,R,_,_,_,_ = mlayer_rough(abs(alpha+delx),k0,n,z,sig)
        yout = yout+exp(-(delx/mu)**2)*abs(R[:,0])**2/norm
    return(yout)



    
    
