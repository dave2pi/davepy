'''
Some calcs for analog filters.
'''
import math as _math

def rc_f(r, c):
	'''
	Calculate the cutoff frequency of a simple
	RC filter.
	
	r = resistance (ohms)
	c = capacitance (F)
	'''
	return 1.0/(2.0*_math.pi*r*c)

def rc_r(f, c):
	'''
	Calulate the resistance required for a 
	simple RC filter.
	
	f = cutoff frequency (Hz)
	c = capacitance (F)
	'''
	return 1.0/(2.0*_math.pi*f*c)

def rc_c(f, r):
	'''
	Calulate the resistance required for a 
	simple RC filter.
	
	f = cutoff frequency (Hz)
	r = resistance (ohms)
	'''
	return 1.0/(2.0*_math.pi*f*r)

def lc_f(l, c):
	'''
	Calulate the cutoff frequency of a simple 
	LC filter.
	
	l = inductance (H)
	c = capacitance (F)
	'''
	return 1.0/(2.0*_math.pi*_math.sqrt(l*c))

def lc_l(f, c):
	'''
	Calulate the inductance required for a 
	simple LC filter.
	
	f = cutoff frequency (Hz)
	c = capacitance (F)
	'''
	return 1.0/(((2.0*_math.pi*f)**2)*c)

def lc_c(f, l):
	'''
	Calulate the capacitance required for a 
	simple LC filter.
	
	f = cutoff frequency (Hz)
	l = inductance (H)
	'''
	return 1.0/(((2.0*_math.pi*f)**2)*l)
