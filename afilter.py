'''
Some calcs for analog filters.
'''
import all_pass

def rc_f(r, c):
	'''
	Calculate the cutoff frequency of a simple
	RC filter.
	
	r = resistance (ohms)
	c = capacitance (F)
	'''
	from math import pi
	return 1.0/(2.0*pi*r*c)

def rc_r(f, c):
	'''
	Calulate the resistance required for a 
	simple RC filter.
	
	f = cutoff frequency (Hz)
	c = capacitance (F)
	'''
	from math import pi
	return 1.0/(2.0*pi*f*c)

def rc_c(f, r):
	'''
	Calulate the resistance required for a 
	simple RC filter.
	
	f = cutoff frequency (Hz)
	r = resistance (ohms)
	'''
	from math import pi
	return 1.0/(2.0*pi*f*r)

def lc_f(l, c):
	'''
	Calulate the cutoff frequency of a simple 
	LC filter.
	
	l = inductance (H)
	c = capacitance (F)
	'''
	from math import pi, sqrt
	return 1.0/(2.0*pi*sqrt(l*c))

def lc_l(f, c):
	'''
	Calulate the inductance required for a 
	simple LC filter.
	
	f = cutoff frequency (Hz)
	c = capacitance (F)
	'''
	from math import pi
	return 1.0/(((2.0*pi*f)**2)*c)

def lc_c(f, l):
	'''
	Calulate the capacitance required for a 
	simple LC filter.
	
	f = cutoff frequency (Hz)
	l = inductance (H)
	'''
	from math import pi
	return 1.0/(((2.0*pi*f)**2)*l)
	

