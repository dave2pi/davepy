'''
Collection of useful resistor calculations.
'''
from e_series import *
import si_prefix as si

def _sum(*x):
	'''
	Sum of values.
	'''
	return sum(x)

def _sum_inv(*x):
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
	return _sum_inv(*r)

def cap_series(*c):
	'''
	Caluclate the capacitance of a series 
	combination of capacitors.
	
	*c = any number of capacitors.
	'''
	return _sum_inv(*c)

def pot_div(v1, r1, r2, v2=0):
	'''
	v1--[r1]--return--[r2]--v2
	'''
	return (v1-v2)*pot_div_ratio(r1,r2)+v2; 

def pot_div_ratio(r1, r2):
	'''
	vin--[r1]--vout--[r2]--gnd
	'''
	return float(r2)/(r1+r2)
	
def find_res_parallel(r_target, series=expand(E24, 1E-1, 10E6)):
	'''
	Search for parallel combinations of resistors close 
	to the target resistance.
	
	r_target = target resistance.
	[series] = series to search.
	'''
	return _finder(r_target, _sum_inv, series)

def find_res_series(r_target, series=expand(E24, 1E-1, 10E6)):
	'''
	Search for series combinations of resistors close 
	to the target resistance.
	
	r_target = target resistance.
	[series] = series to search.
	'''
	return _finder(r_target, _sum, series)
		
def find_cap_parallel(c_target, series=expand(E12, 10E-12, 10E-6)):
	'''
	Search for parallel combinations of capacitors close
	to the target capacitance.
	
	c_target = target capacitance.
	[series] = series to search.
	'''
	return _finder(c_target, _sum, series)

def find_cap_series(c_target, series=expand(E12, 10E-12, 10E-6)):
	'''
	Search for series combinations of capacitors close
	to the target capacitance.
	
	c_target = target capacitance.
	[series] = series to search.
	'''
	return _finder(c_target, _sum_inv, series)

def find_pot_div(r_target, series=expand(E24, 100, 100E3)):
	'''
	Search for a potential divider combination.
	
	r_target = target ratio.
	[series] = series to search.
	'''
	return _finder(r_target, pot_div_ratio, series)

def _finder(target, function, series):
	'''
	Search
	'''
	#print 'TARGET = {0}'.format(si.eng(target))
	def _calc(target, *x):
		calc = function(*x)
		within = calc/target*100.0-100.0
		return (calc, within)
	results = [(a, b) + _calc(target, a, b) for a in series for b in series if b >= a]
	results.sort(key=lambda x: abs(x[3]))
	for x in results[:15]:
		within_str = '{0:.3f}'.format(x[3]).rjust(8)
		print '{0}, {1} = {2} ({3} %)'.format(si.eng(x[0]), si.eng(x[1]), si.eng(x[2]), within_str)
	return [x[:-2] for x in results[:15]]