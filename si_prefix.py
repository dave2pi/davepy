# Define engineering prefix letters

import math

si_prefix = {
	 24 : 'Y',	# yotta
	 21 : 'Z',	# zetta
	 18 : 'E',	# exa
	 15 : 'P',	# peta
	 12 : 'T',	# tera
	 9  : 'G',	# giga
	 6  : 'M',	# mega
	 3  : 'k',	# kilo
	 0  : ' ',
	-3  : 'm',	# milli
	-6  : 'u',	# micro
	-9  : 'n',	# nano
	-12 : 'p',	# pico
	-15 : 'f',	# femto
	-18 : 'a',	# atto
	-21 : 'z',	# zepto
	-24 : 'y'	# yocto
}
	
def si(n, prefix=None, space=1):
	'''
	Converts a number into a string using 
	engineering notation.

	A prefix can optionally be chosen as a 
	string (eg. eng(3800, 'k') or as an 
	integer (eg. eng(3800, 3).
	
	n = number to convert (int | float)
	[prefix] = prefix to apply (int | string)
	[space] = option to include a space between number and prefix (boolean)
	'''
	if n < 0:
		sign = -1
		n = abs(n)
	else:
		sign = 1
	if type(prefix) == type('somestring'):
		# Exponent specified as a string.
		try:
			exponent = (ex for ex,px in si_prefix.items() if px==prefix).next()
		except:
			exponent = math.floor(math.log10(n))
	elif type(prefix) == type(9):
		# Exponent specified as an integer.
		exponent = prefix
	else:
		exponent = math.floor(math.log10(n))
	# Ensure exponent is a float by this point so coef result is a float
	coef = float(n)/10**exponent
	# Place epbounds on exponent.
	ex_max =  max(si_prefix.keys())
	ex_min =  min(si_prefix.keys())
	if exponent > ex_max:
		# Too big.
		coef = coef * 10**(exponent - ex_max)
		exponent = ex_max
	elif exponent < ex_min:
		# Too small.
		coef = coef * 10**(exponent - ex_min)
		exponent = ex_min
	else:
		# Converge on an exponent which is a multiple of 3.
		while exponent%3 != 0.0:
			exponent = exponent - 1
			coef = coef * 10
	coef = coef * sign
	# Return formatted string.
	sp = ' '
	if space == 0:
		sp = ''
	return '{0:.3f}'.format(coef).rjust(8) + sp + si_prefix[exponent]

def sip(n, prefix=None):
	'''
	Prints the result of si().
	See si().
	'''
	print si(n, prefix)

