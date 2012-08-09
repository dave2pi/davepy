'''
Collection of magnetic equations.
'''

from math import pi
u0 = 4.0*pi*1E-7

def air_coil_B_field(current, turns, length):
	return u0*turns*current/length

def fr(f, l, d, t):
	'''
	Calculate Fr, the ratio of AC to DC
	resistance for a winding dure to skin 
	and proximity effects.
	
	f = frequency
	l = number of layers
	d = diameter of conductor
	t = temperature
	'''
	from math import pi, sqrt, sinh, sin, cosh, cos
	from si_prefix import si
	h = 0.886*d 								# height of equivalent rectangular conductor
	w = 2*pi*f 									# angular frequency
	a = h * sqrt(w*u0*0.5/resistivity_cu(t))
	mr = a*(sinh(2*a)+sin(2*a))/(cosh(2*a)-cos(2*a))
	dr = 2*a*(sinh(a)-sin(a))/(cosh(a)+cos(a))
	delta = sqrt(2*resistivity_cu(t)/(w*u0))	# skin depth
	print 'skin depth:', si(delta)+'m'
	fr = mr+(l**2-1)*dr/3						# Fr value
	return fr
	

def resistivity_cu(t):
	'''
	Resistivity of copper at temperature t.
	
	t = Temperature (degrees C)
	'''
	return 67.078E-12*(t+273)-2.56E-9