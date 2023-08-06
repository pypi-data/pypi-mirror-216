# pySWXF 

Code for calculating reflectivity and standing wave x-ray reflectivity

There are three subpackages, refl_funs, for reflectivity calculations, standing_wave, for standing 
wave calculations and xray_utils, for a few auxilary utilities

refl_funs
	mlayer_rough(alpha,k0,n_r,zm0,sig)
	mlayer_conv(alpha,k0,n,z,sig,res,npt)
standing_wave
	reflection_matrix(alpha,E,layers)
	standing_wave(z,T,R,kz,h_i)
xray_utils 
	n_to_rho(material,n,energy)

