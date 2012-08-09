'''
Some calculations for simple LC circuits including 
Q, circuit Q and equivalent circuit transormations.
'''

def inductor_q(ls, rs, f):
	'''
	Calculate the Q of an inductor at frequency f.
	
	ls = equivalent series inductance.
	rs = equivalent series resistance.
	f  = frequency.
	'''
	from math import pi
	return 2.0*pi*f*ls/rs

def inductor_equ_ser_par_transform(ls, rs, f, quiet=0):
	'''
	Convert an inductors equivalent series circuit into
	its equivalent parallel circuit. Valid only at a 
	particular frequency.
	
	ls = equivalent series inductance.
	rs = equivalent series resistance.
	f  = frequency.
	
	returns (lp, rp, q)
	'''
	from math import pi
	w = 2*pi*f		# angular freq
	xs = w*ls			# series circuit reactance
	q = xs/rs			# quality
	if quiet == 0:
		print 'Q={0}'.format(q)
	rp = (q**2+1)*rs	# equivalent parallel resistance
	xp = rp/q			# equivalent parallel reactance
	lp = xp/w			# equivalent parallel inductance
	return (lp, rp, f)

def inductor_equ_par_ser_transform(lp, rp, f, quiet=0):
	'''
	Convert an inductors equivalent parallel circuit into
	its equivalent series circuit.
	
	lp = equivalent parallel inductance.
	rp = equivalent parallel resistance.
	f  = frequency.
	
	returns (ls, rs, q)
	'''
	from math import pi
	w = 2*pi*f		# angular freq
	xp = w*lp			# parallel circuit reactance
	q = rp/xp			# quality
	if quiet == 0:
		print 'Q={0}'.format(q)
	rs = rp/(q**2+1)	# equivalent series resistance
	xs = q*rs			# equivalent series reactance
	ls = xs/w			# equivalent series inductance
	return (ls, rs, f)

def lc_q(rp, f, cp=None, lp=None):
	'''
	Calculate the Q of a simple LC circuit.
	cp OR lp may be ommited as their reactance are equal 
	at resonance.
	
	cp = parallel capacitance.
	lp = parallel inductance.
	rp = parallel resistance.
	f  = frequency.
	'''
	from math import pi
	if lp != None:
		return rp/(2.0*pi*f*lp)
	elif cp != None:
		return rp*2.0*pi*f*cp
	else:
		print 'Define cp OR lp'

def x_ideal(l, c, f):
	from math import pi
	w = 2*pi*f		# angular freq
	return abs(w*l/(1-w**2*l*c))
	
def x_non_ideal(l, c, r, f):
	from math import pi
	l, r, f = inductor_equ_ser_par_transform(l, r, f, quiet=1)
	w = 2*pi*f
	xlc = abs(w*l/(1-w**2*l*c))
	return (xlc*r)/(xlc+r)