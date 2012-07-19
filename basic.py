'''
Colection of very basic electronics calcs.
'''

def sum(*x):
	'''
	Sum of values.
	'''
	return sum(x)

def sum_inv(*x):
	'''
	Sum of inverses.
	1/(1/x+1/y+1/z...)
	'''
	return 1.0/sum([1.0/i for i in x])
	
def res_parallel(*r):
	'''
	Caluclate the resistance of a parallel 
	combination of resistors.
	
	*r = any number of resistors.
	'''
	return sum_inv(*r)

def cap_series(*c):
	'''
	Caluclate the capacitance of a series 
	combination of capacitors.
	
	*c = any number of capacitors.
	'''
	return sum_inv(*c)

def pot_div_ratio(r1, r2):
	'''
	vin--[r1]--vout--[r2]--gnd
	'''
	return float(r2)/(r1+r2)

def pot_div(v1, r1, r2, v2=0):
	'''
	v1--[r1]--return--[r2]--v2
	'''
	return (v1-v2)*pot_div_ratio(r1,r2)+v2; 

def x_capacitor(c, f):
	'''
	Calulate reactance of a capacitor.
	'''
	from math import pi
	return -1.0/(2.0*pi*f*c)

def x_inductor(l, f):
	'''
	Calculate reactance of an inductor.
	'''
	from math import pi
	return 2.0*pi*f*l